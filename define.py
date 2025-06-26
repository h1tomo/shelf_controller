from enum import Enum

# 陳列棚
SHELF_NUM = 6           #段数

# 目標位置の設定
MAX_PULL_DIST = 560     #棚板位置[mm]（最大引き出し時）
MIN_PULL_DIST = 0       #棚板位置[mm]（初期化時）
MAX_BELT_DIST = 0       #商品移動距離[mm]（最大引き出し時）
MIN_BELT_DIST = -450    #商品移動距離[mm]（初期化時）

# コントローラーからのコマンド
class OPE_CMD(Enum):
    MODE = 0 # 通常0orリセット1
    ID = 1
    POS = 2
    MOV = 3
    NUM =4

# 陳列動作指令値の定義（RTC―――>M5）
class SHELF_CMD(Enum):
    ID = 0
    TRG_POS = 1
    PDT_MOV = 2
    LED = 3
    NUM = 4

# 陳列動作指令値のMODEの定義
class SHELF_CMD_MODE(Enum):
    NORMAL = 0
    RESET = 1

# LED表示灯のモード定義
class SHELF_CMD_LED(Enum):
    INITIALIZE = 0
    ACTIVATED = 1
    MOVING = 2
    DETECT_CST = 3
    EMG = 4

# 陳列動作指令値のIDの定義
class SHELF_CMD_ID(Enum):
    SHELF0 = 0
    SHELF1 = 1
    SHELF2 = 2
    SHELF3 = 3
    SHELF4 = 4
    SHELF5 = 5
    ALL_INIT = 6
    ALL_PULL = 7
    EMG_STOP = 8
    LED = 9

# 陳列動作完了信号の定義（RTC<―――M5）
class SHELF_CMP(Enum):
    STATE0 = 0
    STATE1 = 1
    STATE2 = 2
    STATE3 = 3
    STATE4 = 4
    STATE5 = 5
    EMG_STATE = 6
    LED = 7
    RCV = 8
    NUM = 9

# 各棚の動作状態
class SHELF_STATE(Enum):
    STANDBY = 0
    MOVING = 1