from .pres_template import *

import pandas as pd
from datetime import datetime, timedelta, timezone
import random
from .graphics import *
from .coins import *


dff, dff_old = 0, 0   # DataFrame Focus

def focus_download(msg_lbl):
    global dff

    if msg_lbl not in [False, None]:
        msg_lbl.value = 'Downloading FOCUS (Wait...)'

    # Aqui poderia baixar só o final e adicionar no arquivo já baixado
    # O problema seria se mudassem o passado (tem que pesquisar se esse problema acontece)
    url = ('https://olinda.bcb.gov.br/olinda/servico/'
        'Expectativas/versao/v1/odata/ExpectativasMercadoAnuais?'
        '$top=8000&$orderby=Data%20desc&'
        '$format=text/csv&'
        'select=Indicador,IndicadorDetalhe,Data,DataReferencia,Media,Mediana,DesvioPadrao,Minimo,Maximo,numeroRespondentes,baseCalculo'
        f'&rnd={random.random()}'
        )
    # print(url)
    # https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ExpectativasMercadoAnuais?$top=100&$orderby=Data%20desc&$format=text/csv&select=Indicador,IndicadorDetalhe,Data,DataReferencia,Media,Mediana,DesvioPadrao,Minimo,Maximo,numeroRespondentes,baseCalculo&rnd=167
    try:
        df_new = pd.read_csv(url, decimal=",")
    except:
        if msg_lbl not in [False, None]:
            msg_lbl.value = 'FOCUS Download Error (try again later)'
        return

    try:
        dff = df_add_new_rows(dff_old, df_new).sort_values(['Indicador', 'Data'])
        dff.to_csv('data/focus.csv', index=False, compression='zip')
        focus_adjust_data()
    except:
        if msg_lbl not in [False, None]:
            msg_lbl.value = 'FOCUS Saving File Error'
        return

    if msg_lbl not in [False, None]:
        msg_lbl.value = ''


def focus_check_new_data(msg_lbl):
    # última data no arquivo já baixado, e data agora
    last_date = pd.to_datetime(dff.Data.iloc[-1])
    date = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(hours=-3)

    # Se for segunda antes das 9h, volta 1 dia (ainda não tem focus novo)
    if date.weekday() == 0 and date.hour < 8:  # 9
        date -= timedelta(days=1)

    # Última segunda após as 9h
    date -= timedelta(days=date.weekday())

    # terça da semana anterior
    date -= timedelta(days=6)

    # baixar dados novos
    if last_date < date:
        focus_download(msg_lbl)


def focus_adjust_data():
    dff['week'] = pd.to_datetime(dff['Data']).dt.year*100 + pd.to_datetime(dff['Data']).dt.isocalendar().week
    dff['dow']  = pd.to_datetime(dff['Data']).dt.dayofweek


def focus_load_data():
    global dff, dff_old
    if type(dff) == int:
        dff = pd.read_csv('data/focus.csv', skipinitialspace=True, compression='zip', low_memory=False)
        dff_old = dff.copy()
        focus_adjust_data()


def show_focus(fig, annot, symbol, focus_year, date_ini, date_end, debug=None):
    focus_load_data()
    # if not gvar['ONLINE']:
    focus_check_new_data(debug)

    date_ret = dff.Data.iloc[-1]

    gvar['decimal'] = 2

    if symbol == 'FOCUS_Simples':
        show_focus_simple(fig, annot, focus_year, debug=debug)
    elif symbol == 'FOCUS_Dados_2':
        show_focus_data(fig, annot, focus_year, gtype=2, debug=debug)
    elif symbol == 'FOCUS_Dados':
        show_focus_data(fig, annot, focus_year, debug=debug)
    else:
        show_focus_graph(fig, annot, symbol, focus_year, date_ini, date_end, debug=debug)
        date_ret = focus_year

    return date_ret


def show_focus_simple(fig, annot, focus_year, debug=None):
    vars  = ['IPCA', 'PIB Total', 'Câmbio', 'Selic']
    title = ['IPCA', 'PIB',       'CÂMBIO', 'SELIC']
    icons = ['IPCA', 'PIB',       'CAMBIO', 'SELIC']
    # types = ['(%)',  '(%)',     '(R$/US$)', '(%'+'a.a.)']  # Esses $---$ geram itálico no arquivo salvo
    types = ['(%)',  '(%)',       '(US$)',  '(%'+'a.a.)']

    set_graph_center(FOCUS_BLK_X + (FOCUS_BLK_DX + FOCUS_BLK_W) / 2)

    ######################
    # TEXTS BELOW BLOCKS
    ######################

    x = FOCUS_BLK_X
    y = FOCUS_BLK_Y + 1 * FOCUS_BLK_DY + FOCUS_BLK_H + 4
    add_annot(annot, x, y, 'FIM DE PERÍODO',
        FOCUS_FOOT_COLOR, FOCUS_FOOT_FONT_SIZE, yanchor='top')

    x = FOCUS_BLK_X + 1 * FOCUS_BLK_DX
    add_annot(annot, x, y, 'META FIM DE PERÍODO',
        FOCUS_FOOT_COLOR, FOCUS_FOOT_FONT_SIZE, yanchor='top')


    for i in range(4):
        lin = i // 2
        col = i %  2


        ################
        # BLOCK HEADER
        ################
        x1 = FOCUS_BLK_X + col * FOCUS_BLK_DX
        y1 = FOCUS_BLK_Y + lin * FOCUS_BLK_DY
        x2 = x1 + FOCUS_BLK_W
        y2 = y1 + FOCUS_BLK_H
        x1o, y1o, x2o, y2o = x1, y1, x2, y2

        tit_x = x1+FOCUS_TIT_DX
        tit_y = y1+FOCUS_TIT_DY

        add_annot(annot, tit_x, tit_y,
            f'<b>{title[i]}</b>',
            FOCUS_TIT_COLOR, FOCUS_TIT_FONT_SIZE,
            xanchor='center')

        add_annot(annot, tit_x + 90, tit_y, types[i],
            FOCUS_TYPE_COLOR, FOCUS_TYPE_FONT_SIZE)

        img = FOCUS_IMAGES + icons[i] + '.png'
        add_image(fig, img, tit_x - 76, tit_y,
                FOCUS_ICON_W, FOCUS_ICON_H, xanchor='right', yanchor='middle')


        ##############
        # BLOCK DATA
        ##############
        x1 += FOCUS_BLK_IN_DX
        y1 += FOCUS_BLK_IN_DY
        draw_rectangle(fig, x1, y1, x2, y2, FOCUS_BLK_COLOR)
        draw_line(fig, tit_x, y1+FOCUS_DATA_Y1, tit_x, y1+FOCUS_DATA_Y2, T_COLOR_5)
        draw_rectangle_line(fig, x1o, y1o, x2o, y2o, FOCUS_BLK_LINE_C, FOCUS_BLK_LINE_W)

        years = [focus_year, focus_year+1]
        for pos in range(2):
            year = years[pos]

            add_annot(annot, x1+FOCUS_DATA_X[pos], y1+FOCUS_DATA_Y1, f'{year}',
                FOCUS_DATA_COLOR, FOCUS_DATA_FONT_SIZE[0],
                xanchor='center')

            # Last day of each week
            dff2 = dff[
                    (dff.Indicador==vars[i]) &
                    (dff.DataReferencia == year) &
                    (dff.baseCalculo == 0)
                ]
            idx = dff2.groupby(['week'])['dow'].transform(max) == dff2['dow']
            df  = dff2[idx]

            val_old  = round(df.iloc[-2].Mediana, 2)
            val      = round(df.iloc[-1].Mediana, 2)

            val_txt = get_value_txt(val, bold=True)
            add_annot(annot, x1+FOCUS_DATA_X[pos], y1+FOCUS_DATA_Y2, val_txt,
                FOCUS_DATA_COLOR, FOCUS_DATA_FONT_SIZE[1],
                xanchor='center')

            if val <  val_old: img = 'BAIXA'
            if val == val_old: img = 'EQUIVALENTE'
            if val >  val_old: img = 'ALTA'
            img = FOCUS_IMAGES + img + '.png'
            add_image(fig, img,x1+FOCUS_DATA_X[pos]-24, y1+FOCUS_DATA_Y2,
                FOCUS_ARROW_W, FOCUS_ARROW_H, xanchor='right', yanchor='middle', layer='above')


def show_focus_data(fig, annot, focus_year, gtype=None, debug=None):
    vars  = ['IPCA', 'IPCA', 'PIB Total', 'Câmbio', 'Selic']
    basec = [ 0,      1,      0,           0,        0     ]
    title = ['IPCA', 'IPCA', 'PIB',       'CÂMBIO', 'SELIC']
    icons = ['IPCA', 'IPCA', 'PIB',       'CAMBIO', 'SELIC']
    types = ['\xa0  (%)', '\xa0  (%)', '(var. %)',  '\xa0  (US$)', '  (%'+'a.a.)']

    DVAR = FOCUS2_VAR_DISTANCE
    dx = 6

    # years on header
    years = [focus_year, focus_year+1, focus_year+2, focus_year+3]

    focus2_blk_y = FOCUS2_BLK_Y
    focus2_blk_w = FOCUS2_BLK_W

    # Tabela com menos informação
    if gtype == 2:
        focus2_blk_y = FOCUS2_BLK_Y2
        focus2_blk_w = FOCUS2_BLK_W2
        years = [focus_year, focus_year+1]
        del vars[1]
        del basec[1]
        del title[1]
        del icons[1]
        del types[1]

    set_graph_center(FOCUS2_BLK_X + focus2_blk_w / 2)

    # Yers header block
    x1 = FOCUS2_BLK_X + FOCUS2_BLK_IN_DX
    y1 = focus2_blk_y - FOCUS2_HEADER_H - 4
    x2 = FOCUS2_BLK_X + focus2_blk_w
    y2 = focus2_blk_y - 4

    draw_rectangle(fig, x1, y1, x2, y2, FOCUS2_HEADER_BLK_COLOR)

    for pos in range(len(years)):
        x = x1 + FOCUS2_DATA_X[pos]
        y = y1 + FOCUS2_HEADER_H / 2 + 2

        xyear = x - DVAR / 2
        if pos >= 2:
             xyear += DVAR

        year_color = FOCUS2_HEADER_BLK_COLOR
        if template_codes[template_num] == 'JP_':
            year_color = FOCUS2_TIT_COLOR

        add_annot(annot, xyear, y1-30, years[pos],
            year_color, FOCUS2_HEADER_BLK_FS, xanchor='center')

        add_annot(annot, x+dx, y, '<b>HOJE</b>',
            FOCUS2_HEADER_TXT_COLOR, FOCUS2_HEADER_TXT_FS, xanchor='center')

        add_annot(annot, x+DVAR, y, 'COMP.<br>SEMANAL',
            FOCUS2_HEADER_TXT_COLOR, FOCUS2_HEADER_TXT_FS, xanchor='center')

        if pos < 2:
            add_annot(annot, x+dx-DVAR, y, 'HÁ 1<br>SEMANA',
                FOCUS2_HEADER_TXT_COLOR, FOCUS2_HEADER_TXT_FS, xanchor='center')

            add_annot(annot, x+dx-DVAR*2, y, 'HÁ 4<br>SEMANAS',
                FOCUS2_HEADER_TXT_COLOR, FOCUS2_HEADER_TXT_FS, xanchor='center')


    for i in range(len(vars)):

        ################
        # BLOCK HEADER
        ################
        x1 = FOCUS2_BLK_X
        y1 = focus2_blk_y + i * FOCUS2_BLK_DY
        x2 = x1 + focus2_blk_w
        y2 = y1 + FOCUS2_BLK_H
        x1o, y1o, x2o, y2o = x1, y1, x2, y2

        tit_x = x1 + FOCUS2_TIT_DX
        tit_y = y1 + FOCUS2_TIT_DY

        font_size = FOCUS2_TIT_FONT_SIZE
        if icons[i] == 'CAMBIO':
            font_size *= 0.8
        add_annot(annot, tit_x, tit_y,
            f'<b>{title[i]}</b>',
            FOCUS2_TIT_COLOR, font_size,
            xanchor='center')

        if basec[i] == 1:
            add_annot(annot, tit_x, tit_y + 27, 'ÚLTIMOS 5 DIAS ÚTEIS',
                FOCUS2_TIT_COLOR, 15, xanchor='center')

        add_annot(annot, tit_x + 56, tit_y, types[i],
            FOCUS2_TYPE_COLOR, FOCUS2_TYPE_FONT_SIZE)

        img = FOCUS2_IMAGES + icons[i] + '.png'
        add_image(fig, img, tit_x - 64, tit_y,
                FOCUS_ICON_W, FOCUS_ICON_H, xanchor='right', yanchor='middle')


        ##############
        # BLOCK DATA
        ##############
        x1 += FOCUS2_BLK_IN_DX
        y1 += FOCUS2_BLK_IN_DY
        draw_rectangle(fig, x1, y1, x2, y2, FOCUS2_BLK_COLOR)
        draw_rectangle_line(fig, x1o, y1o, x2o, y2o, FOCUS2_BLK_LINE_C, FOCUS2_BLK_LINE_W)

        for pos in range(len(years)):
            year = years[pos]

            # add_annot(annot, x1+FOCUS_DATA_X[pos], y1+FOCUS_DATA_Y1, f'{year}',
            #     FOCUS_DATA_COLOR, FOCUS_DATA_FONT_SIZE[0],
            #     xanchor='center')

            # Last day of each week
            dff2 = dff[
                    (dff.Indicador==vars[i]) &
                    (dff.DataReferencia == year) &
                    (dff.baseCalculo == basec[i])
                ]
            idx = dff2.groupby(['week'])['dow'].transform(max) == dff2['dow']
            df  = dff2[idx]

            val_old2 = round(df.iloc[-5].Mediana, 2)
            val_old  = round(df.iloc[-2].Mediana, 2)
            val      = round(df.iloc[-1].Mediana, 2)

            x = x1 + FOCUS2_DATA_X[pos]

            # Vertical trace lines
            if pos < len(years) - 1:
                xlin = x + DVAR + DVAR/2
                draw_line(fig, xlin, y1, xlin, y2, T_COLOR_5, dash='dot')

            # 'HOJE' value
            val_txt = get_value_txt(val, bold=True)
            add_annot(annot, x+dx, tit_y, val_txt,
                FOCUS2_DATA_COLOR, FOCUS2_DATA_FONT_SIZE,
                xanchor='center')

            if pos < 2:
                val_txt = get_value_txt(val_old)
                add_annot(annot, x+dx-DVAR, tit_y, val_txt,
                    FOCUS2_DATA_COLOR, FOCUS2_DATA_FONT_SIZE,
                    xanchor='center')

                val_txt = get_value_txt(val_old2)
                add_annot(annot, x+dx-DVAR*2, tit_y, val_txt,
                    FOCUS2_DATA_COLOR, FOCUS2_DATA_FONT_SIZE,
                    xanchor='center')


            st  = np.sign(val - val_old)
            if st == -1: img = 'BAIXA'
            if st ==  0: img = 'EQUIVALENTE'
            if st ==  1: img = 'ALTA'

            weeks = 0
            while np.sign(val - val_old) == st:
                weeks += 1
                val = val_old
                val_old = round(df.iloc[-2 -weeks].Mediana, 2)

            add_annot(annot, x+DVAR+10, tit_y, f'{weeks}',
                FOCUS2_DATA_COLOR, FOCUS2_DATA_FONT_SIZE,
                xanchor='center')

            img = FOCUS_IMAGES + img + '.png'
            add_image(fig, img,x+DVAR+10-28, tit_y,
                FOCUS2_ARROW_W, FOCUS2_ARROW_H, xanchor='center', yanchor='middle')


def show_focus_graph(fig, annot, symbol, year, date_ini, date_end, debug=None):

    vars = ['IPCA', 'PIB Total', 'Câmbio', 'Selic']
    if symbol == 'FOCUS_IPCA':   var = vars[0]
    if symbol == 'FOCUS_PIB':    var = vars[1]
    if symbol == 'FOCUS_Cambio': var = vars[2]
    if symbol == 'FOCUS_SELIC':  var = vars[3]

    dff2 = dff[
        (dff.Indicador==var) &
        (dff.DataReferencia == year) &
        (dff.baseCalculo == 0)
    ]
    idx = dff2.groupby(['week'])['dow'].transform(max) == dff2['dow']
    df  = dff2[idx]
    df['Data'] = df['Data'].astype(np.datetime64)
    df = df[(df.Data >= date_ini) & (df.Data <= date_end)]


    set_ref_type(xref='paper', yref='paper')
    left, right = 200, 400
    if template_codes[template_num] in ['IN_', 'INB_', 'NEC_']:
        right = 100
    set_margins(fig, left, right, 200, 160, 4)
    set_graph_center((left - right)/2)  # valor negativo (Subtrai do centro)
    GS = get_scale()

    fig.add_trace(
        go.Scatter(marker_color="#2457BD", mode="lines",
            x = df.Data,
            y = df.Mediana,
            line=dict(color=T_COLOR_6, width=3*GS),
        )
    )

    gridcolor = '#EEEEEE'
    if BG_COLOR != 'white':
        gridcolor = '#333333'

    time_format = 500 * 24*3600 * 100
    fig.update_xaxes(
        visible=True,
        # range=[df.Data.min(), df.Data.max()],
        color=T_COLOR_6,
        tickfont=dict(size=BAR_DATE_FONT_SIZE*GS),
        # tickformat='%m/%Y',
        tickformatstops = [
            dict(dtickrange=[None, time_format], value='%d/%m/%Y'),
            dict(dtickrange=[time_format, None], value='%m/%Y'),
        ],
        gridcolor=gridcolor, gridwidth=1*GS, showgrid=True,
        linecolor = T_COLOR_6, showline=True,
        showspikes=True, ticks='outside',
    )

    fig.update_yaxes(
        visible=True,
        # range=[df.Mediana.min() * 0.90, df.Mediana.max() * 1.10],
        color=T_COLOR_6, nticks=5,
        tickfont=dict(size=BAR_VAL_FONT_SIZE*GS),
        gridcolor=gridcolor, gridwidth=1*GS, showgrid=True,
        showline=False,
        scaleanchor='y',
    )

    fig.update_layout(
        yaxis_tickformat = ',.2f',  # 'digits'
        separators=',.',
    )
