from .pres_template import *
from .graphics import *
from .graphcomp import *

tables = ['Bolsas_Mundo', 'Bolsas_Mundo_USD', 'Moedas', 'Table_Petroleo']

import time

# # Position in label list
LBL_POS_TEXT  = 0
LBL_POS_X     = 1
LBL_POS_Y     = 2
LBL_POS_COLOR = 3
LBL_POS_SIZE  = 4
LBL_POS_ROW   = 5

# # Colors
color_text_1 = TITLE_COLOR
color_text_4 = DFONT_COLOR

color_back_rect = TAB_BRECT_COLOR



IMAGE_WIDTH = 864
IMAGE_HEIGHT = 524

asset_color = TAB_ASSET_FC
asset_size  = TAB_ASSET_FS

block_title_color = color_text_4

# Blocks(1,2,3) positions
b1x, b1y = TAB_B1X, TAB_B1Y
b2x, b2y = TAB_B2X, TAB_B2Y
b3x, b3y = TAB_B3X, TAB_B3Y
b4x, b4y = TAB_B4X, TAB_B4Y

bdx = TAB_BDX  # block distance between left and right text
bdy = TAB_BDY  # block distance to next one

title_x = TAB_TITLE_X
title_y = TAB_TITLE_Y

dfont_x = TAB_DFONT_X
dfont_y = TAB_DFONT_Y

btdx, btdy = TAB_BTIT_DX, TAB_BTIT_DY

labels = [
    ['<b>DOW JONES</b>', b1x, b1y, asset_color, asset_size, 0],
    ['<b>S&P 500</b>',   b1x, b1y, asset_color, asset_size, 1],
    ['<b>NASDAQ</b>',    b1x, b1y, asset_color, asset_size, 2],

    ['<b>DAX</b>',       b2x, b2y, asset_color, asset_size, 0],
    ['<b>FTSE</b>',      b2x, b2y, asset_color, asset_size, 1],
    ['<b>CAC 40</b>',    b2x, b2y, asset_color, asset_size, 2],
    ['<b>IBEX 35</b>',   b2x, b2y, asset_color, asset_size, 3],

    ['<b>SSE</b>',       b3x, b3y, asset_color, asset_size, 0],
    ['<b>NIKKEI</b>',    b3x, b3y, asset_color, asset_size, 1],
    ['<b>HANG SENG</b>', b3x, b3y, asset_color, asset_size, 2],

    ['<b>IBOVESPA</b>',  b4x, b4y, asset_color, asset_size, 0],

    ['ESTADOS UNIDOS',   b1x-btdx, b1y-btdy, block_title_color, TAB_BLKTIT_FS],
    ['EUROPA',           b2x-btdx, b2y-btdy, block_title_color, TAB_BLKTIT_FS],
    ['ASIA',             b3x-btdx, b3y-btdy, block_title_color, TAB_BLKTIT_FS],
    ['BRASIL',           b4x-btdx, b4y-btdy, block_title_color, TAB_BLKTIT_FS],

    ['<b>BOLSAS NO MUNDO</b>',  title_x, title_y, color_text_1, TAB_TITLE_FS],
    ['<b>FONTE</b>: YAHOO FINANCE', dfont_x, dfont_y, color_text_4, TAB_DFONT_FS],
]

asset_codes = [
    '^DJI',   '^GSPC', '^IXIC',             # United States
    '^GDAXI', '^FTSE', '^FCHI', '^IBEX',    # Europe
    '000001.SS', '^N225', '^HSI',           # Asia
    '^BVSP',                                # Brasil
]

coin_asset_codes = [
    'USD', 'USD', 'USD',                            # United States
    'EURUSD=X', 'GBPUSD=X', 'EURUSD=X', 'EURUSD=X', # Europe
    'CNYUSD=X','JPYUSD=X','HKDUSD=X',               # Asia
    'BRLUSD=X',                                     # Brasil
]


def get_label_y(label, block_dy):
    y = label[LBL_POS_Y]
    row = 0
    if len(label) > LBL_POS_ROW:
        row = label[LBL_POS_ROW]

    y += row * block_dy

    return y


def set_labels(annotations, labels, block_dy):
    for label in labels:
        text = label[LBL_POS_TEXT]
        x = label[LBL_POS_X]
        y = get_label_y(label, block_dy)
        color = label[LBL_POS_COLOR]
        size  = label[LBL_POS_SIZE]
        add_annot(annotations, x, y, text, color, size)


def world_indexes_set_values(fig, annotations, block_dy, usd):
    global t_error

    # for i in range(10):
    for i in range(11):
        x = labels[i][LBL_POS_X] + bdx - 5
        y = get_label_y(labels[i], block_dy)
        color = TAB_ASSET_FC
        size  = asset_size

        # Get prices and made calc
        if bolsas_mundo_value_test == 0:
            market_price, old_price = get_prices(asset_codes[i])

            # Converte preços para USD
            if usd and coin_asset_codes[i] != 'USD':
                c_market_price, c_old_price = get_prices(coin_asset_codes[i])
                market_price *= c_market_price
                old_price *= c_old_price

            diff_price = market_price - old_price
            try:
                diff_perc = diff_price / old_price * 100
            except:
                t_error = -1
                diff_perc = 0
        else:
            diff_perc = ((-1)**i) * bolsas_mundo_value_test

        # show arrow
        if diff_perc >= 0:
            img = SETA_ALTA
        else:
            img = SETA_BAIXA
        add_image(fig, img, x-TAB_ARROW_DX, y-14, 24, 24, xanchor='left', yanchor='top')

        # annot value%
        text = get_value_txt(abs(diff_perc), bold=True)
        add_annot(annotations, x-TAB_PERC_DX, y, text, color, size, xanchor='right')
        add_annot(annotations, x,    y, '%',  color, TAB_PERC_FS, xanchor='right')


world_flags =[
    'USA', 'USA', 'USA',
    'DEU', 'GBR', 'FRA', 'ESP',
    'CHN', 'JPN', 'HKG',
    'BRA',
]

def world_indexes_draw_rectangles(fig, labels, block_dy):
    # for i in range(10):
    for i in range(11):
        x = labels[i][LBL_POS_X]
        y = get_label_y(labels[i], block_dy)
        x0 = x - 10
        x1 = x + bdx + 5
        y0 = y - int(TAB_BHEI / 2 - 1)
        y1 = y + int(TAB_BHEI / 2 - 2)

        draw_rectangle(fig, x0, y0, x1, y1, color_back_rect)

        if TEMPLATE == 'JP_MERC_FIN':
            height = y1-y0 + 2.5
            width = height / 780 * 780 # 1191
            add_image(fig, f'images/{world_flags[i]}_ok.png', x0-width+2, y0-1.3, width, height, xanchor='left', yanchor='top')
        else:
            height = y1-y0
            width = height
            draw_rectangle(fig, x0-width/2+1, y0, x0+1, y1, color_back_rect)
            draw_circle(fig, x0-width, y0, x0, y1, TAB_BCIRC_COLOR)
            draw_circle(fig, x0-width+7, y0+7, x0-7, y1-7, TAB_BCIRCW_COLOR)
            add_image(fig, f'images/flags/{world_flags[i]}.png', x0-width+8, y0+8, width-16, height-16, xanchor='left', yanchor='top')




bolsas_mundo_value_test = 0  # -0.34  # test (0 to disable test)

def show_bolsas_mundo(fig, annotations, usd=False):
    global t_error
    t_error = 0

    add_image(fig, TAB_ICO_IMG, TAB_ICO_X, TAB_ICO_Y, TAB_ICO_W, TAB_ICO_H, xanchor='left', yanchor='top')

    world_indexes_draw_rectangles(fig, labels, bdy)

    for i in range(len(labels)):
        if 'BOLSAS NO MUNDO' in labels[i][0]:
            if usd:
                labels[i][0] = '<b>BOLSAS NO MUNDO EM US$</b>'
            else:
                labels[i][0] = '<b>BOLSAS NO MUNDO</b>'

    world_indexes_set_values(fig, annotations, bdy, usd)

    ts_market = {}
    ts_market['time'] = time.time() - 15 * 60  # 15 minutos de desconto
    # ts_market['gmtoffset'] = 3 * 3600  # Brasil -3h
    ts_market['timezone']  = 'BRST'

    market_time_ts = ts_market
    ts = market_time_ts['time']
    # if market_time_ts["timezone"] != 'BRST':
    #     ts += market_time_ts['gmtoffset'] + 3*3600  # 3h Brasil
    dt_obj = dt.fromtimestamp(ts)
    market_time = dt_obj.strftime('%d de %b. %H:%M')
    market_time +=  ' ' + market_time_ts["timezone"]

    labels[16][0] = f'<b>FONTE</b>: YAHOO FINANCE  -  {market_time}'

    set_labels(annotations, labels, bdy)

    if not t_error:
        fig.update_layout(
            annotations=annotations
        )

    return t_error




# Blocks(1,2,3) positions
cb1x, cb1y =  130, 200 # 166
cbdx = 600  # block distance between left and right text
cbdy =  48  # block distance to next one

clabels = [
    ['<b>DÓLAR</b>',    cb1x, cb1y, asset_color, asset_size, 0],
    ['<b>EURO</b>',     cb1x, cb1y, asset_color, asset_size, 1],
    ['<b>BITCOIN</b>',  cb1x, cb1y, asset_color, asset_size, 2],

    ['<b>MOEDAS</b>',   title_x, title_y, color_text_1, 53],
    ['<b>FONTE</b>: YAHOO FINANCE', dfont_x, dfont_y, color_text_4, 15],
]

c_asset_codes = [
    # 'BRL=X'
    'USDBRL=X', 'EURBRL=X', 'BTC-USD',
]


def coins_draw_rectangles(fig, labels, block_dy, graph='coins'):
    coin_img_file_name = ['dolar', 'euro', 'bitcoin']

    for i in range(3):
        x = labels[i][LBL_POS_X]
        y = get_label_y(labels[i], block_dy)
        x0 = x - 55
        x1 = x + cbdx + 5
        y0 = y - 23  # 21
        y1 = y + 21  # 18
        draw_rectangle(fig, x0, y0, x1, y1, color_back_rect)

        # coin symbol image
        if graph == 'coins':
            add_image(fig, f'images/{coin_img_file_name[i]}_ok.png', x0+8, y-18, 35, 35, xanchor='left', yanchor='top')


def coins_set_values(fig, annotations, labels, block_dy):
    global t_error

    coin_money_txt = ['R$', 'R$', 'US$']

    for i in range(3):
        x = labels[i][LBL_POS_X] + cbdx - 120
        y = get_label_y(clabels[i], block_dy)
        color = TAB_ASSET_FC
        size  = asset_size

        # Get prices and made calc
        if coins_value_test == 0:
            market_price, old_price = get_prices(c_asset_codes[i])
            diff_price = market_price - old_price
            try:
                diff_perc = diff_price / old_price * 100
            except:
                t_error = -1
                diff_perc = 0
        else:
            market_price = coins_value_test
            diff_perc = ((-1)**i) * (market_price / 100000)

        # show arrow
        perc_x = x-150
        if diff_perc >= 0:
            img = SETA_ALTA
        else:
            img = SETA_BAIXA
        add_image(fig, img, perc_x-110, y-14, 24, 24, xanchor='left', yanchor='top')

        # price
        text = get_value_txt(market_price, bold=True)
        add_annot(annotations, x-20, y, text,  color, size)
        add_annot(annotations, x-20, y, coin_money_txt[i]+' ', color,  25, xanchor='right')

        # value%
        text = get_value_txt(abs(diff_perc), bold=True)
        add_annot(annotations, perc_x-TAB_PERC_DX, y, text, color, size, xanchor='right')
        add_annot(annotations, perc_x,    y, '%',  color, TAB_PERC_FS, xanchor='right')




coins_value_test = 0  # 56789.23  # test (0 to disable test)

def show_moedas(fig, annotations):
    global t_error
    t_error = 0

    if template_codes[template_num] == 'JP_':
        ico_img = 'images/focus/jp_merc_fin/IPCA.png'
    else:
        ico_img = 'images/ico_moedas_ok.png'

    add_image(fig, ico_img, 22, 20, 42, 42, xanchor='left', yanchor='top')

    coins_draw_rectangles(fig, clabels, cbdy)

    # Adiciona timestamp com 15 minutos de atraso
    dt_obj = dt.fromtimestamp(time.time() - 15 * 60)
    market_time = dt_obj.strftime('%d de %b. %H:%M') + ' BRST'
    clabels[4][0] = f'<b>FONTE</b>: YAHOO FINANCE  -  {market_time}'

    set_labels(annotations, clabels, cbdy)

    coins_set_values(fig, annotations, clabels, cbdy)

    if not t_error:
        fig.update_layout(
            annotations=annotations
        )

    return t_error



# pb1x, pb1y =  130, 200
# cbdx = 600  # block distance between left and right text
# cbdy =  48  # block distance to next one

plabels = [
    ['<b>BARRIL BRENT (EM R$)</b>', cb1x, cb1y, asset_color, asset_size, 0],
    ['<b>GASOLINA (NA BOMBA)</b>',  cb1x, cb1y, asset_color, asset_size, 1],
    ['<b>DIESEL (NA BOMBA)</b>',    cb1x, cb1y, asset_color, asset_size, 2],

    ['<b>Petróleo e Derivados</b>', title_x, title_y, color_text_1, 53],
    ['TEMPO', dfont_x, dfont_y+10, color_text_4, 20],
    ['<b>FONTE</b>: ANP/YAHOO FINANCE', dfont_x, 500, color_text_4, 15],
]

def oil_set_values(fig, annotations, labels, block_dy):
    global t_error

    # oil_money_txt = ['R$', 'R$', 'R$']

    mult_load_data()

    for i in range(3):
        x = labels[i][LBL_POS_X] + cbdx - 120
        y = get_label_y(clabels[i], block_dy)
        color = TAB_ASSET_FC
        size  = asset_size

        # Get prices and made calc
        if i == 0: df = load_brent()
        if i == 1: df = load_gasol()
        if i == 2: df = load_diesel()

        # display(df)
        val_col_name = ['close_R', 'valor', 'valor']

        old_price = df[df.index >= date_ini].iloc[ 0][val_col_name[i]]
        new_price = df[df.index <= date_end].iloc[-1][val_col_name[i]]

        diff_price = new_price - old_price
        try:
            diff_perc = diff_price / old_price * 100
        except:
            t_error = -1
            diff_perc = 0

        # Verica se data está muito longe da selecionada (mais de 35 dias)
        date_min = df[df.index >= date_ini].index[ 0]
        date_max = df[df.index <= date_end].index[-1]
        if abs((date_min-date_ini).days) > 35 or abs((date_max-date_end).days) > 35:
            t_error = -1
            diff_perc = 0

        # show arrow
        perc_x = x + 50  # -150
        if diff_perc >= 0:
            img = SETA_ALTA
        else:
            img = SETA_BAIXA
        add_image(fig, img, perc_x-140, y-14, 24, 24, xanchor='left', yanchor='top')

        # # price
        # text = get_value_txt(new_price, bold=True)
        # add_annot(annotations, x-20, y, text,  color, size)
        # add_annot(annotations, x-20, y, oil_money_txt[i]+' ', color,  25, xanchor='right')

        # value%
        text = get_value_txt(abs(diff_perc), bold=True)
        # text = get_value_txt(diff_perc, bold=True)
        add_annot(annotations, perc_x-TAB_PERC_DX, y, text, color, size, xanchor='right')
        add_annot(annotations, perc_x,    y, '%',  color, TAB_PERC_FS, xanchor='right')

def show_petroleo(fig, annotations):
    global t_error
    t_error = 0

    # add_image(fig, 'images/ico_bolsas_mundo_ok.png', 22, 20, 42, 42, xanchor='left', yanchor='top')

    coins_draw_rectangles(fig, clabels, cbdy, graph='')

    plabels[4][0] = f'VARIAÇAO DE PREÇO ENTRE \xa0{date_ini.strftime("%d/%m/%Y")}\xa0 E \xa0{date_end.strftime("%d/%m/%Y")}'
    set_labels(annotations, plabels, cbdy)

    oil_set_values(fig, annotations, clabels, cbdy)

    if not t_error:
        fig.update_layout(
            annotations=annotations
        )

    return t_error


def tables_error():
    return t_error


def table_set_dates(date_ini_0, date_end_0):
    global date_ini, date_end
    date_ini = date_ini_0
    date_end = date_end_0
