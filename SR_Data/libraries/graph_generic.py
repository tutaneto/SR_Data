# import plotly.graph_objects as go
from .graphics import *

def gen_graph(width, height, margin, df, x_col, y_cols,
        font, fontcolor='black', bgcolor='white',
        gridcolor='black', gridx=False, gridy=True, tick_fs=24, scale=1,
        line_width=3, line_color=None):

    fig = go.FigureWidget()

    # width  = gwidth
    # height = gheight + margin_t + margin_b

    GS = scale

    set_graph(fig, width, height, scale, bgcolor, font)

    fig.update_layout(font=dict(color=fontcolor), showlegend=False)
    set_margins(fig, *margin)
    set_ref_type(xref='paper', yref='paper')

    fig.update_xaxes(showgrid=gridx, tickfont=dict(size=tick_fs), gridcolor=gridcolor, gridwidth=1, showline=True, showspikes=True, ticks='outside', )
    fig.update_yaxes(showgrid=gridy, tickfont=dict(size=tick_fs), gridcolor=gridcolor, gridwidth=1, )

    # line_color = ['#FF5A5A', '#FFC001', '#00BCFF', '#A5A5A5', '#33AA33', ] #'#2B5295']
    pos = 0
    for y_col in df[y_cols]:
        color = line_color
        if color != None:
            color = color[pos]

        fig.add_trace(
            go.Scatter(
                # desloca alguns pixels a linha de cada canal para não sobrepor "+ (len(show_cols) - pos) * line_dy)"
                x=df[x_col], y=df[y_col], # + (len(show_cols) - pos) * line_dy, # name=ch_name_show[col],
                line=dict(width=line_width*GS, color=color), mode='lines',
            ) )
        pos += 1

    # save_graph('png', fig, f'{unidecode(program_info[0])} ({gtype}) ({gmode})')

    return fig


'''
def gen_graph_period(program_date, program_info, universo, gmode='all'):
    df = get_program_data(program_date, program_info)

    nrows = df.shape[0]
    if nrows == 0:
        return  # empty dataframe

    fig = go.FigureWidget()
    annot = []

    bg_color = '#001324'
    gwidth, gheight = 1200, 400

    gmovx, gmovy = 20, 36
    margin_t, margin_b = 200-gmovy, 300+gmovy

    if gvar.get('graph_period_type', None) == 'realtime':
        margin_t, margin_b = 400, 100

    width = gwidth
    height = gheight + margin_t + margin_b

    set_graph(fig, width, height, 1, bg_color, FONT)
    fig.update_layout(font=dict(color='#CCFFFF'), showlegend=False)
    set_margins(fig, l=80+gmovx, r=80-gmovx, t=margin_t, b=margin_b, pad=16)
    set_ref_type(xref='paper', yref='paper')

    fig.update_xaxes(showgrid=False, tickfont=dict(size=24), showline=True, showspikes=True, ticks='outside', )
    fig.update_yaxes(showgrid=True,  tickfont=dict(size=24), gridcolor='#336666', gridwidth=1, )

    show_cols = ['JOVEM PAN NEWS', 'CNN BRASIL', 'GLOBO NEWS', 'BANDNEWS', 'RECORD NEWS']
    if gmode == 2:
        show_cols = ['JOVEM PAN NEWS', 'CNN BRASIL']
    if gmode == 3:
        show_cols = ['JOVEM PAN NEWS', 'CNN BRASIL', 'GLOBO NEWS']

    gtype, tot, decimal, suffix = get_gtype_vars(df, show_cols, universo)

    vmin = df[show_cols].min().min() / tot
    vmax = df[show_cols].max().max() / tot
    line_dy = (2 / gheight) * (vmax-vmin)

    x = TITLE_X + gmovx + 10
    y = height - 150 - gmovy

    if gvar.get('graph_period_type', None) == 'realtime':
        y = 240

    media_abs = ''
    if gtype != 'Rat Abs':
        media_abs = 'Média Abs'

    if program_info[0] == '':
        # set_info_texts(annot, x, y, '#CCFFFF', [gtype.upper(), 'Last min', 'Média', 'Máximo', 'Best min'])
        set_info_texts(annot, x, y, '#CCFFFF', [gtype.upper(), 'Last min RAT', 'Last min', 'Média', 'Máximo', 'Best min'])
    else:
        set_info_texts(annot, x, y, '#CCFFFF', [gtype.upper(), 'Média', 'Máximo', 'Best min', media_abs])

    # JOVEM PAN NEWS / CNN BRASIL / GLOBO NEWS / BANDNEWS / RECORD NEWS
    line_color = ['#FF5A5A', '#FFC001', '#00BCFF', '#A5A5A5', '#33AA33', ] #'#2B5295']
    pos = 0
    for col in show_cols:
        fig.add_trace(
            go.Scatter(
                # desloca alguns pixels a linha de cada canal para não sobrepor "+ (len(show_cols) - pos) * line_dy)"
                x=df['MIN'], y=df[col]/tot + (len(show_cols) - pos) * line_dy, # name=ch_name_show[col],
                line=dict(width=3*GS, color=line_color[pos]), mode='lines',
            ) )

        time_max_idx = df[col].idxmax()
        time_max = df.loc[time_max_idx, 'MIN'].strftime("%H:%M")

        xc = x + 220 + 150 * pos

        img_file = f"images/jp_ibope_icons/{ch_name_show[col].upper().replace(' ', '_')}.png"
        add_image(fig, img_file, xc, y-32, 64, 64, layer=None)

        media_abs, div = '', 1
        if gtype != 'Rat Abs':
            mfactor = 1
            if universo == 'share':
                mfactor = df['TOTAL PAYTV'] / 100
            media_abs = f'{(df[col] * mfactor * UNIVERSO / 100 / 1000).mean():.1f}K'
        if suffix == 'K':
            div = 1000

        val_last = f'{df[col].iloc[-1]/(tot*div):.{decimal}f}{suffix}'
        val_mean = f'{df[col].mean()/(tot*div):.{decimal}f}{suffix}'
        val_max  = f'{df[col].max() /(tot*div):.{decimal}f}{suffix}'

        # Calculado ao contrário quando se apresenta gráfico do Share
        val_rat = f"{df[col].iloc[-1] * df['TOTAL PAYTV'].iloc[-1] / 100:.{decimal}f}"

        # Colunas embaixo com informações
        if program_info[0] == '':
            # set_info_texts(annot, xc, y, line_color[pos], ['', val_last, val_mean, val_max, time_max ], 'center')
            set_info_texts(annot, xc, y, line_color[pos], ['', val_rat, val_last, val_mean, val_max, time_max], 'center')
        else:
            set_info_texts(annot, xc, y, line_color[pos], ['', val_mean, val_max, time_max, media_abs], 'center')
        pos += 1


    # Colunas de vitória quando tem apenas 2 canais
    if len(show_cols) in [2, 3]:
        xc = x + 220 + 150*3.5 - 40
        set_info_texts(annot, xc, y, '#CCFFFF',
            ['JP vs CNN', f'{ch_name_short[show_cols[0]]} ganhou', f'{ch_name_short[show_cols[1]]} ganhou', 'Empate'])

        win  = round((df[show_cols[0]]  > df[show_cols[1]]).sum() / nrows * 100)
        lost = round((df[show_cols[0]]  < df[show_cols[1]]).sum() / nrows * 100)
        # draw = (df[show_cols[0]] == df[show_cols[1]]).sum() / nrows * 100
        draw = 100 - win - lost

        xc = x + 220 + 150*4.5
        set_info_texts(annot, xc, y, '#CCFFFF',
            ['%', f'{win:.0f}', f'{lost:.0f}', f'{draw:.0f}'], 'center')


    hour_ini = program_info[1]
    hour_end = program_info[2]
    dow = program_date.weekday()

    xanchor, align = 'left', 'left'

    txt_programa = ''
    # if OP_PERIODO.startswith('program'):
    #     txt_programa = 'PROGRAMA: '
    title = f'<b>{txt_programa}{program_info[0]}</b>'
    if program_info[0] == '':
        subtit = f"{program_date.strftime('%d/%m/%Y')} ({dow_name[dow][:3]})  -  {hour_ini[:5]} as {hour_end[:5]}\n"
        # subtit = f"{hour_ini[:5]} as {hour_end[:5]}\n"
    else:
        subtit = f"<b>{gtype.upper()}<b>  -  Ibope no dia {program_date.strftime('%d/%m/%Y')} ({dow_name[dow]})  das {hour_ini[:5]} as {hour_end[:5]}\n"

    add_annot(annot, TITLE_X,  TITLE_Y,  title,  TITLE_COLOR,  TITLE_FONT_SIZE,  xanchor=xanchor, align=align)
    add_annot(annot, SUBTIT_X, SUBTIT_Y, subtit, SUBTIT_COLOR, SUBTIT_FONT_SIZE, xanchor=xanchor)

    fig.update_layout(annotations=annot)

    save_graph('png', fig, f'{unidecode(program_info[0])} ({gtype}) ({gmode})')

'''
