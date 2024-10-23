from .gvar import *
gvar['is_SR_Data'] = False

from .util_generic import *
from .graph_generic import *

import googleapiclient.discovery
import requests
import csv



#############################################################
#                    CONFIGURATION                          #
#############################################################

gvar['SITE_CSV_FILE'] = True
gvar['SITE_IMG_FILE'] = True
gvar['SEND_VIDEO_GRAPH'] = True

# OP_TELEGRAM     =   'Test'  # (None / 'Test' / 'JP')
OP_TELEGRAM     =   'JP'



#############################################################
#                       CONSTANTS                           #
#############################################################

GROUPS     = ['JP',      'CNN',        'Band',      'Rec',         'SBT'     ]
GCOLORS    = ['#FF5A5A', '#FFC001',    '#A5A5A5',   '#33AA33',     '#BB00FF' ]  # '#00BCFF'

icon_names = ['JP News', 'CNN Brasil', 'Band News', 'Record News', 'SBT News']  # 'Globo News',

file_name_img_tmp  = 'graphics/temp.png'  # Usado no recorte de imagens

# @Apo_Sport_bot (Sport_Dicas)  /  Grupo: Ex_Genius_Bet
telegram_bot = telebot.TeleBot('5386350950:AAGYTdg7RXxkC6j6OyOLpJbaFSlBaIR1EDw')
telegram_chat_id = [-1001296286944, None, -601995029]

if OP_TELEGRAM == 'JP':
    # @xyz_SR_Data_bot (SR_Data_Bot)  /  Grupo: Audiência JP  (Direção / Jornalismo / Comercial)
    telegram_bot = telebot.TeleBot('5383195715:AAHqAtnu74hMDH7qWfN7Eu_BH_c2KO_PWZA')
    telegram_chat_id = [-1001769268544, -692440616, -1001613370831]  # Era antes de virar: ??? / ??? / -729902503


#############################################################
#                    INITIALIZATION                         #
#############################################################

youtube_data_path = 'data/jp/'
file_name_vid  = youtube_data_path + 'youtube_vid.csv'
file_name_cnt  = youtube_data_path + 'youtube_cnt.csv'
file_name_chn  = youtube_data_path + 'youtube_chn.csv'
file_name_upd  = youtube_data_path + 'jp-youtube.csv'
file_name_rti  = youtube_data_path + 'jp-yt-realtime.csv'

def youtube_live_init():
    global df_chn
    global channel_names #, n_channels
    global channel_group, channel_id, channel_show, channel_live

    # Brazilian R$ format
    locale.setlocale(locale.LC_ALL, 'pt_BR')

    df_chn = read_csv_strip(file_name_chn)

    channel_names = []
    channel_id, channel_group, channel_show, channel_live = {}, {}, {}, {}

    for _, row in df_chn.iterrows():
        channel = row['channel']
        channel_names.append(channel)
        channel_id   [channel] = row['id']      # look for 'externalid' at page source
        channel_group[channel] = row['group']
        channel_show [channel] = row['name']
        channel_live [channel] = []

    # n_channels = len(channel_names)


    global df_vid, df_cnt
    df_vid = pd.read_csv(file_name_vid, sep=';')
    df_cnt = pd.read_csv(file_name_cnt, sep=';', parse_dates=['dtime'])

    # Adiciona vídeos inicializados mas não finalizados
    # print("Vídeos 'Live'")
    for _, row in df_vid.iterrows():
        if str(row['dt_ini']) == '-1' or str(row['dt_end']) == '-1':
            channel_live[row['channel']].append(row['video_id'])
            # print(row['channel'], channel_live[row['channel']][-1])


youtube_live_init()



#############################################################
#                       CAPTURE DATA                        #
#############################################################

def youtube_api_connect():
    # Quando perde a conexão não precisa chamar novo "build",
    # basta chamar "request.execute()" novamente que reconecta

    # API information
    api_service_name, api_version = 'youtube', 'v3'
    DEVELOPER_KEY = ['AIzaSyDMe1gqHp0NW04RQFUCOinQRFJxUhw8P9U',
                     'AIzaSyBjtazGWjbxL8ETvUDQ2-SbhOzh_fiR_4I',]

    gvar['dev_key_pos'] = gvar.get('dev_key_pos', 0) + 1
    if  gvar['dev_key_pos'] > 1:
        gvar['dev_key_pos'] = 0
    developer_key = DEVELOPER_KEY[gvar['dev_key_pos']]

    # API client
    global youtube
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = developer_key)

    print(f'\nYoutube KEY : {developer_key[-8:]}')


# Usando API, quota=100 para cada pesquisa
def youtube_get_live_videos(channel_name):
    request = youtube.search().list(
        channelId=channel_id[channel_name],
        part="snippet", eventType="live", type="video",
        # maxResults=20,
        # order='date', # q="news",
    )
    response = request.execute()

    for item in response['items']:
        vid_id = item['id']['videoId']
        if vid_id not in channel_live[channel_name]:
            channel_live[channel_name].append(vid_id)
        # Título do vídeo = item['snippet']['title']


# Pegando os links direto na página
def youtube_get_live_videos_url(channel_name):
    # HEADERS = ({'User-Agent':
    #             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
    #             (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',\
    #             'Accept-Language': 'en-US, en;q=0.5'})

    # url = 'https://www.youtube.com/c/' + channel_name
    url = 'https://www.youtube.com/channel/' + channel_id[channel_name]

    webpage = requests.get(url)  #, headers=HEADERS)
    page_txt = webpage.text

    # Esta linha é só para garantir que tem Featured (mas não seria necessária)
    pos = page_txt.find('channelFeaturedContentRenderer')

    while pos != -1:
        txt_find = '"videoRenderer":{"videoId":"'  # Somente vídeos Featured contém isso
        pos = page_txt.find(txt_find, pos+10)
        if pos == -1: break

        vid_id_pos = pos + len(txt_find)

        pos_end = page_txt.find('"', vid_id_pos)
        if pos_end == -1: break

        vid_id = page_txt[vid_id_pos:pos_end]

        if vid_id not in channel_live[channel_name]:
            channel_live[channel_name].append(vid_id)


def youtube_get_qty_watching(video_id, channel_name):
    # {'items': [{'liveStreamingDetails': {'actualStartTime': '2022-07-12T12:56:52Z',                                          'scheduledStartTime':'2022-07-12T13:00:00Z', 'concurrentViewers': '399'}}]
    # {'items': [{'liveStreamingDetails': {'actualStartTime': '2022-07-11T20:56:18Z', 'actualEndTime': '2022-07-11T23:03:34Z', 'scheduledStartTime':'2022-07-11T21:00:00Z'}}]
    request = youtube.videos().list(id=video_id, part='snippet,liveStreamingDetails')

    for _ in range(2):  # 2 tries
        try:
            response = request.execute()
            break
        except Exception as e:
            display_exception_treated(e, 'Lendo qty do Youtube')
            youtube_api_connect()
    else:
        return -1, 'ERROR'

    if len(response['items']) == 0:
        # Video unavailable
        if response['pageInfo']['totalResults'] == 0 and response['pageInfo']['resultsPerPage'] == 0:
            vid_title, dt_ini, dt_end, qty = '', -2, -2, -1
        else:
            print('\n\n ***  ITEM VAZIO *** \n\n')
            return -1, 'ERROR'
    else:
        item = response['items'][0]  # ['liveStreamingDetails']
        vid_title = str(item['snippet']['title']).replace(';', ',')
        dt_ini  = item['liveStreamingDetails'].get('actualStartTime',   -1)  # 'scheduledStartTime'
        dt_end  = item['liveStreamingDetails'].get('actualEndTime',     -1)
        qty     = item['liveStreamingDetails'].get('concurrentViewers', -1)
        qty     = int(qty)

    # columns  video_id  channel       title      dt_ini  dt_end
    new_row = [video_id, channel_name, vid_title, dt_ini, dt_end]

    filter = (df_vid['video_id'] == video_id)

    # Cadastra novo vídeo (ainda não estava cadastrado)
    if filter.sum() == 0:
        df_vid.loc[df_vid.shape[0]] = new_row
        with open(file_name_vid, 'a', newline='\n', encoding='utf-8') as f:  # append on file
            write = csv.writer(f, delimiter=';')
            write.writerow(new_row)
        print(f'\nVídeo Iniciado   : {new_row}')

    # Vídeo finalizado
    if qty == -1 and dt_ini != -1 and dt_end != -1:
        channel_live[channel_name].remove(video_id)
        if  dt_ini == -2:  # video unavailable
            new_row[2] = df_vid.loc[filter]['title'].iloc[0]
        df_vid.loc[filter] = new_row
        df_vid.to_csv(file_name_vid, index=False, sep=';')
        print(f'\nVídeo Encerrado : {new_row}')
        gen_graph_video(video_id)

    file_backup('00:15', '01:00', file_name_vid, 'G:/My Drive/Projects/DATA_BACKUP/JP/')

    file_copy_after_time(file_name_vid, 'C:/Power BI/powerbi_jp/youtube_vid.csv', 600)

    return qty, vid_title  # devolver hora inicial e final


def get_live_videos():
    # check every 3 minutes for new videos
    if  time.time() < gvar.get('get_live_last_time', 0) + 3*60 - 1:
        return

    for channel_name in channel_names:
        youtube_get_live_videos_url(channel_name)

    gvar['get_live_last_time'] = time.time()



#############################################################
#                   MANIPULATE DATA                         #
#############################################################

def remove_seconds(dtime):
    return dtime.replace(second=0, microsecond=0, nanosecond=0)

def data_by_group(dt_ini, dt_end, by='group'):
    # Para pegar todos dados do minuto inicial e final (inclusive)
    dt_ini = dt_ini.replace(second=0, microsecond=0)
    dt_end = dt_end.replace(second=59)

    # df <- filtra período com apenas 1 dado por minuto
    filt1 = df_cnt['dtime'] >= dt_ini
    filt2 = df_cnt['dtime'] <= dt_end
    df = df_cnt[filt1 & filt2].copy()
    df['dtime'] = df['dtime'].apply(remove_seconds)
    df = df.drop_duplicates(['video_id', 'dtime'], keep='last')

    vid_info = {'id':[], 'group':[], 'channel':[], 'title':[], 'mean':[], 'max':[], 'timemax':[],}
    # print(f'{"Grupo":6}  {"Canal":15}   {"Título":54}  {" Média":6}  {"Máximo":6}  {"Minuto"}')

    # df2 = completa minutos faltantes de cada vídeos e adiciona channel/group
    df2 = pd.DataFrame()
    for video_id in df['video_id'].unique():
        channel = df_vid[df_vid['video_id'] == video_id]['channel'].iloc[0]
        title   = df_vid[df_vid['video_id'] == video_id]['title'  ].iloc[0]
        group   = df_chn[df_chn['channel' ] == channel ]['group'  ].iloc[0]

        df_vid_id = df[df['video_id'] == video_id].copy()

        df_vid_id['group'  ] = group
        df_vid_id['channel'] = channel

        if by == 'video_id':
            v_mean = round(df_vid_id.qty_viewers.mean())
            v_max  = round(df_vid_id.qty_viewers.max())
            time_max_idx = df_vid_id['qty_viewers'].idxmax()
            v_timemax = df_vid_id.loc[time_max_idx, 'dtime'].strftime("%H:%M")
            vid_info['id'     ].append(video_id)
            vid_info['group'  ].append(group)
            vid_info['channel'].append(channel)
            vid_info['title'  ].append(title)
            vid_info['mean'   ].append(v_mean)
            vid_info['max'    ].append(v_max)
            vid_info['timemax'].append(v_timemax)
            # print(f'{group:6}  {channel:15}   {title:54}  {v_mean:6.0f}  {v_max:6.0f}  {" 09:15":6}')

        time_ini = df_vid_id['dtime'].iloc[ 0]
        time_end = df_vid_id['dtime'].iloc[-1]
        idx = pd.date_range(time_ini, time_end, freq='1min')

        df_vid_id = df_vid_id.set_index('dtime').reindex(idx, method='nearest')
        # resample (ver o que esse comando faz)

        df2 = pd.concat([df2, df_vid_id])

    if by == 'group':
        # df2 = Soma minutos por grupo (vídeos diferentes no mesmo horário)
        df2 = df2[['group', 'qty_viewers']].reset_index().rename(columns={'index':'dtime'}).groupby(['dtime', 'group']).sum().reset_index()

        # df = Colunas com qty de cada cana por minuto
        df = pd.DataFrame()
        idx = pd.date_range(dt_ini, dt_end, freq='1min')
        for group in GROUPS:  # df_chn['group'].unique():
            filt1 = df2['group'] == group
            df[group] = df2[filt1].set_index('dtime').reindex(idx, fill_value=0)['qty_viewers']
    else:
        gvar['vid_info'] = pd.DataFrame(vid_info)

        df2 = df2[['video_id', 'qty_viewers']].reset_index().rename(columns={'index':'dtime'})

        # df = Colunas com qty de cada cana por minuto
        df = pd.DataFrame()
        idx = pd.date_range(dt_ini, dt_end, freq='1min')
        # for group in GROUPS:
        for video_id in df2['video_id'].unique():
            filt1 = df2['video_id'] == video_id
            df[video_id] = df2[filt1].set_index('dtime').reindex(idx, fill_value=0)['qty_viewers']

    return df.reset_index().rename(columns={'index':'dtime'})


def data_by_channel(channel, dt_ini, dt_end):
    pass

def data_by_program(program_name, date):
    pass



#############################################################
#                       GRAPHICS                            #
#############################################################

def set_info_texts(annot, x, y, color, txt, xanchor='left'):
    fs = 24
    dy = fs + 6

    for i in range(len(txt)):
        txt_ok = txt[i]
        color_ok = color
        y_ok = y + i*dy
        if i == 0:
            txt_ok = f'<b>{txt[i]}<b>'
            color_ok = '#0099CC'
            y_ok -= 10
        add_annot(annot, x, y_ok, txt_ok, color_ok, fs, xanchor)

def graph_infos(fig, annot, df, groups):
    x = 150
    y = 240

    set_info_texts(annot, x, y, '#CCFFFF', ['ONLINE', 'Last min', 'Média', 'Máximo', 'Best min'])

    pos = 0
    for group in groups:
        xc = x + 220 + 150 * pos

        img_file = f"images/jp_ibope_icons/{icon_names[pos].upper().replace(' ', '_')}.png"
        add_image(fig, img_file, xc, y-32, 64, 64, layer=None)

        val_last = df[group].iloc[-1]
        val_mean = int(df[group].mean().round())
        val_max  = df[group].max()

        time_max_idx = df[group].idxmax()
        time_max = df.loc[time_max_idx, 'dtime'].strftime("%H:%M")

        set_info_texts(annot, xc, y, GCOLORS[pos], ['', fnum(val_last), fnum(val_mean), fnum(val_max), time_max], 'center')
        pos += 1


def gen_graph_comp_channels(dt_ini, dt_end, filename, realtime=False, title=''):
    df = data_by_group(dt_ini, dt_end)

    FONT = 'Helvetica Neue LT Black'
    fig = gen_graph(1200, 900, (100, 60, 400, 100, 16), df, 'dtime', GROUPS,
            FONT, fontcolor='#CCFFFF', bgcolor='#001324',
            gridcolor='#336666', tick_fs=24,
            line_color=GCOLORS)

    annot = []
    graph_infos(fig, annot, df, GROUPS)

    dow = dt_ini.weekday()

    subtit = f"{dt_ini.strftime('%d/%m/%Y')} ({dow_name_pt[dow][:3]})  -  {dt_ini.strftime('%H:%M')} as {dt_end.strftime('%H:%M')}\n"

    color = '#CCFFFF'
    add_annot(annot, 120,  96, title,  color, 48)
    add_annot(annot, 120, 145, subtit, color, 24)

    if realtime:
        add_annot(annot, 1200-120, 145, '( YOUTUBE  Real Time )', color, 24, xanchor='right')
        df.to_csv(file_name_rti, index=False, sep=';')

    fig.update_layout(annotations=annot)

    delete_file(filename)  # Apaga arquivo antigo p/ ficar com data ok
    pio.write_image(fig, filename)


def gen_graph_comp(dt_ini, dt_end, video_id, vchannel, vtitle, filename):
    df = data_by_group(dt_ini, dt_end, by='video_id')

    # cor de cada vídeo (linha e textos)
    columns_to_show = []
    line_color = []  # {}
    for gnum, group in enumerate(GROUPS):
        dfvi = gvar['vid_info'][gvar['vid_info']['group'] == group]

        color = GCOLORS[gnum]

        for i in range(dfvi.shape[0]):
            vid = dfvi['id'].iloc[i]
            columns_to_show.append(vid)
            # line_color[vid] = color
            line_color.append(color)

            if i < 3:  # Não altera cor a partir da 4a linha
                rgba = [int(round(c*0.82)) for c in webcolor_to_rgba(color)]
                color = rgba_to_webcolor(rgba)[:7]


    imgw, imgh = 1200, 900+800
    mtop = 150

    FONT = 'Helvetica Neue LT Black'
    # fig = gen_graph(1200, 900, (100, 60, 400, 100, 16),
    fig = gen_graph(imgw, imgh, (100, 60, mtop, 400+800, 16),
            df, 'dtime', columns_to_show,
            FONT, fontcolor='#CCFFFF', bgcolor='#001324',
            gridcolor='#336666', tick_fs=24,
            line_color=line_color)

    annot = []
    # graph_infos(fig, annot, df, GROUPS)


    STEP_Y_VIDEO = 30
    STEP_Y_GROUP = 16

    x, xv = 130, 940
    y = mtop  +  400  +  100  +  STEP_Y_VIDEO


    fs = 24

    color = '#CCFFFF'
    y_ok = y - STEP_Y_VIDEO - 10
    add_annot(annot, x  +   0, y_ok, 'Canal',    color, fs)
    add_annot(annot, x  + 220, y_ok, 'Título',   color, fs)
    add_annot(annot, xv +   0, y_ok, 'Média',    color, fs, xanchor='right')
    add_annot(annot, xv + 100, y_ok, 'Máximo' ,  color, fs, xanchor='right')
    add_annot(annot, xv + 200, y_ok, 'Best Min', color, fs, xanchor='right')

    pos, gpos, vpos = 0, 0, 0
    for gnum, group in enumerate(GROUPS):
        dfvi = gvar['vid_info'][gvar['vid_info']['group'] == group]
        if dfvi.shape[0] == 0:
            continue

        xc = x - 50
        y_ok = y + gpos*STEP_Y_GROUP + vpos*STEP_Y_VIDEO
        img_file = f"images/jp_ibope_icons/{icon_names[gnum].upper().replace(' ', '_')}.png"
        add_image(fig, img_file, xc, y_ok+16, 64, 64, layer=None)

        for pos2 in range(dfvi.shape[0]):
            _, _, channel, title, vmean, vmax, timemax = dfvi.iloc[pos2]
            # vid_info = {'group':[], 'channel':[], 'title':[], 'mean':[], 'max':[], 'timemax':[],}
            y_ok = y + gpos*STEP_Y_GROUP + vpos*STEP_Y_VIDEO
            color = line_color[pos]
            add_annot(annot, x  +   0, y_ok, channel_show[channel], color, fs)
            add_annot(annot, x  + 220, y_ok, title[:45],   color, fs)
            add_annot(annot, xv +   0, y_ok, fnum(vmean),  color, fs, xanchor='right')
            add_annot(annot, xv + 100, y_ok, fnum(vmax) ,  color, fs, xanchor='right')
            add_annot(annot, xv + 200, y_ok, timemax    ,  color, fs, xanchor='right')
            pos  += 1
            vpos += 1

        gpos += 1
        if dfvi.shape[0] == 1:
            vpos += 1


    dow = dt_ini.weekday()

    title = f'{vtitle}'
    subtit = f"Canal Youtube: {channel_show[vchannel]}  -  {dt_ini.strftime('%d/%m/%Y')} ({dow_name_pt[dow][:3]})  -  {dt_ini.strftime('%H:%M')} as {dt_end.strftime('%H:%M')}\n"

    color = '#CCFFFF'
    add_annot(annot, 48, 48, title,  color, 48)
    add_annot(annot, 48, 96, subtit, color, 24)

    fig.update_layout(annotations=annot)

    pio.write_image(fig, file_name_img_tmp)  # salva arquivo temporário

    y_ok = y + gpos*STEP_Y_GROUP + vpos*STEP_Y_VIDEO

    im = Image.open(file_name_img_tmp)
    im_cropped = im.crop((0, 0, imgw, y_ok))  # corta parte não usada

    delete_file(filename)  # Apaga arquivo antigo p/ ficar com data ok
    im_cropped.save(filename)

    delete_file(file_name_img_tmp)  # Apaga arquivo temporário


def send_telegram_doc(doc):
    if not OP_TELEGRAM  or  not gvar.get('send_by_telegram', True):
        return

    if exists(doc):
        f = open(doc, 'rb')
        for i in range(len(telegram_chat_id)):
            if not telegram_chat_id[i]:
                continue
            f.seek(0)
            telegram_bot.send_document(telegram_chat_id[i], f)
        f.close()


def gen_graph_video(video_id):  # 'XDLaBADcPl0'
    filter = (df_vid['video_id'] == video_id)
    if filter.sum() == 0:
        return -1   # Não existe vídeo

    row = df_vid.loc[filter]
    video_id, channel, title, dt_ini, dt_end = row.iloc[0]

    if channel_group[channel] != 'JP'  or  dt_ini in ['-1', '-2']  or  dt_end in ['-1', '-2']:
        return

    timezone = -3
    dt_ini = pd.to_datetime(dt_ini).replace(tzinfo=None) + dt.timedelta(hours=timezone)
    dt_end = pd.to_datetime(dt_end).replace(tzinfo=None) + dt.timedelta(hours=timezone)

    filename_video = f'graphics/{channel}__{slugify(title)}__{dt_ini.strftime("%d-%m")}__{dt_ini.strftime("%H-%M")}_as_{dt_end.strftime("%H-%M")}.png'
    gen_graph_comp(dt_ini, dt_end, video_id, channel, title, filename_video)

    if gvar.get('SEND_VIDEO_GRAPH'):
        send_telegram_doc(filename_video)


def check_period():
    periods = {
        'PERIODO DA TARDE':     18,  # hora final
        'PERIODO DA MANHÃ':     12,
        'PERIODO DA MADRUGADA':  6,
        'PERIODO DA NOITE':      0  }

    dt_end = dt_now()
    hour_end = dt_end.hour

    for period in periods:
        if hour_end >= periods[period]:
            break

    file_per_last = f'data/jp/yt_last_period.txt'
    with open(file_per_last, 'r', encoding='utf-8') as f:
        per_last_sent = f.readline().strip()

    if period != per_last_sent:
        dt_end = dt_end.replace(hour=periods[period], minute=0)
        dt_ini = dt_end - dt.timedelta(hours=6)
        file_name_period = f"graphics/YT_{dt_ini.strftime('%d-%m-%Y')}_{slugify(period)}.png"
        gen_graph_comp_channels(dt_ini, dt_end, file_name_period, title=f'YOUTUBE - {period}')
        send_telegram_doc(file_name_period)
        with open(file_per_last, 'w', encoding='utf-8') as f:
            f.write(period)


#############################################################
#                   RASCUNHO / TESTES                       #
#############################################################

def teste():
    channels = ['jovempannews',
                'panicojovempan',
                'saudejp',
                'oanjoinvestidor',
                'jovempanentretenimento',
                'maisumpdc',
                'JovemPan3em1',
                'ospingosnosis',
                'jovempanesportes',
                'morningshow',]

    videos = list( df_vid[(df_vid['channel'].isin(channels)) &  (df_vid['dt_end'] != '-1')]['video_id'].tail(10) )
    for video_id in videos:
        print(video_id)
        gen_graph_video(video_id)



#############################################################
#                       MAIN LOOP                           #
#############################################################

def main_program():
    # gen_graph_video('XDLaBADcPl0')
    # teste()
    # sys.exit(0)

    # dt_end = dt_now().replace(second=0, microsecond=0)
    # gen_graph_comp_channels(dt_end - dt.timedelta(hours=4), dt_end, 'graphics/YT_Groups_Last_Min.png')
    # sys.exit(0)


    # Tenta reabrir se passou mais de 120s do último instante "live"
    if  (time.time() > gvar.get('working_last_time', 0) + 120 or
         time.time() > gvar.get('changed_key_time', 0 ) + 30*60):  # change key every 30 min
        youtube_api_connect()
        gvar['changed_key_time'] = time.time()


    get_live_videos()


    df_upd = pd.DataFrame({'GRUPO':[], 'CANAL':[], 'PROGRAMA':[], 'ASSISTINDO':[]})

    qty_live = 0
    for channel_name in channel_names:
        qty_live += len(channel_live[channel_name])
        for video_id in channel_live[channel_name]:
            qty, vid_title = youtube_get_qty_watching(video_id, channel_name)

            if qty != -1:
                # append data
                dtime = dt_now().replace(microsecond=0)  # second=0
                new_row = [video_id, dtime, qty]
                df_cnt.loc[df_cnt.shape[0]] = new_row

                with open(file_name_cnt, 'a', newline='\n', encoding='utf-8') as f:
                    write = csv.writer(f, delimiter=';')
                    write.writerow(new_row)

                file_backup('00:15', '01:00', file_name_cnt, 'G:/My Drive/Projects/DATA_BACKUP/JP/')

                file_copy_after_time(file_name_cnt, 'C:/Power BI/powerbi_jp/youtube_cnt.csv', 600)

                df_upd.loc[df_upd.shape[0]] = [channel_group[channel_name], channel_show[channel_name], vid_title, qty]

            else:
                # finished vídeo or error
                pass


    #######################################################################
    #   Arquivos com qtde. viewers de todos programas online no momento
    #######################################################################
    df_upd.to_csv(file_name_upd, index=False, sep=';')

    if gvar.get('SITE_CSV_FILE'):
        with open(file_name_upd, 'rb') as f:
            file_dict = {"file":f}
            try:
                r = requests.post("https://plassion.com/projects/jp-youtube/post.php", files=file_dict)
                print(f'\r{dt_now().strftime("%H:%M:%S")} ({qty_live}) ({df_upd.shape[0]}) -> {r.text} ', end='')
            except Exception as e:
                display_exception_treated(e, 'Enviando CSV')
                youtube_api_connect()


    ###################################################################
    #                   Gráfico das últimas 4h
    ###################################################################
    dt_end = dt_now().replace(second=0, microsecond=0)
    file_name_last_min = 'graphics/YT_Groups_Last_Min.png'
    gen_graph_comp_channels(dt_end - dt.timedelta(hours=4), dt_end, file_name_last_min, realtime=True)

    if gvar.get('SITE_IMG_FILE'):
        with open(file_name_last_min, 'rb') as f:
            file_dict = {"file":f}
            try:
                r = requests.post("https://plassion.com/projects/jp-youtube/post_new.php", files=file_dict)
                print(f'\r{dt_now().strftime("%H:%M:%S")} (image.png) -> {r.text} ', end='')
            except Exception as e:
                display_exception_treated(e, 'Enviando PNG')
                youtube_api_connect()


    ###################################################################
    #                   Gráfico por período
    ###################################################################
    check_period()


    # Backup a cada 15 minutos por exemplo e no except
    # df_cnt.to_csv(df_cnt, index=False, sep=';')


    # Waits until hh:mm:10
    time_to_sleep = 70 - dt_now().second
    time.sleep(time_to_sleep)
    # time.sleep(5)


    gvar['working_last_time'] = time.time()

