"""Module for managing Input device templates. Also contains classes for instances of Input devices."""
from __future__ import annotations
import json
from typing import Iterable

from fpga_device_manager.Devices import Output
from fpga_device_manager.device_base import DeviceBasePin, DeviceBaseTemplate, DeviceBaseInstance
from fpga_device_manager.device_params import DeviceParameter
from fpga_device_manager.exceptions import PinIncompatibilityError, InputNotAssociatedError, DeviceIncompatibilityError

_input_templates = {}


class InputPin(DeviceBasePin):
    """Base class for input pins."""
    def __init__(self, *args, **kwargs):
        super(InputPin, self).__init__(*args, **kwargs)

    def copy(self, new_device: DeviceBaseInstance) -> InputPin:
        """
        Creates a copy of itself and assigns it to a device.
        :param new_device:
        :return:
        """
        return InputPin(self.name,
                        device=self.device,
                        active_low=self.active_low,
                        assigned_pin=self.assigned_pin)

    def check_validity(self) -> bool:
        """
        Verifies the configuration of this pin. Will throw a PinIncompatibilityError if the assigned pin is somehow
        incompatible with this pin.
        :return: True if configuration is valid
        """
        super(InputPin, self).check_validity()

        if not self.is_compatible_with(self.assigned_pin):
            raise PinIncompatibilityError(self)

    def is_compatible_with(self, fpga_pin: 'FPGAPin') -> bool:
        """
        Returns whether this pin is compatible with the specified FPGA pin.
        :param fpga_pin: FPGA pin to check compatibility with
        :return: True if compatible, False otherwise
        """
        return fpga_pin.supports_output

    def __str__(self):
        return "Pin %s of input %s" % (self.name, self.device.name)


class InputTemplate(DeviceBaseTemplate):
    """Represents the blueprint on which Input devices can be based off of."""
    def __init__(self, compatible_devices=None, *args, **kwargs):
        super(InputTemplate, self).__init__(*args, **kwargs)

        self.compatible_devices = compatible_devices or []

    @staticmethod
    def load(dev_data: dict) -> InputTemplate:
        """
        Creates an InputTemplate based on loaded JSON data.
        :param dev_data: JSON dict template data
        :return: Template instance
        """
        obj = InputTemplate(dev_name=dev_data["name"],
                            dev_type=dev_data["type"],
                            dev_driver=dev_data["driver"],
                            uses_clk=dev_data["uses_clk"],
                            description=dev_data["description"],
                            compatible_devices=dev_data["compatible_devices"],
                            parameters={
                                param_name: DeviceParameter.load(param_name, param_data)
                                for param_name, param_data in dev_data.get("parameters", {}).items()
                            })

        for pin_name, pin_data in dev_data["pins"].items():
            obj.pins[pin_name] = InputPin(name=pin_name,
                                          device=obj,
                                          active_low=pin_data["active_low"])

        return obj


class Input(DeviceBaseInstance):
    """An input device or sensor."""
    def __init__(self, associated_device=None, *args, **kwargs):
        super(DeviceBaseInstance, self).__init__(*args, **kwargs)

        self.associated_device = associated_device

    @staticmethod
    def create_from_template(dev_name: str, dev_type: int) -> Input:
        """
        Creates an Input device instance based on an InputTemplate.
        :param dev_name: The name of the new device
        :param dev_type: The ID of the template to base the device off of
        :return: Input device instance
        """
        dev_template = get_template(dev_type)

        obj = Input(dev_name=dev_name,
                    dev_type=dev_template.type,
                    uses_clk=dev_template.uses_clk,
                    parameters=dev_template.parameters.copy())

        for name, pin in dev_template.pins.items():
            obj.pins[name] = pin.copy(obj)

        obj.template = dev_template

        return obj

    def save(self) -> dict:
        """
        Exports the input device's state into a format that is JSON serializable.
        :return: JSON serializable dict
        """
        return {
            "name": self.name,
            "type": self.type,
            "associated_device": self.associated_device.dev_id if self.is_associated() else None,
            "pins": {
                pin.name: {
                    "assigned_pin": pin.assigned_pin.name if pin.assigned_pin is not None else None,
                    "active_low": pin.active_low
                } for pin in self.pins.values()
            },
            "parameters": {name: param.value for name, param in self.parameters.items()}
        }

    def on_post_load(self, manager: 'DeviceManager', data: dict) -> None:
        """
        Hook that associates this Input device with an Output device after loading a configuration from file.
        :param manager: Device Manager instance
        :param data: Device data
        """
        self.associate(manager.devices[data["associated_device"]])

    def associate(self, device: Output) -> None:
        """
        Associates this Input device with an Output device.
        If the devices are incompatible with each other, this raises an
        :param device: Output device to associate with
        """
        # Remove old association
        self.deassociate()

        # Associate
        if device.type not in self.template.compatible_devices:
            raise DeviceIncompatibilityError(self, device)

        self.associated_device = device
        device.associated_inputs.append(self)

    def deassociate(self) -> None:
        """Removes the output device association of this device."""
        if self.associated_device is None:
            return

        self.associated_device.associated_inputs.remove(self)
        self.associated_device = None

    def is_associated(self) -> bool:
        """
        Returns whether this device is currently associated with an Output device.
        :return: True if device is associated, False otherwise
        """
        return self.associated_device is not None

    def check_validity(self) -> bool:
        """
        Verifies the validity of this device's configuration by checking whether it is associated with any Output device
        and whether all of its pins are valid
        :return: True if device is configured properly, False otherwise
        """
        if not self.is_associated():
            raise InputNotAssociatedError(self)

        for pin in self.pins.values():
            pin.check_validity()

        return True

    def __str__(self):
        return self.name


def init(filename: str) -> None:
    """
    Initializes the template module by loading and indexing all available Input device templates.
    :param filename: File to load template data from
    """
    global _input_templates
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for tpl_type, tpl_data in data.items():
                tpl_data["type"] = int(tpl_type)
                _input_templates[int(tpl_type)] = InputTemplate.load(tpl_data)

    except OSError as e:
        raise Exception("Couldn't open input template file: %s" % e)


def list_templates() -> Iterable[InputTemplate]:
    """
    Returns an Iterable of all Input device templates, indexed by ID.
    :return: Iterable of Input device templates
    """
    for tpl_id, tpl in _input_templates.items():
        yield tpl_id, tpl


def get_template(dev_type: int) -> InputTemplate:
    """
    Looks up an Input device template by ID.
    :param dev_type: ID of Input device template
    :return: Input device template instance
    """
    try:
        return _input_templates[dev_type]
    except KeyError:
        raise Exception("No such device type: %s" % dev_type)
