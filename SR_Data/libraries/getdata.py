from .indexes import *
from .digitado import *
from .graphcomp import load_ipca


country_filters = []
country_subtit = []
files_created, df = 0, 0
def getdata_init(df0):
    global files_created, df
    files_created = init_files_created()
    df = df0

    global country_filters, country_subtit
    df_cf = pd.read_csv('data/filter/filters.csv', sep=';')
    country_filters += df_cf.filters.tolist()
    country_subtit  += df_cf.subtit.tolist()


def get_files_created():
    return files_created


# Gera valor a partir do índice
def indice_to_valor(symbol):
    valor0 = 0
    df[symbol]['valor'] = (df[symbol].valor / df[symbol].valor.shift(1) - 1) * 100
    df[symbol].loc[0, 'valor'] = valor0

# Atualiza valor pelo IPCA
def valor_with_ipca(symbol):
    df_ipca = load_ipca()
    ipca_last = df_ipca.ipca_index.iloc[-1]
    for i in range(df[symbol].shape[0]):
        date = df[symbol].date.iloc[i]
        # date = date[3:7] + '-' + date[0:2] + '-01'
        date = dt(day=1, month=int(date[0:2]), year=int(date[3:7]))
        ipca_index = df_ipca[df_ipca.index >= date].ipca_index.iloc[0]
        df[symbol]['valor'].iloc[i] = df[symbol]['valor'].iloc[i] * (ipca_last / ipca_index)

def get_date_from_txt(symbol):
    datev = df[symbol].iloc[0,0]

    date_type = symbol_list[symbol].get('date_type',
                discover_date_type(datev) )

    if date_type:
        df[symbol]['dt64']  = df[symbol]['date'].apply(convert_to_date, args=[date_type])
        df[symbol]['year']  = df[symbol]['dt64'].dt.year
        df[symbol]['month'] = df[symbol]['dt64'].dt.month
        return

    # format: mm_yyyy
    mon_i,mon_f,  year_i,year_f = 0,2,  3,7

    if len(datev) == 10:
        if not datev[4].isnumeric():
            # format: yyyy-mm-dd
            mon_i,mon_f,  year_i,year_f = 5,7,  0,4

    df[symbol]['year']  = df[symbol].date.str.slice(year_i, year_f).astype(int)
    df[symbol]['month'] = df[symbol].date.str.slice(mon_i,  mon_f ).astype(int)


df_bc_sgs = bc_sgs_get_indexes_codes()

def index_code(symbol):
    if symbol in df_bc_sgs.index:
        return df_bc_sgs.loc[symbol].code
    else:
        return None

def load_symbol_data(symbol):
    global df

    gvar['legend'] = []

    bc_sgs_agreg, ibge_agreg = 0, 0

    # Arquivos de dados criados manualmente
    if symbol in files_created:
        datahead, skiprows = load_info_digitado(symbol)
        if gvar.get('dig_mode', False):  # Use get() with default False
            load_info_digitado('digitado', symbol)

        if gvar['ERROR'] != '':
            return

        if datahead[:3] == 'BC_':
            bc_sgs_agreg = int(datahead[3:])
        elif datahead[:5] == 'IBGE_':
            ibge_agreg = [int(x.strip()) for x in datahead[5:].split(',')]
            if ibge_agreg[2] == 0:
                ibge_agreg[2] = None
            else:
                ibge_agreg[2] = f'{ibge_agreg[2]}[{ibge_agreg[3]}]'
        elif datahead == 'caged.csv':
            dfc = pd.read_csv('data/mt/caged.csv', index_col=0)
            dft = dfc.tail(1).reset_index()
            if symbol == 'CAGED_SETOR':
                df[symbol] = pd.DataFrame({
                    'setor':['Agropecuária', 'Indústria', 'Construção', 'Comércio', 'Serviços'],
                    'valor':[dft.loc[0,'setA'], dft.loc[0,'setE'], dft.loc[0,'setF'], dft.loc[0,'setG'], dft.loc[0,'setU']]
                })
            elif symbol == 'CAGED_REGIAO':
                df[symbol] = pd.DataFrame({
                    'setor':['Norte', 'Centro-Oeste', 'Sul', 'Nordeste', 'Sudeste'],
                    'valor':[dft.loc[0,'reg1'], dft.loc[0,'reg5'], dft.loc[0,'reg4'], dft.loc[-0,'reg2'], dft.loc[0,'reg3']]
                })
            else:
                dfc.rename(columns={'total':'valor'}, inplace=True)
                dfc['data'] = '01-' + dfc.index.astype(str).str.slice(5,7) + '-' + dfc.index.astype(str).str.slice(0, 4)
                df[symbol] = dfc.copy()
                df[symbol]['year']  = df[symbol].data.str.slice(6, 10).astype(int)
                df[symbol]['month'] = df[symbol].data.str.slice(3,  5).astype(int)

            return
        else:
            df[symbol] = load_data_digitado(symbol, datahead, skiprows)
            gvar['legend'].append(df[symbol].columns[1])
            df[symbol].rename(columns={'x':'setor', df[symbol].columns[1]:'valor'}, inplace=True)
            df[symbol]['setor'] = df[symbol]['setor'].astype(str).str.strip()

            # Se group não for "name" assume como data
            if symbol_list[symbol]['group'] != 'name':
                df[symbol].rename(columns={'setor':'date'}, inplace=True)
                if symbol_list[symbol]['vtype'] == 'rvalue':
                    symbol_list[symbol]['vtype'] = 'value'
                elif symbol_list[symbol]['vtype'] == 'ipca':
                    valor_with_ipca(symbol)
                    symbol_list[symbol]['vtype'] = 'value'
                else:
                    indice_to_valor(symbol)

                get_date_from_txt(symbol)

            return


    fgv_codes = [999999995, 999999996]
    if index_code(symbol) in fgv_codes:
        pos = fgv_codes.index(index_code(symbol))
        fgv_files = ['INCC-M', 'INCC-DI']
        df[symbol] = pd.read_csv(f'data/fgv/{fgv_files[pos]}.csv')
        df[symbol]['year']  = df[symbol].date.str.slice(3, 7).astype(int)
        df[symbol]['month'] = df[symbol].date.str.slice(0, 2).astype(int)

        # Gera valor a partir do índice
        if index_code(symbol) in [999999995, 999999996]:  # INCC
            valor0 = 0  # df[symbol].loc[0, 'valor']
            df[symbol]['valor'] = (df[symbol].nindex / df[symbol].nindex.shift(1) - 1) * 100
            df[symbol].loc[0, 'valor'] = valor0

    else:
        if type(ibge_agreg) == list or symbol in ibge_codes:
            # Dados vieram do digitados
            if type(ibge_agreg) == list:
                df[symbol] = ibge_get_data(ibge_agreg[0], ibge_agreg[1], ibge_agreg[2], 199408, 202312)
            else:
                df[symbol] = ibge_get_index_values(symbol)
            df[symbol]['year']  = df[symbol].data // 10000
            df[symbol]['month'] = (df[symbol].data // 100) % 100

            # Era usado para calcular a partir do valor total
            # if symbol == 'PIB_IBGE_Perc':
            #     for i in range(-1, -15, -1):
            #         diff = df[symbol]['valor'].iloc[i] - df[symbol]['valor'].iloc[i-1]
            #         perc = diff / df[symbol]['valor'].iloc[i-1] * 100
            #         df[symbol]['valor'].iloc[i] = perc


        else:
            # Se agreg não veio do digitado pega aqui
            if not bc_sgs_agreg:
                bc_sgs_agreg = index_code(symbol)

            df[symbol] = bc_sgs_get_index_values(bc_sgs_agreg)

            df[symbol]['year']  = df[symbol].data.str.slice(6, 10).astype(int)
            df[symbol]['month'] = df[symbol].data.str.slice(3,  5).astype(int)


month_txt = ['', 'Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']

def get_symbol_data(symbol):
    # global df_filt
    # global save_file_name

    load_symbol_data(symbol)
    if gvar.get('ERROR_STATE', False):
        return None, None

    data = {}
    set_data_vars(symbol, data)

    # Converte de Índice para %
    if data['convert'] == 'index_to_perc' or data['vtype'] == 'toperc':
        df[symbol]['valor'] = (df[symbol]['valor'] / df[symbol]['valor'].shift(1) - 1) * 100

    # Inserido na v028,  provável que é uma pré-formatação para exibição futura
    # Removido na v041c, pois estava perdendo precisão caso índice fosse corrigido para %, e depois acumulado (CPI_US)
    # O correto é arredondar só na hora da exibição
    # Arredonda valor para número de casas configurado
    # if 'valor' in df[symbol].columns and data['type'][:5] != 'table':
    #     df[symbol]['valor'] = df[symbol]['valor'].round(data['decimal'])

    n = 2
    col_names = df[symbol].columns
    # GAMBIARRA nessa lista
    while n < len(col_names) and col_names[n].strip().lower()[:7] not in ['',
        'date', 'valor', 'dt64', 'year', 'month', 'data', 'setor', 'unnamed']:
        gvar['legend'].append(col_names[n])
        data[f'v{n}'] = df[symbol][col_names[n]]
        n += 1

    if data['group'] == 'name':

        # Veio no formato de data
        # Preciso arrumar isso tudo para ficar padrao
        if df[symbol].columns[0] == 'data':
            df[symbol]['data'] = (df[symbol].month.apply(lambda x:month_txt[x].upper()) +
                '/' + df[symbol].year.astype(str))
            df[symbol].columns = ['setor', 'valor', 'year', 'month']

        # Força em 13 para não estourar na tela e no tempo
        if data['quant'] == 0 and str(data['type'])[:4] != 'rank':
            data['quant'] = 13

        if data['quant'] == 0 or str(data['type'])[:4] == 'rank':
            data['xaxis'] = df[symbol].setor
            data['yaxis'] = df[symbol].valor
        else:
            quant = data['quant']

            # POSSÍVEL SOLUÇÃO PARA GAMBIARRA(1)
            # if data['vstep'] != 1:
            #     quant *= data['vstep'] + 2

            if quant > df[symbol].setor.size:
                quant = df[symbol].setor.size
            data['xaxis'] = df[symbol].setor[-quant:].reset_index(drop=True)
            data['yaxis'] = df[symbol].valor[-quant:].reset_index(drop=True)

        data['size']  = len(data['xaxis']) # n_months

        save_file_name = f'{symbol}'

        return data, save_file_name

    # int, because this conversion somentimes convert to float
    # if all items are numbers and has some a float
    year  = df[symbol].year.iloc[-1]
    month = df[symbol].month.iloc[-1]

    # save month to use in strings (titles, subtitles)
    gvar['last_month_num'] = int(month)

    save_file_name = f'{symbol}_{year}_{month}'


    # Média de 12M, usado no IBC-Br
    if data['group'] == '12m_mean':
        nitems = df[symbol].shape[0]
        vmeans = []
        for i in range(30,0,-1):  # 30 to 1
            vmeans.append(df[symbol].loc[nitems-i-11 : nitems-i, 'valor'].mean())
        for i in range(13,0,-1):
            df[symbol].loc[nitems-i, 'valor'] = (vmeans[-i] / vmeans[-i-12] - 1) * 100
        data['group'] = 1


    # Média até o mês atual, usado no IBC-Br
    if data['group'] == 'year_mean':
        first_year = 2010
        vmeans = []
        for pyear in range(first_year-1, year + 1):
            vmeans.append(df[symbol].loc[(df[symbol].year == pyear) & (df[symbol].month <= month), 'valor'].mean())

        ypos = 1
        nitems = df[symbol].shape[0]
        for pyear in range(first_year, year + 1):
            df[symbol].loc[nitems-1 - (year-pyear), 'data' ] = f'{month:02d}/{pyear}'
            df[symbol].loc[nitems-1 - (year-pyear), 'month'] = month
            df[symbol].loc[nitems-1 - (year-pyear), 'year' ] = pyear
            df[symbol].loc[nitems-1 - (year-pyear), 'valor'] = (vmeans[ypos] / vmeans[ypos-1] - 1) * 100
            ypos += 1
        data['group'] = 1


    if str(data['group'])[:6] == 'yearly':
        first_year = 2010
        if df[symbol].year.iloc[0] > first_year:
            first_year = df[symbol].year.iloc[0]
        n_months = year-first_year + month
        df_filt = df[symbol][ df[symbol].year >= first_year ].reset_index(drop=True)

    elif data['group'] == 'year':
        n_months = month
        # group_size = df[symbol][df[symbol].year == year].shape[0] - 1
        df_filt = df[symbol][ df[symbol].year == year ].reset_index(drop=True)

    elif data['group'] == 'samemonth':
        n_months = 13
        if data['quant'] != 0:
            n_months = data['quant']
        group_size = 0
        df_filt = df[symbol][ df[symbol].month == month ].reset_index(drop=True)
        if df_filt.shape[0] < n_months:
            n_months = df_filt.shape[0]

    else:
        n_months = 13
        if data['quant'] != 0:
            n_months = data['quant']
        if data['vstep'] != 1:
            n_months *= data['vstep'] + 2
        group_size = data['group'] - 1

        pos_ini = n_months + group_size
        if pos_ini > df[symbol].shape[0]:
            pos_ini = df[symbol].shape[0]
            n_months = pos_ini - group_size

        df_filt = df[symbol].iloc[-pos_ini:].reset_index(drop=True)


    xaxis = []
    yaxis = []


    if data['group'] == 'yearly':
        for year in range(first_year, df[symbol].year.iloc[-1] + 1):
            txt = str(year)
            xaxis.append(txt)

            df_filt = df[symbol][ df[symbol].year == year ].reset_index(drop=True)

            if data['vtype'] == 'perc':
                df_filt2 = 1 + df_filt.valor / 100
                val = (df_filt2.product() - 1) * 100
            else:
                val = df_filt.valor.sum()

            yaxis.append(val)

    # Não deu certo para a PROD_IND, só tem dados dos 2 últimos anos
    # A ideia seria pegar o valor do mês de Dezembro em cada ano
    elif data['group'] == 'yearlyv':
        for year in range(first_year, df[symbol].year.iloc[-1] + 1):
            yearmon12 = df[symbol].loc[(df[symbol].year == year) & (df[symbol].month == 12), 'valor'].values
            if len(yearmon12) == 1:
                val = yearmon12[0]
                yaxis.append(val)
                xaxis.append(str(year))
    else:
        for pos in range(df_filt.shape[0] - n_months, df_filt.shape[0]):
            month = df_filt.month.iloc[pos]
            year  = df_filt.year.iloc[pos]

            if data['period'] == 'trim':
                txt = str(month) + 'T/' + str(year - 2000)
            else:
                if data['xformat'] == 'year':
                    txt = f'{year}'
                else:
                    txt = f'{month_txt[month].upper()}/{get_year_yy(year):02d}'

            xaxis.append(txt)

            if data['group'] == 'year':
                group_size = pos

            if group_size == 0:
                val = df_filt.iloc[pos].valor
            else:
                if data['vtype'][-4:] == 'perc':
                    df_filt2 = 1 + (df_filt.valor[pos - group_size : pos+1]) / 100
                    val = (df_filt2.product() - 1) * 100
                else:
                    val = df_filt.valor[pos - group_size : pos+1].sum()

            yaxis.append(val)

    data['size']  = len(xaxis) # n_months
    data['xaxis'] = xaxis
    data['yaxis'] = yaxis

    return data, save_file_name
