from datetime import datetime as dt
import yfinance as yf
from .util import gvar_error

# Info to download data
data_all = {}
data_ts = 0

def download_data_all(symbols):
    global data_all, data_ts

    # read new data only after 50s
    ts = dt.now().timestamp()
    if ts > data_ts + 50:
        try:
            # Convert comma-separated string to list
            symbol_list = symbols.split(',')
            data_all = {}

            # Fetch data for each symbol
            for symbol in symbol_list:
                ticker = yf.Ticker(symbol)
                info = ticker.info
                data_all[symbol] = {
                    'regularMarketPrice': info.get('regularMarketPrice', 0),
                    'regularMarketPreviousClose': info.get('previousClose', 0)
                }
            data_ts = ts
        except Exception as e:
            gvar_error(None, f'download_data_all: {str(e)}', -1)

    return data_all


def get_prices(symbol):
    #                 USA                  EUROPE                   ASIA                COINS
    symbols = ('^DJI,^GSPC,^IXIC,^GDAXI,^FTSE,^FCHI,^IBEX,000001.SS,^N225,^HSI,USDBRL=X,EURBRL=X,BTC-USD,'
               'EURUSD=X,GBPUSD=X,CNYUSD=X,JPYUSD=X,HKDUSD=X,BRLUSD=X,^BVSP')
    data = download_data_all(symbols)

    try:
        if symbol in data:
            market_price = data[symbol]['regularMarketPrice']
            close_price = data[symbol]['regularMarketPreviousClose']
        else:
            raise KeyError(f"Symbol {symbol} not found in data")
    except Exception as e:
        gvar_error(None, f'get_prices: {str(e)}', -1)
        market_price = 0
        close_price = 0

    return market_price, close_price
