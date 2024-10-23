
TEMPLATE = 'INVEST_NEWS_BLACK'

telegram_groups = []
whatsapp_groups = [[r'Editorial InvestNews', r'MEO BRASIL', r'Mercado & Opinião sala 01', r'Mercado & Opinião sala 02', r'Mercado&Opinião sala 03', r'Empresários & Política', r'Inteligência  Financeira']]


#######################################
#           FONTES
#######################################
FONT = 'Rational Display'






#######################################
#           CONFIGS
#######################################
SHOW_PERC = False


#######################################
#           COLORS
#######################################
T_COLOR_1 = 'white'
T_COLOR_2 = '#9C1A7F'  # Magent (graph)
T_COLOR_3 = '#2099C9'  # Cyan (graph)
T_COLOR_4 = '#53929A'  # Dark Cyan Gray
T_COLOR_5 = '#75CCD3'  # Light Cyan
T_COLOR_6 = '#20A0B0'  # Cyan                       ***
T_COLOR_7 = '#393939'

BG_COLOR = 'black'

BLOCK_BG_COLOR_MID_UP = 'gradient_cyan_up.png'
BLOCK_BG_COLOR_MID_DN = 'gradient_purple_down.png'
BLOCK_BG_COLOR_END_UP = BLOCK_BG_COLOR_MID_UP
BLOCK_BG_COLOR_END_DN = BLOCK_BG_COLOR_MID_DN

BLOCK_V3_COLOR = T_COLOR_1 + '.png'

BLOCK_COLORS = [BLOCK_BG_COLOR_MID_DN,                            # T_COLOR_2,
        BLOCK_BG_COLOR_MID_DN, BLOCK_BG_COLOR_MID_UP, T_COLOR_1]  # T_COLOR_2, T_COLOR_3,
LEGEND_COLORS = [T_COLOR_2, T_COLOR_2, T_COLOR_3, T_COLOR_1]

XAXIS_TEXT_COLOR = T_COLOR_1
YAXIS_TEXT_COLOR = T_COLOR_1
YAXIS_LINE_COLOR = T_COLOR_1
YAXIS_LINE_OPACITY = 0.20

TITLE_COLOR  = T_COLOR_1
SUBTIT_COLOR = T_COLOR_1
DFONT_COLOR  = T_COLOR_1

LOGO_BAR_COLOR = '#393939'


#######################################
#       POSITIONS AND SIZES
#######################################
TITLE_X =  70
TITLE_Y = 105
TITLE_DX = 104

SUBTIT_X = TITLE_X
SUBTIT_Y = TITLE_Y + 92
SUBTIT_CAPS = False

TITLE_FONT_SIZE  = 54
SUBTIT_FONT_SIZE = 29
DFONT_FONT_SIZE  = 24

# MAIN_LOGO_X = TITLE_X  # 16
# MAIN_LOGO_Y = TITLE_Y-40
# MAIN_LOGO_H = 110
# MAIN_LOGO_W = MAIN_LOGO_H / 349 * 300

BLOCK_X = 100
BLOCK_Y = 900
BLOCK_W = 45
BLOCK_H = 500
BLOCK_DX = 70
BLOCK_DX_FACTOR = 1

DFONT_X = 10
DFONT_Y = 1058

BAR_VAL_FONT_SIZE  = 22
BAR_DATE_FONT_SIZE = 16
YAXIS_FONT_SIZE = BAR_VAL_FONT_SIZE


#######################################
#           IMAGES
#######################################
ARROW_UP_IMG = 'images/seta_alta_ok.png'
ARROW_DN_IMG = 'images/seta_baixa_ok.png'

MAIN_LOGO_PNG = None


#######################################
#           WATERMARK
#######################################
WATERMARK_IMG = 'images/invest_news/INS_white.png'
WATERMARK_ALPHA = 0.07
WATERMARK_LAYER = 'above'
WM_X, WM_Y, WM_W, WM_H = 540, 660, 1050, 150
WM_X_GT, WM_Y_GT = 540, 660


#######################################
#           RANKING
#######################################
RANK_X = 40  # TITLE_X
RANK_Y = 800

RANK_BAR_W = 74
RANK_BAR_H = 300
RANK_BAR_DX = 102

BLOCK_VERT_DN_IMG = 'images/inv_news_blue.png'
BLOCK_VERT_UP_IMG = 'images/inv_news_blue.png'
BLOCK_VERT_W = 1
BLOCK_VERT_H = 1

RANK_LINE_COLOR = T_COLOR_1

FLAG_CIRCLE_COLOR_UP = 'white' # '#2099C9'
FLAG_CIRCLE_COLOR_DN = 'white' # '#FF80FF'


#######################################
#           FOCUS 1
#######################################

FOCUS_BLK_X = TITLE_X + 200 # 400
FOCUS_BLK_Y = 190
FOCUS_BLK_W = 380
FOCUS_BLK_H = 240
FOCUS_BLK_DX = FOCUS_BLK_W + 8
FOCUS_BLK_DY = FOCUS_BLK_H + 8

FOCUS_BLK_IN_DX =  0
FOCUS_BLK_IN_DY = 80
FOCUS_BLK_IN_H = (FOCUS_BLK_H - FOCUS_BLK_IN_DY)

FOCUS_BLK_COLOR = T_COLOR_6
FOCUS_BLK_LINE_C = T_COLOR_6
FOCUS_BLK_LINE_W = 1

# FOCUS_TIT_DX = []
FOCUS_TIT_DX = FOCUS_BLK_W / 2
FOCUS_TIT_DY = FOCUS_BLK_IN_DY / 2
FOCUS_TIT_COLOR = TITLE_COLOR
FOCUS_TIT_FONT_SIZE = 40

FOCUS_TYPE_COLOR = T_COLOR_6
FOCUS_TYPE_FONT_SIZE = 20

FOCUS_FOOT_COLOR = T_COLOR_6
FOCUS_FOOT_FONT_SIZE = 20

FOCUS_DATA_X  = [FOCUS_BLK_W * 0.25, FOCUS_BLK_W * 0.75]
FOCUS_DATA_Y1 = FOCUS_BLK_IN_H * 0.3
FOCUS_DATA_Y2 = FOCUS_BLK_IN_H * 0.7
FOCUS_DATA_COLOR = T_COLOR_7
FOCUS_DATA_FONT_SIZE = [36, 30, 20]

FOCUS_IMAGES = 'images/focus/jp_merc_fin/'

FOCUS_ICON_H = 76
FOCUS_ICON_W = FOCUS_ICON_H / 159 * 176

FOCUS_ARROW_H = 48
FOCUS_ARROW_W = FOCUS_ARROW_H / 159 * 176


#######################################
#           FOCUS 2
#######################################

FOCUS2_HEADER_H = 60
FOCUS2_HEADER_BLK_COLOR = T_COLOR_5
FOCUS2_HEADER_TXT_COLOR = T_COLOR_7
FOCUS2_HEADER_BLK_FS = 44
FOCUS2_HEADER_TXT_FS = 16

FOCUS2_BLK_X = TITLE_X + 0
FOCUS2_BLK_Y, FOCUS2_BLK_Y2 = 250, 250
FOCUS2_BLK_W, FOCUS2_BLK_W2 = 1480, 1090
FOCUS2_BLK_H = 80
# FOCUS2_BLK_DX = FOCUS2_BLK_W + 8
FOCUS2_BLK_DY = FOCUS2_BLK_H + 8

FOCUS2_BLK_IN_DX = 280
FOCUS2_BLK_IN_DY = 0
FOCUS2_BLK_IN_W = (FOCUS2_BLK_W - FOCUS2_BLK_IN_DX)

FOCUS2_VAR_DISTANCE = 100  # 12 vars x 100 == 1200px

FOCUS2_BLK_COLOR = T_COLOR_6
FOCUS2_BLK_LINE_C = T_COLOR_6
FOCUS2_BLK_LINE_W = 1

# FOCUS_TIT_DX = []
FOCUS2_TIT_DX = FOCUS2_BLK_IN_DX / 2
FOCUS2_TIT_DY = FOCUS2_BLK_H / 2
FOCUS2_TIT_COLOR = TITLE_COLOR
FOCUS2_TIT_FONT_SIZE = 40

FOCUS2_TYPE_COLOR = T_COLOR_6
FOCUS2_TYPE_FONT_SIZE = 20

# FOCUS_FOOT_COLOR = T_COLOR_6
# FOCUS_FOOT_FONT_SIZE = 20

FOCUS2_DATA_X  = [250, 650, 850, 1050]  # [250, 610, 800, 980]
# FOCUS_DATA_Y1 = FOCUS_BLK_IN_H * 0.3
# FOCUS_DATA_Y2 = FOCUS_BLK_IN_H * 0.7
FOCUS2_DATA_COLOR = T_COLOR_7
FOCUS2_DATA_FONT_SIZE = 24

FOCUS2_IMAGES = 'images/focus/jp_merc_fin/'

# FOCUS_ICON_H = 76
# FOCUS_ICON_W = FOCUS_ICON_H / 159 * 176

FOCUS2_ARROW_H = 44
FOCUS2_ARROW_W = FOCUS_ARROW_H / 159 * 176


#######################################
#           001_ (graphtime)
#######################################

# 001
GT_IMAGE_W = 1080
GT_IMAGE_H = 1080
GT_001_MARGINS = 80, 88, 200, 140, 4

GT_PRES_PRICE_FC = '#E7248A'
GT_PRES_PRICE_FS = 46         # FONT_SIZE

GT_TIME_FS = 24
GT_DFONT_FS = 18

GT_TICKS_FONT_COLOR = '#00FFFF'  # T_COLOR_3
GT_TICKS_FONT_SIZE = 24

GT_BLOCK_INFO_COLOR = T_COLOR_2
GT_BLOCK_FONT_COLOR = 'white'
GT_BLOCK_LBL_FS = 20
GT_BLOCK_NUM_FS = 22
GT_BLOCK_DX = 8

GT_COLOR_NEG = '#FF6666'
GT_COLOR_POS = '#00FFFF'
GT_TRACE_WIDTH = 4

GT_INFO_52M = False

# graphtime
GT_MARGINS_LRTBPAD = 150, 100, 300, 160, 10
GT_LEGEND_X = 0.1
GT_LEGEND_Y = 0.9
GT_LEGEND_FS = 22
GT_LEGEND_FC = TITLE_COLOR
GT_XAXIS_FS = 25
GT_YAXIS_FS = BAR_VAL_FONT_SIZE
GT_AXIS_FC = T_COLOR_5


#######################################
#           COMP (graphcomp)
#######################################

CP_MARGINS_LRTBPAD = 150, 100, 300, 160, 10
CP_TRACE_WIDTH = 3
CP_TRACE_COLOR = '#00FFFF'
CP_LINES_COLOR = '#00FFFF'
CP_LINE0_COLOR = '#00FFFF'

CP_XAXIS_FS = BAR_VAL_FONT_SIZE
CP_YAXIS_FS = BAR_VAL_FONT_SIZE


#######################################
#               TABLES
#######################################

TAB_BRECT_COLOR = '#770077.png'
TAB_BCIRC_COLOR = '#550055.png'
TAB_BCIRCW_COLOR = 'white.png'

TAB_B1X, TAB_B1Y = 135, 486
TAB_B2X, TAB_B2Y = 630, TAB_B1Y
TAB_B3X, TAB_B3Y = TAB_B1X, 680
TAB_B4X, TAB_B4Y = TAB_B2X, 734

TAB_BTIT_DX, TAB_BTIT_DY = 44, 44

TAB_BDX = 360  # block distance between left and right text
TAB_BDY =  52  # block distance to next one
TAB_BHEI = 48  # bloch height

TAB_TITLE_X = 220
TAB_TITLE_Y = 130

TAB_DFONT_X = DFONT_X
TAB_DFONT_Y = DFONT_Y

TAB_ASSET_FC = 'white'

TAB_TITLE_FS = TITLE_FONT_SIZE
TAB_DFONT_FS = DFONT_FONT_SIZE

TAB_BLKTIT_FS = 20
TAB_ASSET_FS  = 30
TAB_PERC_FS   = 24

TAB_PERC_DX = 24
TAB_ARROW_DX = 140

TAB_ICO_IMG = 'images/ico_bolsas_mundo_ok.png'
TAB_ICO_X, TAB_ICO_Y, TAB_ICO_W, TAB_ICO_H = TAB_TITLE_X-45, TAB_TITLE_Y-20, 42, 42

SETA_ALTA  = 'images/seta_alta_ok.png'
SETA_BAIXA = 'images/seta_baixa_ok.png'
