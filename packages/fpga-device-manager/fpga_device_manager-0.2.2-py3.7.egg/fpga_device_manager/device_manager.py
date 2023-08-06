from typing import Dict, Optional, Iterable

from fpga_device_manager import Pins, Constants
from fpga_device_manager.device_base import DeviceBaseInstance


class DeviceManager:
    """Manages a type of device."""
    def __init__(self, device_class, max_devices: Optional[int] = None):
        self.devices = {}  # type: Dict[int, DeviceBaseInstance]
        self.max_devices = max_devices or Constants.MAX_DEVICES
        self.available_ids = list(range(0, self.max_devices))

        self.device_class = device_class

    def has_devices(self):
        """
        Returns whether this manager has at least one device.
        :return: True if there are devices, False otherwise
        """
        return len(self.devices) > 0

    def has_max_devices(self):
        """
        Returns whether this manager has no more room for devices.
        :return: True if number of devices is maxed out, False otherwise
        """
        return len(self.devices) == self.max_devices

    def add_device(self, device: DeviceBaseInstance, force_id: Optional[int] = None) -> None:
        """
        Adds a new device.
        :param device: The device to add
        :param force_id: Forces a device ID, if specified. Otherwise just uses the next free one. If the requested ID
                         is not available, this throws an Exception.
        """
        if force_id is not None:
            try:
                self.available_ids.remove(force_id)
                device_id = force_id
            except ValueError:
                raise Exception("The requested device ID %d is not available" % force_id)
        else:
            device_id = self.available_ids.pop(0)

        device.dev_id = device_id
        self.devices[device_id] = device

    def move_device(self, old_id: int, new_id: int) -> None:
        """
        Attempts to move an existing device from one ID to another.
        If the device with the specified ID doesn't exist or the target ID is already occupied, this throws an
        Exception.
        :param old_id: ID of the device to move
        :param new_id: New ID to assign device to
        """
        if new_id not in self.available_ids:
            raise Exception("ID %d is not available" % new_id)

        try:
            self.devices[new_id] = self.devices.pop(old_id)
            self.devices[new_id].dev_id = new_id
            self.available_ids.remove(new_id)
            self.available_ids.append(old_id)
            self.available_ids.sort()
        except KeyError:
            raise Exception("ID %d is not used" % old_id)

    def remove_device(self, device_id: int) -> None:
        """
        Removes a device with the specified ID. If no device with that ID exists, this throws an Exception.
        :param device_id: ID of device to remove
        """
        try:
            # Get device
            device = self.devices[device_id]

            # Return device ID
            self.available_ids.append(device_id)
            self.available_ids.sort()

            # Clear pins
            for pin in device.pins.values():
                if pin.is_assigned():
                    Pins.clear(pin.assigned_pin.name)

            # Remove device
            del self.devices[device_id]

        except KeyError:
            raise Exception("No device with ID %d" % device_id)

    def clear(self) -> None:
        """Removes all devices from this manager, effectively resetting it."""
        for dev_id in self.devices.copy().keys():
            self.remove_device(dev_id)

        self.devices.clear()
        self.available_ids = list(range(0, self.max_devices))

    def get(self, device_id: int) -> DeviceBaseInstance:
        """
        Looks up a device based on its ID and returns it.
        If no device with that ID exists, throws an Exception.
        :param device_id: ID of device to get
        :return: Device
        """
        try:
            return self.devices[device_id]
        except KeyError:
            raise Exception("no device with ID %d exists" % device_id)

    def all_devices(self) -> Iterable[DeviceBaseInstance]:
        """
        Returns all devices managed by this manager.
        :return: All devices
        """
        return self.devices.values()

    def filter(self, dev_types: Iterable[int]) -> Iterable[DeviceBaseInstance]:
        """
        Returns all devices that are of one of the types specified.
        :param dev_types: Filtered list of devices
        """
        for dev in self.devices.values():
            if dev.type in dev_types:
                yield dev

    def load(self, dev_list: dict) -> None:
        """
        Loads devices from JSON data.
        :param dev_list: JSON-loaded dict data
        """
        for dev_id, dev_data in dev_list.items():
            device = self.device_class.load(dev_data)
            self.add_device(device, force_id=int(dev_id))

    def save(self) -> Dict[int, Dict]:
        """
        Exports all devices into a JSON-serializable dictionary.
        :return: Dict to be serialized
        """
        return {dev_id: device.save() for dev_id, device in self.devices.items()}
