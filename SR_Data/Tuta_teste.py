#!/home/rogerup/opt/python-3.9.5/bin/python3

import time
import sys
import os
import logging
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import kaleido  # Used for saving images
import locale
from datetime import timedelta, datetime as dt
import shutil

# Custom module imports (Assumed to be available)
import libraries.gvar as gvar
import libraries.version as version
import libraries.drawgraph as drawgraph
import libraries.set_template as set_template
from libraries.server_util import check_graph_data, server_error_txt, delete_file

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables
TIME_START = time.time()
GVAR = {'ONLINE': True, 'send_by_telegram': False}
MERC_FIN_AUTO_ROBO = False
CGI = False
CRONJOB = True

if any([CGI, CRONJOB]):
    HOME_DIR = os.getenv('HOME', '/home/rogerup')
    os.environ['HOME'] = HOME_DIR

locale.setlocale(locale.LC_ALL, 'pt_BR')

# Initialize data
df = {}
drawgraph.getdata_init(df)
drawgraph.init_countries()
bg_transparent = False

def prepare_template(tp_num):
    save_file_scale = 3
    template_code = version.template_codes[tp_num]
    if template_code in ['IN_', 'NEC_']:
        save_file_scale = 0.675
    elif template_code in ['INB_', 'JP3_']:
        save_file_scale = 1
    set_template.set_template(tp_num)
    return save_file_scale

# Set initial parameters
template_num = 2  # Default template number
save_file_scale = prepare_template(template_num)
year_prev = 2022
today = dt.today()
date_ini = dt(day=31, month=12, year=2021)
date_end = today

drawgraph.set_date_ini(date_ini)
drawgraph.set_date_end(date_end)
drawgraph.set_dend_type('Close')
drawgraph.set_year_prev(year_prev)

def process_batch(auto_file='auto'):
    auto_file = f'{auto_file}.csv' if not auto_file.endswith('.csv') else auto_file
    df_bat = pd.read_csv(f'data/config/{auto_file}', sep=';')
    for _, row in df_bat.iterrows():
        symbol = version.asset_name_to_code(row['symbol'])
        ftype = row['type']
        if symbol.lower() == 'template_num':
            prepare_template(int(ftype))
            continue
        ntries = 0
        while ntries < 3:
            symbol_old = symbol
            button_call(ftype)
            if drawgraph.get_some_error():
                ntries += 1
                time.sleep(5)
            else:
                break

def call_draw_graph(scale, symbol):
    if drawgraph.get_txt_digitado():
        drawgraph.load_data_digitado('digitado', symbol=symbol)
    title = version.symbol_list.get(symbol, {}).get('title', '')
    subtit = version.symbol_list.get(symbol, {}).get('subtit', '')
    dfont = version.symbol_list.get(symbol, {}).get('dfont', '')
    GVAR['ERROR'] = ''
    return drawgraph.draw_graph(scale, symbol, 13, title, subtit, dfont, bg_transparent)

def update_symbol(symbol, previous_symbol):
    symbol_code = version.asset_name_to_code(symbol)
    if symbol_code == previous_symbol and symbol_code != '':
        return previous_symbol
    fig = call_draw_graph(save_file_scale, symbol_code)
    return symbol_code

def button_call(btype):
    global bg_transparent
    btype = btype.upper()
    if btype not in ['PNG', 'JPG', 'VID']:
        return
    bg_transparent = False if btype == 'JPG' else True
    fig_save = call_draw_graph(save_file_scale, symbol_old)
    filepath = f'graphics/{version.template_codes[template_num]}_{drawgraph.get_save_file_name()}.{btype.lower()}'
    if btype == 'VID':
        filepath = drawgraph.file_img_to_video
    delete_file(filepath)
    pio.write_image(fig_save, filepath)
    if btype in ['PNG', 'JPG']:
        drawgraph.send_by_telegram(filepath)
    if btype == 'VID':
        drawgraph.graph_create_video()
        bg_transparent = False
        delete_file(filepath)

def generate_graph():
    button_call('png')
    btype = 'PNG'
    filepath = f'graphics/{version.template_codes[template_num]}_{drawgraph.get_save_file_name()}.{btype.lower()}'
    file_name_out = f'{file_name_base}_{pos_out}.png'
    shutil.move(filepath, file_name_out)

# Main execution
if __name__ == '__main__':
    logger.info("SR_Data Server Online")
    time_alive = 8 * 60
    time_end = TIME_START + time_alive if CRONJOB else TIME_START + 1_000_000_000
    time_cnt = 0

    while time.time() < time_end:
        time.sleep(1)
        time_cnt += 1
        logger.debug(f'Time count: {time_cnt}')

        # Use context manager for file operations
        try:
            with open(file_name_queue, 'r+') as f:
                # File locking and processing logic
                pass  # Include your file processing logic here
        except Exception as e:
            logger.error(f'Error processing queue: {e}')
            continue

        # Additional processing logic...
