from datetime import datetime
import requests
from .util import gvar_error

# Info to download data
headers = {
    'x-rapidapi-host': 'apidojo-yahoo-finance-v1.p.rapidapi.com',
    'x-rapidapi-key': '83d5ffc220msh9768d887d5d02fdp10d2a4jsne8be5b2fc940'
    }

url = 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/stock/v2/get-chart'
params = {'symbol':'^BVSP', 'range':'1d', 'interval':'15m', 'region':'BR'}

url_all = 'https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/v2/get-quotes'
params_all = {'region':'BR', 'symbols':'^DJI,^GSPC,^IXIC'}


data_all, data_ts = 0, 0

def download_data_all(symbols):
    global data_all, data_ts

    # read new data only after 50s
    ts = datetime.now().timestamp()
    if ts > data_ts + 50:
        try:
            params_all['symbols'] = symbols
            response = requests.request("GET", url_all, headers=headers, params=params_all)
            data_all = response.json()
            data_ts = ts
        except:
            gvar_error(None, 'download_data_all', -1)

    return data_all


def get_prices(symbol):
    #                 USA                  EUROPE                   ASIA                COINS
    symbols = ('^DJI,^GSPC,^IXIC,^GDAXI,^FTSE,^FCHI,^IBEX,000001.SS,^N225,^HSI,USDBRL=X,EURBRL=X,BTC-USD,'
               'EURUSD=X,GBPUSD=X,CNYUSD=X,JPYUSD=X,HKDUSD=X,BRLUSD=X,^BVSP')
    data = download_data_all(symbols)

    try:
        info = data['quoteResponse']['result']
        for i in range(len(info)):
            if info[i]['symbol'] == symbol:
                market_price = info[i]['regularMarketPrice']
                close_price  = info[i]['regularMarketPreviousClose']
                break
    except:
        gvar_error(None, 'get_prices', -1)
        market_price = 0
        close_price  = 0

    return market_price, close_price
