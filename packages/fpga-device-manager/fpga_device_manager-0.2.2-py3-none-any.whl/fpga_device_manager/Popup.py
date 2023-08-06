"""Contains utility functions for creating popup messages."""
from typing import Callable

from qtpy.QtWidgets import QMessageBox
import traceback


def _prepare_popup(title: str, message: str, additional_text: str, icon, buttons) -> QMessageBox:
    popup = QMessageBox()
    popup.setWindowTitle(title)
    popup.setText(message)
    popup.setInformativeText(additional_text)
    popup.setIcon(icon)
    popup.setStandardButtons(buttons)
    return popup


def info(title: str, message: str, additional_text: str = "") -> None:
    """
    Creates and displays a notification popup.
    :param title: Title of popup window
    :param message: Popup message text
    :param additional_text: Second popup message text
    """
    _prepare_popup(title=title,
                   message=message,
                   additional_text=additional_text,
                   icon=QMessageBox.Information,
                   buttons=QMessageBox.Ok).exec_()


def alert(title: str, message: str, additional_text: str = "") -> None:
    """
    Creates and displays an alert popup.
    :param title: Title of popup window
    :param message: Popup message text
    :param additional_text: Second popup message text
    """
    _prepare_popup(title=title,
                   message=message,
                   additional_text=additional_text,
                   icon=QMessageBox.Warning,
                   buttons=QMessageBox.Ok).exec_()


def confirm(title: str,
            message: str,
            additional_text: str = "",
            on_yes: Callable[[], None] = lambda: None,
            on_no: Callable[[], None] = lambda: None) -> None:
    """
    Creates and displays a confirmation popup. Calls a different callable depending on whether the user accepts or not.
    :param title: Title of popup window
    :param message: Popup message text
    :param additional_text: Second popup message text
    :param on_yes: Callable that gets called when the user accepts the confirmation
    :param on_no: Callable that gets called when the user rejects or closes the confirmation
    """
    popup = _prepare_popup(title=title,
                           message=message,
                           additional_text=additional_text,
                           icon=QMessageBox.Question,
                           buttons=QMessageBox.Yes | QMessageBox.No)

    on_yes() if popup.exec_() == QMessageBox.Yes else on_no()


def error(title: str, ex: Exception) -> None:
    """
    Creates and displays an error popup that shows the contents of an exception.
    Afterwards, the exception is raised once more.
    :param title: Title of popup window
    :param ex: Exception to display
    """
    alert(title=title,
          message=str(ex),
          additional_text=traceback.format_exc())
    raise
