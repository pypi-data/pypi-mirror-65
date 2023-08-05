#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import argparse
import os
import sys
print('----- txt logo ----')

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

# title subtitle color bgcolor outfile fontfile cfg
using_color = "The color in hex value in formate of #RRGGBB  or #RGB. For example :#00ff00 or #0f0 make a  green version of your pic"


def create_cmd_parser(subparsers):
    parser_txtlogo = subparsers.add_parser(
        'txtlogo', help='Create a app logo 1024x1024 with title and subtitle')
    parser_txtlogo.add_argument("--title",
                                "-t",
                                help="the file to be recolor")
    parser_txtlogo.add_argument("--subtitle",
                                "-s",
                                help="the file to be recolor")
    parser_txtlogo.add_argument("--color",
                                "-c",
                                nargs='?',
                                default='#FFF',
                                help='Title color.'+using_color)
    parser_txtlogo.add_argument("--bgcolor",
                                "-b",
                                nargs='?',
                                default='#39F',
                                help='Background color of the logo.'+using_color)
    parser_txtlogo.add_argument("--outfile",
                                "-o",
                                nargs='?',
                                help="Optional the output file")
    parser_txtlogo.set_defaults(on_args_parsed=_on_args_parsed)


def _on_args_parsed(args):
    params = vars(args)
    title = params['title']
    subtitle = params['subtitle']
    color = params['color']
    bgcolor = params['bgcolor']
    outfile = params['outfile']
    if not outfile:
        outfile = f'{title}_{subtitle}.png' if subtitle else f'{title}.png'

    print(f'txtlogo\n --title={title}\n --subtitle={subtitle}\n'
          + f' --color={color}\n --bgcolor={bgcolor}\n --outfile={outfile}')
