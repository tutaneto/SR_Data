import platform
import pandas as pd
import requests
import shutil
import telebot
import os, sys, traceback
from datetime import datetime as dt

from os.path import exists
from os import remove
from pathlib import Path

from .gvar import *

if gvar.get('ONLINE', False):
    from .pres_template import *

def delete_file(file_name):
    if exists(file_name):
        remove(file_name)


from io import BytesIO
from PIL import Image
if platform.system() == 'Windows':
    import win32clipboard
# from tkinter import Tk

def send_to_clipboard(filepath):
    if platform.system() != 'Windows' or gvar.get('ONLINE', False):
        return

    image = Image.open(filepath)

    output = BytesIO()
    image.convert("RGB").save(output, "BMP")
    data = output.getvalue()[14:]
    output.close()

    clip_type = win32clipboard.CF_DIB
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(clip_type, data)
    win32clipboard.CloseClipboard()

    # https://stackoverflow.com/questions/579687/how-do-i-copy-a-string-to-the-clipboard/
    # r = Tk()
    # r.withdraw()
    # r.clipboard_clear()
    # r.clipboard_append(data)  # String
    # r.update() # now it stays on the clipboard after the window is closed
    # r.destroy()

def remote_path():
    try:
        dir_remote = None
        dir_date = dt.now().strftime("%Y%m%d")
        current_template_val = template_config.current_template
        if current_template_val == 'JP_':
            dir_remote = f'U:/Samy_Dana/Mercado Financeiro/{dir_date}/'
        if current_template_val == 'JP2_':
            dir_remote = f'U:/Samy_Dana/Jornal da Manhã/{dir_date}/'
        if current_template_val == 'JP3_':
            dir_remote = f'U:/Samy_Dana/Pros e Contras/{dir_date}/'
        if dir_remote:
            Path(dir_remote).mkdir(parents=True, exist_ok=True)
    except:
        dir_remote = None

    return dir_remote

def copy_img_to_remote(filename):
    dir_remote = remote_path()
    if not dir_remote:
        return

    remote_file = filename.replace('graphics/', dir_remote)
    delete_file(remote_file)
    shutil.copyfile(filename, remote_file)


if not gvar.get('ONLINE', False):
    from .selenium_base import *
    from selenium.webdriver.common.keys import Keys

browser_opened = False

def open_whatsapp():
    global browser_opened
    if not browser_opened:
        url = 'https://web.whatsapp.com/'
        sel_conn(url)
        browser_opened = True

def close_browser():
    global browser_opened
    if browser_opened:
        sel_rnd_sleep(10, 0.5)
        sel_close()
        browser_opened = False

def send_by_whatsapp(item):
    if whatsapp_groups == []: return

    open_whatsapp()

    for group_name in whatsapp_groups[gvar.get('send_groups_num', 1) - 1]:
        # Aqui procurava direto pelo nome do grupo na lista, o problema é que só funciona se o 'nome' estiver na tela
        # sel_wait_click(f"//*[contains(text(), '{group_name}')]")

        # Entra com nome do grupo na busca
        search_field_xpath = '//*[@id="side"]/div[1]/div/div/div[2]/div/div[2]'
        search_field = sel_wait_values(search_field_xpath)
        search_field[0].send_keys(group_name + Keys.ENTER)
        sel_rnd_sleep(0.5, 0.2)

        # Verifica se selecionou grupo correto
        chat_name_xpath = '//*[@id="main"]/header/div[2]/div[1]/div/span'
        if group_name not in sel_wait_value(chat_name_xpath):
            continue

        # attach_button_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/span'
        # file_button_xpath   = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/span/div/div/ul/li[4]/button/span'
        enter_message_xpath = '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[2]'
        send_button_xpath = '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span'

        enter_text_field = sel_wait_values(enter_message_xpath)

        if enter_text_field != -1:
            enter_text_field = enter_text_field[0]

            if len(gvar.get('send_message', '')) > 1:
                enter_text_field.send_keys(gvar['send_message'] + Keys.ENTER)
                sel_rnd_sleep(0.1, 0.1)

            # Anexa e envia imagem que está no clipboard
            enter_text_field.send_keys(Keys.CONTROL + 'v')
            sel_rnd_sleep(1, 0.2)
            sel_wait_click(send_button_xpath)
            sel_rnd_sleep(3, 0.2)


def send_by_telegram(item):
    if not gvar.get('QUEUE_ENABLED', False):
        return

    send_by_whatsapp(item)

    if telegram_groups != []:
        # @Apo_Sport_bot (Sport_Dicas)  /  Grupo: Ex_Genius_Bet
        # bot = telebot.TeleBot('5386350950:AAGYTdg7RXxkC6j6OyOLpJbaFSlBaIR1EDw')   # -1001296286944

        # @xyz_SR_Data_bot (SR_Data_Bot)  /  Grupo: SR_Data
        bot = telebot.TeleBot('5383195715:AAHqAtnu74hMDH7qWfN7Eu_BH_c2KO_PWZA')  # -1001787168682

        f = open(item, 'rb')
        for chat_id in telegram_groups[gvar.get('send_groups_num', 1) - 1]:
            if len(gvar.get('send_message', '')) > 1:
                bot.send_message(chat_id, gvar.get('send_message', ''))
                sel_rnd_sleep(0.1, 0.1)

            f.seek(0)
            bot.send_document(chat_id, f)
        f.close()

    gvar['send_message'] = ''


def get_qty_groups():
    return max(len(telegram_groups), len(whatsapp_groups))


import plotly.graph_objects as go
import plotly.io as pio

def create_shape(type, color):
    fig = go.FigureWidget()

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        width=64, height=64,
        margin={"l": 0, "r": 0, "t": 0, "b": 0},
        xaxis={'visible':False, 'range':[0, 64]},
        yaxis={'visible':False, 'range':[0, 64]},
    )
    # fig.update_xaxes(visible=False, range=[0, 64])
    # fig.update_yaxes(visible=False, range=[0, 64])

    fig.add_shape(type=type,
        x0=0, y0=0, x1=64, y1=64,
        line=dict(width=0), fillcolor=color,)

    if type == 'circle':
        type += '_'
    else:
        type = ''
    pio.write_image(fig, f'images/{type}{color}.png')


def try_int_float(val):
    if type(val) == str:
        val = val.strip()

    try:
        val = float(val)
        if val == int(val):
            val = int(val)
    except: pass

    return val

def get_perc(val, old):
    try:
        return (val - old) / old * 100
    except:
        return 0


def get_xy_anchors(x, y):
    xanchors = {'l':'left', 'c':'center', 'm':'center', 'r':'right'}
    yanchors = {'t':'top', 'm':'middle', 'c':'middle',  'b':'bottom', 'd':'bottom'}
    xanchor, yanchor = 'left', 'top'

    # 'p' = Coluna da barra
    if type(x) == str and x[0] == 'p':
        xanchor = 'center'
        x = float(x[1:])
        x = (gvar.get('bar_xc', {}).get(round(x - 0.1), 0) + gvar.get('bar_xc', {}).get(round(x + 0.1), 0)) / 2

    if type(x) == str and x[0] in 'lcmr':
        xanchor = xanchors[x[0]]
        x = float(x[1:])

    if type(y) == str and y[0] in 'tmcbd':
        yanchor = yanchors[y[0]]
        y = float(y[1:])

    # Relative position
    if x > -1.5 and x < 1.5:
        x *= gvar['gwidth'] if 'gwidth' in gvar else 1.0

    if y > -1.5 and y < 1.5:
        y *= gvar['gheight']

    if template_config.current_template == 'SBT_':
        yanchor = 'bottom'

    return x, y, xanchor, yanchor


def get_txt_color(color, ret_bold=True):
    TXT_COLORS = [T_COLOR_1,
        T_COLOR_1, T_COLOR_2, T_COLOR_3, T_COLOR_4, T_COLOR_5, T_COLOR_6, T_COLOR_7]

    bold = False

    if type(color) == str and color[:5] == 'bold_':
        bold = True
        color = try_int_float(color[5:])

    c = color
    if type(c) == str and c[0] == '#' and len(c) == 9:  # '#color' with Alpha in last position
        r,g,b,a = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16), int(c[7:9],16) / 255
        color = f'rgba({r},{g},{b},{a})'

    if type(color) == int:
        color = TXT_COLORS[color % len(TXT_COLORS)]

    if ret_bold:
        return color, bold
    else:
        return color


def get_leg_color(color):
    if type(color) == int:
        color = LEGEND_COLORS[color % len(LEGEND_COLORS)]

    return color



def get_color_pos(colors, pos):
    if type(colors) == list:
        return colors[pos % len(colors)]
    else:
        return colors

def df_add_new_rows(df, df_new):
    return pd.concat([df, df_new]).drop_duplicates().reset_index(drop=True)


# Ignore case in comparison, and returns the original text
def get_original_txt(word, words):
    word = word.upper()
    words_up = [w.upper() for w in words]
    if word in words_up:
        pos = words_up.index(word)
        return words[pos]
    else:
        return -1


month_dict = {'JAN':1,'FEB':2,'MAR':3,'APR':4,'MAY':5,'JUN':6,'JUL':7,'AUG':8,'SEP':9,'OCT':10,'NOV':11,'DEC':12,
                      'FEV':2,        'ABR':4,'MAI':5,                'AGO':8,'SET':9,'OUT':10,         'DEZ':12,}
def mmm_yy_to_date(date_in):
    month, year = date_in.split('/')
    month = month_dict[month.upper()]
    return ymd_to_datetime64(year, month)

def mm_yy_to_date(date_in):
    month, year = date_in.split('/')
    return ymd_to_datetime64(year, month)

def dd_mm_yy_to_date(date_in):
    day, month, year = date_in.split('/')
    return ymd_to_datetime64(year, month, day)

def yy_mm_dd_to_date(date_in):
    year, month, day = date_in.split('-')
    return ymd_to_datetime64(year, month, day)

def yyyymmdd_to_date(date_in):
    date_in = int(date_in)
    day   = date_in  % 100
    month = date_in // 100 % 100
    year  = date_in // 10000
    return ymd_to_datetime64(year, month, day)

def ymd_to_datetime64(year, month, day=1):
    year, month, day = int(year), int(month), int(day)
    if year <  100: year += 1900
    if year < 1930: year +=  100
    return pd.Timestamp(day=day, month=month, year=year).to_datetime64()

def convert_to_date(date_in, date_type):
    if date_type in ['mm_yy', 'mm_yyyy']:
        return mm_yy_to_date(date_in)
    if date_type in ['mmm_yy', 'mmm_yyyy']:
        return mmm_yy_to_date(date_in)
    if date_type in ['dd_mm_yy', 'dd_mm_yyyy']:
        return dd_mm_yy_to_date(date_in)
    if date_type in ['yy_mm_dd', 'yyyy_mm_dd']:
        return yy_mm_dd_to_date(date_in)
    if date_type in ['yymmdd', 'yyyymmdd']:
        return yyyymmdd_to_date(date_in)
    return 0

def discover_date_type(date_in):
    if str(date_in).isdecimal():    # 19940801 (int or str)
        return 'yyyymmdd'
    if date_in[:3].isalpha():       # Jun/19 or Jan/2013
        return 'mmm_yy'
    if date_in[2] in ['/', '-'] and date_in[5] in ['/', '-']:   # 01/04/22 or 01/04/2022
        return 'dd_mm_yy'
    if date_in[2] in ['/', '-']:    # 04/22 or 04/2022
        return  'mm_yy'
    if date_in[4] in ['/', '-']:    # 2022-04-01
        return  'yyyy_mm_dd'
    return None

def get_year_yy(year):
    if year <  100: return year
    if year < 2000: return year - 1900
    return year - 2000



month_names = ['', 'janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
def set_str_fields(txt):
    txt = txt.replace('{last_month}', month_names[ gvar.get('last_month_num', 0) ])
    return txt



def gvar_error(default, e_msg, e_num):
    if default != None:
        return default
    elif e_msg != '':
        gvar['LAST_ERROR'] = 'ERROR: ' + e_msg
        gvar['ERROR_STATE'] = True
        return e_num
    else:
        gvar['LAST_ERROR'] = f'ERROR: Something wrong ocurred!'
        gvar['ERROR_STATE'] = True
        return e_num

def get_listp(listp, pos, default=None, e_msg='', e_num=-1):
    if pos < len(listp) and -pos <= len(listp):
        return listp[pos]
    else:
        return gvar_error(default, 'Faltando dados em ' + e_msg, e_num)



# FILE OF CONFIGS
def set_config(var, val):
    config_data[var] = val
    with open(config_file_name, 'w') as fp:
        json.dump(config_data, fp)


# FILE OF CONFIGURABLE VARS
def get_config_var(var_name, default):
    file_name = 'data/digitado/config_var.csv'
    if not exists(file_name):
        return default

    file = open(file_name, 'r', encoding='utf8')
    lines = file.readlines()
    file.close()

    # var_name = var_name.lower()

    for line in lines:
        line = line.strip()
        attribution_char = '='
        if attribution_char in line:
            # AQUI
            # SÓ SEPARAR EM DUAS PARTES, ANTES E DEPOIS DO '='
            # AQUI
            var = [v.strip() for v in line.split(attribution_char)]
            if var[0] == var_name:
                return try_int_float(var[1])

    return default

# FILE OF ERRORS
def save_error(error_str, open_mode='w'):
    f = open('ERROR.txt', open_mode, encoding='UTF-8')
    f.write(error_str)
    f.close()

def display_exception(e, file_to_save=None, html_page=False, lines=''):
    lines += '<br>===========================================================<br>'
    lines += 'INFO:<br>'
    now  = dt.utcnow()
    now += timedelta(hours=-3)  # Brazil
    lines += f'Time: {now.strftime("%Y-%m-%d %H:%M:%S")}<br>'
    lines += '-----------------------------------------------------------<br>'

    lines += 'EXCEPTION:<br>'
    lines += f'G Error: {e} <br>'
    lines += '-----------------------------------------------------------<br>'

    lines += 'SYS EXC_INFO:<br>'
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    lines += f'{exc_type, fname} {exc_tb.tb_lineno} <br>'
    lines += '-----------------------------------------------------------<br>'

    lines += 'TRACEBACK:<br>'
    lines += f'{traceback.format_exc()}'
    lines += '===========================================================<br>'

    if not html_page:
        lines = lines.replace('<br>', '\n')

    if file_to_save:
        with open(file_to_save, 'a') as f:
            f.writelines(lines)
    else:
        print(lines)


# CHECK FOR UPDATES ON PLASSION
symbols_online_list = []

def get_symbols_online_list():
    global symbols_online_list

    if len(symbols_online_list) > 0:
        return

    try:
        df = pd.read_csv('https://plassion.com/projects/SR_Data/data/last_val.csv', sep=';')
        symbols_online_list = list(df.symbol)
    except:
        pass

def check_symbol_update(symbol):
    get_symbols_online_list()
    if symbol not in symbols_online_list:
        return
    print(f"*** SYMBOL UPDATE {symbol}")
    url = f'https://plassion.com/projects/SR_Data/data/get_last_val.py?symbol={symbol}'
    resp = requests.get(url)
    if not resp.ok:
        return

    v_site = [v.strip() for v in resp.text.split(';')]

    if v_site[0] != symbol:
        return

    filename = f'data/digitado/{symbol}.csv'
    with open(filename, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
    while lines[-1].strip() == '':
        lines.pop()
    sep = ';'

    # Dados do Banco Central
    if lines[-1].startswith('BC_'):
        filenum = lines[-1].split('_')[1].strip()
        filename = f'data/bc/{filenum}.csv'
        with open(filename, 'r', encoding='UTF-8') as f:
            lines = f.readlines()
        while lines[-1].strip() == '':
            lines.pop()
        sep = ','

    v_file = [v.strip() for v in lines[-1].split(sep)]

    dt_file = convert_to_date(v_file[0], discover_date_type(v_file[0]))
    dt_site = convert_to_date(v_site[1], discover_date_type(v_site[1]))
    if dt_site <= dt_file:
        return

    if not '\n' in lines[-1]:
        lines[-1] = lines[-1] + '\n'

    lines.append(f'{v_site[1]}{sep}{v_site[2]}')

    with open(filename, 'w', encoding='UTF-8', newline='\n') as f:
        f.writelines(lines)

    # Copia arquivo para pasta wwwsec
    if gvar.get('ONLINE', False) and filename.startswith('data/digitado/'):
        shutil.copyfile(filename, f'../wwwsec/digitado/{filename[len("data/digitado/"):]}')
