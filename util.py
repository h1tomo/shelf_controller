import serial
import serial.tools.list_ports
import struct

from define import *

# COMポートを探す関数
def find_COMport(keyword=""):
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if keyword.lower() in port.description.lower():
            return port.device  # 例: 'COM3'
    return None

# 棚板全段完了をチェックする関数
def allCompleted(shelfData_):
    cmp = True
    for i in range(SHELF_CMP.NUM.value - 1):
        if shelfData_[i] == SHELF_STATE.MOVING.value:
            cmp = False
    return cmp

# 送信データリスト作成関数
def sendDataListup(opeCmd_):
    """
    引数： CLからの受信データ

    処理： リセットと通常を見極めて，M5に送信するデータリストを作成

    返り値： M5への送信データリスト
        [0]棚ID
        [1]目標値
        [2]商品移動量
        [3]表示灯モード
    """
    print("M5への送信データリストアップ")
    sendData = [0]*SHELF_CMD.NUM.value
    if opeCmd_[OPE_CMD.MODE.value] == SHELF_CMD_MODE.RESET.value:
        sendData[SHELF_CMD.ID.value] = SHELF_CMD_ID.ALL_INIT.value
        sendData[SHELF_CMD.TRG_POS.value] = 0
        sendData[SHELF_CMD.PDT_MOV.value] = 0
        sendData[SHELF_CMD.LED.value] = SHELF_CMD_LED.MOVING.value
    else:
        sendData[SHELF_CMD.ID.value] = opeCmd_[OPE_CMD.ID.value]
        sendData[SHELF_CMD.TRG_POS.value] = opeCmd_[OPE_CMD.POS.value]
        sendData[SHELF_CMD.PDT_MOV.value] = opeCmd_[OPE_CMD.MOV.value]
        sendData[SHELF_CMD.LED.value] = SHELF_CMD_LED.MOVING.value
    print(sendData)
    return sendData

# LEDだけ送るときの送信データリスト作成関数
def sendDataListupLED(LEDMode_):
    """
    引数： 表示灯のモード

    処理： M5に送信するリストにする

    返り値： M5への送信データリスト
        [0]棚ID=9 ※LEDだけ
        [1]目標値=0
        [2]商品移動量=0
        [3]表示灯モード
    """
    print("M5への送信データリストアップ")
    sendData = [0]*SHELF_CMD.NUM.value
    sendData[SHELF_CMD.ID.value] = SHELF_CMD_ID.LED.value
    sendData[SHELF_CMD.TRG_POS.value] = 0
    sendData[SHELF_CMD.PDT_MOV.value] = 0
    sendData[SHELF_CMD.LED.value] = LEDMode_
    print(sendData)
    return sendData

# 動作開始したことを確認する関数
def moveStarted(shlefData_, sendData_):
    moveStart = False
    id = sendData_[SHELF_CMD.ID.value]
    if id != None:
        if id >= SHELF_CMD_ID.SHELF0.value and id <= SHELF_CMD_ID.SHELF5.value:
            if shlefData_[id] == SHELF_STATE.MOVING.value:
                moveStart = True
        
        elif id == SHELF_CMD_ID.ALL_INIT.value or id == SHELF_CMD_ID.ALL_PULL.value or id == SHELF_CMD_ID.EMG_STOP.value:
            if shlefData_[0] == SHELF_STATE.MOVING.value: #一旦id0が動いていたらOKにする，あとで考える
                moveStart = True
    return moveStart

# 受信成功したことを確認する関数
def rcvSuccessed(shelfData_):
    if shelfData_[SHELF_CMP.RCV.value] == 1:
        return True
    else:
        return False
