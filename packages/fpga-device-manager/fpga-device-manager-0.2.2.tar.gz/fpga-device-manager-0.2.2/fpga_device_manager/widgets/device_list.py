from fpga_device_manager.windows.base import BaseWidget


class DeviceListWidget(BaseWidget):
    """A widget that displays devices."""
    def __init__(self, *args, **kwargs):
        super(DeviceListWidget, self).__init__("device_list.ui", *args, **kwargs)
