from .pres_template import *
if gvar.get('is_SR_Data', True):
    from .focus import *
from .rank import *
from .tables import *
from .graphtime import *
from .drawtable import *
from .drawpizza import *
from .video import *
from .water import *
from .getdata import *

# BARHOR = False  # True

# text_bold = lambda txt, st:'<br>'*st + txt + '</br>'*st
def text_bold(txt, st):
    if st:
        txt = f'<b>{txt}</b>'
    return txt

def val_to_y(yref, y0, val, val_min, val_max):
    val_range = val_max - min(yref, val_min)
    return y0 - block_h * (val - yref) / val_range

def get_bar_color(color):
    # BLOCK_COLORS = [BLOCK_V3_COLOR,
    #     BLOCK_V3_COLOR, T_COLOR_2, T_COLOR_3, T_COLOR_4, T_COLOR_5, BLOCK_BG_COLOR_MID_UP, T_COLOR_7]

    if type(color) == int:
        color = BLOCK_COLORS[color % len(BLOCK_COLORS)]
    return color

def get_block_dx(data, pos):
    block_dx = data.get('blk_dx', BLOCK_DX)
    if type(block_dx) == list and block_dx not in [[],[0]]:
        block_dx = block_dx[pos % len(block_dx)]  # espaçamentos diferentes
    block_dx *= BLOCK_DX_FACTOR
    return block_dx


def index_draw_graph(fig, annot, symbol, n_months, val_col=None):
    global save_file_name

    data, save_file_name = get_symbol_data(symbol)
    if gvar['ERROR'] != '':
        return None, None

    # Salva dados de saída
    mdict = {'x':data['xaxis'], 'y':data['yaxis'],}
    pd.DataFrame(mdict).to_csv(f'data/out/{symbol}.csv', sep=';', index=False)

    graph_type = data['type']

    txt_bg_color, graph_layer = True, None
    if TEMPLATE in ['INVEST_NEWS_BLACK', 'JP_MERC_FIN_3']:
        txt_bg_color = False
        graph_layer = 'above'

    bar_val_fs = BAR_VAL_FONT_SIZE
    if data['bar_val_fs'] != 0:
        bar_val_fs = data['bar_val_fs']

    # Gráfico do tipo de tabela
    if graph_type[:5] == 'table':
        draw_table(fig, annot, symbol, data)
        show_extra_labels(fig, annot, symbol, data, bar_val_fs, graph_layer)
        return

    # Gráfico do tipo de pizza
    if graph_type[:5] == 'pizza':
        draw_pizza(fig, annot, symbol, data)
        show_extra_labels(fig, annot, symbol, data, bar_val_fs, graph_layer)
        return

    # GAMBIARRA(1)
    if data['vstep'] != 1:
        data['yaxis'] = data['yaxis'][-45::4]
        data['xaxis'] = data['xaxis'][-45::4]
        data['size']  = 12
        for i in range(data['size']):
            data['xaxis'][i] = f"{2022 - data['size'] + i}"

    # POSSÍVEL SOLUÇÃO PARA GAMBIARRA(1)
    # if data['vstep'] != 1:
    #     data['yaxis'] = data['yaxis'][::data['vstep']].reset_index(drop=True)
    #     data['xaxis'] = data['xaxis'][::data['vstep']].reset_index(drop=True)
    #     # data['size'] = data['size'] // data['vstep']
    #     data['size'] = data['xaxis'].size
    #     print(f"\n{data['yaxis'].size}  {data['xaxis'].size}  {data['size']}\n")


    # Workaround para fazer na mão
    # O correto é procurar por 'yearly' no group, e adicionar o texto com mês automaticamente
    # O data precisa conter o último mês em que há dados
    obs = ''
    if '*' in data['subtit']:
        obs = ' *'


    # Ajusta valores não-default (se houver no 'digitado')
    block_x = BLOCK_X
    if data['blk_x'] != 0:
        block_x = data['blk_x']

    block_w = data.get('blk_w', BLOCK_W)

    global block_h
    block_h = data.get('blk_h', BLOCK_H)

    xaxis_dy = data.get('xaxis_dy', False)

    size = data['size']

    # Ajusta v2, v3, ... caso existam
    n, vnmax = 2, 0
    while f'v{n}' in data:
        data[f'v{n}'] = data[f'v{n}'][-size:].reset_index(drop=True)
        vnmax = n
        n += 1

    # Soma valores na barra anterior para empilhar
    if graph_type == 'bars' and vnmax >= 2:
        for n in range(vnmax, 2, -1):
            data[f'v{n-1}'] += data[f'v{n}']
        data['yaxis'] += data['v2']


    # Abre valores em várias linhas para ficar igual formato antigo de barras paralelas (v042b)
    if graph_type == 'barp' and vnmax >= 2:
        xaxis, yaxis = [], []
        for p in range(size):
            xaxis.append(data['xaxis'][p])
            yaxis.append(data['yaxis'][p])
            for n in range(2, vnmax+1):
                xaxis.append('nan')  # Cria linha vazia ('nan', antigo método)
                yaxis.append(data[f'v{n}'][p])
        data['xaxis'] = xaxis.copy()
        data['yaxis'] = yaxis.copy()
        size *= vnmax

        # Cria lista de cores se não foi definido no .csv
        if not data.get('blk_cor', None):
            data['blk_cor'] = list(range(1, vnmax+1))

        # Cria lista de espaçamentos se não foi definida, ou se é apenas um número
        blk_dx = data.get('blk_dx', None)
        if not blk_dx or type(blk_dx) != list:
            blk_dx = data.get('blk_w', BLOCK_W) * 1.4   # Espaçamento = 40% maior que largura
            data['blk_dx'] = [blk_dx] * (vnmax-1) + [blk_dx * 1.6]  # 60% a mais na separação dos grupos


    val_max = max(data['yaxis'])
    val_min = min(data['yaxis'])
    # val_range = val_max - val_min

    yref = data.get('yref', 0)

    # y axis variable
    block_y = data.get('blk_y', BLOCK_Y)
    if yref == 0:
        if val_min >= 0:
            val_min = 0
        elif val_max < 0:
            val_max = 0
        val_range = val_max - val_min
        block_y += block_h * val_min / val_range
    elif val_min < yref:
        val_range = val_max - val_min
        block_y += block_h * (val_min - yref) / val_range

    ylines = data['ylines'].copy()
    if len(ylines) <= 1:  # == 0:
        ylines = get_ylines(val_min, val_max)

    y0 = block_y

    # calcula tamanho da linha horizontal
    block_dx_tot = 0
    for pos in range(size-1):
        block_dx_tot += get_block_dx(data, pos)

    # Largura total das linhas horizontais
    x0 = block_x - 24
    x1 = block_x + block_dx_tot + block_w + 24
    xmax = x1

    set_graph_center((x0 + x1) / 2 - 20)  # descota 20 (largura dos valores no eixo y)

    # draw yaxis lines (horizontal lines)
    for val in ylines:
        y = val_to_y(yref, y0, val, val_min, val_max)

        if val == yref:  # trick to appear very small positive bar
            y += 1

        if val == yref:
            width, opacity = 2, 1.00
        else:
            width, opacity = 1, YAXIS_LINE_OPACITY

        draw_line(fig, x0, y, x1, y, YAXIS_LINE_COLOR, width=width, opacity=opacity, layer=graph_layer)

        if val != 0 or yref != 0:
            txt = format_data_to_show(data, val)
            add_annot(annot, x0 - 6, y, txt, YAXIS_TEXT_COLOR, YAXIS_FONT_SIZE,
                xanchor='right', bg_color=txt_bg_color)

    # Pre-calcula todas as posições das barras
    x0s = []
    x0 = block_x
    for pos in range(size):
        x0s.append(x0)
        x0 += get_block_dx(data, pos)

    gvar['bar_xc'] = []

    # draw bars
    for pos in range(size):
        val  = data['yaxis'][pos]
        x0 = x0s[pos]
        block_dx = get_block_dx(data, pos)

        if graph_type == 'step':
            x1 = x0 + block_dx
        else:
            x1 = x0 + block_w
        xc = (x0+x1) / 2

        y1 = val_to_y(yref, y0, val, val_min, val_max)

        # Verifica se é último e se vai exibir diferente
        is_last = (pos == size - 1)
        last_diff = is_last and data.get('last_diff', True)

        # cor e se último pinta diferente pode vir do data
        # if val >= 0:
        if val >= yref:
            color = BLOCK_BG_COLOR_MID_UP
            xaxis_fc = get_color_pos(XAXIS_TEXT_COLOR, 0)
            if last_diff:
                color = BLOCK_BG_COLOR_END_UP
                xaxis_fc = get_color_pos(XAXIS_TEXT_COLOR, 2)
        else:
            color = BLOCK_BG_COLOR_MID_DN
            xaxis_fc = get_color_pos(XAXIS_TEXT_COLOR, 1)
            if last_diff:
                color = BLOCK_BG_COLOR_END_DN
                xaxis_fc = get_color_pos(XAXIS_TEXT_COLOR, 3)

        if graph_type[:3] != 'bar' and TEMPLATE != 'JP_MERC_FIN':
            color = T_COLOR_3

        color = data.get('blk_cor', color)
        if type(color) == list:
            color = color[pos % len(color)]
        if graph_type[:3] == 'bar':
            color = get_bar_color(color)
        else:
            color, bold = get_txt_color(color)

        global x_old, y_old
        if graph_type == 'line':
            xm = (x0 + x1) / 2
            if pos > 0:
                draw_line(fig, x_old, y_old, xm, y1, color, width=3, layer='above')
            x_old, y_old = xm, y1
        elif graph_type == 'step':
            if pos > 0:
                draw_line(fig, x_old, y_old, x_old, y1, color, width=3, layer='above')
            draw_line(fig, x0, y1, x1, y1, color, width=3, layer='above')
            x_old, y_old = x1, y1
        else:
            if graph_type in ['barv', 'bars']:
                color = get_bar_color(1)
            # if BARHOR:
            #     draw_rectangle(fig, 900-y0, x0, 900-y1, x1, color, layer=graph_layer) #, opacity=0.2)
            # else:
            draw_rectangle(fig, x0, y0, x1, y1, color, layer=graph_layer) #, opacity=0.2)

            gvar['bar_xc'].append((x0 + x1) / 2)

            n = 2
            while graph_type in ['barv', 'bars'] and f'v{n}' in data:
                v2 = data[f'v{n}'][pos]
                y2 = val_to_y(yref, y0, v2, val_min, val_max)
                draw_rectangle(fig, x0, y0, x1, y2, get_bar_color(n), layer='above')
                n += 1

        # Colors

        color = data.get('xaxis_fc', xaxis_fc)
        color, bold = get_txt_color(color)

        # Cor configurada no digitado
        bar_val_fc = data.get('bar_val_fc', color)
        if type(bar_val_fc) == list:
            bar_val_fc = bar_val_fc[pos % len(bar_val_fc)]
        bar_val_fc, bar_val_bold = get_txt_color(bar_val_fc)

        # Positions
        val_y  = y1 - 6
        date_y = y0 + 6
        val_yanchor  = 'bottom'
        date_yanchor = 'top'
        if val < yref:
            val_y  = y1 + 6
            date_y = y0 - 6
            val_yanchor, date_yanchor = date_yanchor, val_yanchor

        # Value at end of the bar
        if graph_type[:3] == 'bar' or (graph_type == 'step' and is_last):
            txt = format_data_to_show(data, val)
            txt = text_bold(txt, last_diff or bar_val_bold)
            add_annot(annot, xc, val_y, txt, bar_val_fc, bar_val_fs,
                xanchor='center', yanchor=val_yanchor, bg_color=txt_bg_color)

        # Value 2 at end of the bar
        if 'v2' in data and graph_type == 'bar2v':
            txt = data['v2'][pos]
            # txt = text_bold(txt, last_diff)
            v2y = val_y - 30
            if val < yref:
                v2y = val_y + 30
            add_annot(annot, xc, v2y, txt, bar_val_fc, bar_val_fs,
                xanchor='center', yanchor=val_yanchor, bg_color=txt_bg_color)

        # Step para exibição da info no eixo X
        if data['xstep'] != 1:  # and graph_type != 'bar':
            # steps para sempre exibir o último
            if pos % data['xstep'] != (size-1) % data['xstep']:
                continue

        # Abaixo só executa se não entrar no continue do if acima


        # Legenda embaixo das Barras Paralelas
        if graph_type == 'barp' and data.get('show_leg', 1) == 2:
            font_size = data.get('xaxis_fs', BAR_DATE_FONT_SIZE)
            legend = gvar['legend'][ pos % len(gvar['legend']) ]
            add_annot(annot, xc, date_y, legend, color, font_size,
                xanchor='center', yanchor=date_yanchor, bg_color=txt_bg_color)


        # Date at beginnig of the bar
        txt = str(data['xaxis'][pos])
        if txt == 'nan':
            continue

        txt = str(try_int_float(txt))

        cnt = 1
        for next in range(pos+1, size):
            if str(data['xaxis'][next]) == 'nan':
                cnt += 1
                xc += x0s[next] + (x1-x0)/2
            else:
                break
        xc /= cnt

        if xaxis_dy is not False:
            date_y = block_y + xaxis_dy
            date_yanchor = 'top'

        if is_last:
            txt += obs
        txt = text_bold(txt, last_diff)
        font_size = data.get('xaxis_fs', BAR_DATE_FONT_SIZE)
        if symbol[:9] in ['CAGED_SET', 'CAGED_REG']:
            font_size = bar_val_fs

        if graph_type == 'barp' and data.get('show_leg', 1) == 2:
            date_y += font_size * 1.3

        add_annot(annot, xc, date_y, txt, color, font_size,
            xanchor='center', yanchor=date_yanchor, bg_color=txt_bg_color)

    # Legenda
    if graph_type in ['bars', 'barp'] and data.get('show_leg', 1) == 1:
        block_dx = data.get('blk_dx', BLOCK_DX)
        if type(block_dx) == list:
            block_dx = max(block_dx)
        leg_x = xmax - block_w + block_dx
        leg_y = 200

        leg_x = data.get('leg_x', leg_x)
        leg_y = data.get('leg_y', leg_y)

        n = 1
        for legend in gvar['legend']:
            data['label'].append([legend, leg_x, leg_y+n*30, get_leg_color(n), 24, 'square'])
            n += 1

    # Extra labels
    show_extra_labels(fig, annot, symbol, data, bar_val_fs, graph_layer)


grapht, grapht_symbols = False, []

# Separa título em 2 linhas se for o caso
def adjust_title(title):
    if TEMPLATE == 'INVEST_NEWS_BLACK':
        pos = 25 + title[25:].find(' ')
        if pos != 25-1:  # -1 = returned if not found
            return [title[:pos], title[pos+1:]]
    return [title, '']

txt_digitado = False
def set_txt_digitado(st):
    global txt_digitado
    txt_digitado = st
def get_txt_digitado():
    return txt_digitado

dig_values = {}
def set_txt_digitado_values(title, subtit, dfont):
    dig_values['title'] = title
    dig_values['subtit'] = subtit
    dig_values['dfont'] = dfont

def ajust_txt(txt_old, txt_new):
    if txt_digitado:
        return txt_old
    else:
        return txt_new

def update_graph(fig, symbol, n_months, title, subtit, dfont, bg_transparent, val_col=None):
    global save_file_name
    global year_prev, date_ini, date_end
    global grapht, grapht_symbols
    global some_error

    annot = []

    show_labels = True
    axes_mode_old = True
    set_ref_type()
    set_margins(fig)
    years_enable(False)
    period_enable(False)
    dend_type_enable(False)
    period001_enable(False)
    country_enable(False)
    update_enable(False)

    if grapht:
        period_enable(True)
        axes_mode_old = False
        if symbol != '' and not symbol in grapht_symbols:
            grapht_symbols.append(symbol)
        # else:
        #     grapht_symbols.remove(symbol)

        if len(grapht_symbols) > 0:
            title, subtit, dfont, date_min, date_max = draw_graph_time(fig, annot, date_ini, date_end, grapht_symbols, debug=debug)
            save_file_name = (f'{title}  ('
                f'{date_min.strftime("%Y-%m-%d")}  a  '
                f'{date_max.strftime("%Y-%m-%d")})')
    elif symbol == '':
        return
    elif symbol in tables:
        if symbol == 'Bolsas_Mundo':
            show_bolsas_mundo(fig, annot)
        if symbol == 'Bolsas_Mundo_USD':
            show_bolsas_mundo(fig, annot, usd=True)
        if symbol == 'Moedas':
            show_moedas(fig, annot)
        if symbol == 'Table_Petroleo':
            period_enable(True)
            table_set_dates(date_ini, date_end)
            show_petroleo(fig, annot)
        some_error = tables_error()
        save_file_name = f'{symbol}'
        show_labels = False
    elif symbol[:5] == 'FOCUS':
        if gvar['ONLINE']:
            load_info_digitado(symbol)
            year_prev = symbol_list[symbol].get('year_prev', year_prev)
            date_ini  = symbol_list[symbol].get('date_ini' , date_ini)
            date_end  = symbol_list[symbol].get('date_end' , date_end)
            if type(date_ini) == str:
                date_ini = datetime.strptime(date_ini, '%Y-%m-%d')
            if type(date_end) == str:
                date_end = datetime.strptime(date_end, '%Y-%m-%d')

        date = show_focus(fig, annot, symbol, year_prev, date_ini, date_end, debug=debug)
        save_file_name = f'{symbol}_{date}'
        years_enable(True)
        if symbol == 'FOCUS_Simples':
            subtit = f'{date[8:]}/{month_txt[int(date[5:7])].upper()}/{date[:4]}'
        elif symbol in ['FOCUS_Dados', 'FOCUS_Dados_2']:
            subtit = f'Medianas nas expectativas do mercado: {date[8:]}/{month_txt[int(date[5:7])].upper()}/{date[:4]}'
        else:
            axes_mode_old = False
            title += f' {year_prev}'
            subtit = f'Expectativas de merc. entre {date_ini.strftime("%d/%m/%Y")} E {date_end.strftime("%d/%m/%Y")} - ' + subtit
            period_enable(True)
    elif symbol[:5] == 'GRAPH':
        axes_mode_old = False
        show_graph_comp(fig, annot, symbol, debug=debug)
        subtit += f". (Dados até {gvar['gcomp_date_end'].strftime('%d/%m/%Y')})"
        save_file_name = f'{symbol}'
    elif str(get_symbol_var(symbol, 'type'))[:4] == 'rank':
        country_enable(True)
        save_file_name, subtit = show_rank_dig(fig, annot, symbol, qtd=10, debug=debug)
        if gvar['ERROR'] != '':
            return
        # Atualiza para o caso de ter mudado conteúdo
        title  = symbol_list[symbol]['title']
        dfont  = symbol_list[symbol]['dfont']
    elif symbol[:4] == 'RANK':
        country_enable(True)
        period_enable(True)
        dend_type_enable(True)
        update_enable(True)
        qtd = 10
        if TEMPLATE == 'INVEST_NEWS_BLACK':
            subtit = ajust_txt(subtit, subtit + f' (DE {date_ini.strftime("%d/%m/%y")} A {date_end.strftime("%d/%m/%y")})')
        else:
            subtit = ajust_txt(subtit, subtit + f' (DE {date_ini.strftime("%d/%m/%Y")} A {date_end.strftime("%d/%m/%Y")})')
        save_file_name = (f'{symbol}  ('
            f'{date_ini.strftime("%Y-%m-%d")}  a  '
            f'{date_end.strftime("%Y-%m-%d")})'
            f'_{country_filter[0]}')
        rank_tot = show_rank(fig, annot, symbol, date_ini, date_end, dend_type, save_file_name, qtd, debug=debug)
        title = ajust_txt(title, f'{rank_tot} ' + title)
    elif symbol in symbol_list:
        index_draw_graph(fig, annot, symbol, n_months, val_col)
        if gvar['ERROR'] != '':
            return
        # Atualiza para o caso de ter mudado conteúdo
        title  = symbol_list[symbol]['title']
        subtit = symbol_list[symbol]['subtit']
        dfont  = symbol_list[symbol]['dfont']
    else:
        axes_mode_old = False
        draw_graph_001(fig, annot, date_ini, date_end, symbol, bg_transparent, debug=debug)
        some_error = get_g001_error()
        period001_enable(True)
        date_ini_enable(True)
        save_file_name = f'{symbol}'  # Talvez adicionar aqui "_{periodo}"
        # save_file_name = (f'{symbol}  ('
        #     f'{date_ini.strftime("%Y-%m-%d")}  a  '
        #     f'{date_end.strftime("%Y-%m-%d")})')
        show_labels = False

    if axes_mode_old:
        set_graph_axes(fig)

    if TEMPLATE == 'INVEST_NEWS' and not g001:
        draw_rectangle(fig, TITLE_X, TITLE_Y-40, GWIDTH-40, TITLE_Y+70, LOGO_BAR_COLOR)
        draw_rectangle(fig, TITLE_X, DFONT_Y+20, GWIDTH-40, DFONT_Y+60, 'gradient_purple_right.png')

    if MAIN_LOGO_PNG and not g001:
        add_image(fig, MAIN_LOGO_PNG, MAIN_LOGO_X, MAIN_LOGO_Y,
                MAIN_LOGO_W, MAIN_LOGO_H, xanchor='left', yanchor='top', layer='above')

    if WATERMARK_IMG != None and WATERMARK_LAYER == 'above':
        show_watermark(fig, g001)

    if show_labels:
        if get_txt_digitado():
            # title, subtit, dfont = dig_values['title'], dig_values['subtit'], dig_values['dfont']
            if dig_values['title']  != '': title  = dig_values['title']
            if dig_values['subtit'] != '': subtit = dig_values['subtit']
            if dig_values['dfont']  != '': dfont  = dig_values['dfont']

        titles = adjust_title(title)
        title_fc = get_symbol_var(symbol, 'title_fc', TITLE_COLOR)
        title_fc, bold = get_txt_color(title_fc)
        title_fs = get_symbol_var(symbol, 'title_fs', TITLE_FONT_SIZE)

        title_x = TITLE_X + TITLE_DX
        xanchor, align = 'left', 'left'
        titbold = True

        if template_codes[template_num] == 'JP2_':
            title_x = get_graph_center()
            xanchor, align = 'center', 'center'

        if template_codes[template_num] == 'JP3_':
            titbold = False

        if gvar.get('JP_Ibope'):
            title_x -= 40

        if titles[1] == '':
            add_annot(annot, title_x, TITLE_Y,
                    text_bold(title, titbold), title_fc, title_fs,
                    xanchor=xanchor, align=align)
        else:
            add_annot(annot, title_x, TITLE_Y-26,
                    text_bold(titles[0], titbold), title_fc, title_fs,
                    align='left')
            add_annot(annot, title_x, TITLE_Y+26,
                    text_bold(titles[1], titbold), title_fc, title_fs,
                    align='left')

        subtit_fc = get_symbol_var(symbol, 'subtit_fc', SUBTIT_COLOR)
        subtit_fc, bold = get_txt_color(subtit_fc)
        subtit_fs = get_symbol_var(symbol, 'subtit_fs', SUBTIT_FONT_SIZE)

        dfont_fc = get_symbol_var(symbol, 'dfont_fc', DFONT_COLOR)
        dfont_fc, bold = get_txt_color(dfont_fc)
        dfont_fs = get_symbol_var(symbol, 'dfont_fs', DFONT_FONT_SIZE)

        subtit_txt = subtit
        if gvar.get('server_error_msg', '') != '':  # '' = no error
            subtit_txt = gvar['server_error_msg']
        subtit_txt = set_str_fields(subtit_txt)
        if SUBTIT_CAPS:
            subtit_txt = subtit_txt.upper()
        add_annot(annot, title_x, SUBTIT_Y,
                f'{subtit_txt}', subtit_fc, subtit_fs, xanchor=xanchor)

        if len(dfont) > 1:
            add_annot(annot, DFONT_X, DFONT_Y,
                f'FONTE: {dfont}', dfont_fc, dfont_fs)

        fig.update_layout(annotations=annot)


def draw_graph(scale, symbol, n_months, title, subtit, dfont, bg_transparent, val_col=None):
    global GWIDTH, GHEIGHT

    GWIDTH, GHEIGHT = 1700, 800

    if TEMPLATE == 'INVEST_NEWS' or TEMPLATE == 'NECTON':
        GWIDTH = 1326
        
    if TEMPLATE == 'SBT':
        GWIDTH, GHEIGHT = 1920, 1080

    if TEMPLATE == 'JP_IBOPE':
        GWIDTH = 800

    if template_codes[template_num] == 'JP3_':
        GWIDTH, GHEIGHT = 1920, 1080

    gvar['decimal'] = 2

    check_symbol_update(symbol)

    fig = go.FigureWidget()

    bg_color = BG_COLOR
    if bg_transparent:
        bg_color = 'rgba(0,0,0,0)'

    global gwidth, gheight, g001
    gwidth, gheight, g001 = GWIDTH, GHEIGHT, False

    if symbol in tables:
        gwidth, gheight = 864, 524
        if TEMPLATE == 'INVEST_NEWS':
            gwidth, gheight = 1326, 800
    elif (not grapht) and (symbol not in symbol_list):
        gwidth, gheight = 980, 600
        g001 = True

    if TEMPLATE == 'INVEST_NEWS_BLACK':
        gwidth, gheight = 1080, 1080

    gvar['gwidth'] = gwidth
    gvar['gheight'] = gheight

    set_graph_center(gwidth / 2)

    set_graph(fig, gwidth, gheight, scale, bg_color, FONT)

    bg_img = get_symbol_var(symbol, 'bg_img', setlower=False)
    if bg_img:
        add_image(fig, bg_img, 0, 0, gwidth, gheight,
                xanchor='left', yanchor='top', layer='below')

    if template_codes[template_num] == 'JP3_' and not bg_img:
        add_image(fig, 'images/bg_images/BG_Merc_Fin_Bar.jpg', 0, 0,
                gwidth, gheight, xanchor='left', yanchor='top', layer='below')

    if TEMPLATE == 'INVEST_NEWS_BLACK' and not g001:
        add_image(fig, 'images/invest_news/InvNews_Bg_Black.jpeg', 0, 0,
                1080, 1080, xanchor='left', yanchor='top', layer='below')
    
    if TEMPLATE == 'SBT' and not g001:
        add_image(fig, 'images/sbt/bg.png', 0, 0,
                GWIDTH, GHEIGHT, xanchor='left', yanchor='top', layer='below')
    
    if WATERMARK_IMG != None and WATERMARK_LAYER == 'below':
        show_watermark(fig, g001)

    update_graph(fig, symbol, n_months, title, subtit, dfont, bg_transparent, val_col=val_col)

    return fig


some_error = 0
def get_some_error():
    if some_error:
        return some_error
    elif gvar.get('ERROR', '') != '':
        return gvar['ERROR']
    else:
        return 0


def get_save_file_name():
    return save_file_name

def graph_create_video(pos='CHEIA'):
    file_name = f'{template_codes[template_num]}_{save_file_name}'
    create_video(file_name, gwidth, gheight, debug=debug, pos=pos)


def st_to_vars(st):
    disabled = not st
    visibility = 'visible'
    if disabled:
        visibility = 'hidden'
    return disabled, visibility

def period_enable(st=True):
    if gvar['ONLINE']: return
    disabled, visibility = st_to_vars(st)
    date_ini_sel.disabled = disabled
    date_end_sel.disabled = disabled
    date_ini_sel.layout.visibility = visibility
    date_end_sel.layout.visibility = visibility

def date_ini_enable(st=True):
    if gvar['ONLINE']: return
    disabled, visibility = st_to_vars(st)
    date_ini_sel.disabled = disabled
    date_ini_sel.layout.visibility = visibility

def dend_type_enable(st=True):
    if gvar['ONLINE']: return
    disabled, visibility = st_to_vars(st)
    dend_type_sel.disabled = disabled
    dend_type_sel.layout.visibility = visibility

def years_enable(st=True):
    if gvar['ONLINE']: return
    disabled, visibility = st_to_vars(st)
    year_prev_sel.disabled = disabled
    year_prev_sel.layout.visibility = visibility

def period001_enable(st=True):
    if gvar['ONLINE']: return
    disabled, visibility = st_to_vars(st)
    period_sel.disabled = disabled
    period_sel.layout.visibility = visibility

def country_enable(st=True):
    if gvar['ONLINE']: return
    disabled, visibility = st_to_vars(st)
    country_sel.disabled = disabled
    country_sel.layout.visibility = visibility

def update_enable(st=True):
    if gvar['ONLINE']: return
    disabled, visibility = st_to_vars(st)
    upd_bt.disabled = disabled
    upd_bt.layout.visibility = visibility

debug = False
def set_view_fields(date_ini, date_end, dend_type, year_prev, period, country, update, debug0):
    global date_ini_sel, date_end_sel, dend_type_sel, year_prev_sel, period_sel, country_sel, upd_bt, debug
    date_ini_sel = date_ini
    date_end_sel = date_end
    dend_type_sel = dend_type
    year_prev_sel = year_prev
    period_sel = period
    country_sel = country
    upd_bt = update
    debug = debug0

def set_date_ini(val):
    global date_ini
    date_ini = val
    gvar['date_ini'] = val

def set_date_end(val):
    global date_end
    date_end = val
    gvar['date_end'] = val

def set_dend_type(val):
    global dend_type
    dend_type = val

def set_year_prev(val):
    global year_prev
    year_prev = val

def set_grapht(val):
    global grapht, grapht_symbols
    grapht = val
    grapht_symbols = []

def get_grapht():
    return grapht

