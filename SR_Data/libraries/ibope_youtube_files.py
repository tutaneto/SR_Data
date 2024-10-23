from .util_generic import *

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


data_path = 'data/jp/'

ibope_min_file     = data_path + 'Ibope_minutos.csv'                # Ibope
ibope_prg_file     = data_path + 'program.csv'

youtube_chn_file   = data_path + 'youtube_chn.csv'                  # Youtube Live
youtube_vid_file   = data_path + 'youtube_vid.csv'
youtube_cnt_file   = data_path + 'youtube_cnt.csv'

yt_on_dem_chn_file = data_path + 'yt_on_dem_chn.csv'                # Youtube on Demand
yt_on_dem_vid_file = data_path + 'yt_on_dem_vid.csv'
yt_on_dem_cnt_file = data_path + 'yt_on_dem_cnt.csv'
yt_on_dem_rep_vid_file = data_path + 'yt_on_dem_rep_vid.csv'
yt_on_dem_rep_chn_file = data_path + 'yt_on_dem_rep_chn.csv'


DEVELOPER_KEY = 'AIzaSyB7fzuAgwOxxJCSgpUhC-q4qPLtMfI88PE'  # Yt-On_Dem
# youtube = build('youtube', 'v3', developerKey = DEVELOPER_KEY)



#######################################################################
#   Parte feita pelo Joao Aguilera para pegar dados de $ do Youtube   #
#######################################################################

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtubepartner',
    'https://www.googleapis.com/auth/yt-analytics-monetary.readonly',
    'https://www.googleapis.com/auth/yt-analytics.readonly'
]

CREDENTIALS_FILE="client_secret_308227256651-8cb7d4572qbd53g8t8g84gego3q6gchi.apps.googleusercontent.com.json"

def get_creds():
    """Create the token.json file if it doesn't exist and generate credentials.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

contentOwner = 'p7kSgcTADGitVYFZ90Dkmw'
metrics_list = ["views", "redViews", "comments", "likes", "dislikes", "videosAddedToPlaylists", "videosRemovedFromPlaylists", "shares",
    "estimatedMinutesWatched", "estimatedRedMinutesWatched", "averageViewDuration", "averageViewPercentage", "annotationClickThroughRate",
    "annotationCloseRate", "annotationImpressions", "annotationClickableImpressions", "annotationClosableImpressions", "annotationClicks", "annotationCloses",
    "cardClickRate", "cardTeaserClickRate", "cardImpressions", "cardTeaserImpressions", "cardClicks", "cardTeaserClicks", "subscribersGained", "subscribersLost",
    "estimatedRevenue", "estimatedAdRevenue", "grossRevenue", "estimatedRedPartnerRevenue", "monetizedPlaybacks", "playbackBasedCpm", "adImpressions", "cpm"]

def get_content_owner_video_report(youtubeAnalytics, video_id, start_date, end_date):
    request = youtubeAnalytics.reports().query(
        dimensions='video',
        metrics=f"{','.join(metrics_list)}",
        filters=f"video=={video_id}",
        ids=f'contentOwner=={contentOwner}',
        startDate=start_date, endDate=end_date
    )
    return request.execute()

def get_content_owner_channel_report(youtubeAnalytics, channel_id, start_date, end_date):
    request = youtubeAnalytics.reports().query(
        dimensions='channel',
        metrics=f"{','.join(metrics_list)}",
        filters=f"channel=={channel_id}",
        ids=f'contentOwner=={contentOwner}',
        startDate=start_date, endDate=end_date
    )
    return request.execute()


# creds = get_creds()

# youtubeAnalytics = build("youtubeAnalytics", "v2", credentials=creds)
# youtube = build("youtube", "v3", credentials=creds)
# youtubereporting = build("youtubereporting", "v1", credentials=creds)

#######################################################################



def load_dataframes():
    global channel_names #, n_channels
    global channel_group, channel_ids, channel_show

    # Brazilian R$ format
    locale.setlocale(locale.LC_ALL, 'pt_BR')

    global df_channels
    df_channels = read_csv_strip(youtube_chn_file)

    channel_names = []
    channel_ids, channel_group, channel_show = {}, {}, {}

    for _, row in df_channels.iterrows():
        channel = row['channel']
        channel_names.append(channel)
        channel_ids  [channel] = row['id']      # look for 'externalid' at page source
        channel_group[channel] = row['group']
        channel_show [channel] = row['name']

    global df_ib_min, df_ib_prg
    df_ib_min = pd.read_csv(ibope_min_file.replace('.csv', gvar['complete_file'] if 'complete_file' in gvar else '' + '.csv'), sep=';', parse_dates=['MIN'])
    df_ib_prg = pd.read_csv(ibope_prg_file, sep=';')

    global df_live_vid, df_live_cnt
    df_live_vid = pd.read_csv(youtube_vid_file, sep=';')  # , parse_dates=['dt_ini', 'dt_end'])
    df_live_cnt = pd.read_csv(youtube_cnt_file.replace('.csv', gvar['complete_file'] if 'complete_file' in gvar else '' + '.csv'), sep=';', parse_dates=['dtime'])

    global df_chn, df_vid, df_cnt, df_rep_vid, df_rep_chn
    df_chn = pd.read_csv(yt_on_dem_chn_file, sep=';', parse_dates=['dtime'])
    df_vid = pd.read_csv(yt_on_dem_vid_file, sep=';').sort_values('published_at')  # parse_dates=['published_at']
    df_cnt = pd.read_csv(yt_on_dem_cnt_file, sep=';', parse_dates=['dtime'])
    df_rep_vid = pd.read_csv(yt_on_dem_rep_vid_file, sep=';', parse_dates=['dtime'])
    df_rep_chn = pd.read_csv(yt_on_dem_rep_chn_file, sep=';', parse_dates=['dtime'])

load_dataframes()
