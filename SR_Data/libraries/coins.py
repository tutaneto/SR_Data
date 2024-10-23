from .pres_template import *
# from invest_news import *

import pandas as pd
import json
import locale
import requests
import json
from datetime import datetime as dt, date
from os.path import exists, getmtime
from .gvar import *


def dojo_yf_download_data(symbol, p_range, interval):
    headers = {
        'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com',
        'x-rapidapi-key': '83d5ffc220msh9768d887d5d02fdp10d2a4jsne8be5b2fc940'
    }

    url = 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart'
    params = {'symbol':'^BVSP', 'range':'1d', 'interval':'15m', 'region':'BR'}

    params['symbol'] = symbol
    params['range']  = p_range
    params['interval'] = interval
    response = requests.request("GET", url, headers=headers, params=params)

    return response.json()


def check_today_file(file_name):
    # Check if file already exists
    if exists(file_name):
        # And if date is today
        ts = getmtime(file_name)
        dt_obj = dt.fromtimestamp(ts)
        if dt_obj.date() >= dt.today().date():
            return True
    return False


def check_date_file(file_name, same='day'):
    # Check if file already exists
    if exists(file_name):
        if same == 'any':
            return True
        # And if date is the same
        ts = getmtime(file_name)
        dt_obj = dt.fromtimestamp(ts)
        now = dt.today()
        if same == 'day':
            if dt_obj.date() >= now.date():
                return True
        if same == 'month':
            if dt_obj.year*10000+dt_obj.month*100 >= now.year*10000+now.month*100:
                return True
    return False


def symbol_load_data(symbol, period='5y'):
    per_num, same = 6, 'day'
    if period != '5y':
        per_num, same = 7, 'any'

    file = f'data/data_{symbol}_{per_num}.json'

    if not check_date_file(file, same=same):
        # download and save file to disk
        data = dojo_yf_download_data(symbol, period, '1d')
        with open(file, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False) #, indent=4)
    else:
        # load file from disk
        with open(file) as json_file:
            data = json.load(json_file)

    return data

def coin_load_data(coin_code):
    symbol = f'USD{coin_code}=X'
    return symbol_load_data(symbol)

def json_to_def(data):
    info   = data['chart']['result'][0]
    tstamp = info['timestamp']
    infov  = info['indicators']['quote'][0]
    openp  = infov['open']
    close  = infov['close']
    high   = infov['high']
    low    = infov['low']

    datet, dtime = [], []
    for ts in tstamp:
        dt_obj = dt.fromtimestamp(ts)
        datet.append(dt_obj)
        dtime.append(dt_obj.strftime('%d/%m/%Y %H:%M'))

    # Create dataframe with data
    df = pd.DataFrame({'tstamp':tstamp, 'datet':datet, 'dtime':dtime,
        'open':openp, 'close':close, 'high':high, 'low':low}
        ).dropna().reset_index(drop=True)

    return df

def symbol_load_df(symbol):
    # Database diario de 5 anos
    df  = json_to_def(symbol_load_data(symbol))

    # Database de mais tempo (vem somente dados mensais)
    dfm = json_to_def(symbol_load_data(symbol, 'max'))

    # Adiciona dados mensais antes dos dados diários
    tstamp0 = df.loc[0, 'tstamp'].item()
    df = pd.concat([df, dfm[dfm.tstamp < tstamp0]])

    return df

def get_coin_to_usd(coin_code):
    if coin_code == 'USD':
        return None

    # Load data from
    data = coin_load_data(coin_code)

    # ************   AQUI   *****************
    # Precisa ver se a data no tstamp é local do país
    # se não for, precisa ajustar pelo timezone do
    # header

    info   = data['chart']['result'][0]
    tstamp = info['timestamp']
    infov  = info['indicators']['quote'][0]
    openp  = infov['open']
    close  = infov['close']
    high   = infov['high']
    low    = infov['low']

    datet, dtime, dtformat = [], [], []
    for ts in tstamp:
        dt_obj = dt.fromtimestamp(ts)
        datet.append(dt_obj)
        dtime.append(dt_obj.strftime('%d/%m/%Y %H:%M'))
        # dtformat.append(dt_obj.strftime(date_format[period]))

    # Create dataframe with data
    df = pd.DataFrame({'tstamp':tstamp, 'datet':datet, 'dtime':dtime,
        'open':openp, 'close':close, 'high':high, 'low':low}
        ).dropna().reset_index(drop=True)

    return df

def get_coins_data(df, date_ini, date_end):
    date_ini = dt.fromisoformat(date_ini)
    date_end = dt.fromisoformat(date_end + ' 23:59:59')
    date_ini = dt.timestamp(date_ini)
    date_end = dt.timestamp(date_end)

    df2 = pd.DataFrame({
            'code':[], 'open':[], 'close':[], 'pdiff':[], 'perc':[]
        })

    for coin_code in df.keys():
        dfc = df[coin_code]
        popen  = dfc[dfc.tstamp < date_ini].close.iloc[-1]
        pclose = dfc[dfc.tstamp < date_end].close.iloc[-1]
        pdiff = pclose - popen
        pperc = -pdiff / popen * 100
        df3 = pd.DataFrame({
            'code':[coin_code],
            'open':[popen],  'close':[pclose],
            'pdiff':[pdiff], 'perc':[pperc]
        })
        df2 = df2.append(df3)

    df2 = df2.reset_index(drop=True)
    # df2.open  = df2.open.round(2)
    # df2.close = df2.close.round(2)
    # df2.pdiff  = df2.pdiff.round(2)
    # df2.perc  = df2.perc.round(2) #.astype(str) + '%'

    return df2


def money_format(val):
    decimal = gvar.get('decimal', 2) if 'decimal' in gvar else 2
    return locale.format_string(f'%0.{decimal}f', val, grouping=True)

def get_value_txt(val, bold=False):
    if bold:
        return f'<b>{money_format(val)}</b>'
    else:
        return f'{money_format(val)}'

def format_data_to_show(data, val):
    vtype = data['vtype']
    decimal = data['decimal']
    show_perc = data.get('show_perc', SHOW_PERC)
    show_coin = data.get('show_coin', '')
    if show_coin != '':
        show_coin += ' '

    if vtype[-4:] == 'perc' or data.get('show_perc', False):
        # Tem que pegar o numero de casas no data
        # if max(data['yaxis']) < 10:
        txt = locale.format_string(f'%0.{decimal}f', val, grouping=True)
        # else:
        #     txt = locale.format_string('%0.1f', val, grouping=True)
        if show_perc:
            txt += '%'
    else:
        mult = data['mult']
        divshow = data['divshow']
        val *= mult / divshow
        txt = f'{show_coin}'
        txt += locale.format_string(f'%0.{decimal}f', val, grouping=True)
        suffix = ''
        if divshow == 1_000:
            suffix = 'K'
        if divshow == 1_000_000:
            suffix = 'M'
        elif divshow == 1_000_000_000:
            suffix = 'B'
        elif divshow == 1_000_000_000_000:
            suffix = 'T'
        txt += suffix

    return txt

def adjust_val(data, val):
    mult = data['mult']
    divshow = data['divshow']
    val *= mult / divshow

    return val


def val_max_round(val):
    val_int = int(val)
    val_str = str(val_int)
    val_siz = len(val_str)
    val_round = val_str[0] + '0' * (val_siz-1)
    val_new = int(val_round)
    if val_int - val_new < val_new * 0.10:
        val_round = str(int(val_str[0])-1) + '0' * (val_siz-1)
        val_new = int(val_round)

    return val_new


def get_ylines(val_min, val_max):
    ylines = []
    val_max_r = val_max_round(val_max)

    ylines.append(0)
    ylines.append(val_max_r)
    ylines.append(val_max_r / 2)

    if -val_max_r / 2 > val_min:
        ylines.append(-val_max_r / 2)

    if -val_max_r > val_min:
        ylines.append(-val_max_r)

    return ylines
