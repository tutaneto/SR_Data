import numpy as np
import plotly.graph_objects as go
# import plotly.io as pio
from PIL import Image
from os.path import exists
from .util import *
from .get_prices import get_prices
from .coins import get_value_txt

if gvar.get('ONLINE', False):
    from .symbols import get_symbol_var

GRAPH_WIDTH  = 0
GRAPH_HEIGHT = 0
GS           = 1  # Graph Scale
GHSC         = 0  # Graph Height Scaled
GBC_COLOR    = 'white'

MARGINL =  0
MARGINR =  0
MARGINT =  0
MARGINB =  0


g_xref, g_yref = 'x', 'y'
def set_ref_type(xref='x', yref='y'):
    global g_xref, g_yref
    g_xref = xref
    g_yref = yref

def adjust_xy(x, y, scale=True):
    if scale:
        x = x*GS
        y = GHSC - y*GS

    if g_xref != 'x':
        PAPERW = GRAPH_WIDTH  - (MARGINL + MARGINR)
        PAPERH = GRAPH_HEIGHT - (MARGINT + MARGINB)
        x = (x - MARGINL * GS) / (PAPERW * GS)
        y = (y - MARGINB * GS) / (PAPERH * GS)

    return x, y

def adjust_wh(w, h):
    w = w*GS
    h = h*GS

    if g_xref != 'x':
        PAPERW = GRAPH_WIDTH  - (MARGINL + MARGINR)
        PAPERH = GRAPH_HEIGHT - (MARGINT + MARGINB)
        w = w / (PAPERW * GS)
        h = h / (PAPERH * GS)

    return w, h

def set_margins(fig, l=0, r=0, t=0, b=0, pad=0, update=True):
    global MARGINL, MARGINR, MARGINT, MARGINB
    MARGINL = l
    MARGINR = r
    MARGINT = t
    MARGINB = b
    if update:
        fig.update_layout(
            margin=dict(l=l*GS, r=r*GS, t=t*GS, b=b*GS, pad=pad*GS),
        )

def get_scale():
    return GS


def add_image(fig, img_file, x, y, width, height, xanchor='center', yanchor='middle', opacity=1.0, layer=None):
    if not exists(img_file):
        # draw_rectangle(fig, x-width/2, y-height/2, x+width/2, y+height/2, 'black')
        return

    py_image = Image.open(img_file)

    x, y = adjust_xy(x, y)
    width, height = adjust_wh(width, height)

    # Seleciona default de acordo com a documentação do add_image
    if layer == None:
        layer = 'above'
        if g_xref == 'paper' and g_yref == 'paper':
            layer = 'below'

    # Add image
    fig.add_layout_image(
        dict(
            # x=x*GS, y=GHSC - y*GS,
            x=x, y=y,
            # sizex=width*GS, sizey=height*GS,
            sizex=width, sizey=height,
            xref=g_xref, yref=g_yref,
            xanchor = xanchor, yanchor = yanchor,
            opacity=opacity, layer=layer,
            sizing="stretch",
            # source="https://raw.githubusercontent.com/michaelbabyn/plot_data/master/bridge.jpg"
            source=py_image,  # Local image doesn't work directly (it needs PIL)
        )
    )


def label_to_dict(x, y, text, color, size, xanchor='left',
        yanchor='middle', align='center', bg_color=True): #, xref='x', yref='y'):
    if bg_color:
        bg_color = GBC_COLOR
    else:
        bg_color = 'rgba(0,0,0,0)'

    x, y = adjust_xy(x, y, False)

    return dict(
        xref=g_xref, yref=g_yref,
        xanchor = xanchor, yanchor = yanchor,
        align=align,
        x=x, y=y,
        text=f'{text}',
        font=dict(color=color, size=size),
        bgcolor = bg_color,
        showarrow=False)


def add_annot(annotations, x, y, txt, color, size, xanchor='left', yanchor='middle', align='center', bg_color=False, contour=False):
    # annotations.append(label_to_dict(
    #     (x-2)*GS, GHSC - (y+2)*GS,
    #     txt, '#CCCCCC', size*GS, xanchor, yanchor, align, bg_color))
    # se usar a sombra, bg_color abaixo precisa trocar para False
    
    annotations.append(label_to_dict(
    x*GS, GHSC - y*GS,
    txt, color, size*GS, xanchor, yanchor, align, bg_color))
    


def draw_line(fig, x0, y0, x1, y1, color, width=1, opacity=1.0, dash='solid', layer=None, val=None):
    if layer == None:
        layer = 'below'
    
    if template_config.current_template == 'JP4_' and val != 0:
        dash='dot'

    x0, y0 = adjust_xy(x0, y0)
    x1, y1 = adjust_xy(x1, y1)
    fig.add_shape(type='line',
        xref=g_xref, yref=g_yref,
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(color=color, width=width*GS, dash=dash),
        opacity=opacity, layer=layer
        )

def draw_circle(fig, x0, y0, x1, y1, color, opacity=1.0):
    if type(color) == str and color[-4:] == '.png':
        if not exists(f'images/circle_{color}'):
            create_shape('circle', color[:-4])

        x, y = min(x0, x1), min(y0, y1)
        w, h = abs(x1-x0), abs(y1-y0)
        add_image(fig, f'images/circle_{color}', x, y, w, h, xanchor='left', yanchor='top')
        return

    x0, y0 = adjust_xy(x0, y0)
    x1, y1 = adjust_xy(x1, y1)
    fig.add_shape(type='circle',
        xref=g_xref, yref=g_yref,
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(width=0),
        fillcolor=color,
        layer='below', opacity=opacity,
        )

def draw_circle_line(fig, x0, y0, x1, y1, color, width=1, opacity=1.0):
    x0, y0 = adjust_xy(x0, y0)
    x1, y1 = adjust_xy(x1, y1)
    fig.add_shape(type='circle',
        xref=g_xref, yref=g_yref,
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(width=width*GS, color=color),
        layer='above', opacity=opacity,
        )

def draw_rectangle(fig, x0, y0, x1, y1, color, opacity=1.0, layer=None):
    if type(color) == str and color[-4:] == '.png':
        if not exists(f'images/{color}'):
            create_shape('rect', color[:-4])

        x, y = min(x0, x1), min(y0, y1)
        w, h = abs(x1-x0), abs(y1-y0)
        add_image(fig, 'images/'+color, x, y, w, h, xanchor='left', yanchor='top', layer=layer)
        return

    # if type(color) == tuple or type(color) == list:
    #     draw_rectangle_gradient(fig, x0, y0, x1, y1, color, opacity)
    #     return

    x0, y0 = adjust_xy(x0, y0)
    x1, y1 = adjust_xy(x1, y1)

    if layer == None and (template_config.current_template != 'JP_MERC_FIN_4'):
        layer = 'below'

    color = get_txt_color(color, ret_bold=False)

    fig.add_shape(type='rect',
        xref=g_xref, yref=g_yref,
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(width=0),
        fillcolor=color,
        layer=layer, opacity=opacity,
        )

def draw_rectangle_line(fig, x0, y0, x1, y1, color, width=1, opacity=1.0):
    x0, y0 = adjust_xy(x0, y0)
    x1, y1 = adjust_xy(x1, y1)
    fig.add_shape(type='rect',
        xref=g_xref, yref=g_yref,
        x0=x0, y0=y0, x1=x1, y1=y1,
        line=dict(width=width*GS, color=color),
        layer = 'above', opacity=opacity,
        )


def draw_rectangle_gradient(fig, x0, y0, x1, y1, color, opacity=1.0):
    step  = 2
    if y1 < y0:
        step = -step

    height = y1 - y0
    n_steps = height // step

    r0 = color[0][0]
    r1 = color[1][0]
    g0 = color[0][1]
    g1 = color[1][1]
    b0 = color[0][2]
    b1 = color[1][2]

    rstep = (r1 - r0) / (n_steps - 1)
    gstep = (g1 - g0) / (n_steps - 1)
    bstep = (b1 - b0) / (n_steps - 1)

    y = y0
    while y < y1:
        color=f'rgb({r0/255.0}, {g0/255.0}, {b0/255.0})'

        r0 += rstep
        g0 += gstep
        b0 += bstep

        draw_rectangle(fig, x0, y, x1, y+step, color, opacity)

        y += step


def set_graph(fig, width, height, scale, bg_color, font):

    global GRAPH_WIDTH, GRAPH_HEIGHT, GS, GHSC, GBC_COLOR

    # Workaround para 001_ no INVEST_NEWS
    if width == 980 and scale == 0.675:
        scale = 0.900

    GRAPH_WIDTH  = width
    GRAPH_HEIGHT = height
    GS   = scale
    GHSC = height * scale

    GBC_COLOR = bg_color

    width  *= scale
    height *= scale

    fig.update_layout(
        paper_bgcolor=bg_color,
        plot_bgcolor=bg_color,
        font_family=font,
        width=width,
        height=height,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
    )

def set_graph_axes(fig):
    fig.update_xaxes(
        visible=False,
        range=[0, GRAPH_WIDTH * GS]
    )

    fig.update_yaxes(
        visible=False,
        range=[0, GRAPH_HEIGHT * GS],
        # the scaleanchor attribute ensures that the aspect ratio stays constant
        scaleanchor="x"
    )

def show_extra_labels(fig, annot, symbol, data, bar_val_fs, graph_layer):
    for lbl in data['label']:
        for p in range(len(lbl)):
            lbl[p] = get_symbol_var(symbol, lbl[p], lbl[p], setlower=False)
            lbl[p] = try_int_float(lbl[p])
        txt = lbl[0]

        if txt == '(rect)':
            x, y, w, h, color = lbl[1:6]
            draw_rectangle(fig, x, y, x + w, y + h, color, layer='below')
            continue

        if txt[-4:] in ['.png', '.jpg']:
            x, y, w, h = lbl[1:5]
            add_image(fig, txt, x, y, w, h, xanchor='left', yanchor='top')
            continue

        if txt[:1] == '{' and txt[-1:] == '}':
            symbol, perc, arrow = txt[1:-1], False, False
            if symbol.endswith('_perc'):
                symbol = symbol.replace('_perc', '')
                perc = True
            if symbol.endswith('_arrow'):
                symbol = symbol.replace('_arrow', '')
                arrow = True

            val, old = get_prices(symbol)

            if perc:
                txt = get_value_txt(get_perc(val, old))
            elif arrow:
                x, y, w, h, img, img2 = lbl[1:7]
                if val < old:
                    img = img2
                add_image(fig, img, x, y, w, h)
                continue
            else:
                txt = get_value_txt(val)

        x,  y, xanchor, yanchor = get_xy_anchors(lbl[1], lbl[2])
        fc, fs = lbl[3], lbl[4]
        fc, bold = get_txt_color(fc)
        if fc == '': fc = get_color_pos(XAXIS_TEXT_COLOR, 0)
        if fs == '': fs = bar_val_fs
        img = lbl[5]
        if img != '':
            draw_rectangle(fig, x-8, y+8, x-fs, y+fs, fc, layer=graph_layer)
        if template_config.current_template == 'INVEST_NEWS_BLACK':
            fc = 'white'
        if bold: txt = f'<b>{txt}</b>'
        add_annot(annot, x, y, txt, fc, fs,
            xanchor=xanchor, yanchor=yanchor, align=xanchor)


graph_center = 0

def set_graph_center(center):
    global graph_center
    if center < 0:
        graph_center += center
    else:
        graph_center  = center

def get_graph_center():
    return graph_center
