symbol_list = {
    'INPC':{
        'title' : 'INPC   Preços ao Consumidor',
        'subtit': 'Variação do Índice Nacional de Preços ao Consumidor sobre o mês anterior, em %',
        'dfont' : 'IBGE',
        'decimal': 2,
        'ylines': [0, 0.5, 1],
    },

    'INPC_12M':{
        'title' : 'INPC   Preços ao Consumidor',
        'subtit': 'Acumulado do Índice Nacional de Preços ao Consumidor em 12 meses, em %',
        'dfont' : 'IBGE',
        'decimal': 2,
        'blk_dx': 84,
        'ylines': [0, 4, 8],
    },

    'INPC_ANO':{
        'title' : 'INPC   Preços ao Consumidor',
        'subtit': 'Acumulado do Índice Nacional de Preços ao Consumidor no ano, em %',
        'dfont' : 'IBGE',
        'decimal': 2,
        'ylines': [0, 4, 8],
    },

    'INPC_ANUAL':{
        'title' : 'INPC   Preços ao Consumidor',
        'subtit': 'Acumulado do Índice Nacional de Preços ao Consumidor no ano, em %',
        'dfont' : 'IBGE',
        'group' : 'yearly',
        'decimal': 2,
        'blk_dx': 76,
        'ylines': [0, 4, 8],
    },


    'INCC-M':{
        'title' : 'INCC-M   Inflação da construção',
        'subtit': 'Variação mensal do Índice Nacional de Custo da Construção, em %',
        'dfont' : 'FGV',
        'decimal': 2,
        'blk_dx': 74,
        # 'ylines': [0, 2, 4] # mudar esse para yaxis e os valores para yvalues
    },

    'INCC-M_12M':{
        'title' : 'INCC-M   Inflação da construção',
        'subtit': 'Acumulado em 12 meses do Índice Nacional de Custo da Construção, em %',
        'dfont' : 'FGV',
        'group' :  12,
        'decimal': 2,
        'blk_dx': 80,
        # 'ylines': [0, 15, 30],
    },

    'INCC-M_ANO':{
        'title' : 'INCC-M   Inflação da construção',
        'subtit': 'Acumulado do ano do Índice Nacional de Custo da Construção, em %',
        'dfont' : 'FGV',
        'group' : 'year',
        'decimal': 2,
        'blk_dx': 80,
        # 'ylines': [0, 7, 14],
    },

    'INCC-M_ANUAL': {
        'title' : 'INCC-M   Inflação da construção',
        'subtit': 'Acumulado em cada ano do Índice Nacional de Custo da Construção, em %',
        'dfont' : 'FGV',
        'group' : 'yearly',
        'decimal': 2,
        'blk_dx': 80,
        # 'ylines': [0, 10, 20],
    },

    'INCC-DI':{
        'title' : 'INCC-DI   Inflação da construção',
        'subtit': 'Variação mensal do Índice Nacional de Custo da Construção, em %',
        'dfont' : 'FGV',
        'decimal': 2,
        'blk_dx': 74,
        # 'ylines': [0, 2, 4] # mudar esse para yaxis e os valores para yvalues
    },

    'INCC-DI_12M':{
        'title' : 'INCC-DI   Inflação da construção',
        'subtit': 'Acumulado em 12 meses do Índice Nacional de Custo da Construção, em %',
        'dfont' : 'FGV',
        'group' :  12,
        'decimal': 2,
        'blk_dx': 80,
        # 'ylines': [0, 15, 30],
    },

    'INCC-DI_ANO':{
        'title' : 'INCC-DI   Inflação da construção',
        'subtit': 'Acumulado no ano do Índice Nacional de Custo da Construção, em %',
        'dfont' : 'FGV',
        'group' : 'year',
        'decimal': 2,
        'blk_dx': 80,
        # 'ylines': [0, 7, 14],
    },

    'INCC-DI_ANUAL': {
        'title' : 'INCC-DI   Inflação da construção',
        'subtit': 'Acumulado em cada ano do Índice Nacional de Custo da Construção, em %',
        'dfont' : 'FGV',
        'group' : 'yearly',
        'decimal': 2,
        'blk_dx': 80,
        # 'ylines': [0, 10, 20],
    },

    'GRAPH_GASOL':{
        'title' : 'Preço da gasolina',
        'subtit': 'Preço médio por litro de combusível, em R$',
        'dfont' : 'ANP',
    },

    'GRAPH_DIESEL':{
        'title' : 'Preço do diesel',
        'subtit': 'Preço médio por litro de combusível, em R$',
        'dfont' : 'ANP',
    },

    'GRAPH_ETANOL':{
        'title' : 'Preço do etanol',
        'subtit': 'Preço médio por litro de combusível, em R$',
        'dfont' : 'ANP',
    },

    'GRAPH_GASOL_IPCA':{
        'title' : 'Preço da gasolina corrigido pelo IPCA',
        'subtit': 'Preço médio por litro em R$, corrigido pela inflação',
        'dfont' : 'ANP/IBGE',
    },

    'GRAPH_DIESEL_IPCA':{
        'title' : 'Preço do diesel corrigido pelo IPCA',
        'subtit': 'Preço médio por litro em R$, corrigido pela inflação',
        'dfont' : 'ANP/IBGE',
    },

    'GRAPH_ETANOL_IPCA':{
        'title' : 'Preço do etanol corrigido pelo IPCA',
        'subtit': 'Preço médio por litro em R$, corrigido pela inflação',
        'dfont' : 'ANP/IBGE',
    },

    'GRAPH_USD_x_BRL':{
        'title' : 'Dólar x Real',
        'subtit': 'Comparação das moedas dos EUA e Brasil, com correção pela inflação dos países',
        'dfont' : 'BC/IBGE/BLS',
    },

    'GRAPH_IBOV_IPCA':{
        'title' : 'Ibovespa corrigido pelo IPCA',
        'subtit': 'Evolução do principal indicador da bolsa corrigida pela inflação',
        'dfont' : 'B3/IBGE',
    },

    'GRAPH_IBOV_USD':{
        'title' : 'Ibovespa em dólar',
        'subtit': 'Evolução do principal indicador da bolsa, sem correção pela inflaçãoSEM CORREÇÃO PELA INFLAÇÃO',
        'dfont' : 'B3/Bacen',
    },

    'GRAPH_IBOV_USD_CPI':{
        'title' : 'Ibovespa em dólar e corrigido',
        'subtit': 'Principal indicador da bolsa brasileira, em dólar e corrigido pela inflação nos EUA (CPI)',
        'dfont' : 'B3/Bacen/BLS',
    },

    'GRAPH_IBOV_x_CDI':{
        'title' : 'Ibovespa x CDI',
        'subtit': 'Percentual de vitórias, de 1994 a 2022',
        'dfont' : 'B3',
    },

    'GRAPH_NASDAQ_CPI':{
        'title' : 'Nasdaq corrigido pela inflação',
        'subtit': 'Índice tecnológico de Wall Street corrigido pelo CPI',
        'dfont' : 'BLS',
    },


    # https://www.fipe.org.br/pt-br/indices/ipc/#indice-mensal&mindex


    'Viagens_Desp': {
        'title' : 'Gastos de brasileiros no exterior',
        'subtit': 'Soma em US$',
        'dfont' : 'BCB-DSTAT',
        'vtype' : 'value',
        'mult'  :  1_000_000,
        'divshow': 1_000_000,
        'decimal': 0,
        'blk_dx': 80,
    },


    # https://dados.gov.br/dataset/4513-divida-liquida-do-setor-publico-pib-total-setor-publico-consolidado (ESSE)
    # https://dados.gov.br/dataset/4536-divida-liquida-do-governo-geral-pib
    # https://br.investing.com/economic-calendar/brazil-debt-to-gdp-ratio-763

    'Div_Liq_PIB_Perc': {
        'title' : 'Dívida Liquída / PIB',
        'subtit': 'Relação entre a dívida e o tamanho da economia, em %',
        'dfont' : 'BCB-DSTAT',
        'decimal': 1,
        'blk_dx': 80
    },

    'Div_Bruta_PIB_Perc': {
        'title' : 'Dívida Bruta / PIB',
        'subtit': 'Relação entre a dívida e o tamanho da economia, em %',
        'dfont' : 'BCB-DSTAT',
        'decimal': 1,
        'blk_dx': 80
    },

    'RANK_ALL': {
        'title' : 'Bolsas do mundo',
        'subtit': 'Melhores desempenhos em moeda local',
        'dfont' : 'Investing',
    },

    'RANK_ALL_Pior': {
        'title' : 'Bolsas do Mundo',
        'subtit': 'Piores desempenhos em moeda local',
        'dfont' : 'Investing',
    },

    'RANK_ALL_USD': {
        'title' : 'Bolsas do mundo',
        'subtit': 'Melhores desempenhos em US$',
        'dfont' : 'Investing',
    },

    'RANK_ALL_USD_Pior': {
        'title' : 'Bolsas do mundo',
        'subtit': 'Piores desempenhos em US$',
        'dfont' : 'Investing',
    },

    'RANK_MOEDAS': {
        'title' : 'Moedas do mundo',
        'subtit': 'Melhores desempenhos, considerando variação da cotação em US$',
        'dfont' : 'Investing',
    },

    'RANK_MOEDAS_Pior': {
        'title' : 'Moedas no mundo',
        'subtit': 'Piores desempenhos, considerando variação da cotação em US$',
        'dfont' : 'Investing',
    },
}

# Usado para retornar valores antigos, caso altere pelo botão "digitado"
import copy
symbol_list_backup = copy.deepcopy(symbol_list)

symbol_vars = {
    'title' : '',
    'subtit': '',
    'dfont' : '',
    'vtype' : 'perc',
    'decimal': 0,
    'mult'  :  1,
    'divshow': 1,
    'group' :  1,
    'yref'  :  0,  #'free',
    'ylines': [],
    'blk_x':   0,
    'period': 'month',
    'quant' : 0,
    'type'  :'bar',
    'xformat':'',
    'xstep' : 1,
    'vstep' : 1,
    'convert': '',
    'bar_val_fs': 0,
    'label': [],
}


def set_data_vars(symbol, data):
    for var in symbol_list[symbol]:
        data[var] = symbol_list[symbol][var]

    for var in symbol_vars:
        if var not in symbol_list[symbol]:
            data[var] = symbol_vars[var]

    gvar['symbol_data'] = data


def get_symbol_var(symbol, var, val=None, setlower=True):
    if symbol in symbol_list and var in symbol_list[symbol]:
        val = symbol_list[symbol][var]
        if setlower and type(val) == str:
            val = val.lower()
    return val



from .gvar import *
from .util import gvar_error

def get_svar_err(var, default=None, e_msg='', e_num=-1):
    if var in gvar['symbol_data']:
        return gvar['symbol_data'][var]
    else:
        if e_msg == '':
            e_msg = f'Falta definir {var} no .csv'
        return gvar_error(default, e_msg, e_num)
