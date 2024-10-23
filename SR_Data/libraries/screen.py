import plotly.graph_objects as go
import ipywidgets as widget
from .gvar import *
from .util import save_error, set_config
from .graphics import set_graph, set_graph_axes, add_image, add_annot
from .pres_template import config_data

def show_text():
    annot = []

    text = gvar['scr_text']
    x, y  = float(gvar['scr_x']), float(gvar['scr_y'])
    color = gvar['scr_color']
    size  = float(gvar['scr_size'])

    # Troca \ por quebra de linha
    text2 = text.replace('\\n', '<br>').replace('\\', '<br>')
    text2 = f'<b>{text2}</b>'

    add_annot(annot, x, y, text2, color, size,
        xanchor='left', yanchor='top', align='left')

    fig.update_layout(annotations=annot)


def init_text(text, x, y, color, size):
    gvar['scr_x'], gvar['scr_y'] = str(x), str(y)
    gvar['scr_text']  = text
    gvar['scr_color'] = color
    gvar['scr_size']  = str(size)
    show_text()

def on_trait_txt(chg):
    if chg['name'] != 'value': return

    var = chg['owner'].placeholder
    val = chg['new']

    gvar[f'scr_{var}'] = str(val)
    show_text()


def button_scr_call(btype):
    btype = btype.upper()

    if btype == 'SCR':
        screen_end()
        return

    if btype == 'VID':
        msg[0].value = 'Generating Video (WAIT...)'
        var_def.clear()
        clips.clear()

        # set_img(['', 'anima/images/BG.png'])
        global video
        video = (mp.VideoFileClip('images/bg_videos/FUNDO_ANIMADO.mp4', audio=False,))
        clips.append(video)

        set_txt(['', gvar.get('scr_text', ''), gvar.get('scr_size', 30), gvar.get('scr_color', 'white'),
            gvar.get('scr_x', 0), gvar.get('scr_y', 0), 0.1, 0.03] )
        file_num = config_data.get('txt_vid_file_num', 1)
        set_out(['', f'videos/Texto_Video_{file_num:04d}.mp4'])
        set_config('txt_vid_file_num', file_num+1)
        msg[0].value = ''

def on_button_clicked(btn):
    button_scr_call(btn.description)

msg = [0]
def screen_hbox():
    close_bt = widget.Button(description='scr', layout=widget.Layout(width='42px'))
    close_bt.on_click(on_button_clicked)

    video_bt = widget.Button(description='vid', layout=widget.Layout(width='40px'))
    video_bt.on_click(on_button_clicked)

    text_txt = widget.Text(
        placeholder='text', value=gvar.get('scr_text', ''), indent=False,
        layout=widget.Layout(width='800px'),
    )
    text_txt.observe(on_trait_txt)

    # x_txt = widget.BoundedFloatText(
    x_txt = widget.Text(
        description='x:', placeholder='x', value=gvar.get('scr_x', ''), indent=False,
        layout=widget.Layout(width='150px'),
    )
    x_txt.observe(on_trait_txt)

    y_txt = widget.Text(
        description='y:', placeholder='y', value=gvar['scr_y'], indent=False,
        layout=widget.Layout(width='150px'),
    )
    y_txt.observe(on_trait_txt)

    color_txt = widget.Text(
        description='color:', placeholder='color', value=gvar.get('scr_color', '#000000'), indent=False,
        layout=widget.Layout(width='250px'),
    )
    color_txt.observe(on_trait_txt)

    size_txt = widget.Text(
        description='size:', placeholder='size', value=gvar['scr_size'], indent=False,
        layout=widget.Layout(width='150px'),
    )
    size_txt.observe(on_trait_txt)

    msg[0] = widget.Label(value = '.')


    hbox = widget.HBox([
        text_txt,
    ])

    hbox2 = widget.HBox([
        close_bt,
        x_txt, y_txt, color_txt, size_txt,
        video_bt, msg[0]
    ])

    return  (hbox, hbox2)


def screen_init(vbox):
    global vbox_saved, vbox_children_saved
    vbox_saved = vbox
    vbox_children_saved = vbox.children

    screen_graph()
    vbox.children = vbox.children[0:1] + screen_hbox() + (fig,)

def screen_end():
    vbox_saved.children = vbox_children_saved


def screen_graph():
    global fig
    fig = go.FigureWidget()

    bg_color = 'rgba(0,0,0,0)'

    gwidth, gheight = 1920, 1080
    # gvar['gwidth'] = gwidth
    # gvar['gheight'] = gheight
    # set_graph_center(gwidth / 2)

    scale = 0.5
    font = 'DIN Next LT Pro'
    set_graph(fig, gwidth, gheight, scale, bg_color, font)
    set_graph_axes(fig)

    add_image(fig, 'images/bg_perguntas.jpg', 0, 0, 1920, 1080,
        xanchor='left', yanchor='top', layer='below')

    # init_text('text', 170, 370, 'rgba(15,30,45,0.75)', 58)
    init_text('text', 170, 370, '#223344', 58)

    # return fig














import numpy as np
import moviepy.editor as mp
from PIL import Image, ImageFont, ImageDraw

quality = 6
fps = 24
dur_tot = 4.0  # 2.0
# gfont = ''
gfont = 'images/fonts/DINNextLTPro-Bold.ttf'

var_def = {}  # variaveis criadas no script
clips = []


def t_size(size_ini, size_step, t, dur_mov):
    if t < dur_mov:
        return size_ini + size_step * t
    else:
        return 1

def t_pos(x_ini, y_ini, x_step, y_step, t, dur_mov):
    if t >= dur_mov:
        t = dur_mov
    return x_ini - x_step * t, y_ini - y_step * t

def set_clip(img, xc, yc, w, h, size_ini, dur_mov, dur_tot):
    if dur_mov > 0:
        size_step = (1 - size_ini) / dur_mov
    else:
        size_step = 0

    x_ini = xc - (w * size_ini / 2)
    y_ini = yc - (h * size_ini / 2)
    x_step = w * size_step / 2
    y_step = h * size_step / 2

    clip = (mp.ImageClip(img)
        .resize(lambda t : t_size(size_ini, size_step, t, dur_mov))  # method='bilinear'
        .set_position(lambda t: t_pos(x_ini, y_ini, x_step, y_step, t, dur_mov))
        .set_end(dur_tot))

    return clip



def set_fon(vars):
    global gfont
    gfont = f'fonts/{vars[1]}'

def set_txt(vars):
    t, letter_time = 0, 0

    text, size, color, x, y = vars[1:6]
    if len(vars) > 6: t = float(vars[6])
    if len(vars) > 7: letter_time = float(vars[7])

    text = text.replace('\\n', '\n')
    text = text.replace('\\n', '\n').replace('\\', '\n')

    x, y = float(x), float(y)
    size = int(round(float(size)))
    font = ImageFont.truetype(gfont, size=size)

    if letter_time == 0:
        img = Image.new("RGBA", size=(2048, 200))
        draw = ImageDraw.Draw(img)
        draw.text((50, 50), text, font=font, fill=color)

        clip = (mp.ImageClip( np.array(img) )
            .set_position((x-50, y-50))
            .set_start(t)
            # .set_duration(dur_tot)
            .set_end(dur_tot)
        )
        clips.append(clip)
    else:
        for i in range(len(text)):
            img = Image.new("RGBA", size=(2048, 300))
            draw = ImageDraw.Draw(img)
            draw.text((50, 50), text[:i+1], font=font, fill=color, spacing=40)
            # draw.multiline_text((50, 50), text[:i+1], font=font, fill=color)

            clip = (mp.ImageClip( np.array(img) )
                .set_position((x-50, y-50))
                .set_start(t + i*letter_time))

            if i < len(text)-1:
                clip = clip.set_duration(letter_time)  # intermediário vai trocando
            else:
                clip = clip.set_end(video.duration)  # último vai até o fim

            clips.append(clip)


def set_img(vars):
    x, y = '0', '0'
    w, h = '1920', '1080'
    t = '0'

    img = f'{vars[1]}'

    if len(vars) > 2: x = vars[2]
    if len(vars) > 3: y = vars[3]
    if len(vars) > 4: w = vars[4]
    if len(vars) > 5: h = vars[5]
    if len(vars) > 6: t = vars[6]

    t = float(t)

    w, h = float(w), float(h)

    if x[0] in 'lcmr':
        align = x[0]
        x = float(x[1:])
    else:
        align = 'l'
        x = float(x)
    # if   align in 'cm': x -= w/2
    # elif align == 'r':  x -= w

    if y[0] in 'tcmd':
        align = y[0]
        y = float(y[1:])
    else:
        align = 't'
        y = float(y)
    # if   align in 'cm': y -= h/2
    # elif align == 'd':  y -= h

    # clip = mp.ImageClip(img).set_duration(dur_tot)
    # clip1 = set_clip(img1, 640, 500, 440, 440, 0.1, 0.35, dur_tot)
    # img, BG.png
    # img, circ.png,  c640, c500, 440, 440, 0.35

    clip = set_clip(img, x, y, w, h, 0.1, t, dur_tot)
    clips.append(clip)


def set_out(vars):
    out = f'{vars[1]}'
    vid = mp.CompositeVideoClip(clips)
    vid.write_videofile(out, fps=fps, bitrate=str(10 ** quality))


def exe_line(vars):
    global var_def

    commands = ['fon', 'txt', 'img', 'out']
    command_func = [set_fon, set_txt, set_img, set_out]

    for i in range(len(vars)):
        vars[i] = vars[i].strip()
        if vars[i] in var_def:
            vars[i] = var_def[ vars[i] ]

    comm = vars[0]
    if comm in commands:
        pos = commands.index(comm)
        command_func[pos](vars)
    elif len(vars) >= 2 and vars[0][:2] != '//':
        var_def[vars[0]] = vars[1]
    else:
        pass  # comment


# template = 'laranja.txt'
# template = 'teste.txt'

# file = open(f'templates/{template}', 'r', encoding='utf8')
# Lines = file.readlines()

# # Strips the newline character
# for line in Lines:
#     vars = line.strip().split(';')
#     exe_line(vars)
