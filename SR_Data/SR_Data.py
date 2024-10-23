#!/home/rogerup/opt/python-3.9.5/bin/python3

import time
import sys, os, platform
import argparse
import signal
import logging
from datetime import datetime, timedelta

time_start = time.time()

from libraries.gvar import *
from libraries.server_manager import ServerManager
# Override default offline mode for main program
gvar['ONLINE'] = True


# Robô gerador de imagens
# MERC_FIN_AUTO_ROBO = True
# CGI = False
# CRONJOB = False

# Parse command line arguments
parser = argparse.ArgumentParser(description='Financial Data Visualization')
parser.add_argument('--mode', type=str, help='Operation mode (MERC_FIN_AUTO_ROBO, CGI, CRONJOB)')
parser.add_argument('--auto-file', type=str, default='auto', help='Auto file name')
parser.add_argument('--reset', action='store_true', help='Reset server state and clear temporary data')
args = parser.parse_args()

# Roda no servidor
MERC_FIN_AUTO_ROBO = args.mode == 'MERC_FIN_AUTO_ROBO'
CGI = args.mode == 'CGI'
CRONJOB = args.mode == 'CRONJOB'

if CGI:
    print("Content-type: text/html\n\n")
    print('<head><meta charset="UTF-8"></head>\n')

if CGI or CRONJOB:
    os.environ['HOME'] = '/home/rogerup'

if MERC_FIN_AUTO_ROBO:
    gvar['template_num'] = 1

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import ipywidgets as widget
import kaleido  # import para gerar erro caso esteja faltando

from libraries.version import *
from libraries.drawgraph import *

from libraries.set_template import set_template

# Brazilian R$ format
import locale
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except locale.Error:
        print("Warning: Brazilian locale not available, using system default")



df = {}
getdata_init(df)
init_countries()

bg_transparent = False

def prepare_template(tp_num):
    global save_file_scale, scale, template_num

    if template_num != tp_num:
        template_num = tp_num
        set_template(template_num)

    save_file_scale = 3
    if template_codes[template_num] in ['IN_', 'NEC_']:
        save_file_scale = 0.675
    if template_codes[template_num] in ['INB_', 'JP3_']:
        save_file_scale = 1

prepare_template(template_num)




from datetime import timedelta, datetime as dt

year_prev = 2022
# last day of previous month
today = dt.today()
date_ini = dt(day=31, month=12, year=2021)
date_end = today

set_date_ini(date_ini)
set_date_end(date_end)
set_dend_type('Close')
set_year_prev(year_prev)




def process_bat(auto_file=None):
    global symbol_old

    # Use command line argument if available, otherwise use default
    if auto_file is None:
        # Strip .csv extension if present in args.auto_file
        auto_file = args.auto_file.replace('.csv', '') if args.auto_file else 'auto'

    # Always ensure .csv extension
    if not auto_file.lower().endswith('.csv'):
        auto_file += '.csv'

    # Prevent command line arguments from being treated as filenames
    if auto_file.startswith('--'):
        auto_file = 'auto.csv'

    config_file = f'data/config/{auto_file}'
    try:
        if not os.path.exists(config_file):
            print(f"Error: Could not find file '{config_file}'")
            # Fall back to default auto.csv if specified file doesn't exist
            config_file = 'data/config/auto.csv'
            if not os.path.exists(config_file):
                print("Error: Could not find default auto.csv file either")
                return

        df_bat = pd.read_csv(config_file, sep=';')
    except Exception as e:
        print(f"Error reading {auto_file}: {str(e)}")
        return

    for i in range(df_bat.shape[0]):
        symbol = asset_name_to_code(df_bat.loc[i,'symbol'])
        ftype = df_bat.loc[i,'type']

        if symbol.lower() == 'template_num':
            prepare_template(int(ftype))
            continue

        ntries = 0
        while ntries < 3:
            symbol_old = symbol
            button_call(ftype)
            if get_some_error():  # Some error in any place
                ntries += 1
                time.sleep(5)
            else:
                break




symbol_old, symbol_old_real = '', ''

def call_draw_graph(scale, symbol):
    title, subtit, dfont = '', '', ''

    if get_txt_digitado():
        load_data_digitado('digitado', symbol=symbol_old_real)

    if symbol in symbol_list:
        title  = symbol_list[symbol]['title']
        subtit = symbol_list[symbol]['subtit']
        dfont  = symbol_list[symbol]['dfont']

    gvar['ERROR'] = ''
    gvar['ONLINE'] = False  # Ensure offline mode for testing

    return draw_graph(scale, symbol, 13,
                title, subtit, dfont, bg_transparent,)

def update_symbol(symbol):
    global vbox, fig, scale, symbol_old

    symbol = asset_name_to_code(symbol)

    if symbol == symbol_old and symbol != '':
        return

    if get_txt_digitado() and symbol != symbol_old_real:
        set_txt_digitado(False)
        if symbol_old_real in symbol_list_backup:
            symbol_list[symbol_old_real] = copy.deepcopy(symbol_list_backup[symbol_old_real])

    symbol_old = symbol

    fig = call_draw_graph(scale, symbol)


def redraw_symbol():
    global symbol_old
    symbol = symbol_old
    symbol_old = ''
    update_symbol(symbol)


def get_symbols(group):
    symbol_sel_list = []
    if group == 'PIB':
        symbol_sel_list.append('Div_Liq_PIB_Perc')
        symbol_sel_list.append('Div_Bruta_PIB_Perc')
    for symbol in symbol_list:
        if symbol[:len(group)] == group:
            symbol_sel_list.append(symbol)
    return symbol_sel_list

def on_trait_group(chg):
    if chg['name'] != 'value':
        return


def button_call(btype):
    global bg_transparent

    # Convert numeric types to string and handle type conversion
    if isinstance(btype, (int, float, np.integer, np.floating)):
        btype = str(int(btype))

    # Map numeric types to corresponding actions
    type_mapping = {
        '1': 'PNG',
        '2': 'JPG',
        '3': 'VID'
    }

    if isinstance(btype, str):
        btype = type_mapping.get(btype, btype.upper())

    if btype not in ['PNG', 'JPG', 'VID']:
        return

    # bg_transparent = transp_check.value

    if btype == 'JPG':
        bg_transparent = False

    if btype == 'VID':
        bg_transparent = True

    fig_save = call_draw_graph(save_file_scale, symbol_old)

    filepath = f'graphics/{template_codes[template_num]}_{get_save_file_name()}.{btype.lower()}'
    if btype == 'VID':
        filepath = file_img_to_video

    delete_file(filepath)  # Apaga arquivo antigo p/ ficar com data ok
    pio.write_image(fig_save, filepath)
    # send_to_clipboard(filepath)

    if btype in ['PNG', 'JPG']:
        send_by_telegram(filepath)

    if btype == 'VID':
        graph_create_video()
        graph_create_video(pos='CHEIA2')
        # if telao1_check.value: graph_create_video(pos='TELAO_ESQ')
        # if telao2_check.value: graph_create_video(pos='TELAO_MEIO')
        # if telao3_check.value: graph_create_video(pos='TELAO_DIR')

        bg_transparent = False
        delete_file(filepath)  # Apaga imagem usada para gerar o vídeo

    bg_transparent = False



fig = go.FigureWidget()



scale = 1

file_path       = '../wwwsec/output/'
file_name_queue = file_path + 'queue.txt'
file_name_base  = file_path + 'out'
# file_name_in  = '../wwwsec/output/out.csv'
# file_name_out = '../wwwsec/output/out.png'


def copy_graph_data_file():
    if platform.system() != 'Windows':
        # Copia arquivo para pasta digitados
        shutil.copyfile(file_name_in, f"data/digitado/{symbol_old}.csv")

def generate_graph():
    button_call('png')

    btype = 'PNG'
    filepath = f'graphics/{template_codes[template_num]}_{get_save_file_name()}.{btype.lower()}'

    file_name_out = f'{file_name_base}_{pos_out}.png'
    shutil.move(filepath, file_name_out)


# https://stackoverflow.com/questions/464040/how-are-post-and-get-variables-handled-in-python
from random import random


#######################################
#           RUNNING CGI
#######################################
if CGI:
    # variables: user, pw, file, template, symbol
    POST={}
    if platform.system() != 'Windows':
        args=sys.stdin.read().split('&')
        for arg in args:
            t=arg.split('=')
            if len(t)>1: k, v=arg.split('='); POST[k]=v
    else:
        # debug para rodar sem receber args
        POST['file'] = 'out.csv'
        POST['symbol'] = 'RANK_Exp_Infla'

    # symbol_old = 'IPCA'
    # symbol_old = 'out'
    symbol_old = POST['symbol']
    file_name_in = ''  # Precisa definir para FUNCIONAR

    copy_graph_data_file()
    generate_graph()

    # print(f'<a href="{filepath}" download rel="noopener noreferrer" target="_blank">Download</a><br>')
    # print(f'<img src="{filepath}?rnd={random()}" alt={get_save_file_name()}><br>')

    sys.exit()


#######################################
#       GENERATE FILES DO MERCFIN
#######################################
if MERC_FIN_AUTO_ROBO:
    gvar['send_by_telegram'] = True
    gvar['ONLINE'] = True  # Set online mode for actual processing

    # Initialize server manager
    graphics_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'graphics')
    server = ServerManager(file_name_queue, graphics_dir)

    print("SR_Data Server Online")

    # Handle reset request if specified
    if args.reset:
        server.reset_server()
        sys.exit(0)

    last_health_check = datetime.now()
    health_check_interval = timedelta(minutes=5)

    while server.running:
        try:
            # Perform periodic health check
            if datetime.now() - last_health_check > health_check_interval:
                if not server.check_health():
                    server.logger.error("Server health check failed")
                server.log_server_status()
                last_health_check = datetime.now()

            with open(file_name_queue, 'r') as f:
                command = f.readline().strip()
                if command:
                    parts = command.split()
                    if len(parts) >= 2:
                        ftype, symbol = parts[0], parts[1]
                        # Check for reset command
                        if ftype == 'reset':
                            server.reset_server()
                            continue

                        symbol_old = symbol
                        server.logger.info(f"Processing command: {ftype} {symbol}")
                        button_call(ftype)
                        # Clear the queue file after processing
                        open(file_name_queue, 'w').close()
                        server.logger.info("Command processed successfully")
        except Exception as e:
            server.logger.error(f"Error processing queue: {str(e)}")
        time.sleep(1)


#######################################
#        RUNNING ON SERVER
#######################################

import traceback
from fcntl import flock, LOCK_EX, LOCK_UN
from libraries.server_util import *

print("SR_Data Server Online")


time_alive = 8 * 60     # Cron Job (8 minutes)
time_end   = time_start + time_alive
time_cnt   = 0

if not CRONJOB:
    time_end = time_start + 1_000_000_000

# while 1:              # Use this to never stop
while time.time() < time_end:
    time.sleep(1)
    time_cnt += 1
    print(f'{time_cnt}', end = '\r')

    f = open(file_name_queue, 'r+');            # open
    flock(f.fileno(), LOCK_EX)                  # lock
    v0, v1 = f.readline().split()               # read
    pos_in, pos_out = int(v0), int(v1)
    if pos_in <= pos_out:
        flock(f.fileno(), LOCK_UN)
        f.close()
        continue
    f.truncate(0)                               # clean
    f.seek(0)                                   # position
    pos_out += 1                                # increment
    f.write(f'{pos_in} {pos_out}')              # write
    f.flush()                                   # flush
    flock(f.fileno(), LOCK_UN)                  # unlock
    f.close()                                   # close

    file_name_in = f'{file_name_base}_{pos_out}.csv'
    if not exists(file_name_in):
        time.sleep(1)
    if not exists(file_name_in):
        # timeout
        # display some error
        continue


    # Variáveis extra (estáticas)
    extra_var = {}
    file_name_extra = f'{file_name_base}_{pos_out}.ext'
    with open(file_name_extra, encoding='UTF-8') as f:
        lines = f.readlines()
    for line in lines:
        var = [v.strip() for v in line.split(';')]
        extra_var[var[0]] = var[1]

    tp_name = extra_var.get('template', '_in')
    user    = extra_var.get('user')
    passwd  = extra_var.get('passwd')

    access_ok = False
    if user in ['rogerup', 'samy']  and  passwd == 'senhaforte':
        access_ok = True
    if user in ['invnews']  and passwd == '9955' and tp_name in ['_in', '_inb']:
        access_ok = True
    if user in ['jp']       and passwd == '1009' and tp_name in ['_jp', '_jp2', '_jp3']:
        access_ok = True

    if access_ok:
        tp_num = {'_inb':3, '_jp':1, '_jp2':5, '_jp3':7, '_nec':4}.get(tp_name, 2)
        prepare_template(tp_num)

        file_name_symbol = f'{file_name_base}_{pos_out}.txt'

        with open(file_name_symbol) as f:
            symbol_old = f.read()

        print(symbol_old, end=' - ')

        copy_graph_data_file()

        gvar['server_error_msg'] = ''   # Sem erro ainda
        gvar['ERROR_STATE'] = False     # Reset error state
        gvar['LAST_ERROR'] = None       # Clear last error

        error = check_graph_data(symbol_old)
        msg = f'{server_error_txt[error]}'
    else:
        msg = 'Template not available.'

    if msg == '':                   # Verifica se há erro no arquivo de entrada
        try:
            generate_graph()
            msg = str(gvar['ERROR_STATE'])
        except Exception as e:
            msg = f'G Error: {e}'

            # Saves error on File
            original_stdout = sys.stdout
            fp = open('SR_Server_Errors.txt', 'a')
            sys.stdout = fp

            print('INFO:')
            # usuario
            now = dt.utcnow()
            now += timedelta(hours=-3)
            print(f'Seq: {pos_out}   Symbol: {symbol_old}   Time: {now.strftime("%Y-%m-%d %H:%M:%S")}')
            print('-----------------------------------------------------------')

            print('EXCEPTION:')
            print(msg)
            print('-----------------------------------------------------------')

            print('SYS EXC_INFO:')
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)
            print('-----------------------------------------------------------')

            print('TRACEBACK')
            print(traceback.format_exc())
            print('===========================================================\n')

            sys.stdout = original_stdout
            fp.close()


    if msg == '':                   # Verifica se ocorreu erro na geração do gráfico
        msg = 'Generated'
    else:
        gvar['server_error_msg'] = msg
        gvar['ERROR_STATE'] = True
        gvar['LAST_ERROR'] = msg
        symbol_old = 'error'
        generate_graph()

    print(msg)
