import pyodbc
import pandas as pd
from .gvar import *
from .util_generic import read_csv_strip


def sql_connect():
    server = 'srdbintdados.database.windows.net'
    database = 'SRDB'
    username = 'adminsrdb'
    password = "3kR58Q-.Y]'xwl\\"
    driver= '{ODBC Driver 18 for SQL Server}'

    global cnxn, cursor
    cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
    cursor = cnxn.cursor()

    gvar['cnxn'  ] = cnxn
    gvar['cursor'] = cursor
    

def int_anyway(val):
    try:    return int(float(val))
    except: return 0


def sql_fill(filename, tab_cols, col_order, col_value):
    csvname = f'data/jp/{filename}.csv'
    filename = filename.replace('_COMPLETO', '')

    if filename == 'youtube_chn':
        df = read_csv_strip(csvname)
    else:
        df = pd.read_csv(csvname, sep=';')

    if type(col_value) == list:
        df = df[~ df[col_order].isin(col_value)]
    elif col_value != None:
        col_value = str(col_value)
        df = df[df[col_order] > col_value]
    
    print(df.shape[0], 'lines')

    pos, nlines = 0, 1_000
    while pos < df.shape[0]:
        print(f'\r{pos}.     ', end='')
        rows = []
        for _, row in df[pos:pos + nlines].iterrows():
            row = [str(v).replace("'", '"') for v in row.values]
            if filename == 'ibope_minutos':
                row[1] = int_anyway(row[1])  # 'BASE'
            if filename == 'yt_on_dem_vid':
                row[3] = int_anyway(row[3])  # 'category_id'
                row[4] = int_anyway(row[4])  # 'duration'
            rows.append(tuple(row))

        values = ', '.join(map(str, rows))
        sql = f'INSERT INTO {filename} {tab_cols} VALUES {values}'
        # print(f'{sql}\n')
        cursor.execute(sql)

        pos += nlines

    cnxn.commit()


def sql_insert(query):
    cursor.execute(query)
    cnxn.commit()


def sql_read_1(filename, col_order):
    filename = filename.replace('_COMPLETO', '')
    cursor.execute(f'SELECT TOP 1 * FROM {filename} ORDER BY {col_order} DESC')
    if row := cursor.fetchone():
        return row
    return None


def sql_read(filename, cols):
    items = []
    filename = filename.replace('_COMPLETO', '')
    cursor.execute(f'SELECT {cols} FROM {filename}')
    while row := cursor.fetchone():
        items.append(row[0])
    return items


def sql_read_show(filename, col_order, limit=10, start=0):
    cursor.execute(f'SELECT * from {filename} ORDER BY {col_order} OFFSET {start} ROWS FETCH NEXT {limit} ROWS ONLY')
    # cursor.execute(f'SELECT TOP {limit} * FROM {filename} ORDER BY {col_order} DESC')

    while row := cursor.fetchone():
        for val in row:
            print(val, end='  ')
        print()
