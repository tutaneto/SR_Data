from .pres_template import *
from .graphics import add_image

def show_watermark(fig, gt):
    if WATERMARK_IMG == None:
        return

    x, y = WM_X, WM_Y
    if gt:
        x, y = WM_X_GT, WM_Y_GT

    add_image(fig, WATERMARK_IMG, x, y, WM_W, WM_H,
        opacity=WATERMARK_ALPHA, layer=WATERMARK_LAYER)

    # Vários no meio
    # for lin in range(3):
    #     for col in range(3):
    #         if lin%2 and col==2:
    #             continue
    #         y = 300 + lin * 100
    #         x = 250 + col * 500 + lin%2*250
    #         add_image(fig, WATERMARK_IMG, x, y, 350, 50,
    #             opacity=WATERMARK_ALPHA, layer=WATERMARK_LAYER)


