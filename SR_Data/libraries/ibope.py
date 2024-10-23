# Site:
# https://www.realtimebrasil.com/
# samy@jovempan.com.br
# sS166800!


import os, shutil, datetime
from pathlib import Path
import pandas as pd

from .selenium_base import *
from .util_generic import file_backup, file_copy_after_time


download_path = str(Path.home() / 'Downloads') + '\\'


# Nomes dos arquivos
file_all = 'data/jp/Ibope_minutos.csv'
file_bak = 'data/jp/Ibope_minutos_backup.csv'



# xpath dos botões utilizados
enter_button_xpath  = '//*[@id="main"]/div/div/div/div/form/div/div/input'
open_menu_xpath     = '//*[@id="main"]/div/div/menu/div[1]/button'
send_to_xpath       = '//*[@id="menu-container"]/div/div/div/div[6]/ol/li[1]/a'
send2_to_xpath      = '//*[@id="menu-container"]/div/div[2]/div/div[2]/ol/li/div/a'
download_csv_xpath  = '//*[@id="exportCSV"]'
auto_update_xpath   = '//*[@id="main"]/div/div/menu/div[3]/span/span[2]'
error_xpath         = '//*[@id="main"]/div/div/div[8]/div/div/div/form/div/input'
info_xpath          = '//*[@id="main"]/div/div/div[7]/span'
time_tot_xpath      = '//*[@id="row-headers"]/table/tbody/tr'
channels_xpath      = '//*[@id="table-contents"]/table/tbody/tr'

pass_exp_msg_xpath  = '//*[@id="main"]/div/div/div/div/div[2]/div/div/div/p'
pass_exp_but_xpath  = '//*[@id="main"]/div/div/div/div/div[2]/div/div/div/form/div/input'
pass_alt_esc_xpath  = '//*[@id="main"]/div/div/div/form/fieldset/div[4]/div[2]/div/input'


def open_realtimebrasil():
    url = 'https://www.realtimebrasil.com/'
    sel_conn(url, beta=True)
    time.sleep(15)  # 30



def main_enter():
    sel_switch_window(0)
    sel_reload_page()
    time.sleep(10)

    if sel_click(enter_button_xpath) != -1:
        time.sleep(5)  # Wait after click to Enter

    # Aparece mensagem para alterar senha, mesmo já tendo alterado
    resp = sel_wait_value(pass_exp_msg_xpath, timeout=3, retry=False)
    print(f'Pedido para alterar senha: {resp}')
    if 'senha vence' in resp:
        print(f'Clica em botão')
        sel_click(pass_exp_but_xpath)
        time.sleep(3)
        print(f'Clica em cancelar')
        sel_click(pass_alt_esc_xpath)


def close_error():
    # Se botão não existe (-1) ou não é clicável (-2), NÃO GERA ERRO
    return sel_click(error_xpath)


def close_menu():
    while True:
        close_error()

        resp = sel_get_value(send_to_xpath)

        if resp == -1:  # menu button not exists
            main_enter()
            continue

        if resp == '':  # menu is already closed
            break

        # closes menu
        sel_click(open_menu_xpath)
        time.sleep(1)


def auto_switch(value):
    while True:
        resp = sel_get_values(auto_update_xpath)[0].value_of_css_property('background-color')

        if resp == -1:  # auto button not exists
            main_enter()
            continue

        if resp == value:  # auto is equal to state wanted
            break

        # switch auto state (on/off)
        sel_click(auto_update_xpath)
        time.sleep(1)


def auto_update():
    auto_off = 'rgba(255, 255, 255, 0.5)'
    auto_on  = 'rgba(105, 223, 0, 1)'

    while True:
        auto_switch(auto_off)
        auto_switch(auto_on)

        time.sleep(10)

        # Has no text in info window, everything is ok
        if sel_get_value(info_xpath) == '':
            break


def ibope_get_new_data():
    while True:
        close_menu()
        auto_update()

        # Vai para página de download
        if sel_click(open_menu_xpath) == -1: continue
        if sel_click(send_to_xpath)   == -1: continue
        if sel_click(send2_to_xpath)  == -1: continue

        # A página para download é aberta em uma nova janela (que fecha após download)
        try:
            # AQUI, estava funcionando mas parece que precisaria de waits
            time.sleep(1)
            sel_switch_window(1)
            # sel_click(download_csv_xpath)
            sel_wait_click(download_csv_xpath, timeout=20, retry=False)
        except:
            pass  # Tentou abrir nova janela e deu algum erro

        # Volta para página principal e fecha menu
        sel_switch_window(0)
        close_menu()
        break


def last_file_downloaded():
    last_file_time = 0
    last_file_name = None

    for f in os.listdir(download_path):
        file_time = os.path.getctime(download_path + f)
        if f.startswith('Realtime') and f.endswith('.csv') and file_time > last_file_time:
            last_file_time = file_time
            last_file_name = f

    if last_file_name != None:
        last_file_name = download_path + last_file_name

    return last_file_name


def ibope_add_new_data(df):
    # Copia arquivo para caso dê algum problema
    # shutil.copyfile(file_all, file_bak)

    # Adiciona novos horários ao arquivo
    df_all = pd.read_csv(file_all, sep=';', parse_dates=['MIN'])
    df_all = pd.concat([df_all, df])
    df_all = pd.concat([df_all, df]).drop_duplicates(['MIN'], keep='last').sort_values('MIN')
    df_all.to_csv(file_all, sep=';', index=False)

    file_copy_after_time(file_all, 'C:/Power BI/powerbi_jp/csv Ibope/Ibope_minutos.csv', 600)

    file_backup('00:15', '01:00', file_all, 'G:/My Drive/Projects/DATA_BACKUP/JP/')

    return df_all['MIN'].iloc[-1]  # Last minute updated


def move_file_to_backup_folder(file_downloaded, prefix = ''):
    # Move file downloaded to backup folder
    backup_path = download_path + 'Ibope_Realtime_Files\\'
    Path(backup_path).mkdir(parents=True, exist_ok=True)
    shutil.move(file_downloaded,
        backup_path + f'{prefix}{datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}_Realtime.csv')


def get_last_minute_updated():
    # Aqui poderia pegar só última linha (ou nem ficar lendo e manter em memória)
    df_all = pd.read_csv(file_all, sep=';', parse_dates=['MIN'])
    return df_all['MIN'].iloc[-1]


def ibope_save_new_data():
    file_downloaded = last_file_downloaded()
    if not file_downloaded:
        return get_last_minute_updated()


    # Pega data a partir de linha com data
    f = open(file_downloaded, 'r', encoding='utf-8')
    f.readline()
    data_line = f.readline()
    f.close()
    # Linha exemplo: Data;04-07-2022
    d, m, y = [v.strip() for v in data_line.split(';')[1].split('-')]
    data_atual = f'{y}-{m}-{d}'


    df = pd.read_csv(file_downloaded, sep=';', skiprows=6, skipfooter=1, engine='python', decimal=',')


    # Verifica se cabeçalho está ok
    if list(df.columns) != ['MIN', 'BASE', 'JOVEM PAN NEWS', 'CNN BRASIL', 'GLOBO NEWS', 'BANDNEWS', 'RECORD NEWS', 'TOTAL PAYTV']:
        move_file_to_backup_folder(file_downloaded, 'COLUMNS_ERROR_')
        return get_last_minute_updated()


    # Troca '-''  por 0, e depois converte colunas para float
    df.replace('-', 0, inplace=True)
    df.iloc[:, 2:] = df.iloc[:, 2:].astype(float)


    # Adiciona data aos minutos e converte para tipo datetime
    df['MIN'] = pd.to_datetime( data_atual + ' ' + df['MIN'] )

    # Adiciona 1 dia aos horarios de 00:00 as 05:59 (6:00 começa novo dia para o Ibope)
    df.loc[df['MIN'].dt.hour < 6, 'MIN'] += pd.DateOffset(1)


    # Adiciona novos horários ao arquivo
    last_minute_updated = ibope_add_new_data(df)

    move_file_to_backup_folder(file_downloaded)

    return last_minute_updated


def get_program_data(program_date, program_info):

    hour_ini = program_info[1]
    hour_end = program_info[2]

    if hour_end.startswith('24'):
        hour_end = '23:59:59'
        program_date -= datetime.timedelta(days=1)

    date_ini = program_date.replace(hour=int(hour_ini[0:2]), minute=int(hour_ini[3:5]), second=0, microsecond=0)
    date_end = program_date.replace(hour=int(hour_end[0:2]), minute=int(hour_end[3:5]), second=0, microsecond=0)

    # Faixa horária virando o dia
    if date_ini > date_end:
        date_ini -= datetime.timedelta(days=1)

    df_all = pd.read_csv(file_all, sep=';', parse_dates=['MIN'])

    return df_all[ (df_all['MIN'] >= date_ini) & (df_all['MIN'] < date_end) ]


def try_float(v):
    try:    return float(v)
    except: return 0

def ibope_get_data_from_screen():
    time_tot_fields = sel_get_values(time_tot_xpath)
    channels_fields = sel_get_values(channels_xpath)

    mdict = {
        'MIN':[], 'BASE':[],
        'JOVEM PAN NEWS':[], 'CNN BRASIL':[], 'GLOBO NEWS':[], 'BANDNEWS':[], 'RECORD NEWS':[],
        'TOTAL PAYTV':[]
    }

    for i in range(min(len(time_tot_fields), len(channels_fields))):
        time_tot_vals = time_tot_fields[i].text.split()
        channels_vals = channels_fields[i].text.split()

        if len(time_tot_vals) != 2 or len(channels_vals) != 6:
            break

        jp, cn, gn, bn, rn, tot_pay_tv = [try_float(v) for v in channels_vals]

        # print(f'{i} = ({time_tot_fields[i].text})')
        minute, base = time_tot_vals
        base = int(base)
        hour, minute = [int(v) for v in minute.split(':')]

        now = datetime.datetime.now()
        ibope_dt = now.replace(hour=hour, minute=minute, second=0, microsecond=0)

        if now.hour < 6 and hour > 18:
            ibope_dt -= datetime.timedelta(days=1)  # minuto do dia anterior
        elif now.hour > 18 and hour < 6:
            ibope_dt += datetime.timedelta(days=1)  # minuto do dia seguinte (ibope adiantado)

        mdict['MIN'].append(ibope_dt)
        mdict['BASE'].append(base)
        mdict['JOVEM PAN NEWS'].append(jp)
        mdict['CNN BRASIL'].append(cn)
        mdict['GLOBO NEWS'].append(gn)
        mdict['BANDNEWS'].append(bn)
        mdict['RECORD NEWS'].append(rn)
        mdict['TOTAL PAYTV'].append(tot_pay_tv)

    # Adiciona novos horários ao arquivo
    return ibope_add_new_data( pd.DataFrame(mdict) )
