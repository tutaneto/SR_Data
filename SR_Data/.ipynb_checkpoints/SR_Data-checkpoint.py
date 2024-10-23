#!/home/rogerup/opt/python-3.9.5/bin/python3

import time

time_start = time.time()

from libraries.gvar import *
gvar['ONLINE'] = True


# Robô gerador de imagens
# MERC_FIN_AUTO_ROBO = True
# CGI = False
# CRONJOB = False

# Roda no servidor
MERC_FIN_AUTO_ROBO = False
CGI = False
CRONJOB = True

import sys, os, platform

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
locale.setlocale(locale.LC_ALL, 'pt_BR')



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




from datetime import timedelta, datetime

year_prev = 2022
# last day of previous month
today = datetime.today()
date_ini = datetime(day=31, month=12, year=2021)
date_end = today

set_date_ini(date_ini)
set_date_end(date_end)
set_dend_type('Close')
set_year_prev(year_prev)




def process_bat(auto_file='auto'):
    global symbol_old

    if auto_file[-4].lower() != '.csv':
        auto_file += '.csv'

    df_bat = pd.read_csv(f'data/config/{auto_file}', sep=';')

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

    btype = btype.upper()

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
    auto_file = 'auto'
    if len(sys.argv) >= 2:
        auto_file = sys.argv[1]
    process_bat(auto_file)
    sys.exit()


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

        error = check_graph_data(symbol_old)
        msg = f'{server_error_txt[error]}'
    else:
        msg = 'Template not available.'

    if msg == '':                   # Verifica se há erro no arquivo de entrada
        try:
            generate_graph()
            msg = str(gvar['ERROR'])
        except Exception as e:
            msg = f'G Error: {e}'

            # Saves error on File
            original_stdout = sys.stdout
            fp = open('SR_Server_Errors.txt', 'a')
            sys.stdout = fp

            print('INFO:')
            # usuario
            now = datetime.utcnow()
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
        symbol_old = 'error'
        generate_graph()

    print(msg)
