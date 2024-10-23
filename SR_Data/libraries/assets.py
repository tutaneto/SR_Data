import requests
import numpy as np
import pandas as pd
import json
from datetime import datetime as dt, timedelta
from unidecode import unidecode
from .coins import *
from .gvar import *

# Info to download data
headers = {
    'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com',
    'x-rapidapi-key': '83d5ffc220msh9768d887d5d02fdp10d2a4jsne8be5b2fc940'
    }

url = 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart'
params = {'symbol':'^BVSP', 'range':'1d', 'interval':'15m', 'region':'BR'}

# Period/range details
bt_text      = [ '1D',  '5D',  '1M', '6M',  'YTD', '1A', '5A', 'Max', 'Var']
bt_range     = [ '1d',  '5d', '1mo', '6mo', 'ytd', '1y', '5y', 'max', '1y']
bt_interval  = [ '5m', ' 5m',  '1d', '1d',   '1d', '1d', '1d',  '1d', '1d']  # max uses '1mo'
per_intspace = [    1,     6,     1,    1,      1,    1,    5,     1,   1]
date_format  = ['%H:%M', '%d/%m', '%d/%m', '%d/%m', '%d/%m', '%m/%Y', '%Y', '%Y', '%m/%Y']
# date_format = ['%H:%M', '%d/%m', '%d/%m/%Y', '%d/%m/%Y', '%d/%m/%Y', '%m/%Y', '%Y', '%Y', '%Y']

bt_qty = len(bt_text)
# bt_qty -= 1  # remove 'Max'
data = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

dojo_error = 0








from os.path import exists, getmtime

# symbol_code = '^BVSP'  # IBovespa
# symbol_code = '^GSPC'  # S&P 500

symbol_typed = ''
symbol = ''

def download_data(symbol_code):
    global symbol_typed, symbol, params, data, dojo_error

    symbol_typed = symbol_code

    market_date_int = 0

    # Remove ^ from symbol name
    symbol = symbol_code
    # if symbol[0] == '^':
    #     symbol = symbol[1:]

    for period in range(bt_qty):
        p_range = bt_range[period]
        interval = bt_interval[period]

        # Only 5d and 5y, the other data get from these two
        if p_range != '5d' and p_range != '5y' and p_range != 'max':
            continue

        # Check if file already exists
        file_name = f'data/data_{symbol}_{period}.json'

        # debug só pega se muda dia
        if check_today_file(file_name):
            if p_range == '5y' or p_range == 'max':
                continue

        # Set parameters of data do be got
        params['symbol'] = symbol_code
        params['range'] = p_range
        params['interval'] = interval

        try:
            response = requests.request("GET", url, headers=headers, params=params)

            # Copy json to data
            data[period] = response.json()

            # Save file
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(data[period], f, ensure_ascii=False) #, indent=4)

            ts = data[period]['chart']['result'][0]['meta']['regularMarketTime']
            dt_obj = dt.fromtimestamp(ts)
            market_date_int = dt_obj.year*10000 + dt_obj.month*100 + dt_obj.day
        except:
            dojo_error = -1  # download fail








def load_data():
    global symbol, data, dojo_error

    try:
        for period in [1, 6, 7]:
            with open(f'data/data_{symbol}_{period}.json') as json_file:
                data[period] = json.load(json_file)

        data[0] = data[1]
        data[2] = data[6]
        data[3] = data[6]
        data[4] = data[6]
        data[5] = data[6]
        if (dt.today() - gvar['date_ini']).days <= 5*365 + 1:
            data[8] = data[6]  # 'Var' = '5y'
            date_format[8]='%m/%Y'
        else:
            data[8] = data[7]  # 'Var' = 'max'
            date_format[8]='%Y'
    except:
            dojo_error = -1








df_period = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
ts_market = 0

def convert_data():
    global df_period, ts_market, dojo_error

    try:
        info = data[1]['chart']['result'][0]['meta']
        ts_market = info['regularMarketTime']
        dt_market = dt.fromtimestamp(ts_market)
        date_market = dt_market.replace(hour=0, minute=0, second=0)

        df = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        ndays = [0, 4, 30, 182,  0, 365, 5*365, 30*365, 365]

        # days to the beginning of the year
        date_year_init = date_market.replace(month=1, day=1)
        ndays[4] = (date_market - date_year_init).days # + 1

        # variable days
        if 'date_ini' not in gvar:
            gvar['date_ini'] = date_market - timedelta(days=365)  # Default to 1 year if not set
        ndays[8] = (date_market - gvar['date_ini']).days # + 1

        for period in range(bt_qty):
            tstamp = data[period]['chart']['result'][0]['timestamp']
            openp  = data[period]['chart']['result'][0]['indicators']['quote'][0]['open']
            close  = data[period]['chart']['result'][0]['indicators']['quote'][0]['close']
            high   = data[period]['chart']['result'][0]['indicators']['quote'][0]['high']
            low    = data[period]['chart']['result'][0]['indicators']['quote'][0]['low']

            # Convert timestamp to datetime
            datet, dtime, dtformat = [], [], []
            for ts in tstamp:
                dt_obj = dt.fromtimestamp(ts)
                datet.append(dt_obj)
                dtime.append(dt_obj.strftime('%d/%m/%Y %H:%M'))
                dtformat.append(dt_obj.strftime(date_format[period]))

            # Create dataframe with data
            df[period] = pd.DataFrame({'tstamp':tstamp, 'datet':datet, 'dtime':dtime, 'dtformat':dtformat,
                'open':openp, 'close':close, 'high':high, 'low':low}
                ).dropna().reset_index(drop=True)

            # df[period] = df[period][ df[period].tstamp >= ts_market - ndays[period] * 24*3600 ].reset_index(drop=True)
            if bt_range[period] != 'max':
                df[period] = df[period][ df[period].datet >= (date_market -
                            timedelta(days=ndays[period])) ].reset_index(drop=True)

            df_period[period] = df[period].copy()
    except:
        dojo_error = -1








def adjust_data():
    convert_data()
    # include_CPI()

def update_data(symbol_code):
    global dojo_error
    dojo_error = 0

    download_data(symbol_code)
    load_data()
    adjust_data()

def get_dojo_error():
    return dojo_error


def get_info_prices(period):
    #####################################################
    # Pegando os dados só pra ver
    # Melhorar essa parte do código
    # 0=preço atual, 1=close anterior, 2=maximo, 3=minimo, 4=max52, 5=min52
    info_prices = []
    info_prices.append(data[0]['chart']['result'][0]['meta']['regularMarketPrice'])
    info_prices.append(data[0]['chart']['result'][0]['meta']['previousClose'])  # or 'chartPreviousClose' ???

    # This way, picks the real max and min
    info_prices.append(df_period[period].high.max())
    info_prices.append(df_period[period].low.min())

    # This way, picks the max and min of close/open (value presented in graph)
    # if bt_interval[period] == '1d':
    #     info_prices.append(df_period[period].close.max())
    #     info_prices.append(df_period[period].close.min())
    # else:
    #     info_prices.append(df_period[period].open.max())
    #     info_prices.append(df_period[period].open.min())

    info_prices.append(df_period[5].high.max())
    info_prices.append(df_period[5].low.min())

    return info_prices








def get_asset_data(symbol, date_ini):
    global dojo_error

    update_data(symbol)
    try:
        if df_period[6].loc[0, 'datet'] <= date_ini:
            return df_period[6]
        else:
            return df_period[7]
    except:
        dojo_error = -1

dfcn = 0
def load_dfcn():
    global dfcn
    if type(dfcn) == int:
        dfcn = pd.read_csv('data/config/assets_codes.csv')

def asset_code_to_name(code):
    load_dfcn()
    code_ok = unidecode(code.lower())
    for i, df_code in dfcn.code.items():
        if unidecode(df_code.lower()) == code_ok:
            return dfcn.iloc[i, 1]
    return code

def asset_name_to_code(name):
    load_dfcn()
    name_ok = unidecode(name.lower())
    for i, df_name in dfcn.name.items():
        if unidecode(df_name.lower()) == name_ok:
            return dfcn.iloc[i, 0]
    return name
