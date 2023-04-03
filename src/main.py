#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import time

import logging
import requests
from datetime import datetime
from waveshare_epd import epd2in13_V2
from PIL import Image, ImageDraw, ImageFont

logging.basicConfig(level=logging.DEBUG)


def draw_label(draw, label: str, anchor, padding: int = 3):
    font_text_left = ImageFont.truetype('font/LLPIXEL3.ttf', 20)
    label_text_size = font_text_left.getbbox(label)
    label_text_size = (
        label_text_size[2], label_text_size[3])
    draw.rounded_rectangle((anchor[0], anchor[1], anchor[0] + label_text_size[0] +
                           padding * 2, anchor[1] + label_text_size[1] + padding * 2), fill=0, radius=7)
    draw.text((anchor[0] + padding, anchor[1] + padding + label_text_size[1] / 2),
              label, font=font_text_left, fill=255, anchor="lm")


try:
    logging.info("starting raspeink")

    epd = epd2in13_V2.EPD()
    epd.init(epd.FULL_UPDATE)
    epd.Clear(0xFF)

    while (1):
        # epd.init(epd.FULL_UPDATE)
        block_height: str = requests.get(
            "http://192.168.1.37:3006/api/blocks/tip/height").text

        logging.debug("current block height: {}".format(block_height))

        # Drawing on the image
        today = datetime.now()

        text_date = today.strftime("%b-%d-%Y")
        text_hours = today.strftime("%H:%M")

        image = Image.new("1", (epd.height, epd.width), 255)
        draw = ImageDraw.Draw(image)

        font_text = ImageFont.truetype('font/open_24_display_st.ttf', 60)
        draw.text((240, 35), str(block_height),
                  font=font_text, fill=0, anchor="rm")

        draw_label(draw, "Block", (5, 28))

        draw.rounded_rectangle(
            [(0, 80), (epd.height, epd.width)], fill=0, radius=7)
        font_bottom = ImageFont.truetype('font/LLPIXEL3.ttf', 17)
        draw.text((5, 100), text_date, font=font_bottom,
                  fill=255, alpha=1,  anchor="lm")
        draw.text((245, 100), text_hours,
                  font=font_bottom, fill=255, anchor="rm")

        epd.init(epd.PART_UPDATE)
        epd.displayPartial(epd.getbuffer(image.rotate(180)))

        time.sleep(10)

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.info("ctrl + c:")
    epd2in13_V2.epdconfig.module_exit()
    exit()
