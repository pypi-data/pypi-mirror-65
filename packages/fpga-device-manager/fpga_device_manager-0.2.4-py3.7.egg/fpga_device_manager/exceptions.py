"""This module holds all exceptions that can possibly occur during device management."""


class DeviceInvalidError(BaseException):
    """Gets thrown when a device, both Output or Input, has not been configured properly."""
    pass


class InvalidConfigError(BaseException):
    """
    Gets thrown when the device configuration as a whole did not pass vailidity checks.
    The errors parameter is a list of error messages that have been generated during verification.
    """
    def __init__(self, errors):
        super(InvalidConfigError, self).__init__()
        self.errors = errors


class PinNotAssignedError(DeviceInvalidError):
    """Gets thrown when a device pin has not been assigned to any FPGA pin."""
    def __init__(self, pin):
        super(PinNotAssignedError, self).__init__(f'Pin "{pin.name}" of device "{pin.device.name}" '
                                                  f'is not assigned to any FPGA pin')


class PinIncompatibilityError(DeviceInvalidError):
    """Gets thrown when a device pin has been assigned to an FPGA pin it is not compatible with."""
    def __init__(self, pin):
        super(PinIncompatibilityError, self).__init__(
            f'Pin "{pin.name}" of device "{pin.device.name}" '
            f'is not compatible with assigned pin "{pin.assigned_pin.name}"')


class DeviceIncompatibilityError(DeviceInvalidError):
    """Gets thrown when a pair of Input and Output devices are associated, but somehow incompatible with each other."""
    def __init__(self, dev_in, dev_out):
        super(DeviceIncompatibilityError, self).__init__(f'Devices "{dev_in.name}" and "{dev_out.name}" are not'
                                                         f'compatible with each other')


class InputNotAssociatedError(DeviceInvalidError):
    """Gets thrown when an Input device has not been assigned to any Output device."""
    def __init__(self, device):
        super(InputNotAssociatedError, self).__init__(f'Device "{device.name}" '
                                                      f'is not associated with any output device')


class DeviceLoadError(BaseException):
    """Gets thrown when an error occurs during loading of a device instance from a configuration."""
    pass


class UnknownPinException(DeviceLoadError):
    """Gets thrown during the attempt to load a device configuration that contains a device with a pin it shouldn't
    possess."""
    def __init__(self, device, pin):
        super(UnknownPinException, self).__init__(device,
                                                  f'Attempted to set up unknown pin "{pin.name}" '
                                                  f'on device "{device.name}.')
