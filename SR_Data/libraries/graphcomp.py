#  Afazer
# CPI americano: ver como atualizar automaticamente

from .pres_template import *

import numpy as np
import pandas as pd
# import locale
# locale.setlocale(locale.LC_ALL, 'pt_BR')
import investpy
from pandas.tseries.offsets import MonthEnd
from .graphics import *
from .coins import *

path = 'Estudos/'

# DataFrames globais
df_cpi = 0
df_ipca, df_ipca_today = 0, 0
df_usd = 0
df_bov = 0
df_nasdaq = 0
df_res = 0
df_gasol, df_diesel, df_etanol, df_brent = 0, 0, 0, 0


def mult_load_data():
    if type(df_cpi) == int:
        load_pci_usa()
        load_ipca()
        load_USD_BRL()
        load_ibov()
        load_nasdaq()
        load_cdi()
        load_gasol()
        load_diesel()
        load_etanol()
        load_brent()

def show_graph_comp(fig, annot, symbol, debug=None):
    mult_load_data()

    gvar['gcomp_date_end'] = ''

    if symbol == 'GRAPH_GASOL':
        draw_graph_comp(fig, annot, df_gasol, 'valor')
    if symbol == 'GRAPH_GASOL_IPCA':
        draw_graph_comp(fig, annot, df_gasol, 'infla_br')

    if symbol == 'GRAPH_DIESEL':
        draw_graph_comp(fig, annot, df_diesel, 'valor')
    if symbol == 'GRAPH_DIESEL_IPCA':
        draw_graph_comp(fig, annot, df_diesel, 'infla_br')

    if symbol == 'GRAPH_ETANOL':
        draw_graph_comp(fig, annot, df_etanol, 'valor')
    if symbol == 'GRAPH_ETANOL_IPCA':
        draw_graph_comp(fig, annot, df_etanol, 'infla_br')

    if symbol == 'GRAPH_USD_x_BRL':
        draw_graph_comp(fig, annot, df_usd, 'infla')
    if symbol == 'GRAPH_IBOV_IPCA':
        draw_graph_comp(fig, annot, df_bov, 'infla_br')
    if symbol == 'GRAPH_IBOV_USD':
        draw_graph_comp(fig, annot, df_bov.loc['1994-07-01':], 'usd')
    if symbol == 'GRAPH_IBOV_USD_CPI':
        draw_graph_comp(fig, annot, df_bov.loc['1994-07-01':], 'usd_infla')
    if symbol == 'GRAPH_IBOV_USD_BRL':
        draw_graph_comp(fig, annot, df_bov.loc['1994-07-01':], 'usd_infla_br')

    if symbol == 'GRAPH_NASDAQ_CPI':
        draw_graph_comp(fig, annot, df_nasdaq, 'ind_infla')

    if symbol == 'GRAPH_IBOV_x_CDI':
        draw_graph_bovcdi(fig, annot)


def draw_graph_comp(fig, annot, df, col):
    set_ref_type(xref='paper', yref='paper')
    set_margins(fig, *CP_MARGINS_LRTBPAD)
    set_graph_center((CP_MARGINS_LRTBPAD[0] - CP_MARGINS_LRTBPAD[1])/2)  # valor negativo (Subtrai do centro)
    GS = get_scale()

    if TEMPLATE == 'INVEST_NEWS_BLACK':
        add_image(fig, 'images/invest_news/InvNews_Bg_Black.jpeg', 0, 0,
                1080, 1080, xanchor='left', yanchor='top', layer='below')

    gvar['gcomp_date_end'] = df.index[-1]  # Data final

    val_min = df[col].min()
    val_min_date = df[col].idxmin()

    val_max = df[col].max()
    val_max_date = df[col].idxmax()

    val_range = val_max - val_min

    curr_txt = 'R$'
    if col == 'infla_br':
        curr_txt = ''
    if col in ['usd', 'usd_infla', 'ind_infla']:
        curr_txt = 'US$'

    fig.add_trace(
        go.Scatter(
            x=df.index, y=df[col],
            hovertemplate = ' %{x|%d/%m/%Y} <br> ' + f'{curr_txt} ' + '%{y} <extra></extra>',
            line=dict(color=CP_TRACE_COLOR, width=CP_TRACE_WIDTH*GS),
        ))

    n_dec = 2
    if val_max > 10000:
        n_dec = 0

    fig.update_layout(
        hoverlabel=dict(align='right'), # bgcolor='black'),
        yaxis_tickformat = f',.{n_dec}f',
        separators=',.', yaxis_zeroline=False, xaxis_zeroline=False)

    gridcolor = '#EEEEEE'
    if BG_COLOR != 'white':
        gridcolor = '#333333'

    fig.update_xaxes(
        visible=True,
        color=CP_LINES_COLOR,
        tickfont=dict(size=CP_XAXIS_FS*GS),
        gridcolor=gridcolor, gridwidth=1*GS, showgrid=True,
        linecolor = CP_LINE0_COLOR, showline=True,
        showspikes=True, ticks='outside',)

    fig.update_yaxes(
        visible=True,
        color=CP_LINES_COLOR, # nticks=5,
        tickfont=dict(size=CP_YAXIS_FS*GS),
        gridcolor=gridcolor, gridwidth=1*GS, showgrid=True,)

    annot.append(dict(x=val_min_date, y=val_min - val_range/10,
        font=dict(color=SUBTIT_COLOR, size=BAR_DATE_FONT_SIZE*GS),
        text=f'<b>MIN = {curr_txt} {money_format(val_min)}<br>'
             f'{val_min_date.strftime("%d/%m/%Y")}</b>', showarrow=False,))

    annot.append(dict(x=val_max_date, y=val_max + val_range/10,
        font=dict(color=SUBTIT_COLOR, size=BAR_DATE_FONT_SIZE*GS),
        text=f'<b>{val_max_date.strftime("%d/%m/%Y")}<br>'
             f'MAX = {curr_txt} {money_format(val_max)}</b>', showarrow=False,))

    if col not in ['infla_br', 'ind_infla', 'valor']:
        dolar_atual = df_usd.iloc[-1].close
        annot.append(dict(x=1, y=1, xref='paper', yref='paper',
            font=dict(color=SUBTIT_COLOR, size=BAR_DATE_FONT_SIZE*GS),
            # bgcolor='white',  # removido pois aparecia fundo branco no vídeo
            # text=f'<b>1 US$ = R$ {money_format(dolar_atual)} ', showarrow=False,))
            text=f'<b> Dólar atual <br> R$ {money_format(dolar_atual)} ', showarrow=False,))


def draw_graph_bovcdi(fig, annot):
    set_ref_type(xref='paper', yref='paper')
    set_margins(fig, 200, 400, 200, 160, 10)
    GS = get_scale()

    date_ini = datetime(1994,  7,  4)
    date_end = datetime(2029, 12, 31)

    df_test = generate_all_windows(date_ini, date_end, 21, taxes=True)  # 21 dias uteis ~ 1 mês
    # df_test.to_excel('GRAPH_IBOV_x_CDI.xlsx')

    fig.add_trace(
        go.Scatter(#data=df_test,
            x=df_test.window_size, y=df_test.cdi_win/100, name='CDI',
            line=dict(color=T_COLOR_3, width=3*GS),
        ))

    fig.add_trace(
        go.Scatter(#data=df_test,
            x=df_test.window_size, y=df_test.bov_win/100, name='IBOV',
            line=dict(color=T_COLOR_2, width=3*GS),
        ))

    fig.update_layout(
        hoverlabel=dict(align='right'), # bgcolor='black'),
        yaxis_tickformat = ',.0%',
        separators=',.', yaxis_zeroline=False, xaxis_zeroline=False,
        showlegend=True, legend=dict(
        font=dict(size=GT_LEGEND_FS*GS, color=GT_LEGEND_FC),
        # x=legend_x, y=legend_y, xanchor='auto',
        # bgcolor='rgba(0,0,0,0)'
        ))

    gridcolor = '#EEEEEE'
    if BG_COLOR != 'white':
        gridcolor = '#333333'

    fig.update_xaxes(
        visible=True,
        color=CP_LINES_COLOR,
        tickfont=dict(size=CP_XAXIS_FS*GS),
        gridcolor=gridcolor, gridwidth=1*GS, showgrid=True,
        linecolor = CP_LINE0_COLOR, showline=True,
        showspikes=True, ticks='outside',
        title='Tamanho da janela (em meses)',

    )

    fig.update_yaxes(
        visible=True,
        color=CP_LINES_COLOR, # nticks=5,
        tickfont=dict(size=CP_YAXIS_FS*GS),
        gridcolor=gridcolor, gridwidth=1*GS, showgrid=True,
        title='Vitórias'
    )


######################################
#               CPI USA
######################################
def load_pci_usa():
    # https://data.bls.gov/cgi-bin/surveymost?cu (U.S. city average, All items - CUUR0000SA0)
    # https://fred.stlouisfed.org/categories/9 (CPI Not Seasonally Adjusted)

    df = pd.read_csv(path + 'data_BLS/CPI_USA.csv')

    # Colunas de interesse
    dates = []
    cpi_usa = []

    for year in range(df.Year.min(), df.Year.max()+1):
        for month in range(1, 13):
            try:
                cpi_month = float(df.iloc[year-1913, month])
            except:
                continue

            date = f'{year}-{month:02}-{1:02}'
            dates.append(date)
            cpi_usa.append(cpi_month)

    # Gera DataFrame com as colunas de interesse
    df = pd.DataFrame({
        'date':dates,
        'cpi_usa':cpi_usa,
        })

    # Converte data de string para formato de data
    df['date'] = pd.to_datetime(df['date'])

    # Repete último índice até o fim do ano
    df.fillna(method='ffill', inplace=True)

    # CPI mensal
    df['cpi_month'] = df.cpi_usa / df.cpi_usa.shift(1) - 1
    df.loc[0, 'cpi_month'] = 0

    # CPI diario
    df['cpi_day'] = (1 + df.cpi_month) ** (1 / df.date.dt.daysinmonth) - 1

    # Insere dias faltantes e seta data como índice
    last_day = pd.Period(df.iloc[-1, 0],freq='M').end_time.date()
    idx = pd.date_range(df.loc[0, 'date'], last_day)
    df.set_index('date', inplace=True)
    df = df.reindex(idx, method='ffill')

    # Indice corrigido diariamente
    df['cpi_index'] = df.cpi_usa / (1+df.cpi_month) * (1+df.cpi_day) ** df.index.day

    # Último dia do mês recebe valor original (precisão 3 casas)
    last_days = list(dict.fromkeys( pd.to_datetime(df.index, format="%Y%m") + MonthEnd(1) ))
    last_days.pop()  # Remove last day
    df.loc[last_days, 'cpi_index'] = df.loc[last_days, 'cpi_usa']

    # Somente coluna do cpi_index
    global df_cpi
    df_cpi = pd.DataFrame(df['cpi_index'])

    return df_cpi


######################################
#               IPCA
######################################
def load_ipca():
    ## valores mensais da inflação (63)
    ## ibge_get_data(1737, 63, None, 197911, 202712)

    # Índices mensais (2266)
    # df = ibge_get_data(1737, 2266, None, 197911, 202712)
    # df.to_csv(path + 'data_IBGE/IPCA_index.csv', index=False)

    df = pd.read_csv(path + 'data_IBGE/IPCA_index.csv')

    # Converte campo para datetime
    df['data'] = ((df.data // 10000).astype(str) + '-' +
                (df.data % 10000 // 100).astype(str)  + '-' +
                (df.data % 100).astype(str))
    df['data'] = pd.to_datetime(df['data'])

    # Adiciona 2 meses no final e repete índice (inflção que ainda não entrou)
    ldate = df['data'].iloc[-1]
    lvalue = df['valor'].iloc[-1]
    df_last = pd.DataFrame({
        'data':[ldate + pd.DateOffset(months=1), ldate + pd.DateOffset(months=2)],
        'valor':[lvalue, lvalue]})
    df = pd.concat([df, df_last]).reset_index(drop=True)

    # CPI mensal
    df['cpi_month'] = df.valor / df.valor.shift(1) - 1
    df.loc[0, 'cpi_month'] = 0

    # CPI diario
    df['cpi_day'] = (1 + df.cpi_month) ** (1 / df.data.dt.daysinmonth) - 1

    # Insere dias faltantes e seta data como índice
    last_day = pd.Period(df.iloc[-1, 0],freq='M').end_time.date()
    idx = pd.date_range(df.iloc[0, 0], last_day)
    df.set_index('data', inplace=True)
    df = df.reindex(idx, method='ffill')

    # Indice corrigido diariamente
    df['ipca_index'] = df.valor / (1+df.cpi_month) * (1+df.cpi_day) ** df.index.day

    # Último dia do mês recebe valor original
    last_days = list(dict.fromkeys( pd.to_datetime(df.index, format="%Y%m") + MonthEnd(1) ))
    last_days.pop()  # Remove last day
    df.loc[last_days, 'ipca_index'] = df.loc[last_days, 'valor']

    # Somente coluna do ipca_index
    global df_ipca, df_ipca_today
    df_ipca = pd.DataFrame(df['ipca_index'])

    # IPCA até a data atual
    df_ipca_today = df_ipca.copy()
    r = pd.date_range(start=df_ipca_today.index[0], end=date.today())
    df_ipca_today = df_ipca_today.reindex(r, method='ffill')

    return df_ipca


######################################
#          USD BRL
######################################
def download_USD_BRL_Investing():
    df = investpy.get_currency_cross_historical_data(
        currency_cross=f'USD/BRL',
        from_date='01/12/1979',
        to_date='31/12/2029').reset_index()
    df.to_csv(path + 'data_Investing/USD_BRL.csv', index=False, line_terminator='\n')

def download_USD_BRL_Bacen():
    file_name = path + 'data_BC/dolar.csv'
    df = pd.read_csv(file_name)

    if check_today_file(file_name):
        return df

    url = ('https://olinda.bcb.gov.br/olinda/servico/'
        'PTAX/versao/v1/odata/CotacaoDolarPeriodo'
        '(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?'
        # "@dataInicial='01-01-1900'&@dataFinalCotacao='12-31-2029'&"  # tudo
        "@dataInicial='12-01-2021'&@dataFinalCotacao='12-31-2029'&"    # somente final
        '$format=text/csv&'
        '$select=dataHoraCotacao,cotacaoCompra,cotacaoVenda')
    df_new = pd.read_csv(url, decimal=",")

    last_date_ok = df['dataHoraCotacao'].iloc[-1]
    df = pd.concat([df, df_new[df_new.dataHoraCotacao > last_date_ok]])

    df.to_csv(file_name, index=False, lineterminator='\n') #, compression='zip')

    return df


def load_USD_BRL():
    # Usando dados do Investing
    #download_USD_BRL_Investing()
    #df_us = pd.read_csv(path + 'data_Investing/USD_BRL.csv')
    #df_us['Date'] = pd.to_datetime(df_us['Date'])
    #df_us.set_index('Date', inplace=True)
    #df_us.index.name = None
    #df_us = pd.DataFrame(df_us.Close)
    #df_us.rename(columns={'Close':'close'}, inplace=True)

    # Problema aqui é que pega data de Close anterior, não bate com atual (Carnaval fica 5 dias sem info)
    # Usando dados do Bacen
    df_us = download_USD_BRL_Bacen()
    df_us['data'] = pd.to_datetime(df_us.dataHoraCotacao.str.slice(0,10))
    df_us.drop_duplicates(subset='data', keep='last', inplace=True)
    df_us.set_index('data', inplace=True)
    df_us.index.name = None
    df_us = pd.DataFrame(df_us.loc['1994-07-01':, 'cotacaoCompra'])
    df_us.rename(columns={'cotacaoCompra':'close'}, inplace=True)

    global df_usd
    df_usd = df_us.join(df_ipca).join(df_cpi)

    ipca_atual = df_ipca.iloc[-1].ipca_index
    cpi_atual  = df_cpi.iloc[-1].cpi_index

    df_usd['infla'] = df_usd.close * (ipca_atual / df_usd.ipca_index) / (cpi_atual / df_usd.cpi_index)

    return df_usd

def get_df_usd():
    return df_usd


######################################
#             IBOVESPA
######################################
def download_ibov():
    # verificar se tem fechamento do dia util anterior
    # se nao tiver baixa dados e adiciona dias faltantes
    # no banco de dados

    # Usando dojo yahoo finance(não tem centavos)
    # Fechamento errado em 03/12/2021, igual ao dia 2
    # df = symbol_load_df('^BVSP')
    # return df

    # Usando investpy (não tem centavos)
    index_name = 'bovespa'
    file_name = path + f"data_Investing/{index_name.replace('/', '_')}.csv"

    #if check_date_file(file_name, same='day'):
    df = pd.read_csv(file_name) #, compression='zip')
    #else:
    #    df = investpy.get_index_historical_data(
    #        index=index_name, country='brazil',
    #        from_date='01/12/2021',
    #        to_date='31/12/2029').reset_index()
    #    df.to_csv(file_name, index=False, line_terminator='\n') #, compression='zip')

    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.index.name = None
    df.rename(columns={'Close':'close'}, inplace=True)
    df = pd.DataFrame(df['close'])

    return df

def load_ibov():
    df_bo = pd.read_csv(path + 'data_B3/IBOV_Diario.csv')
    df_bo['date'] = pd.to_datetime(df_bo['date'])
    df_bo.set_index('date', inplace=True)
    df_bo.index.name = None

    download_ibov()
    last_date_ok = df_bo.index[-1]
    df_new = download_ibov()
    print(df_new.index)
    df_bo = pd.concat([df_bo, df_new.loc[df_new.index > last_date_ok]])

    global df_bov
    df_bov = df_bo.loc['1980-01-01':].join(df_ipca).join(df_cpi).join(df_usd['close'], rsuffix='_usd')

    ipca_atual = df_ipca.iloc[-1].ipca_index
    df_bov['infla_br'] = df_bov.close * (ipca_atual / df_bov.ipca_index)

    cpi_atual  = df_cpi.iloc[-1].cpi_index
    dolar_atual = df_usd.iloc[-1].close

    df_bov['usd'] = df_bov.close / df_bov.close_usd
    df_bov['usd_infla'] = df_bov['usd'] * (cpi_atual / df_bov.cpi_index)
    df_bov['usd_infla_br'] = df_bov['usd_infla'] * dolar_atual

    return df_bov


######################################
#             NASDAQ
######################################
def download_nasdaq():
    pass

def load_nasdaq():
    df_nq = pd.read_csv('data/rank/NASDAQ.csv')
    df_nq['Date'] = pd.to_datetime(df_nq['Date'])
    df_nq.set_index('Date', inplace=True)
    df_nq.index.name = None

    # download_nasdaq()
    # last_date_ok = df_nq.index[-1]
    # df_new = download_nasdaq()
    # df_nq = df_nq.append(df_new.loc[df_new.index > last_date_ok])

    global df_nasdaq
    df_nasdaq = df_nq.join(df_cpi)

    cpi_atual  = df_cpi.iloc[-1].cpi_index

    df_nasdaq['ind_infla'] = df_nasdaq.Close * (cpi_atual / df_nasdaq.cpi_index)

    return df_nasdaq


######################################
#               CDI
######################################
def load_cdi(only_cdi=False):
    # https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-de-segmentos-e-setoriais/serie-historica-do-di.htm
    df_cdi = pd.read_csv(path + 'data_B3/DI.xls', sep='\t', skiprows=38, encoding='windows-1252')
    df_cdi.drop(columns=['Nr. Operações', 'Volume', 'Fator Diário'], inplace=True)
    df_cdi.rename(columns={'Data':'date', 'Média':'media'}, inplace=True)

    df_cdi['date'] = (
        df_cdi.date.str.slice(6, 10) + '-' +
        df_cdi.date.str.slice(3,  5) + '-' +
        df_cdi.date.str.slice(0,  2))

    df_cdi['date'] = pd.to_datetime(df_cdi['date'])

    # .replace(',', '.', regex=False)
    df_cdi['media'] = (df_cdi['media']
        .str.replace('.',  '', regex=False)
        .str.replace(',', '.', regex=False)).astype(float)

    df_cdi['day'] = 1

    # (a) Até 30/06/1989, as taxas dos dias que precediam a fins de semana e feriados
    # eram divididas pelo número de dias destes, de forma a mostrar a taxa over paga
    # pelos dias náo úteis.

    # (b) Até 31/05/1990, taxas divulgadas ao ano de 360 dias, com expressão linear.
    df_cdi.loc[df_cdi.date <= '1990-05-31', 'day'
            ] = (1 + df_cdi.media / 100 / 360)

    #  Entre 01/06/1990 e 31/12/1997, somente taxas diárias expressas linear ao mês.
    df_cdi.loc[(df_cdi.date >= '1990-06-01') &
            (df_cdi.date <= '1997-12-31'), 'day'
            ] = (1 + df_cdi.media / 100 / 30)

    # (c) A partir de 01/01/1998, taxas médias diárias de DI-Over e de SELIC
    # divulgadas ao ano de 252 dias úteis, com expressão exponencial.
    df_cdi.loc[df_cdi.date >= '1998-01-01', 'day'] = (1 + df_cdi.media / 100) ** (1/252)

    # Desloca 1 dia para frente, pois a taxa é overnight
    df_cdi['nindex'] = df_cdi['day'].cumprod().shift(1)
    df_cdi.loc[0, 'nindex'] = 1

    if only_cdi:
        return df_cdi

    # Dados a partir de Jul/1994 (Plano Real)
    date_ini = datetime.strptime('1994-07-01', '%Y-%m-%d').date()
    date1 = pd.Timestamp(date_ini)

    df_cdi2 = df_cdi[df_cdi.date >= date1][['date', 'nindex']].copy()
    df_cdi2.set_index('date', inplace=True)

    # df_bov2 = df_bov[df_bov.date >= date1].copy()
    df_bov2 = df_bov[df_bov.index >= date1].copy()
    # df_bov2.set_index('date', inplace=True)

    # Junta CDI e Bovesta na mesma tabela
    global df_res
    df_res = df_cdi2.join(df_bov2, how='outer').fillna(method='ffill')
    df_res.rename(columns={'nindex':'cdi_index', 'close':'bov_close'}, inplace=True)

    # df_res.to_csv('teste.csv', index=False)


def generate_all_windows(date_ini, date_end, window_days, taxes=True):
    list1, list2, list3, list4, list5, list6 = [],[],[],[],[],[]

    for window_mult in range(1, 1_000_000):
        date1 = pd.Timestamp(date_ini)
        date2 = pd.Timestamp(date_end)

        # Calculo das janelas
        window_size = window_mult * window_days
        bov_res = (df_res[date1:date2].bov_close.shift(-window_size) /
                      df_res[date1:date2].bov_close) - 1
        cdi_res = (df_res[date1:date2].cdi_index.shift(-window_size) /
                      df_res[date1:date2].cdi_index) - 1

        # falta Calcular ndays corretamente
        # ndays = (df_res[date1:date2].index.shift(-window_size) -
        #          df_res[date1:date2].index)

        # Remove os NAN's
        bov_res = bov_res[~bov_res.isna()]
        cdi_res = cdi_res[~cdi_res.isna()]

        # Número de janelas
        n_windows = bov_res.shape[0]
        if n_windows == 0:
            break

        # Calcula imposto
        if taxes:
            bov_res *= (1 - 0.150)

            ndays = window_days * window_mult
            if   ndays <= 252 * (180/365):
                cdi_res *= (1 - 0.225)
            elif ndays <= 252 * (360/365):
                cdi_res *= (1 - 0.200)
            elif ndays <= 252 * (720/365):
                cdi_res *= (1 - 0.175)
            else:
                cdi_res *= (1 - 0.150)

        bov_win = (bov_res > cdi_res).sum() / n_windows
        cdi_win = 1 - bov_win

        list1 += [window_mult]
        list2 += [bov_win * 100]
        list3 += [cdi_win * 100]
        list4 += [n_windows]
        list5 += [bov_res.mean() * 100]  # ganho médio líquido
        list6 += [cdi_res.mean() * 100]

    df_test = pd.DataFrame({
        'window_size':list1,
        'bov_win':list2,
        'cdi_win':list3,
        'n_windows':list4,
        'bov_perc':list5,
        'cdi_perc':list6,
        })

    return df_test


######################################
#           COMBUSTIVEIS
######################################
def load_gasol():
    global df_gasol
    if type(df_gasol) != int: return df_gasol
    if type(df_ipca) == int: load_ipca()

    # df = pd.read_csv('data/anp/gasol_br_semana.csv')
    df = pd.read_csv('data/anp/gasol_mes_media_pond.csv')

    df['data'] = pd.to_datetime(df['data'])

    # Altera para dia 15 (para pega inflação média do mês)
    # df['mes'] = df['mes'].apply(lambda dt: dt.replace(day=15))

    df.set_index('data', inplace=True)
    df.index.name = None

    df_gasol = df.join(df_ipca_today)

    ipca_atual = df_ipca_today.iloc[-1].ipca_index
    df_gasol['infla_br'] = df_gasol.valor * (ipca_atual / df_gasol.ipca_index)

    # Para fazer pelo dia, depois teria que fazer a média ponderada
    # Pois tem dias que tem bem mais dados que outros
    # df = pd.read_csv('data/anp/gasol_br_dia.csv')

    # df['data'] = df['data'].astype(np.datetime64)
    # df.set_index('data', inplace=True)
    # df.index.name = None

    # df = df.join(df_ipca)
    # ipca_atual = df_ipca.iloc[-1].ipca_index
    # df['infla_br'] = df.valor * (ipca_atual / df.ipca_index)

    # df['mes'] = pd.to_datetime(df.index, format="%Y%m") + MonthEnd(0)

    # global df_gasol
    # df_gasol = pd.DataFrame(df.groupby(['mes']).infla_br.mean())

    return df_gasol


def load_diesel():
    global df_diesel
    if type(df_diesel) != int: return df_diesel
    if type(df_ipca) == int: load_ipca()

    # df = pd.read_csv('data/anp/diesel_br_semana.csv')
    df = pd.read_csv('data/anp/diesel_mes_media_pond.csv')

    df['data'] = pd.to_datetime(df['data'])

    # Altera para dia 15 (para pega inflação média do mês)
    # df['mes'] = df['mes'].apply(lambda dt: dt.replace(day=15))

    df.set_index('data', inplace=True)
    df.index.name = None

    df_diesel = df.join(df_ipca_today)

    print(df_diesel)

    ipca_atual = df_ipca_today.iloc[-1].ipca_index
    df_diesel['infla_br'] = df_diesel.valor * (ipca_atual / df_diesel.ipca_index)

    return df_diesel

def load_etanol():
    global df_etanol
    if type(df_etanol) != int: return df_etanol
    if type(df_ipca) == int: load_ipca()

    df = pd.read_csv('data/anp/etanol_mes_media_pond.csv')

    df['data'] = pd.to_datetime(df['data'])

    # Altera para dia 15 (para pega inflação média do mês)
    # df['mes'] = df['mes'].apply(lambda dt: dt.replace(day=15))

    df.set_index('data', inplace=True)
    df.index.name = None

    df_etanol = df.join(df_ipca_today)

    ipca_atual = df_ipca_today.iloc[-1].ipca_index
    df_etanol['infla_br'] = df_etanol.valor * (ipca_atual / df_etanol.ipca_index)

    return df_etanol


def download_brent():
    df = symbol_load_df('BZ=F')
    df['datet'] = pd.to_datetime(df['datet']).dt.date
    df.set_index('datet', inplace=True)  # Data como índice
    df.index.name = None
    df.drop(columns=['tstamp','dtime','open', 'high', 'low'], inplace=True)
    return df

def load_brent():
    global df_brent
    if type(df_brent) != int: return df_brent
    if type(df_cpi) == int: load_pci_usa()
    if type(df_ipca) == int: load_ipca()
    if type(df_usd) == int: load_USD_BRL()

    df_brent = download_brent()

    # Preenche datas faltantes com último valor
    df_usdc = df_usd[['close']].copy()

    r = pd.date_range(start=df_usdc.index[0], end=df_usdc.index[-1])
    df_usdc = df_usdc.reindex(r, method='ffill')

    # valor em R$
    df_brent = df_brent.join(df_usdc['close'], rsuffix='_usd')
    df_brent['close_R'] = df_brent['close'] * df_brent['close_usd']

    # valor em US$ corrigido pelo PCI
    # valor em R$ corrigido pelo IPCA
    # valor em R$ corrigido pelo PCI e IPCA

    return df_brent
