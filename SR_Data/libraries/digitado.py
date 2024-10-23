# Arquivos de dados criados manualmente

from .pres_template import *

import pandas as pd
from .symbols import *
from .util import *

def get_list(symbol_data, var, sep=','):
    vals = []

    for x in var.split(sep):
        val = symbol_data.get(x, x)
        val = try_int_float(val)
        if val != '' or vals != []:
            vals.append(val)

    return vals


def get_digitado_lines(file_name, return_lines=True):
    file_path = f'data/digitado/{file_name}.csv'
    file = open(file_path, 'r', encoding='utf8')
    lines = file.readlines()
    file.close()

    data_line = 20
    # procura a linha com o token 'data' (default=20 para os 'digitados' antigos, que não têm o token 'data')
    for i, line in enumerate(lines):
        var = line.strip().split(';')
        if var[0] == 'data':
            data_line = i + 1

    if return_lines:
        return data_line, lines
    else:
        return data_line

def load_info_digitado(file_name, symbol=None):
    data_line, lines = get_digitado_lines(file_name)
    print(f"**Loading {file_name}...")
    if file_name == 'digitado' and symbol:
        if symbol in symbol_list:
            symbol_data = symbol_list[symbol]
        else:
            symbol_data = {}
            symbol_data['label'] = []
    else:
        symbol = file_name
        symbol_data = {}
        symbol_data['label'] = []

    for line in lines[:data_line]:
        var = line.strip().split(';')
        if var[0] == '' or var[0] == 'data' or var[1] == '':
            continue

        # Ignora variáveis específicas para o JP3
        if template_codes[template_num] == 'JP3_' and var[0] in ['blk_w', 'blk_dx', 'bar_val_fs', 'xaxis_fs']:
            continue

        # JP2_ também aceita modificador '_jp'
        if TEMPLATE == 'JP_MERC_FIN' and var[0][-3:] == '_jp':
            var[0] = var[0][:-3]

        if TEMPLATE == 'INVEST_NEWS' and var[0][-3:] == '_in':
            var[0] = var[0][:-3]

        if TEMPLATE == 'INVEST_NEWS_BLACK' and var[0][-4:] == '_inb':
            var[0] = var[0][:-4]

        if TEMPLATE == 'NECTON' and var[0][-4:] == '_nec':
            var[0] = var[0][:-4]

        # JP2_ além do '_jp' acima, também aceita '_jp2'
        if template_codes[template_num] == 'JP2_' and var[0][-4:] == '_jp2':
            var[0] = var[0][:-4]

        if template_codes[template_num] == 'JP3_' and var[0][-4:] == '_jp3':
            var[0] = var[0][:-4]

        # Converte variáveis de configuração para minúsculas
        if var[0] not in ['title', 'subtit', 'dfont', 'label'] and var[0] in symbol_vars:
            var[1] = var[1].lower()

        if var[0] in ['decimal','mult','divshow','quant','xstep','vstep', 'bar_val_fs']:
            var[1]  = int(var[1])
        if var[0] in ['yref', 'blk_x']:
            var[1]  = float(var[1])
        if var[0] in ['ylines', 'label']:
            var[1] = get_list(symbol_data, var[1])
        if var[0] == 'group':
            try:
                var[1] = int(var[1])
            except:
                pass

        if var[0] == 'decimal':
            gvar['decimal'] = var[1]

        # Variável não definida no dicionário básico
        if var[0] not in symbol_vars:
            var[1] = try_int_float(var[1])

        # Variável do tipo lista, usando '\' para separar os valores
        if type(var[1]) == str and var[1][-1:] == ',':
            var[1] = get_list(symbol_data, var[1][:-1])

        if var[0] == 'label':
            symbol_data[var[0]] += [var[1]]
        else:
            symbol_data[var[0]] = var[1]

    # Preenche valores faltantes
    for var in symbol_vars:
        if not var in symbol_data:
            symbol_data[var] = symbol_vars[var]

    symbol_list[symbol] = symbol_data

    # Aceita dados começando exatamente na linha 20, ou após 'data;begin'
    if (len(lines) > 20 or data_line != 20) and data_line < len(lines):
        return lines[data_line].strip(), data_line  # header of data
    elif file_name == 'digitado':
        return
    else:
        gvar_error(None, "Faltam dados para gerar o gráfico (data;begin)", -1)
        return None, None

def init_files_created():
    files_created = []
    df_files = pd.read_csv('data/digitado/files.csv')
    for file_name in df_files.files:
        files_created += [file_name]
        load_info_digitado(file_name)
    return files_created

def load_data_digitado(symbol, datahead, skiprows):
    sep = ';'
    if datahead[-4:] == '.csv':
        file_path = f'data/digitado/{datahead}'
        skiprows = get_digitado_lines(datahead[:-4], return_lines=False)
    elif datahead == 'FILES':
        dff = pd.read_csv(f'data/digitado/{symbol}.csv', sep=sep, skiprows=skiprows)
        dfo = pd.DataFrame()
        for idx, row in dff.iterrows():
            try:
                df = pd.read_csv(f'data/out/{idx}.csv', sep=';')
                dfo = pd.concat([dfo, df.iloc[-row[0]:]])
            except:
                pass
        return dfo
    elif datahead[:3] == 'BC_':
        sep, skiprows = ',', 0
        file_path = f'data/bc/{datahead[3:]}.csv'
    elif datahead[:5] == 'IBGE_':
        sep, skiprows = ',', 0
        values = datahead[5:].split(',')
        file_name = f'{values[0]}_{values[1]}_'
        if values[2] == '0' and values[3] == '0':
            file_name += 'None'
        else:
            file_name += f'{values[2]}[{values[3]}]'
        file_path = f'data/ibge/{file_name}.csv'
    else:
        file_path = f'data/digitado/{symbol}.csv'

    return pd.read_csv(file_path, sep=sep, skiprows=skiprows)
