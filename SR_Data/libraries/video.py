import moviepy.editor as mp
from datetime import datetime
from pathlib import Path
from PIL import Image
from .util import *

file_img_to_video = 'graphics/img_to_video.png'
quality = 6
fps = 30
# dur_tot = 8.0  # 2.0

# def set_clip(img, x, y, w, h):
#     clip = (mp.ImageClip(img)
#         .resize((w, h))
#         .set_position((x, y))
#         .set_duration(video.duration))

#     return clip

def create_video(file_name, w, h, x=-1, y=-1, debug=None, adj_center=True, pos='CHEIA'):
    clips = []

    OPTION = 1
    MULT = 1.30

    if pos == 'TELAO_ESQ':
        video = (mp.VideoFileClip('images/bg_videos/BG_TELAO_LEFT.mp4', audio=False,))
    elif pos == 'TELAO_DIR':
        # video = (mp.VideoFileClip('images/bg_videos/BG_TELAO_LEFT.mp4', audio=False,).fx(mp.vfx.mirror_x))
        video = (mp.VideoFileClip('images/bg_videos/BG_TELAO_RIGHT.mp4', audio=False,))
    else:
        if template_codes[template_num] != 'JP2_':
            if pos == 'CHEIA2':
                # video = (mp.VideoFileClip('images/bg_videos/BG_GRAFICOS_LOOP_30P.mp4', audio=False,))
                # video = (mp.ImageClip('images/bg_videos/BG_2K_MERCADO_FINANCEIRO.jpg'))
                video = (mp.ImageClip('images/bg_videos/FUNDO_2K_CLARO.jpg'))
            else:
                # video = (mp.VideoFileClip('images/bg_videos/BG_GRAFICOS_LOOP.mp4', audio=False,))
                # video = (mp.ImageClip('images/bg_videos/BG_2K_MERCADO_FINANCEIRO.jpg'))
                video = (mp.ImageClip('images/bg_videos/FUNDO_2K_CLARO.jpg'))
        else:
            if OPTION == 2:
                # Escuro original
                video = (mp.VideoFileClip('images/bg_videos/BG_LOOP_01.mp4', audio=False,))
                MULT = 1.20
            else:
                # Opção 3 de blur branco
                # video = (mp.VideoFileClip('images/bg_videos/bg_loop_teste_3.mp4', audio=False,))
                # Opção 3.5 de blur branco
                # video = (mp.VideoFileClip('images/bg_videos/ENTRADA_3_V2.mp4', audio=False,))
                # Opção mais escura com blur mais horizontal feita na JP
                # video = (mp.VideoFileClip('images/bg_videos/BG_LOOP_01.mp4', audio=False,))
                video = (mp.ImageClip('images/bg_videos/BG_LOOP_01.jpg'))
                # video = (mp.VideoFileClip('C:/Users/Rogerup/Downloads/Samy_Proj_Files/SAMY_BASE_TABELA.mp4', audio=False,))

    clips.append(video)

    h2 = 800             # 007_
    if h in [600, 524]:  # 001_, 002_
        h2 = 720
        adj_center=False

    w2 = round(w/h * h2)
    if x < 0:
        x = round((1920-w2) / 2)
    if y < 0:
        y = 30               # 007_
        if h in [600, 524]:  # 001_, 002_
            y = 50

    if pos == 'CHEIA2':
        w2 *= MULT
        h2 *= MULT
        x = round((1920-w2) / 2)
        if template_codes[template_num] == 'JP_':
            if h in [600, 524]:  # 001_, 002_
                x += 60

            y += 35

            if h in [600]:    # 001_
                y += 0
            elif h in [524]:  # 002_
                y += 50
            else:
                y -= 50
        else:
            y += 50

    xd, img_w = left_pixel(file_img_to_video, w, w2)
    if adj_center:
        x += xd

    # Na esquerda, mais para baixo, 75% do tamanho
    if pos == 'TELAO_ESQ':
        w2 *= 0.75
        h2 *= 0.75
        x -= 250
        y += 220

    # No meio, mais para baixo, 80% do tamanho
    if pos == 'TELA_MEIO':
        w2 *= 0.80
        h2 *= 0.80
        x += 100
        y += 220

    # Na direita, mais para baixo, 75% do tamanho
    if pos == 'TELAO_DIR':
        w2 *= 0.75
        h2 *= 0.75
        img_w *= 0.75
        x = 1920 - img_w - 250
        y += 220

    if OPTION == 2:  # esse OPTION 2 foi um teste que não ficou bom
        image_bg = (mp.ImageClip('images\white.png')
        .set_opacity(0.60)
        .resize((1920-x*2 - 80, h2 - 40))
        .set_position((x + 40, y))
        .set_duration(video.duration))
        clips.append(image_bg)

    image = (mp.ImageClip(file_img_to_video)
        .resize((w2, h2))
        .set_position((x, y))
        .set_duration(video.duration))
    clips.append(image)

    # Para JP1, 'CHEIA2' passou a se chamar 'TELAO' (v042b)
    if template_codes[template_num] == 'JP_' and pos == 'CHEIA2':
        pos = "TELAO"

    out = f'videos/{file_name}_{pos}.mp4'
    delete_file(out)
    vid = mp.CompositeVideoClip(clips)

    dir_remote = remote_path()

    if template_codes[template_num] in ['JP_', 'JP2_']:
        # https://zulko.github.io/moviepy/getting_started/videoclips.html
        out = out[:-3] + 'png'
        vid.save_frame(out)
        if dir_remote:
            try:
                vid.save_frame(out.replace('videos/', dir_remote))
            except: pass
    else:
        vid.write_videofile(out, fps=fps, bitrate=str(10 ** quality))
        if template_codes[template_num] == 'JP2_' and dir_remote:
            try:
                vid.write_videofile(out.replace('videos/', dir_remote), fps=fps, bitrate=str(10 ** quality))
            except: pass

    send_by_telegram(out)


def left_pixel(file_img, w0, w2):
    im = Image.open(file_img)

    w, h = im.size
    x, y, a = w, 0, 0
    step = 20

    # right pixel
    while a == 0:  # while has alpha != 0
        x -= step

        while a == 0:
            y += step
            if y >= h - step:
                y = 0
                break

            a = im.getpixel((x, y))[3]

    # left pixel
    xleft, y, a = 0, 0, 0
    while a == 0:  # while has alpha != 0
        xleft += step

        while a == 0:
            y += step
            if y >= h - step:
                y = 0
                break

            a = im.getpixel((xleft, y))[3]

    im.close()

    #                 scale * margin
    return ((w - (x + ( w/w0 *  120 ))) / 2 * (w2/w),
        (x - xleft) * (w2/w))
