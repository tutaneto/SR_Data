from .graphics import *
# from .coins import *
# from .symbols import get_svar_err

# import plotly.graph_objects as go

# https://plotly.com/python/reference/pie/
# https://plotly.com/python/reference/layout/

def draw_pizza(fig, annot, symbol, data):
    # set_margins(fig, *GT_MARGINS_LRTBPAD)
    # set_graph_center((GT_MARGINS_LRTBPAD[0] - GT_MARGINS_LRTBPAD[1])/2)  # valor negativo (Subtrai do centro)

    set_ref_type(xref='paper', yref='paper')
    # rmargin = 200 # jp2
    rmargin = 600 # jp1
    textinfo = 'none'
    showlegend = False

    if gvar.get('JP_Ibope', False):
        rmargin = 0
        textinfo='percent+label'
        showlegend=False

    set_margins(fig, l=0, r=rmargin, t=200, b=100, pad=0)
    set_graph_center((0 - rmargin)/2)  # valor negativo (Subtrai do centro)
    GS = get_scale()

    # colors = ['gold', 'mediumturquoise', 'darkorange', 'lightgreen']
    colors = ['royalblue', 'darkblue', 'darkred']

    fig.add_trace(
        go.Pie(
            labels=data['xaxis'], values=data['yaxis'],
            textfont=dict(size=36*GS),
            # marker_colors=[BLOCK_V3_COLOR, T_COLOR_4, T_COLOR_2, T_COLOR_3,],
            # marker_colors=['#FF5A5A', '#FFC001', '#00BCFF', '#A5A5A5', '#33AA33', ], #'#2B5295']
            marker_colors = colors,
            textinfo=textinfo,
            textposition='inside',

            # name=f'{name} ({perc_str}%)',

            # line=dict(width=3*GS, color=get_txt_color(line_color[pos], ret_bold=False)), mode='lines',
        ))


    fig.update_layout(
    #     # width=500, height=500,
    #     # margin=dict(t=200, b=200, l=200, r=200)
    #     # yaxis_tickformat = yaxis_tickformat,
    #     # separators=',.', yaxis_zeroline=False, xaxis_zeroline=False,
        showlegend=showlegend, legend=dict(
            font=dict(size = 24*GS,),  #size=GT_LEGEND_FS*GS,),
            # itemsizing='constant',
    #       color=GT_LEGEND_FC),
    #       x=legend_x, y=legend_y, xanchor='auto',
            # x=0.88, y=1, xanchor='auto',
            # x=0.65, y=1, xanchor='left',
            bgcolor='rgba(0,0,0,0)')
        )

    # Retângulos da legenda
    # x =   0 + 0.65 * (gvar['gwidth' ] - 200)
    # y = 200 + 0.00 * (gvar['gheight'] - 300)
    # draw_rectangle(fig, x, y, x+20, y+20, T_COLOR_1)
