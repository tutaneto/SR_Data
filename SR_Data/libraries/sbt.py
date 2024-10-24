
TEMPLATE = 'SBT'

telegram_groups = [[]]
whatsapp_groups = []


#######################################
#           FONTES
#######################################
FONT = 'Montserrat'

#######################################
#           CONFIGS
#######################################
SHOW_PERC = True

#######################################
#           COLORS
#######################################

T_COLOR_1 = '#FFFFFF'  # title
T_COLOR_2 = '#FFFFFF'  # behind title
T_COLOR_3 = '#FFFFFF'  # date text
T_COLOR_4 = '#FFFFFF'  # above graph text
T_COLOR_5 = '#FFFFFF'  # bellow graph text
T_COLOR_6 = '#FFFFFF'  # negative color
T_COLOR_7 = '#FFFFFF'  # positive color

BG_COLOR = '#263240'

BLOCK_BG_COLOR_MID_UP = 'sbt_pos_sub.png'
BLOCK_BG_COLOR_MID_DN = 'sbt_neg_desc.png'
BLOCK_BG_COLOR_END_UP = 'sbt_neg_sub.png'  # T_COLOR_4  # new
BLOCK_BG_COLOR_END_DN = 'sbt_pos_desc.png'  # T_COLOR_1  # new

BLOCK_V3_COLOR = BLOCK_BG_COLOR_MID_UP

BLOCK_COLORS = [BLOCK_BG_COLOR_MID_UP, BLOCK_BG_COLOR_MID_DN]
LEGEND_COLORS = BLOCK_COLORS

XAXIS_TEXT_COLOR =  ['#AFDCFF', '#FFAFB8']
YAXIS_TEXT_COLOR = None
YAXIS_LINE_COLOR = '#FFFFFF'
YAXIS_LINE_OPACITY = 0

TITLE_COLOR  = '#FFFFFF'  # T_COLOR_1
SUBTIT_COLOR = '#CCFFFF'  # T_COLOR_7
DFONT_COLOR  = '#0A2038'  # T_COLOR_7


#######################################
#       POSITIONS AND SIZES
#######################################
TITLE_X = 120
TITLE_Y = 110
TITLE_DX = 0

SUBTIT_X = TITLE_X
SUBTIT_Y = TITLE_Y + 90
SUBTIT_CAPS = True

TITLE_FONT_SIZE  = 55
SUBTIT_FONT_SIZE = 22 # 20
DFONT_FONT_SIZE  = 40 # 20

# MAIN_LOGO_X =
# MAIN_LOGO_Y =
# MAIN_LOGO_W =
# MAIN_LOGO_H =

BLOCK_X = TITLE_X + 100
BLOCK_Y = TITLE_Y + 650
BLOCK_W = 50
BLOCK_H = 430
BLOCK_DX = 80
BLOCK_DX_FACTOR = 1

DFONT_X = TITLE_X + 1340
DFONT_Y = TITLE_Y

BAR_VAL_FONT_SIZE  = 30  # 25
BAR_DATE_FONT_SIZE = 22  # 18
YAXIS_FONT_SIZE = BAR_VAL_FONT_SIZE

#######################################
#           IMAGES
#######################################
ARROW_UP_IMG = 'images/sbt/seta_down.png'
ARROW_DN_IMG = 'images/sbt/seta_up.png'

MAIN_LOGO_PNG = None

#######################################
#           WATERMARK
#######################################
WATERMARK_IMG = None
# WATERMARK_ALPHA = 0.03
# WATERMARK_LAYER = 'above'
# WM_X, WM_Y, WM_W, WM_H = 700, 400, 1050, 150
# WM_Y_GT, WM_Y_GT = 500, 300

#######################################
#           RANKING
#######################################
RANK_X = TITLE_X
RANK_Y = TITLE_Y + 540 - 100

RANK_BAR_W = 80
RANK_BAR_H = 300
RANK_BAR_DX = 110

BLOCK_VERT_DN_IMG = 'images/block_circ_vert.png'
BLOCK_VERT_UP_IMG = 'images/block_circ_vert_up.png'
BLOCK_VERT_W = 568
BLOCK_VERT_H = 597

RANK_LINE_COLOR = T_COLOR_6

FLAG_CIRCLE_COLOR_UP = T_COLOR_6
FLAG_CIRCLE_COLOR_DN = FLAG_CIRCLE_COLOR_UP

#######################################
#           FOCUS 1
#######################################

FOCUS_BLK_X = TITLE_X + 500  # 200
FOCUS_BLK_Y = 300  # 190
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
FOCUS_TIT_FONT_SIZE = 53

FOCUS_TYPE_COLOR = T_COLOR_6
FOCUS_TYPE_FONT_SIZE = 24

FOCUS_FOOT_COLOR = T_COLOR_6
FOCUS_FOOT_FONT_SIZE = 20

FOCUS_DATA_X  = [FOCUS_BLK_W * 0.25, FOCUS_BLK_W * 0.75]
FOCUS_DATA_Y1 = FOCUS_BLK_IN_H * 0.3
FOCUS_DATA_Y2 = FOCUS_BLK_IN_H * 0.7
FOCUS_DATA_COLOR = T_COLOR_7
FOCUS_DATA_FONT_SIZE = [40, 34, 25]

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
FOCUS2_HEADER_BLK_FS = 52
FOCUS2_HEADER_TXT_FS = 20

FOCUS2_BLK_X = TITLE_X + 300
FOCUS2_BLK_Y, FOCUS2_BLK_Y2 = 360, 385
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
FOCUS2_TIT_FONT_SIZE = 48

FOCUS2_TYPE_COLOR = T_COLOR_6
FOCUS2_TYPE_FONT_SIZE = 24

# FOCUS_FOOT_COLOR = T_COLOR_6
# FOCUS_FOOT_FONT_SIZE = 20

FOCUS2_DATA_X  = [250, 650, 850, 1050]  # [250, 610, 800, 980]
# FOCUS_DATA_Y1 = FOCUS_BLK_IN_H * 0.3
# FOCUS_DATA_Y2 = FOCUS_BLK_IN_H * 0.7
FOCUS2_DATA_COLOR = T_COLOR_7
FOCUS2_DATA_FONT_SIZE = 30

FOCUS2_IMAGES = 'images/focus/jp_merc_fin/'

# FOCUS_ICON_H = 76
# FOCUS_ICON_W = FOCUS_ICON_H / 159 * 176

FOCUS2_ARROW_H = 44
FOCUS2_ARROW_W = FOCUS_ARROW_H / 159 * 176

#######################################
#           001_ (graphtime)
#######################################

# 001
GT_IMAGE_W = 1600
GT_IMAGE_H = 200
GT_001_MARGINS = 80, 88, 200, 140, 4

GT_PRES_PRICE_FC = T_COLOR_1  # FONT_COLOR
GT_PRES_PRICE_FS = 53         # FONT_SIZE

GT_TIME_FS = 24   #  30  # 20
GT_DFONT_FS = 22  #  24  # 15

GT_TICKS_FONT_COLOR = T_COLOR_5  # new  '#33727A'
GT_TICKS_FONT_SIZE =  28  # 36  # 20

GT_BLOCK_INFO_COLOR = '#001122'  # '#1B2C3E'  # T_COLOR_6  # new
GT_BLOCK_FONT_COLOR = 'white'
GT_BLOCK_LBL_FS = 24  # 30  # 20
GT_BLOCK_NUM_FS = 24  # 30  # 20
GT_BLOCK_DX = 2

GT_COLOR_NEG = T_COLOR_2
GT_COLOR_POS = T_COLOR_1  # T_COLOR_6  # new
GT_TRACE_WIDTH = 6

GT_INFO_52M = True

# graphtime
GT_MARGINS_LRTBPAD = 200, 440, 200, 170, 10
GT_LEGEND_X = 1.02
GT_LEGEND_Y = 1
GT_LEGEND_FS = 18
GT_LEGEND_FC = TITLE_COLOR
GT_XAXIS_FS = BAR_DATE_FONT_SIZE
GT_YAXIS_FS = BAR_VAL_FONT_SIZE
GT_AXIS_FC = T_COLOR_6

#######################################
#           COMP (graphcomp)
#######################################

CP_MARGINS_LRTBPAD = 200, 400, 200, 160, 10
CP_TRACE_WIDTH = 3
CP_TRACE_COLOR = "#1956FF"
CP_LINES_COLOR = T_COLOR_6
CP_LINE0_COLOR = T_COLOR_6

CP_XAXIS_FS = BAR_DATE_FONT_SIZE
CP_YAXIS_FS = BAR_VAL_FONT_SIZE

#######################################
#               TABLES
#######################################

TAB_BRECT_COLOR = T_COLOR_6



TAB_B1X, TAB_B1Y = 105, 166
TAB_B2X, TAB_B2Y = 500, TAB_B1Y
TAB_B3X, TAB_B3Y = TAB_B1X, 360
TAB_B4X, TAB_B4Y = TAB_B2X, 404

TAB_BTIT_DX, TAB_BTIT_DY = 35, 35

TAB_BDX = 290  # block distance between left and right text
TAB_BDY =  45  # block distance to next one
TAB_BHEI = 45  # bloch height

TAB_TITLE_X = 70
TAB_TITLE_Y = 43

TAB_DFONT_X = TAB_TITLE_X + 2
TAB_DFONT_Y = TAB_TITLE_Y + 35

TAB_ASSET_FC = 'white'

TAB_TITLE_FS = 53
TAB_DFONT_FS = 15

TAB_BLKTIT_FS = 20
TAB_ASSET_FS = 32
TAB_PERC_FS = 25

TAB_PERC_DX = 20
TAB_ARROW_DX = 110

TAB_ICO_IMG = 'images/ico_bolsas_mundo_ok.png'
TAB_ICO_X, TAB_ICO_Y, TAB_ICO_W, TAB_ICO_H = 22, 20, 42, 42

SETA_ALTA  = 'images/seta_alta_ok.png'
SETA_BAIXA = 'images/seta_baixa_ok.png'
