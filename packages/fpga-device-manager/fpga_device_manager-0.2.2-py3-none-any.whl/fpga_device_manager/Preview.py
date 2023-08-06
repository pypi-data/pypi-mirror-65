from math import ceil
from os import path

from PIL import Image, ImageDraw, ImageFont, ImageQt

from fpga_device_manager import Pins

_PINS = [
    ("Pin header 1", 5, [
        ("34", "32", "GND", "27", "GND", "25", "23", "GND", "21", "19",
         "GND", "13", "11", "GND", "9", "5", "3", "1", "3.3", "3.3"),

        ("35", "33", "GND", "28", "GND", "26", "24", "GND", "22", "20",
         "GND", "14", "12", "GND", "10", "6", "4", "2", "NC", "IO3")
    ]),
    ("On-board LEDs", 4, [
        ("107", "106", "105", "104", "100", "99", "98", "97")
    ])
]

_SIZE = (800, 400)
_BOX_BORDER_WIDTH = 4
_PIN_SIZE = 24
_PIN_BORDER_WIDTH = 3
_PIN_MARGIN = 6
_BANK_MARGIN = 16
_BOX_PADDING = 11

_FONT = ImageFont.truetype(font=path.join(path.dirname(__file__), "res", "fonts", "libsans.ttf"), size=20)
_FONT_SMALL = ImageFont.truetype(font=path.join(path.dirname(__file__), "res", "fonts", "libsans-bold.ttf"), size=12)


def draw_pin_header(header_data):
    """

    :param header_data:
    :return:
    """
    header_bank_size = header_data[1]
    header_pins = header_data[2]
    maxn = max(len(x) for x in header_pins)

    header_box_width = round(_PIN_SIZE * maxn +
                             (ceil(maxn/header_bank_size) - 1) * _BANK_MARGIN +
                             (maxn - ceil(maxn/header_bank_size)) * _PIN_MARGIN +
                             _BOX_PADDING * 2)
    header_box_height = _PIN_SIZE * len(header_pins) + _PIN_MARGIN * (len(header_pins) - 1) + _BOX_PADDING * 2

    im = Image.new("RGBA", (header_box_width + 1, header_box_height * 2), (255, 255, 255, 0))
    im_draw = ImageDraw.ImageDraw(im)

    im_draw.rectangle((0, 0, header_box_width, header_box_height), (230, 230, 230, 255), (0, 0, 0), _BOX_BORDER_WIDTH)
    x = y = _BOX_PADDING
    for pin_row in header_pins:
        for i, pin in enumerate(pin_row):
            # Determine pin color
            try:
                pin_obj = Pins.get(pin)
                pin_name = pin_obj.display_name
                pin_color = pin_obj.color()
                font = _FONT
            except KeyError:
                pin_name = pin
                pin_color = Pins.color(Pins.PIN_RESERVED)
                font = _FONT_SMALL

            # Draw pin
            im_draw.rectangle((x, y, x + _PIN_SIZE, y + _PIN_SIZE), pin_color, (0, 0, 0), _PIN_BORDER_WIDTH)

            # Draw label
            tw, th = font.getsize(pin_name)
            tx = x + (_PIN_SIZE - tw) / 2
            ty = y + header_box_height + (_PIN_SIZE - th) * .75 - 8
            im_draw.text((tx+1, ty+1), text=str(pin_name), font=font, fill=(90, 90, 90))
            im_draw.text((tx, ty), text=str(pin_name), font=font, fill=pin_color)

            x += _PIN_SIZE + ((i % header_bank_size != header_bank_size-1) and _PIN_MARGIN or _BANK_MARGIN)
        x = _BOX_PADDING
        y += _PIN_SIZE + _PIN_MARGIN

    return im


def draw():
    """

    :return:
    """
    width = 0
    height = 0
    images = []
    for header in _PINS:
        header_im = draw_pin_header(header)
        images.append(header_im)
        width = max(width, header_im.width)
        height = height + header_im.height

    im = Image.new("RGBA", (width, height), (255, 255, 255, 0))

    y = 0
    for header_im in images:
        im.paste(header_im, (round((width - header_im.width) / 2), y))
        y += header_im.height

    return ImageQt.ImageQt(im)
