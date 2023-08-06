"""A widget that draws the FPGA preview image, displaying pin headers and pin assignments."""
from collections import namedtuple
from math import ceil
from typing import Tuple

from qtpy.QtCore import QRect, Qt
from qtpy.QtGui import QPainter, QImage, QPixmap, QColor, QPen, QBrush, QFont
from qtpy.QtWidgets import QLabel

from fpga_device_manager import Pins

"""A pin header is defined as a tuple containing a name, pin group size and a list of tuples of pins."""
PinHeader = namedtuple("PinHeader", "name bank_width pins")

_PINS = [
    PinHeader("Pin header 1", 5, [
        ("34", "32", "GND", "27", "GND", "25", "23", "GND", "21", "19",
         "GND", "13", "11", "GND", "9", "5", "3", "1", "3.3", "3.3"),

        ("35", "33", "GND", "28", "GND", "26", "24", "GND", "22", "20",
         "GND", "14", "12", "GND", "10", "6", "4", "2", "NC", "IO3")
    ]),

    PinHeader("On-board LEDs", 4, [
        ("D8", "106", "105", "104", "100", "99", "98", "97")
    ])
]

_SIZE = (450, 200)
_BOX_BORDER_WIDTH = 4
_PIN_SIZE = 24
_PIN_BORDER_WIDTH = 3
_PIN_MARGIN = 6
_BANK_MARGIN = 16
_BOX_PADDING = 11


class PinHeaderImage(QImage):
    """The image of a single FPGA pin header."""
    def __init__(self, header: PinHeader):
        self.header = header
        width, height = self._header_box_size()

        super(PinHeaderImage, self).__init__(width, height * 2, QImage.Format_RGB32)

        self.painter = QPainter(self)
        self.pen = QPen(QColor(0, 0, 0), _BOX_BORDER_WIDTH, Qt.SolidLine)
        self.pen.setJoinStyle(Qt.MiterJoin)
        self.painter.setPen(self.pen)

        self._update()

    def _header_box_size(self) -> Tuple[int, int]:
        maxn = max(len(x) for x in self.header.pins)
        width = round(_PIN_SIZE * maxn +
                      (ceil(maxn / self.header.bank_width) - 1) * _BANK_MARGIN +
                      (maxn - ceil(maxn / self.header.bank_width)) * _PIN_MARGIN +
                      _BOX_PADDING * 2)
        height = (_PIN_SIZE * len(self.header.pins) +
                  _PIN_MARGIN * (len(self.header.pins) - 1) +
                  _BOX_PADDING * 2)
        return width, height

    def _update(self):
        self._clear()
        self._draw()

    def _clear(self):
        self.fill(QColor(255, 255, 255))

    def _draw(self):
        self._draw_bg()
        self._draw_pins()
        self.painter.end()

    def _draw_bg(self):
        self.pen.setWidth(_BOX_BORDER_WIDTH)
        self.painter.setPen(self.pen)
        self.painter.setBrush(QBrush(QColor(230, 230, 230)))

        border_offset = _BOX_BORDER_WIDTH // 2
        x = y = border_offset
        w, h = self._header_box_size()
        w -= border_offset * 2
        h -= border_offset * 2
        self.painter.drawRect(x, y, w, h)

    def _draw_pins(self):
        _, box_h = self._header_box_size()

        x = y = _BOX_PADDING

        font: QFont = self.painter.font()

        for pin_row in self.header.pins:
            for i, pin in enumerate(pin_row):
                # Determine pin color
                try:
                    pin_obj = Pins.get(pin)
                    pin_name = pin_obj.display_name
                    pin_color = pin_obj.color()
                    font_size = 18
                    font_bold = True

                except KeyError:
                    pin_name = pin
                    pin_color = Pins.color(Pins.PIN_RESERVED)
                    font_size = 11
                    font_bold = False

                font.setPixelSize(font_size)
                font.setBold(font_bold)
                self.painter.setFont(font)

                # Draw pin
                self.pen.setColor(QColor(0, 0, 0))
                self.pen.setWidth(_PIN_BORDER_WIDTH)
                self.painter.setPen(self.pen)
                self.painter.setBrush(QBrush(QColor(*pin_color)))
                border_offset = _PIN_BORDER_WIDTH // 2
                pin_x = x - border_offset
                pin_y = y - border_offset
                pin_w = pin_h = _PIN_SIZE - (_PIN_BORDER_WIDTH - border_offset)
                self.painter.drawRect(pin_x, pin_y, pin_w, pin_h)

                # Draw label + shadow
                self.pen.setColor(QColor(90, 90, 90))
                self.painter.setPen(self.pen)
                font_rect = QRect(x - 12, y + box_h - 12, _PIN_SIZE + 20, _PIN_SIZE + 20)
                self.painter.drawText(font_rect, Qt.AlignHCenter | Qt.AlignVCenter, pin_name)

                font_rect.setX(x - 14)
                font_rect.setY(y + box_h - 14)
                self.pen.setColor(QColor(*pin_color))
                self.painter.setPen(self.pen)
                self.painter.drawText(font_rect, Qt.AlignHCenter | Qt.AlignVCenter, pin_name)
                x += _PIN_SIZE + (_BANK_MARGIN if (i % self.header.bank_width == self.header.bank_width - 1)
                                  else _PIN_MARGIN)

            x = _BOX_PADDING
            y += _PIN_SIZE + _PIN_MARGIN


class FPGAPreview(QLabel):
    """The entire FPGA preview image."""
    def __init__(self, *args):
        super(FPGAPreview, self).__init__(*args)
        self.im_width = int(_SIZE[0] * 1.5)
        self.im_height = int(_SIZE[1] * 1.5)

        self.image = QImage(self.im_width, self.im_height, QImage.Format_RGB32)
        self.painter = QPainter(self.image)

        self.setFixedSize(*_SIZE)

        self.update()

    def update(self) -> None:
        """Updates the preview image with the current pin assignment data."""
        self._clear()
        self._draw()
        self.setPixmap(QPixmap(self.image))
        self.setScaledContents(True)

    def _clear(self):
        self.painter = QPainter(self.image)
        self.image.fill(QColor(255, 255, 255))

    def _draw(self):
        width = 0
        height = 0
        images = []

        # Draw all pin header images
        for header in _PINS:
            header_im = PinHeaderImage(header)
            images.append(header_im)
            width = max(width, header_im.width())
            height = height + header_im.height()

        y = (self.im_height - height) // 2

        # Copy pin header images onto own image
        for header_im in images:
            x = (self.im_width - header_im.width()) // 2

            self.painter.drawImage(x, y, header_im)
            y += header_im.height()

        self.painter.end()
