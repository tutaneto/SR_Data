from .pres_template import *

# Graphic size and margins
IMAGEW  =  GT_IMAGE_W
IMAGEH  =  GT_IMAGE_H
MARGINL, MARGINR, MARGINT, MARGINB, MARGINPAD =  GT_001_MARGINS

if TEMPLATE == 'INVEST_NEWS_BLACK':
    MARGINT = 240
    MARGINL = 120

# Paper = Area where chart is designed, equivalent in px of 0.0 to 1.0
PAPERW  = IMAGEW - (MARGINL + MARGINR)
PAPERH  = IMAGEH - (MARGINT + MARGINB)

# Convert from pixel (px) to relational
px_rel = lambda px: px/PAPERW
py_rel = lambda py: py/PAPERH

# Image limits in paper proportion, < 0.0 and > 1.0
IMAGEL = 0 - px_rel(MARGINL)
IMAGER = 1 + px_rel(MARGINR)
IMAGEB = 0 - py_rel(MARGINB)
IMAGET = 1 + py_rel(MARGINT)

# Font size multiplier factor
FONT_SIZE_MF = 1

# Colors
# color_text_1 = '#9A0E40'  # Red
color_text_2 = GT_COLOR_NEG
color_text_3 = GT_COLOR_POS
color_text_4 = GT_TICKS_FONT_COLOR
color_text_5 = GT_COLOR_POS  # '#75CCD3'  # Light Cyan

color_ticks = color_text_4
size_ticks  = GT_TICKS_FONT_SIZE

color_diff_neg = color_text_2
color_diff_pos = color_text_3

# Label positions
pp_x = IMAGEL + px_rel(8)
pp_y = IMAGET - py_rel(40)  # 80

if TEMPLATE == 'INVEST_NEWS_BLACK':
    pp_x += px_rel(160)
    pp_y -= px_rel( 60)

diff_x = pp_x
diff_y = pp_y - py_rel(45)

title_x = pp_x
title_y = pp_y + py_rel(45)

time_x  = pp_x
time_y  = pp_y - py_rel(85)  # 90

asset_x = IMAGER - px_rel(8)
asset_y = pp_y - py_rel(0)

if TEMPLATE == 'INVEST_NEWS_BLACK':
    asset_x -= px_rel(2)

dfont_x = asset_x  # pp_x
dfont_y = pp_y - py_rel(35)

close_x = asset_x  # IMAGER - px_rel(8)
close_y = 0.5


# Block at bottom with information
block_info_x0   = IMAGEL + px_rel(8)  # pp_x
block_info_y0   = IMAGEB + py_rel(8)
block_info_x1   = IMAGER - px_rel(8)
block_info_y1   = 0 - py_rel(60)

block_info_w    = block_info_x1 - block_info_x0
block_info_h    = block_info_y1 - block_info_y0
block_info_cen  = block_info_x0 + block_info_w * 0.5
block_info_mid  = block_info_y0 + block_info_h * 0.5

block_info_lbl_dx = [0.14, 0.10, 0.15]

if template_num == 1:
    block_info_y1   = 0 - py_rel(68)
    block_info_lbl_dx = [0.20, 0.12, 0.22]

if GT_INFO_52M:
    if template_num == 1:
        block_info_lbl_x = [
            block_info_cen - block_info_w * 0.31,
            block_info_cen - block_info_w * 0.03,
            block_info_cen + block_info_w * 0.35
        ]

        block_info_line_x = [
            block_info_lbl_x[1] - block_info_lbl_dx[1] - 0.05,
            block_info_lbl_x[2] - block_info_lbl_dx[2] - 0.04
        ]
    else:
        block_info_lbl_x = [
            block_info_cen - block_info_w * 0.33,
            block_info_cen - block_info_w * 0.02,
            block_info_cen + block_info_w * 0.36
        ]

        block_info_line_x = [
            block_info_lbl_x[1] - block_info_lbl_dx[1] - 0.10,
            block_info_lbl_x[2] - block_info_lbl_dx[2] - 0.10
        ]
else:
    block_info_lbl_x = [
        block_info_cen - block_info_w * 0.25,
        block_info_cen + block_info_w * 0.25,
        block_info_cen,  # não usado
    ]

    block_info_line_x = [
        block_info_cen,
        block_info_cen,
    ]


block_info_lbl_y = [
        block_info_mid + block_info_h * 0.17,
        block_info_mid - block_info_h * 0.23
]

# Position in label list
LBL_POS_X = 0
LBL_POS_Y = 1
LBL_POS_COLOR = 2
LBL_POS_SIZE = 3