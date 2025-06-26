#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file shelf_controller.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist

# Module for milo_actuator_ctrlRTC
from define import *
from util import *


# COMポート開いて確認
COMport = find_COMport("SERIAL")
if COMport:
    try:
        ser = serial.Serial(COMport, baudrate=115200, timeout=1)
        print(f"Connected to {COMport}")
    except serial.SerialException as e:
        print(f"Failed to connect: {e}")
else:
    print("Micro Controller port not found")


# 送信データをエンコードする関数
def sendToM5(opeCmds_):
    """
    引数： 符号付整数4つのリスト
            [0]棚板ID
            [1]棚板目標値
            [2]商品移動距離
            [3]表示灯モード
    """
    binary0 = struct.pack('>h', opeCmds_[0])[0]
    binary1 = struct.pack('>h', opeCmds_[0])[1]
    high0 = (binary0 & 0b11111100) >> 6
    mid0 = ((binary0 & 0b00111111) << 1) | ((binary1 & 0b10000000) >> 7)
    low0 = (binary1 & 0b01111111)

    binary2 = struct.pack('>h', opeCmds_[1])[0]
    binary3 = struct.pack('>h', opeCmds_[1])[1]
    high1 = (binary2 & 0b11111100) >> 6
    mid1 = ((binary2 & 0b00111111) << 1) | ((binary3 & 0b10000000) >> 7)
    low1 = (binary3 & 0b01111111)
    
    binary4 = struct.pack('>h', opeCmds_[2])[0]
    binary5 = struct.pack('>h', opeCmds_[2])[1]
    high2 = (binary4 & 0b11111100) >> 6
    mid2 = ((binary4 & 0b00111111) << 1) | ((binary5 & 0b10000000) >> 7)
    low2 = (binary5 & 0b01111111)
    
    binary6 = struct.pack('>h', opeCmds_[3])[0]
    binary7 = struct.pack('>h', opeCmds_[3])[1]
    high3 = (binary6 & 0b11111100) >> 6
    mid3 = ((binary6 & 0b00111111) << 1) | ((binary7 & 0b10000000) >> 7)
    low3 = (binary7 & 0b01111111)

    encodedData = struct.pack('BBBBBBBBBBBBB',255,high0,mid0,low0,high1,mid1,low1,high2,mid2,low2,high3,mid3,low3)
    print("エンコードしたバイト列")
    print(encodedData)

    ser.write(encodedData)



# Import Service implementation class
# <rtc-template block="service_impl">

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
shelf_controller_spec = ["implementation_id", "shelf_controller", 
         "type_name",         "shelf_controller", 
         "description",       "ModuleDescription", 
         "version",           "1.0.0", 
         "vendor",            "Hosokawa", 
         "category",          "Controller", 
         "activity_type",     "STATIC", 
         "max_instance",      "1", 
         "language",          "Python", 
         "lang_type",         "SCRIPT",
         ""]
# </rtc-template>

# <rtc-template block="component_description">
##
# @class shelf_controller
# @brief ModuleDescription
# 
# 
# </rtc-template>
class shelf_controller(OpenRTM_aist.DataFlowComponentBase):
	
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_opeCmd = OpenRTM_aist.instantiateDataType(RTC.TimedLongSeq)
        """
        """
        self._opeCmdIn = OpenRTM_aist.InPort("opeCmd", self._d_opeCmd)
        self._d_detectCust = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
        """
        """
        self._detectCustIn = OpenRTM_aist.InPort("detectCust", self._d_detectCust)
        self._d_opeCmp = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        """
        self._opeCmpOut = OpenRTM_aist.OutPort("opeCmp", self._d_opeCmp)
        self._d_emgStop_cst = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
        """
        """
        self._emgStop_cstOut = OpenRTM_aist.OutPort("emgStop_cst", self._d_emgStop_cst)
        self._d_emgStop_chg = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
        """
        """
        self._emgStop_chgOut = OpenRTM_aist.OutPort("emgStop_chg", self._d_emgStop_chg)


		


        # initialize of configuration-data.
        # <rtc-template block="init_conf_param">
		
        # </rtc-template>


		 
    ##
    #
    # The initialize action (on CREATED->ALIVE transition)
    # 
    # @return RTC::ReturnCode_t
    # 
    #
    def onInitialize(self):
        # Bind variables and configuration variable
		
        # Set InPort buffers
        self.addInPort("opeCmd",self._opeCmdIn)
        self.addInPort("detectCust",self._detectCustIn)
		
        # Set OutPort buffers
        self.addOutPort("opeCmp",self._opeCmpOut)
        self.addOutPort("emgStop_cst",self._emgStop_cstOut)
        self.addOutPort("emgStop_chg",self._emgStop_chgOut)
		
        # Set service provider to Ports
        # Set service consumers to Ports
        # Set CORBA Service Ports


        # M5に指令送信（表示灯点滅）
		
        # 変数定義
        self.opeCmd = [None]*OPE_CMD.NUM.value
        self.sendFlag = False
        self.findHeader = False
        self.movingFlag = False
        self.shelfData = [None]*SHELF_CMP.NUM.value
        self.shelfDataPast = [None]*SHELF_CMP.NUM.value
        self.emgButtonPast = False
        self.emgButtonNow = False
        self.sendTime = 0
        self.moveStartTime = 0
        self.shelfID = 0
        self.sendData = [None]*SHELF_CMD.NUM.value
        self.aploachCst = False
        self.sendCount = 0
        self.rcvSuccess = False

        print("shelf_controller is ready!")
        return RTC.RTC_OK
	
    ###
    ## 
    ## The finalize action (on ALIVE->END transition)
    ## 
    ## @return RTC::ReturnCode_t
    #
    ## 
    #def onFinalize(self):
    #

    #    return RTC.RTC_OK
	
    ###
    ##
    ## The startup action when ExecutionContext startup
    ## 
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onStartup(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The shutdown action when ExecutionContext stop
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onShutdown(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ##
    #
    # The activated action (Active state entry action)
    #
    # @param ec_id target ExecutionContext Id
    # 
    # @return RTC::ReturnCode_t
    #
    #
    def onActivated(self, ec_id):
        # M5に指令送信（表示灯点灯＿緑＆全棚板初期状態へ）

        # 変数初期化

        print("shelf_controller is activated!")
        return RTC.RTC_OK
	
    ##
    #
    # The deactivated action (Active state exit action)
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #
    def onDeactivated(self, ec_id):
        #M5に指令送信（表示灯消灯）

        print("shelf_controller is deactivated!")
        return RTC.RTC_OK
	
    ##
    #
    # The execution action that is invoked periodically
    #
    # @param ec_id target ExecutionContext Id
    #
    # @return RTC::ReturnCode_t
    #
    #

    def onExecute(self, ec_id):
        # 棚板動作指令受信
        if self._opeCmdIn.isNew():
            print("receive operation command.")
            # 受信データ読み込み
            self.opeCmd = self._opeCmdIn.read()
            print(self.opeCmd.data)
            # 送信データリスト作成
            self.sendData = sendDataListup(self.opeCmd.data)
            # M5への送信フラグを立てる
            self.sendFlag = True


        # M5への通常動作指令送信（送信フラグがTrueのとき || （送信後一定時間(2秒)経過 && 受信成功していない）） 
        if self.sendFlag == True or (self.rcvSuccess == False and (time.time() - self.sendTime) > 2 and self.sendCount != 0):
            print("M5へ動作指令送信")
            sendToM5(self.sendData) # 受信データをエンコードしてM5にシリアル送信
            self.sendCount += 1
            self.sendTime = time.time() # 送信時間記録
            self.sendFlag = False # 送信フラグを倒す
            self.rcvSuccess = False


        # 動作完了したら完了信号送信
        if self.movingFlag == True and allCompleted(self.shelfData) == True:
            if not self.sendData[SHELF_CMD.ID.value] == SHELF_CMD_ID.LED.value or self.sendData[SHELF_CMD.ID.value] == SHELF_CMD_ID.EMG_STOP.value:
                print("動作完了")
                self._d_opeCmp.data = 0
                self._opeCmpOut.write()
            self.movingFlag = False
        # 動作未完了かつ棚板動作開始から一定時間(10秒)経過
        elif self.movingFlag == True and allCompleted(self.shelfData) == False and (time.time() - self.moveStartTime) > 10:
            a = 1 # M5に指令送信（表示灯にエラー出す）


        # M5からのシリアル受信
        if self.findHeader == True:
            if ser.in_waiting > 9:
                self.shelfDataPast = self.shelfData
                self.shelfData = list(ser.read(9))
                self.findHeader = False
                # 指令値シリアル受信成功判定とって時刻も記録
                if self.movingFlag == False and rcvSuccessed(self.shelfData):
                    self.moveStartTime = time.time()
                    print(self.moveStartTime)
                    self.movingFlag = True
                    self.rcvSuccess = True
                # 非常停止スイッチ押下状態変数更新
                self.emgButtonPast = self.emgButtonNow
                self.emgButtonNow = self.shelfData[SHELF_CMP.EMG_STATE.value]               
                print(self.shelfData)
        else:
            while self.findHeader == False and ser.in_waiting > 0:
                if ser.read(1) == b'\xff':
                    self.findHeader = True


        # 非常停止スイッチ状態変化時
        if self.emgButtonNow != self.emgButtonPast:
            print("非常停止スイッチ状態変化")
            # ボタンの状態をデータポートからCLへ送信
            self._d_emgStop_chg.data = self.emgButtonNow
            self._emgStop_chgOut.write()
            # 非常停止スイッチ解除時，まだ棚板動作中なら動作開始時刻をアプデ．適切なLED信号も送信
            if self.emgButtonNow == False:
                a = 1#まだ書いてない
            else:
              # M5に表示灯の制御指令
                self.sendData = sendDataListupLED(SHELF_CMD_LED.EMG.value)
                self.sendFlag = True  

        
        # 客検知状態受信
        if self._detectCustIn.isNew():
            print("デバッグ用:receive detect cst")
            # 受信データ読み込み
            detectCst = self._detectCustIn.read()
            self.aploachCst = detectCst.data
            # 受信した客検知状態をポートから出力
            self._d_emgStop_cst.data = detectCst.data
            self._emgStop_cstOut.write()
            # 客検知したならM5に表示灯の制御指令送信
            if self.aploachCst == True:
                self.sendData = sendDataListupLED(SHELF_CMD_LED.DETECT_CST.value)
                self.sendFlag = True
    
        return RTC.RTC_OK
	
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onAborting(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The error action in ERROR state
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onError(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The reset action that is invoked resetting
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onReset(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The state update action that is invoked after onExecute() action
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##

    ##
    #def onStateUpdate(self, ec_id):
    #
    #    return RTC.RTC_OK
	
    ###
    ##
    ## The action that is invoked when execution context's rate is changed
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    ##
    ##
    #def onRateChanged(self, ec_id):
    #
    #    return RTC.RTC_OK
	



def shelf_controllerInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=shelf_controller_spec)
    manager.registerFactory(profile,
                            shelf_controller,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    shelf_controllerInit(manager)

    # create instance_name option for createComponent()
    instance_name = [i for i in sys.argv if "--instance_name=" in i]
    if instance_name:
        args = instance_name[0].replace("--", "?")
    else:
        args = ""
  
    # Create a component
    comp = manager.createComponent("shelf_controller" + args)

def main():
    # remove --instance_name= option
    argv = [i for i in sys.argv if not "--instance_name=" in i]
    # Initialize manager
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager()

if __name__ == "__main__":
    main()

