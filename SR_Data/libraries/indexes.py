import pandas as pd
import requests
from os.path import exists
from datetime import datetime


##########################
#  BANCO CENTRAL - SGS
##########################

def bc_sgs_get_indexes_codes():
    df = pd.read_csv('data/config/BCB_SGS.csv')
    df.set_index('name', inplace=True)
    df.index.name = None
    return df


def bc_sgs_get_index_values(agreg):
    file_name = f'data/bc/{agreg}.csv'
    if exists(file_name):
        df0 = pd.read_csv(file_name)

    try:
        url = f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{agreg}/dados?formato=json'
        df = pd.read_json(url)

        df = df[df.valor != '']  # Algumas datas voltam com string vazia no campo valor
        df['valor'] = df.valor.astype(float)

        new_data = True
        if 'df0' in locals():
            d_new = datetime.strptime(df.data.iloc[-1],  '%d/%m/%Y')
            d_old = datetime.strptime(df0.data.iloc[-1], '%d/%m/%Y')
            if d_new < d_old:  # Usa "<" pois podem corrigir dados, então se for igual usa o que baixou
                df = df0
                new_data = False
        if new_data:
            df.to_csv(file_name, index=False, line_terminator='\n')
    except:
        df = df0

    return df



##########################
#  IBGE
##########################

# IBGE (Pesquisa)
# https://servicodados.ibge.gov.br/api/docs/agregados?versao=3#api-Variaveis-agregadosAgregadoPeriodosPeriodosVariaveisVariavelGet

ibge_codes = {
    # IBGE (Pesuisa): Índice Nacional de Preços ao Consumidor Amplo
    # 'IPCA': {
    #     'agreg'  :1737,
    #     'var'    :63,
    #     'classif':None,},


    # IBGE (Pesuisa): Índice Nacional de Preços ao Consumidor
    'INPC': {
        'agreg'  :1736,
        'var'    :44,
        'classif':None,},

    'INPC_12M': {
        'agreg'  :1736,
        'var'    :2292,
        'classif':None,},

    'INPC_ANO': {
        'agreg'  :1736,
        'var'    :68,  # 63 (if prefer to use monthly tax and group 'year')
        'classif':None,},

    'INPC_ANUAL': {
        'agreg'  :1736,
        'var'    :44,
        'classif':None,},


    # IBGE (Pesuisa): Pesquisa Nacional por Amostra de Domicilio Continua
    # 'PNAD_Desemprego_Perc': {
    #     'agreg'  :6381,
    #     'var'    :4099,
    #     'classif':None,},


    # IBGE (Pesuisa): Contas Nacionais Trimestrais
    # https://br.investing.com/economic-calendar/brazilian-gdp-858
    # https://br.investing.com/economic-calendar/brazilian-gdp-413
    # 'PIB_IBGE': {
    #     'agreg'  :2072,
    #     'var'    :933,
    #     'classif':None,},

    # 'PIB_IBGE_2': {  # Mesmos valores que o de cima, mas pega em outra série
    #     'agreg'  :1846,
    #     'var'    :585,
    #     'classif':'11255[90707]',},

    # 'PIB_IBGE_Perc': {
    #     'agreg'  :5932,
    #     'var'    :6564,
    #     'classif':'11255[90707]',},

    # 'PIB_IBGE_Perc_2': {
    #     'agreg'  :5932,
    #     'var'    :6561,
    #     'classif':'11255[90707]',},

    # 'PIB_4Tri_Perc': {
    #     'agreg'  :5932,
    #     'var'    :6562,
    #     'classif':'11255[90707]',},


    # PROD_IND
    # IBGE (Pesquisa) Pesquisa Industrial Mensal - Produção Física
    # https://g1.globo.com/economia/noticia/2021/11/04/producao-industrial-cai-04percent-em-setembro-mostra-ibge.ghtml
    # https://br.investing.com/economic-calendar/brazilian-industrial-production-1146
    # Mudanças
    # https://www.ibge.gov.br/novo-portal-destaques.html?destaque=33322
    # 3653 -> 8159

    # VOL_SERV
    # IBGE (Pesquisa) Pesquisa Mensal de Serviços
    # https://g1.globo.com/economia/noticia/2021/11/12/setor-de-servicos-cai-06percent-em-setembro.ghtml
    # Mudanças
    # https://www.ibge.gov.br/novo-portal-destaques.html?destaque=33383
    # 6442 -> 8161

    # VENDAS_COM
    # IBGE (Pesquisa) Pesquisa Mensal de Comércio
    # https://g1.globo.com/economia/noticia/2021/11/11/vendas-do-comercio-caem-13percent-em-setembro.ghtml
    # Mudanças
    # 3416-> 8185
}

def ibge_get_json(agreg, var, classif, period_ini, period_end):
    period_txt = '-10000'
    url  = f'https://servicodados.ibge.gov.br/api/v3/agregados/{agreg}'
    url += f'/periodos/' + period_txt
    url += f'/variaveis/{var}'
    url += f'?localidades=N1[all]'
    if classif:
        url += f'&classificacao={classif}'  # limite de tamanho, abaixo de 4200 caracteres

    try:
        response = requests.request("GET", url)
        data = response.json()
    except:
        data = None

    return data

def ibge_get_data(agreg, var, classif, period_ini, period_end):
    data = ibge_get_json(agreg, var, classif, period_ini, period_end)

    file_name = f'data/ibge/{agreg}_{var}_{classif}.csv'
    if exists(file_name):
        df0 = pd.read_csv(file_name)

    try:
        df = pd.DataFrame({'valor':data[0]['resultados'][0]['series'][0]['serie']})
        df = df.reset_index().rename(columns={'index':'data'})

        # add "day 1" to data
        df['data'] = df['data'].astype(int) * 100 + 1

        # remove rows with invalid values
        valores = df.valor
        for valor in valores:
            try:
                float(valor)
            except ValueError:
                df = df[df.valor != valor]
        df = df.reset_index(drop=True)
        df['valor'] = pd.to_numeric(df['valor'])

        new_data = True
        if 'df0' in locals():
            d_new = df.data.iloc[-1]
            d_old = df0.data.iloc[-1]
            if d_new < d_old:  # Usa "<" pois podem corrigir dados, então se for igual usa o que baixou
                df = df0
                new_data = False
        if new_data:
            if str(agreg) == '3065' and str(var) == '355':  # IPCA-15 (tem passado na mão)
                df = pd.concat([df0[:68], df])
            df.to_csv(file_name, index=False, line_terminator='\n')
    except:
        df = df0

    return df


def ibge_get_index_values(symbol):
    agreg = ibge_codes[symbol]['agreg']
    var = ibge_codes[symbol]['var']
    classif = ibge_codes[symbol]['classif']
    df = ibge_get_data(agreg, var, classif, 199408, 202312)  # Inicio do Plano Real
    return df

