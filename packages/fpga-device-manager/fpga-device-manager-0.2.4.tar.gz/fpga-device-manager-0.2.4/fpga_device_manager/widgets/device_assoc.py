from qtpy.QtCore import Slot
from qtpy.QtWidgets import QComboBox

from fpga_device_manager import Config
from fpga_device_manager.windows.base import BaseWidget


class DeviceAssociationWidget(BaseWidget):
    """A widget for choosing an output device to associate with."""
    def __init__(self, device_widget: 'InputWidget', *args, **kwargs):
        super(DeviceAssociationWidget, self).__init__("device_assoc.ui", *args, **kwargs)

        self.device_widget = device_widget
        self.device = device_widget.device
        self.main_window = device_widget.main_window

    def refresh(self) -> None:
        """Updates the widget. This displays all association possibilities."""
        self.combo_devices: QComboBox
        self.combo_devices.clear()

        if self.device.is_associated():
            self.combo_devices.addItem(self.device.associated_device.name, self.device.associated_device)
        else:
            self.combo_devices.addItem("", None)

        for supported_device in Config.outputs().filter(self.device.template.compatible_devices):
            if supported_device is not self.device.associated_device:
                self.combo_devices.addItem(supported_device.name, supported_device)

        if self.device.is_associated():
            self.lb_device.setStyleSheet("font-weight: normal; color: inherit")
        else:
            self.lb_device.setStyleSheet("font-weight: bold; color: red;")

    @Slot(int)
    def on_combo_devices_currentIndexChanged(self, index: int):
        """
        Handler for changing the device combo box.
        :param index: Index of chosen output device in combo box.
        """
        self.combo_devices: QComboBox
        dev_selected = self.combo_devices.itemData(index)
        if dev_selected is not None and dev_selected is not self.device.associated_device:
            self.device.associate(dev_selected)
            self.main_window.set_dirty()
            self.main_window.refresh()
