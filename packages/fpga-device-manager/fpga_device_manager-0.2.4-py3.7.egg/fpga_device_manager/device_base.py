from __future__ import annotations
from abc import ABC

from fpga_device_manager import Pins
from fpga_device_manager.Pins import FPGAPin
from fpga_device_manager.exceptions import PinNotAssignedError, UnknownPinException, DeviceLoadError


class DeviceBase(ABC):
    """Base class for all devices and device templates."""
    def __init__(self, dev_name, dev_type, uses_clk=False, pins=None, parameters=None):
        self.name = dev_name
        self.type = dev_type
        self.uses_clk = uses_clk
        self.pins = pins or {}
        self.parameters = parameters or {}


class DeviceBaseTemplate(DeviceBase, ABC):
    """Base class for device templates."""
    def __init__(self, dev_driver, description="", *args, **kwargs):
        super(DeviceBaseTemplate, self).__init__(*args, **kwargs)

        self.driver = dev_driver
        self.description = description


class DeviceBaseInstance(DeviceBase, ABC):
    """Base class for device instances."""
    def __init__(self, dev_id=None, *args, **kwargs):
        super(DeviceBaseInstance, self).__init__(*args, **kwargs)
        self.template = None
        self.dev_id = dev_id

    @staticmethod
    def create_from_template(dev_name: str, dev_type: int) -> DeviceBaseInstance:
        """
        Creates a new device instance from a template, identified by its index.
        :param dev_name: Name of new device
        :param dev_type: ID of template to base device off of
        :return: Newly created device
        """
        raise NotImplementedError

    @classmethod
    def load(cls, dev_data: dict) -> DeviceBaseInstance:
        """
        Loads a device from JSON data, loaded from a file.
        :param dev_data: JSON imported data structure
        :return: Loaded device object
        """
        try:
            obj = cls.create_from_template(dev_name=dev_data["name"],
                                           dev_type=dev_data["type"])
        except KeyError as e:
            raise DeviceLoadError(f'While setting up a device, a required key "{e}" was missing')

        for pin_name, pin_data in dev_data["pins"].items():
            if pin_name not in obj.pins:
                raise UnknownPinException(obj, pin_name)

            Pins.assign(pin_data["assigned_pin"], obj.pins[pin_name])
            obj.pins[pin_name].active_low = pin_data.get("active_low", False)

        for param_name, param_data in dev_data["parameters"].items():
            if param_name not in obj.parameters:
                continue

            obj.parameters[param_name].set_value(param_data)

        return obj

    def check_validity(self) -> bool:
        """
        Checks the device for proper configuration.
        Incorrect configurations throw an InvalidDeviceError.
        :return: True if device has been set up properly
        """
        raise NotImplementedError

    def save(self) -> dict:
        """
        Exports the device's properties to a JSON-serializable dict.
        :return: Device settings as dict
        """
        raise NotImplementedError


class DeviceBasePin(ABC):
    """Base class for device pins."""
    def __init__(self, name, device, active_low=False, assigned_pin=None):
        self.name = name
        self.device = device
        self.active_low = active_low
        self.assigned_pin = assigned_pin

    def copy(self, new_device: DeviceBaseInstance) -> DeviceBasePin:
        """
        Creates a copy of itself and assigns it to the specified device.
        :param new_device: Device to copy itself to
        :return: Copy of pin
        """
        raise NotImplementedError

    def is_assigned(self) -> bool:
        """
        Returns whether the pin is assigned to an FPGA pin.
        :return: True if pin is assigned, False otherwise
        """
        return self.assigned_pin is not None

    def is_compatible_with(self, fpga_pin: FPGAPin) -> bool:
        """
        Returns whether the pin is compatible with the specified FPGA pin.
        :param fpga_pin: Pin to check compatibility with
        :return: True if pins are compatible, False otherwise
        """
        raise NotImplementedError

    def check_validity(self) -> bool:
        """
        Checks whether the pin is configured properly.
        If not, throws a PinNotAssignedError.
        :return: True if pin is set up properly
        """
        if self.assigned_pin is None:
            raise PinNotAssignedError(self)

        return True
