"""Module that manages FPGA pins."""
import json
from typing import Optional, Tuple, Iterable, Generator, Iterator

_pins = {}

PIN_RESERVED = 0
PIN_OCCUPIED_DEVICE = 1
PIN_OCCUPIED_INPUT = 2
PIN_AVAILABLE_PWM = 3
PIN_AVAILABLE = 4

_PIN_COLORS = {
    PIN_RESERVED: (80, 80, 80),
    PIN_OCCUPIED_DEVICE: (220, 80, 80),
    PIN_OCCUPIED_INPUT: (240, 150, 100),
    PIN_AVAILABLE_PWM: (180, 220, 180),
    PIN_AVAILABLE: (180, 180, 220)
}


class FPGAPin:
    """Represents a physical pin on the FPGA."""
    def __init__(self, name, display_name=None, supports_pwm=True, supports_output=True, supports_input=True,
                 fpga_addr=31, device_pin=None):
        self.name = name
        self.display_name = display_name or name
        self.supports_pwm = supports_pwm
        self.supports_output = supports_output
        self.supports_input = supports_input
        self.fpga_addr = fpga_addr
        self.device_pin = device_pin

    def is_assigned(self) -> bool:
        """
        Returns whether this pin is currently assigned to a device.
        :return: True if pin is assigned, False otherwise
        """
        return self.device_pin is not None

    def is_assignable(self, device_pin: Optional['DevicePin'] = None) -> bool:
        """
        Returns whether this pin is currently assignable. If a device pin is specified, it also checks
        for compatibility with it.
        :param device_pin: Optional device pin to check compatibility with
        :return: True if this pin is currently assignable, False otherwise
        """
        if device_pin is None:
            return not self.is_assigned()

        return not self.is_assigned() and device_pin.is_compatible_with(self)

    def is_input(self) -> bool:
        """
        Returns whether this pin is currently assigned to the pin of an Input device.
        :return: True if this pin is connected to an Input pin, False otherwise
        """
        from fpga_device_manager.Inputs import InputPin
        return self.is_assigned() and isinstance(self.device_pin, InputPin)

    def is_output(self) -> bool:
        """
        Returns whether this pin is currently assigned to the pin of an Output device.
        :return: True if this pin is connected to an Output pin, False otherwise
        """
        from fpga_device_manager.Devices import DevicePin
        return self.is_assigned() and isinstance(self.device_pin, DevicePin)

    def color(self) -> Tuple[int, int, int]:
        """
        Returns this pin's color for the preview image. The color depends on the current state of the pin
        and the device pin it might be connected to.
        :return: Pin's color, as a RGB color triplet (0..255)
        """
        return color(self.is_input() and PIN_OCCUPIED_INPUT or
                     self.is_output() and PIN_OCCUPIED_DEVICE or
                     self.supports_pwm and PIN_AVAILABLE_PWM or
                     PIN_AVAILABLE)


def init(filename: str) -> None:
    """
    Initializes the FPGA pin database by loading the pin configuration from the specified filename.
    The file must be in JSON format and contains pin settings, indexed by the FPGA's pin names.
    At the very least, each pin must contain the properties 'addr' (an integer describing the pin's internal adress)
    and 'pwm' (a Boolean value describing whether the pin supports PWM output).
    Optionally, it can also contain a 'name' attribute (a string overriding the FPGA pin name for the preview image)
    and 'output' and 'input' attributes (Boolean values describing whether the pin supports output or input,
    respectively, defaulting to True).

    Example of a configuration file:
    {
        "1": {
            "pwm": true,
            "addr": 1
        },
        "2": {
            "pwm": false,
            "input": false,
            "addr": 2
        }
        "99": {
            "pwm": false,
            "output": false,
            "name": "D1",
            "addr": 3
        }
    }

    :param filename: FPGA pin configuration file
    """
    global _pins
    _pins = {}

    try:
        with open(filename, "r") as file:
            pin_data = json.load(file)

        for pin, pin_args in pin_data.items():
            display_name = pin_args.get("name", pin)
            _pins[pin] = FPGAPin(name=pin,
                                 display_name=display_name,
                                 supports_pwm=pin_args["pwm"],
                                 supports_input=pin_args.get("input", True),
                                 supports_output=pin_args.get("output", True),
                                 fpga_addr=pin_args.get("addr", 31))

    except OSError as e:
        raise Exception("failed to load pin data file: %s" % e)


def get(pin_name: str) -> FPGAPin:
    """
    Looks up a FPGA pin by its name and returns it.
    If no pin with the specified name exists, this will throw a KeyError.
    :param pin_name: Name of the FPGA pin to look up
    :return: FPGA pin instance
    """
    return _pins[pin_name]


def get_next_available_pin(device_pin: 'DevicePin' = None) -> FPGAPin:
    """
    Searches for the next available pin that is compatible with the supplied device pin and returns it.
    If no pins are available, this raises an Exception.
    :param device_pin: Device pin to find assignable FPGA pin for
    :return: FPGA Pin instance that is available for assignment
    """
    for pin in _pins.values():
        if pin.is_assignable(device_pin):
            return pin
    raise Exception("No pins available")


def lookup(pin_display_name: str) -> FPGAPin:
    """
    Looks up a FPGA pin by its display name and returns it.
    The display name is the same as its name, unless it was overridden via configuration.
    If no pin with the specified display name exists, this will throw an Exception.
    :param pin_display_name: Display name of the FPGA pin to look up
    :return: FPGA pin instance
    """
    for pin in _pins.values():
        if pin.display_name == pin_display_name:
            return pin
    raise Exception("No such pin: %s" % pin_display_name)


def available(device_pin: 'DevicePin') -> Iterator[FPGAPin]:
    """
    A generator that supplies every FPGA pin that is assignable to the given device pin.
    :param device_pin: Iterator of assignable FPGA pins
    """
    for pin in _pins.values():
        if pin.is_assignable(device_pin):
            yield pin


def all() -> Iterable[FPGAPin]:
    """
    Returns an Iterable of all FPGA pins.
    :return: All FPGA pins
    """
    return _pins.values()


def assign(pin_name: str, device_pin: 'DevicePin') -> FPGAPin:
    """
    Attempts to assign the supplied device pin to the FPGA pin of the given name.
    This throws a KeyError if no FPGA pin with that name exists. Additionally, on incompatibility between the two pins
    an Exception is thrown.
    :param pin_name: Name of FPGA pin to assign the device pin to
    :param device_pin: Device pin to assign to the FPGA pin
    :return: Instance of FPGA pin
    """
    try:
        pin = _pins[pin_name]

        # Check if pins are already connected
        if pin.device_pin == device_pin:
            return pin

        # Check if pin is assignable to device pin
        if not pin.is_assignable(device_pin):
            raise Exception("Device pin %s is not assignable to pin %s" % (device_pin.name, pin_name))

        # Free previously assigned pin
        if device_pin.assigned_pin is not None:
            device_pin.assigned_pin.device_pin = None

        # Assign to new pin
        _pins[pin_name].device_pin = device_pin
        device_pin.assigned_pin = pin

        return pin

    except KeyError:
        raise Exception("Pin %s does not exist" % pin_name)


def clear(pin_name: str) -> FPGAPin:
    """
    Clears the FPGA pin with the given name of its associated pin. Does nothing if the FPGA pin is unassigned.
    :param pin_name: Name of FPGA pin to clear
    :return: FPGA Pin instance
    """
    try:
        pin = _pins[pin_name]
        pin.device_pin.assigned_pin = None
        pin.device_pin = None
        return pin
    except KeyError:
        raise Exception("Pin %s does not exist" % pin_name)


def color(pin_type: int) -> Tuple[int, int, int]:
    """
    Returns the color for the specified raw pin type.
    :param pin_type: Raw pin type ID
    :return: Color for pin type as RGB color triplet (0..255)
    """
    return _PIN_COLORS[pin_type]
