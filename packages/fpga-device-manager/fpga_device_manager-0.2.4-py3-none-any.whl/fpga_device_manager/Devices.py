"""Module for managing Output device templates. Also contains classes for instances of Output devices."""
from __future__ import annotations
import json
from typing import Iterable

from fpga_device_manager.device_base import DeviceBasePin, DeviceBaseInstance, DeviceBaseTemplate
from fpga_device_manager.device_params import DeviceParameter
from fpga_device_manager.exceptions import PinIncompatibilityError

_device_templates = {}


class DevicePin(DeviceBasePin):
    """Base class for device pins."""
    def __init__(self, requires_pwm=False, *args, **kwargs):
        super(DevicePin, self).__init__(*args, **kwargs)
        self.requires_pwm = requires_pwm

    def copy(self, device: DeviceBaseInstance) -> DevicePin:
        """
        Creates a copy of itself and assigns it to a device.
        :param device: Device the pin belongs to
        :return: Pin copy
        """
        return DevicePin(name=self.name,
                         requires_pwm=self.requires_pwm,
                         device=device,
                         active_low=self.active_low,
                         assigned_pin=self.assigned_pin)

    def check_validity(self) -> bool:
        """
        Verifies the configuration of this pin. Will throw a PinIncompatibilityError if the assigned pin is somehow
        incompatible with this pin.
        :return: True if configuration is valid
        """
        super(DevicePin, self).check_validity()

        if not self.is_compatible_with(self.assigned_pin):
            raise PinIncompatibilityError(self)

        return True

    def is_compatible_with(self, fpga_pin: 'FPGAPin') -> bool:
        """
        Returns whether this pin is compatible with the specified FPGA pin.
        :param fpga_pin: FPGA pin to check compatibility with
        :return: True if compatible, False otherwise
        """
        return fpga_pin.supports_output and not (self.requires_pwm and not fpga_pin.supports_pwm)

    def __str__(self):
        return "Pin %s of device %s" % (self.name, self.device.name)


class OutputTemplate(DeviceBaseTemplate):
    """Represents the blueprint on which Output devices can be based off of."""
    def __init__(self, uses_bus=False, *args, **kwargs):
        super(OutputTemplate, self).__init__(*args, **kwargs)
        self.uses_bus = uses_bus

    @staticmethod
    def load(dev_data: dict) -> OutputTemplate:
        """
        Creates an OutputTemplate based on loaded JSON data.
        :param dev_data: JSON dict template data
        :return: Template instance
        """
        obj = OutputTemplate(dev_name=dev_data["name"],
                             dev_type=dev_data["type"],
                             dev_driver=dev_data["driver"],
                             uses_clk=dev_data.get("uses_clk", True),
                             uses_bus=dev_data.get("uses_bus", False),
                             description=dev_data["description"],
                             parameters={
                                 param_name: DeviceParameter.load(param_name, param_data)
                                 for param_name, param_data in dev_data.get("parameters", {}).items()
                             })

        for pin_name, pin_data in dev_data["pins"].items():
            obj.pins[pin_name] = DevicePin(name=pin_name,
                                           device=obj,
                                           requires_pwm=pin_data["requires_pwm"],
                                           active_low=pin_data["active_low"])

        return obj


class Output(DeviceBaseInstance):
    """An output device or appliance."""
    def __init__(self, uses_bus=False, *args, **kwargs):
        super(Output, self).__init__(*args, **kwargs)
        self.associated_inputs = []
        self.uses_bus = uses_bus

    @staticmethod
    def create_from_template(dev_name: str, dev_type: int) -> Output:
        """
        Creates an Output device instance based on an OutputTemplate.
        :param dev_name: The name of the new device
        :param dev_type: The ID of the template to base the device off of
        :return: Output device instance
        """
        dev_template = get_template(dev_type)

        obj = Output(dev_name=dev_name,
                     dev_type=dev_template.type,
                     uses_clk=dev_template.uses_clk,
                     uses_bus=dev_template.uses_bus,
                     parameters={name: param.copy() for name, param in dev_template.parameters.items()})

        obj.template = dev_template

        for name, pin in dev_template.pins.items():
            obj.pins[name] = pin.copy(obj)

        return obj

    def save(self) -> dict:
        """
        Exports the device's state into a format that is JSON serializable.
        :return: JSON serializable dict
        """
        return {
            "name": self.name,
            "type": self.type,
            "pins": {
                pin.name: {
                    "assigned_pin": pin.assigned_pin.name if pin.assigned_pin is not None else None,
                    "active_low": pin.active_low
                } for pin in self.pins.values()
            },
            "parameters": {name: param.value for name, param in self.parameters.items()}
        }

    def remove_associations(self) -> None:
        """Removes all associated Input devices from this Output."""
        for input_dev in self.associated_inputs:
            input_dev.deassociate()

    def check_validity(self) -> bool:
        """
        Verifies the validity of this device's configuration by checking whether all of its pins are valid.
        :return: True if device is configured properly, False otherwise
        """
        for pin in self.pins.values():
            pin.check_validity()
        return True

    def __str__(self):
        return self.name


def init(filename: str) -> None:
    """
    Initializes the template module by loading and indexing all available Output device templates.
    :param filename: File to load template data from
    """
    global _device_templates
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            for tpl_type, tpl_data in data.items():
                tpl_data["type"] = int(tpl_type)
                _device_templates[int(tpl_type)] = OutputTemplate.load(tpl_data)

    except OSError as e:
        raise Exception("Couldn't open device template file: %s" % e)


def list_templates() -> Iterable[OutputTemplate]:
    """
    Returns an Iterable of all Output device templates, indexed by ID.
    :return: Iterable of Output device templates
    """
    for tpl_id, tpl in _device_templates.items():
        yield tpl_id, tpl


def get_template(dev_type: int) -> OutputTemplate:
    """
    Looks up an Output device template by ID.
    :param dev_type: ID of Output device template
    :return: Output device template instance
    """
    try:
        return _device_templates[dev_type]
    except KeyError:
        raise Exception("No such device type: %s" % dev_type)
