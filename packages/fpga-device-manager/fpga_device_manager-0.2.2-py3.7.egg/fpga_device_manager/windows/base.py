from qtpy import QtWidgets, uic
from os import path


class BaseWindow(QtWidgets.QMainWindow):
    """Base class for all windows.

    Automatically assigns all of its children widgets as attributes to itself.
    """
    def __init__(self, ui_file: str, *args, **kwargs):
        super(BaseWindow, self).__init__(*args, **kwargs)
        uic.loadUi(path.join(path.dirname(__file__), "..", "res", "ui", ui_file), self)

        for child in self.findChildren(QtWidgets.QWidget):
            name = child.objectName()
            setattr(self, name, child)


class BaseDialog(QtWidgets.QDialog):
    """Base class for all dialogs.

    Automatically assigns all of its children widgets as attributes to itself.
    """
    def __init__(self, ui_file, *args, **kwargs):
        super(BaseDialog, self).__init__(*args, **kwargs)
        uic.loadUi(path.join(path.dirname(__file__), "..",  "res", "ui", ui_file), self)

        for child in self.findChildren(QtWidgets.QWidget):
            name = child.objectName()
            setattr(self, name, child)


class BaseWidget(QtWidgets.QWidget):
    """Base class for all widgets.

    Automatically assigns all of its children widgets as attributes to itself.
    """
    def __init__(self, ui_file, *args, **kwargs):
        super(BaseWidget, self).__init__(*args, **kwargs)
        uic.loadUi(path.join(path.dirname(__file__), "..",  "res", "ui", ui_file), self)

        for child in self.findChildren(QtWidgets.QWidget):
            name = child.objectName()
            setattr(self, name, child)
