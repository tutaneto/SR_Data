from .graphics import *
from .coins import *
from .symbols import get_svar_err

def draw_table(fig, annot, symbol, data):
    tab_type = 'h'
    if data['type'] == 'tablev':
        tab_type = 'v'

    size = data['size']
    for pos in range(size):
        for colp in range(100):
            if colp == 0: col_name = 'xaxis'
            if colp == 1: col_name = 'yaxis'
            if colp >= 2: col_name = f'v{colp}'
            if col_name not in data:
                break

            txt = try_int_float(data[col_name][pos])
            if type(txt) in [int, float]:
                txt = format_data_to_show(data, txt)

            # tx e ty podem vir como inicio da tabela ou lista de posições
            tx = data['tab_x']
            ty = data['tab_y']
            x,y = tx,ty

            if tab_type == 'h':
                if type(tx) == list: x = get_listp(tx, colp, e_msg='tab_x')
                if type(ty) == list: y = get_listp(ty, pos,  e_msg='tab_y')
            else:
                if type(tx) == list: x = get_listp(tx, pos,  e_msg='tab_x')
                if type(ty) == list: y = get_listp(ty, colp, e_msg='tab_y')

            x, y, xanchor, yanchor = get_xy_anchors(x, y)

            tab_dx, tab_dy = 0, 0
            if type(tx) != list: tab_dx = get_svar_err('tab_dx')
            if type(ty) != list: tab_dy = get_svar_err('tab_dy')

            if tab_type == 'h':
                x += colp * tab_dx
                y += pos  * tab_dy
                if colp >= 1: x += data.get('tab_tit_dx', tab_dx) - tab_dx
            else:
                x += pos  * tab_dx
                y += colp * tab_dy
                if colp >= 1: y += data.get('tab_tit_dy', tab_dy) - tab_dy

            fs = get_svar_err('tab_fs')
            fc = get_svar_err('tab_fc')
            rect = get_svar_err('tab_rect')
            if colp == 0:  # cor/tam diferente para o título da tabela
                fs = data.get('tab_tit_fs', fs)
                fc = data.get('tab_tit_fc', fc)
                rect = data.get('tab_tit_rect', rect)

            if type(fc) != list:
                fc = [fc]

            color, bold = get_txt_color(fc[colp % len(fc)])
            if bold:
                txt = f'<b>{txt}</b>'

            add_annot(annot, x, y, txt, color, fs,
                xanchor=xanchor, yanchor=yanchor, align=xanchor, ) # bg_color=bg_color)

            # Draw rectangle below text
            if rect:
                w, h, color  = rect[0], rect[1], rect[2]
                draw_rectangle(fig, x - w/2, y - h/2, x + w/2, y + h/2, color, layer='below')
