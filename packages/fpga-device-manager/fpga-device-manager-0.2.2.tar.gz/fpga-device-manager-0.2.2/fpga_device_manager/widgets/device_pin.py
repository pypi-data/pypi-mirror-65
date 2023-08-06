from qtpy.QtCore import Slot
from qtpy.QtWidgets import QComboBox

from fpga_device_manager import Pins
from fpga_device_manager.device_base import DeviceBasePin
from fpga_device_manager.exceptions import DeviceInvalidError
from fpga_device_manager.windows.base import BaseWidget
from fpga_device_manager.Devices import DevicePin


class DevicePinWidget(BaseWidget):
    """A widget representing a device pin."""
    def __init__(self, device_widget: 'DeviceBaseWidget', device_pin: DeviceBasePin, *args, **kwargs):
        super(DevicePinWidget, self).__init__("device_pin.ui", *args, **kwargs)

        self.device_widget = device_widget
        self.main_window = device_widget.main_window
        self.device_pin = device_pin

        self.lb_pin_name.setText(self.device_pin.name)
        self.chk_active_low.setChecked(self.device_pin.active_low)

        if isinstance(self.device_pin, DevicePin):
            self.chk_pwm.setChecked(self.device_pin.requires_pwm)

        self.refresh()

    def refresh(self) -> None:
        """Updates the widget to reflect the current state of the pin."""
        self.combo_pins: QComboBox
        self.combo_pins.clear()

        if self.device_pin.assigned_pin is not None:
            self.combo_pins.addItem(self.device_pin.assigned_pin.display_name)
        else:
            self.combo_pins.addItem("")

        self.combo_pins.addItems(pin.display_name for pin in Pins.available(self.device_pin))

        try:
            self.device_pin.check_validity()
            self.lb_pin_name.setStyleSheet("")
        except DeviceInvalidError:
            self.lb_pin_name.setStyleSheet("font-weight: bold; color: red")

    @Slot(int)
    def on_chk_active_low_stateChanged(self, state: int):
        """
        Handler for changing the state of the active low checkbox.
        :param state: The checkbox's new state.
        """
        self.main_window.set_dirty()
        self.device_pin.active_low = state == 2

    @Slot(str)
    def on_combo_pins_currentTextChanged(self, new_pin: str):
        """
        Handler for changing the pin assignment combo box.
        :param new_pin: The selected FPGA pin to assign to.
        """
        if new_pin != '':
            if self.device_pin.assigned_pin is None or new_pin != self.device_pin.assigned_pin.display_name:
                pin_name = Pins.lookup(new_pin).name
                Pins.assign(pin_name, self.device_pin)
                self.main_window.set_dirty()
                self.main_window.refresh()
