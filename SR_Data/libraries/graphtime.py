from .pres_template import *

# import numpy as np
import pandas as pd
import re
# import locale
# locale.setlocale(locale.LC_ALL, 'pt_BR')
# import investpy
# from pandas.tseries.offsets import MonthEnd
from .graphics import *
from .graphcomp import *
from .symbols import *
# from .coins import *
# from .assets import *
from .ingraph import set_001_GS
from .digitado import *


def add_dfont(dfont, newdf):
    if newdf not in dfont:
        if dfont != '':
            dfont += ', '
        dfont += newdf
    return dfont

def draw_graph_time(fig, annot, date_ini, date_end, glist, debug=None):
    set_ref_type(xref='paper', yref='paper')
    set_margins(fig, *GT_MARGINS_LRTBPAD)
    set_graph_center((GT_MARGINS_LRTBPAD[0] - GT_MARGINS_LRTBPAD[1])/2)  # valor negativo (Subtrai do centro)
    GS = get_scale()

    names, dfont = '', ''
    date_min = date_ini
    date_max = date_end
    dfg = {}

    showlegend = len(glist) > 1
    gpos = -1
    for gname in glist:
        gpos += 1
        gname_org = get_original_txt(gname, list(symbol_list.keys()))
        if gname_org != -1:
            gname = gname_org
            glist[gpos] = gname_org

        if gname[:3] == 'PRE':
            dfont = add_dfont(dfont, 'B3')
            # PRE20220128.csv
            df = pd.read_csv(f'data/b3/{gname}.csv')
            df['data'] = gname[3:7] + '-' + gname[7:9] + '-' + gname[9:11]
            df['data'] = df['data'].astype(np.datetime64)
            df['data'] = df['data'] + pd.to_timedelta(df['dias'], unit='D')
            # date_min = df.loc[0, 'data']
            # date_max = df.iloc[-1]['data']
            date_min = dt(day=1, month=1, year=2021)
            date_max = dt(day=31, month=12, year=2060)
            date_ini = date_min
            date_end = date_max
        elif gname == 'IPCA':
            dfont = add_dfont(dfont, 'IBGE')
            # df = pd.read_csv('data/ibge/1737_63_None.csv')
            df = pd.read_csv('Estudos/data_IBGE/IPCA_index.csv')
            df['data'] = ((df.data//10000).astype(str) + '-' +
                (df.data%10000//100).astype(str) + '-' +  (df.data%100).astype(str)
                ).astype(np.datetime64)
        elif gname == 'IGPM':
            dfont = add_dfont(dfont, 'FGV')
            df = pd.read_csv('data/fgv/IGPM_BR.csv')
            df['data'] = (df.date.str.slice(3,7) + '-' +
                df.date.str.slice(0,2) + '-01').astype(np.datetime64)
            df['valor'] = df.nindex
        elif gname == 'CDI':
            dfont = add_dfont(dfont, 'B3')
            df = load_cdi(True)
            df.rename(columns={'date':'data'}, inplace=True)
            df['valor'] = df.nindex
        # GAMBIARRA (explicação no Gambiarras.txt)
        elif gname in symbol_list and exists(f'data/digitado/{gname}.csv'):
            datahead, skiprows = load_info_digitado(gname)
            dfont = add_dfont(dfont, symbol_list[gname]['dfont'])
            df = load_data_digitado(gname, datahead, skiprows)
            df.columns = ['data', 'valor']
            date_type = symbol_list[gname].get('date_type',
                        discover_date_type(df.iloc[0,0]) )
            df['data'] = df['data'].apply(convert_to_date, args=[date_type])
        elif gname[:5].lower() in ['gasol', 'diese', 'etano']:
            dfont = add_dfont(dfont, 'ANP')
            if gname[:5].lower() == 'gasol': df = load_gasol().copy()
            if gname.lower() == 'diesel': df = load_diesel().copy()
            if gname.lower() == 'etanol': df = load_etanol().copy()
            df.index.name = 'data'
            if gvar.get('ipca_on', False):  # Add default False value for ipca_on check
                df['valor'] = df['infla_br']
            df.reset_index(inplace=True)
        elif gname.lower() == 'brentr':
            dfont = add_dfont(dfont, 'YAHOO FINANCE')
            df = load_brent().copy()
            df.index.name = 'data'
            df.reset_index(inplace=True)
            df['valor'] = df['close_R']
        elif gname[:4].lower() == 'inv_':
            dfont = add_dfont(dfont, 'Investing')
            from_date = date_ini.strftime('%d/%m/%Y')
            to_date   = '31/12/2029'
            vars = re.split('_|-|,|/', gname[4:])
            vars = [x.strip().lower() for x in vars]
            try:
                if 'com' in vars[0]:  # acrescentar novas commodities em: investpy/resources/commodities.csv
                    df = investpy.get_commodity_historical_data(commodity=vars[1], from_date=from_date, to_date=to_date)
                elif 'sto' in vars[0]:
                    df = investpy.get_stock_historical_data(stock=vars[1], country=vars[2], from_date=from_date, to_date=to_date)
                elif 'ind' in vars[0]:
                    df = investpy.get_index_historical_data(index=vars[1], country=vars[2], from_date=from_date, to_date=to_date)
                elif 'cur' in vars[0]:
                    df = investpy.get_currency_cross_historical_data(currency_cross=vars[1], from_date=from_date, to_date=to_date)
                else:
                    continue
            except: continue

            df.reset_index(inplace=True)
            df.rename(columns={'Date':'data', 'Close':'valor'}, inplace=True)
        else:
            dfont = add_dfont(dfont, 'YAHOO FINANCE')
            df = get_asset_data(gname, date_ini)
            df.rename(columns={'datet':'data', 'close':'valor'}, inplace=True)

            # mult_load_data()
            # if gname == 'BTC-USD':
            #     display(df)
            #     display(get_df_usd())

        # Last day of month
        if gname in ['IPCA', 'IGPM']:
            df['data'] = pd.to_datetime(df['data'], format="%Y%m") + MonthEnd(1)

        df = df[(df.data >= date_ini) & (df.data <= date_end)].reset_index()
        if df.loc[0, 'data'] > date_min:
            date_min = df.loc[0, 'data']
        if df.iloc[-1]['data'] < date_max:
            date_max = df.iloc[-1]['data']
        dfg[gname] = df.copy()

    perc_max = 0
    for gname in glist:
        df = dfg[gname].copy()
        df = df[(df.data >= date_min) & (df.data <= date_max)].reset_index()

        valor0 = df.loc[0, 'valor']
        if gname[:3] == 'PRE':
            df['valor2'] = df.valor / 100
        else:
            df['valor2'] = (df.valor / valor0 - 1)  # * 100
        dfg[gname] = df.copy()

        perc = df.iloc[-1]['valor2']
        if perc > perc_max:
            perc_max = perc

    if gvar.get('grapht_val', False):
        vprecis = 2
        if df.iloc[0]['valor'] > 1000: vprecis = 0

    precis = 2
    perc_max *= 100
    if perc_max >  100: precis = 1
    if perc_max > 1000: precis = 0

    pos = 0
    for gname in glist:
        df = dfg[gname].copy()

        perc = df.iloc[-1]['valor2']
        perc_str = locale.format_string(f'%0.{precis}f', perc*100, grouping=True)

        name = asset_code_to_name(gname)
        names += f'{name}, '

        # line_color = [3, '#6688AA', 1]
        if TEMPLATE == 'INVEST_NEWS_BLACK':
            line_color = [1, 5, 6]
        else:
            line_color = ['#557799', 1, 3,  '#000044', '#000077', '#0000CC', '#444444', '#666666', '#999999']
        line_color += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]

        if gvar.get('grapht_val', False):
            y_values = df.valor
            yaxis_tickformat = f',.{vprecis}f'
        else:
            y_values = df.valor2
            yaxis_tickformat = f',.{precis}%'

        show_leg = True
        if gname in symbol_list:
            show_leg = symbol_list[gname].get('show_leg', True)
        if show_leg == 0:
            showlegend = False
        if show_leg == 'only_name':
            leg_name = f'{name}'
        else:
            leg_name = f'{name} ({perc_str}%)'
            showlegend = True

        fig.add_trace(
            go.Scatter(
                x=df.data, y=y_values, name=leg_name,
                line=dict(width=3*GS, color=get_txt_color(line_color[pos], ret_bold=False)), mode='lines',
            ))

        pos += 1

    # legend_x = gvar.get('mouse_x', GT_LEGEND_X)
    # legend_y = gvar.get('mouse_y', GT_LEGEND_Y)
    legend_x = get_config_var('legend_x', GT_LEGEND_X)
    legend_y = get_config_var('legend_y', GT_LEGEND_Y)
    fig.update_layout(
    #     hoverlabel=dict(align='right'), # bgcolor='black'),
        yaxis_tickformat = yaxis_tickformat,
        separators=',.', yaxis_zeroline=False, xaxis_zeroline=False,
        showlegend=showlegend, legend=dict(
        font=dict(size=GT_LEGEND_FS*GS, color=GT_LEGEND_FC),
        x=legend_x, y=legend_y, xanchor='auto',
        bgcolor='rgba(0,0,0,0)'))

    gridcolor = '#EEEEEE'
    if BG_COLOR != 'white':
        gridcolor = '#333333'

    fig.update_xaxes(
        visible=True,
        color=GT_AXIS_FC,
        tickfont=dict(size=GT_XAXIS_FS*GS),
        gridcolor=gridcolor, gridwidth=1*GS, showgrid=True,
        linecolor = GT_AXIS_FC, showline=True,
        showspikes=True, ticks='outside',
    #     title='Tamanho da janela (em meses)',
    )

    fig.update_yaxes(
        visible=True,
        color=GT_AXIS_FC, # nticks=5,
        tickfont=dict(size=GT_YAXIS_FS*GS),
        gridcolor=gridcolor, gridwidth=1*GS, showgrid=True,
    #     title='Vitórias'
    )

    if gvar.get('grapht_val', False):
        subtit = 'Valores entre'
    else:
        subtit = 'Acumulado em % entre'

    subtit += f' {date_min.strftime("%d/%m/%Y")} E {date_max.strftime("%d/%m/%Y")} '

    return names[:-2], subtit, dfont, date_min, date_max




##############################################################
#                           001_
##############################################################

from .ingraph import *
from .ingpos import *

g001_error = 0
g001_period = 0

def main_001(fig, GS):
    set_001_GS(GS)

    set_ref_type(xref='paper', yref='paper')
    # Graph Line
    fig.add_trace(
        go.Scatter(marker_color="#2457BD", mode="lines")
    )

    # # Graph Layout
    set_layout(fig)

    draw_block_info(fig)

    init_close_line(fig)


def draw_graph_001(fig, annot, date_ini, date_end, symbol, bg_transparent, debug=None):
    global g001_error
    g001_error = 0

    GS = get_scale()
    main_001(fig, GS)

    if TEMPLATE == 'INVEST_NEWS_BLACK':
        add_image(fig, 'images/invest_news/InvNews_Bg_Black.jpeg', 0, 0,
                1080, 1080, xanchor='left', yanchor='top', layer='below')

    period = g001_period

    update_data(symbol)

    if get_dojo_error():
        g001_error = -1
        return

    try:
        df = df_period[period]
        if bt_interval[period] == '1d':
            df['price'] = df.close
        else:
            df['price'] = df.open

        info_prices = get_info_prices(period)

        info = data[0]['chart']['result'][0]['meta']

        ts_market = {}
        ts_market['time']      = info['regularMarketTime']
        ts_market['gmtoffset'] = info['gmtoffset']
        ts_market['timezone']  = info['timezone']

        currency = info['currency']

        if currency == 'BRL':
            separators=',.'
            locale.setlocale(locale.LC_ALL, 'pt_BR')
        else:
            separators='.,'
            locale.setlocale(locale.LC_ALL, 'en_US')

        ts_market_ok = ts_market
        # if HOLI_checked:
        #     ts_market_ok = 0
        update_labels(fig, period, df.price, info_prices, ts_market_ok, symbol, currency)

        if period == 0:
            show_close_line(fig, info_prices[1])
        else:
            hide_close_line(fig)

        # Update axis and line of the graph
        scatter = fig.data[0]
        scatter.line=dict(color=diff_price_label[LBL_POS_COLOR], width=GT_TRACE_WIDTH*GS)
        scatter.x = df.dtime[::per_intspace[period]]
        scatter.y = df.price[::per_intspace[period]]

        # Max of ticks
        tick_divisor = 6
        if period == 1 or period == 6:  # 5 days / 5 years
            tick_divisor = df.dtime.size
        tick_step = df.dtime.size // tick_divisor
        tickvals = df.dtime[::per_intspace[period]][::tick_step].to_list()
        ticktext = df.dtformat[::per_intspace[period]][::tick_step].to_list()

        # Remove repeated ticks
        tpos = 1
        while tpos < len(ticktext):
            if ticktext[tpos] == ticktext[tpos-1]:
                ticktext.pop(tpos)
                tickvals.pop(tpos)
            else:
                tpos += 1
        if period >= 6:  # Removes first year to not overlap
            ticktext.pop(0)
            tickvals.pop(0)

        # Update ticks in x axis
        fig.update_xaxes(
            # tickangle=45,
            tickmode = 'array',
            tickvals = tickvals,
            ticktext = ticktext)

        # decimal places if number is greater than 1000
        if info_prices[0] < 1000:
            yaxis_tickformat = ',.2f'
        else:
            yaxis_tickformat = ',.0f'

        # y axix superior limit
        ytick_max = max(info_prices[2], info_prices[1]) + (info_prices[2] - info_prices[3]) * 0.10
        ytick_min = min(info_prices[3], info_prices[1]) * 0.9999 # precisa dessa mult. para exibir (próx. do 0 não exibe linha pontilhada)

        bg_color = 'white'
        if bg_transparent:
            bg_color = 'rgba(0,0,0,0)'

        # set number format in y axis
        fig.update_layout(
            yaxis_tickformat = yaxis_tickformat,
            separators=separators,
            yaxis_range=[ytick_min, ytick_max], yaxis_nticks=6,
            paper_bgcolor=bg_color,
            plot_bgcolor=bg_color,
        )
    except:
        g001_error = -1


def get_g001_error():
    return g001_error

def set_g001_period(period_text):
    global g001_period
    g001_period = bt_text.index(period_text)
