import pandas as pd

# def load_jp_programs():
#     global df_program
#     df_program = pd.read_csv('data/jp/programas.csv', sep=';')

def get_last_program_finished(dow, hour_minute, file_name):
    # Funciona porque nenhum programa termina entre 00:00 e 00:59
    if hour_minute >= '00:00' and hour_minute < '00:59':
        hour_minute = '24:' + hour_minute[3:]
        dow -= 1
        if dow < 0:
            dow = 6

    df = pd.read_csv(f'data/jp/{file_name}.csv', sep=';')
    df = df[(df['dow'] == dow) & (df['hour_end'] < hour_minute)]

    if df.shape[0] == 0:
        return None

    last_program = df.iloc[-1]

    return last_program['program'], last_program['hour_ini'], last_program['hour_end']


def get_program_list(dow, file_name):
    dow2 = dow + 1
    if dow2 > 6:
        dow2 = 0

    df = pd.read_csv(f'data/jp/{file_name}.csv', sep=';')
    df = df[((df['dow'] == dow) & (df['hour_ini'] >= '06:00')) | ((df['dow'] == dow2) & (df['hour_ini'] < '06:00'))].reset_index(drop=True)

    return df

def init_dataframes():
    filename = 'data/jp/lives.csv'
    df_lives = pd.read_csv(filename, sep=';')
    df_lives = df_lives.groupby(['dow', 'hour_ini', 'hour_end'])['perc_tv'].mean().reset_index()
    return df_lives
