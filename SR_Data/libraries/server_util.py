from .digitado import load_info_digitado

ERR_GRAPH_DATA_EMPTY = 1

server_error_txt = ['',                             # 0  (No Error)
    'Faltam dados para a geração do gráfico.',      # 1
    '',
    '',
    '',
]

def check_graph_data(symbol):
    datahead, skiprows = load_info_digitado(symbol)
    if datahead == None or len(datahead) < 3:
        return ERR_GRAPH_DATA_EMPTY

    # Verificar no datahead se é um tipo válido (x;y  IBGE_  BC_  INV_, ...)
    # Verificar consistência dos dados

    return 0
