#!/usr/bin/env python3
# -*- coding: utf-8 -*- #文件也为UTF-8
import sys
import os
from PIL import Image, ImageDraw, ImageFont

ANTIALIAS_SIZE = 16
LOGO_SIZE = 1024*ANTIALIAS_SIZE
MAIN_POS = 546*ANTIALIAS_SIZE
CIRCLE_EDGE_Y = 848*ANTIALIAS_SIZE
CIRCLE_RADIUS = 1380*ANTIALIAS_SIZE
SUB_POS = 986*ANTIALIAS_SIZE
COLOR_MAIN = '#268bf1'
COLOR_SECOND = '#ffffff'
FONT_MAIN_SUM = 840*ANTIALIAS_SIZE
FONT_SIZE_SUB = 104*ANTIALIAS_SIZE
SUB_TITLE = u'智课'


# https://www.zcool.com.cn/article/ZNDg2Mzg4.html
# FONT_FILE_NAME = 'HappyZcool-2016.ttf'
# FONT_FILE_NAME = 'zcoolqinkehuangyouti.ttf'
# FONT_FILE_NAME = 'lianmengqiyilushuaizhengruiheiti.ttf'

FONT_FILE_NAME = 'ZhenyanGB.ttf'


def brother_path(file_name):
    return os.path.join(os.path.abspath(
        os.path.dirname(__file__)), file_name)


def draw_zk_bg():
    img = Image.new('RGB', (LOGO_SIZE, LOGO_SIZE), COLOR_MAIN)
    draw = ImageDraw.Draw(img)

    ellipseX1 = LOGO_SIZE/2 - CIRCLE_RADIUS
    ellipseX2 = LOGO_SIZE/2 + CIRCLE_RADIUS
    draw.ellipse((ellipseX1, CIRCLE_EDGE_Y, ellipseX2,
                  CIRCLE_EDGE_Y+CIRCLE_RADIUS*2), COLOR_SECOND)
    return img


def text_horzontal_center(text, color, font, img, base_y):
    text_width, text_height = font.getsize(text)
    draw = ImageDraw.Draw(img)
    x = (LOGO_SIZE-text_width)/2
    y = base_y-text_height
    draw.text((x, y), text, color, font=font)


def print_using():
    print("使用方法：zk_logo_maker.py 产品名 filename")


def count_length(title):
    len = 0
    for s in title:
        len += 1
    return len


def main():
    param_len = len(sys.argv)

    if param_len < 2:
        print_using()
        exit()

    title = sys.argv[1]
    if param_len == 2:
        file_path = f"{title}.png"
    else:
        file_path = f"{sys.argv[2]}.png"

    print(f"title:{title}")
    print(f"file_path:{file_path}")

    title_len = len(title)
    main_title_font_size = int(FONT_MAIN_SUM/title_len)
    font = ImageFont.truetype(
        brother_path(FONT_FILE_NAME),
        main_title_font_size
    )
    img = draw_zk_bg()
    text_horzontal_center(
        title,
        COLOR_SECOND,
        font,
        img,
        MAIN_POS)

    font_sub = ImageFont.truetype(
        brother_path(FONT_FILE_NAME),
        FONT_SIZE_SUB
    )
    text_horzontal_center(
        SUB_TITLE,
        COLOR_MAIN,
        font_sub,
        img,
        SUB_POS)

    logo_size = int(LOGO_SIZE/ANTIALIAS_SIZE)
    img = img.resize((logo_size, logo_size), Image.ANTIALIAS)
    img.save(file_path, 'PNG')


if __name__ == "__main__":
    main()
