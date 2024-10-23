import os, sys, shutil, traceback
import time
import json
import numpy as np
import pandas as pd
import datetime as dt
import locale
import unicodedata
import re

from .gvar import *
# from .selenium_base import *


dow_name_pt = ['Segunda',  'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']


def display_exception(e, file_to_save=None, html_page=False, lines=''):
    lines += '<br>===========================================================<br>'
    lines += 'INFO:<br>'
    now  = dt.datetime.utcnow()
    now += dt.timedelta(hours=-3)  # Brazil
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


def display_exception_treated(e, txt):
    print(f'\n\n ***  ERRO: {txt} *** \n\n')

    error_known = False

    if 'An existing connection was forcibly closed by the remote host' in str(e):
        error_known = True

    if not error_known:
        display_exception(e)


def read_csv_strip(filename, sep=';'):
    df = pd.read_csv(filename, sep=sep, skipinitialspace=True)

    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].str.strip()

    return df

def read_csv_strip_str(*args, **kwargs):
    df = pd.read_csv(*args, skipinitialspace=True, **kwargs)

    df.columns = [c.strip() for c in df.columns]

    for col in df.columns:
        if pd.api.types.is_string_dtype(df[col]):
            df[col] = df[col].str.strip()

    return df


# This function only makes sense if the time in computer is correct, returning the hour in the timezone specified
def dt_now(timezone=-3):
    return dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=timezone)



# Format number grouping in thousands
def fnum(val, decimal=0):
    return locale.format_string(f'%0.{decimal}f', val, grouping=True)

def fnum2(val):
    return fnum(val, decimal=2)


def webcolor_to_rgba(c):
    ok = True

    if type(c) != str or c[:1] != '#': ok = False

    len_c = len(c)
    if len_c not in [4, 5, 7, 9]: ok = False

    if ok:
        try:
            r,g,b,a = 0, 0, 0, 255

            if len_c in [4, 5]:
                r,g,b = int(c[1:2], 16)*17, int(c[2:3], 16)*17, int(c[3:4], 16)*17
                if len_c == 5:
                    a = int(c[4:5],16)*17

            if len_c in [7, 9]:
                r,g,b = int(c[1:3], 16), int(c[3:5], 16), int(c[5:7], 16)
                if len_c == 9:
                    a = int(c[7:9],16)

            return r,g,b,a
        except:
            pass

    return c

def rgba_to_webcolor(rgba):
    r,g,b,a = rgba
    return f'#{r:02x}{g:02x}{b:02x}{a:02x}'


# https://stackoverflow.com/questions/295135/turn-a-string-into-a-valid-filename
def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value)  # .lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')


def file_backup(hour_ini, hour_end, filename, backup_path):
    now = dt_now()
    hour = now.strftime('%H:%M')

    # Out of backup time
    if hour < hour_ini or hour > hour_end:
        return

    bakname = filename.replace('.', f"_{now.strftime('%Y-%m-%d')}.")
    bakname = bakname[bakname.rfind('/') + 1:]

    if len(backup_path) and backup_path[-1] != '/':
        backup_path += '/'
    bakname = backup_path + bakname

    # Backup already done
    if os.path.exists(bakname):
        return

    shutil.copyfile(filename, bakname)

def file_copy_after_time(file_in, file_out, seconds):
    if os.path.exists(file_out):
        fts = os.path.getmtime(file_out)
        fdt = dt.datetime.fromtimestamp(fts)
        dif_sec = (dt.datetime.now() - fdt).total_seconds()
        if dif_sec < seconds:
            return
    shutil.copyfile(file_in, file_out)


# def open_browser(url, beta=False, headless=False, wait=20):
#     try:
#         sel_close_window()
#         sel_close()
#         time.sleep(5)  # Espera 5s para reabrir
#     except:
#         # Browser não estava aberto (algum erro no close)
#         pass

#     sel_conn(url, beta, headless)
#     time.sleep(wait)
