#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Python -*-

# <rtc-template block="description">
"""
 @file shelf_controllerTest.py
 @brief ModuleDescription
 @date $Date$


"""
# </rtc-template>

from __future__ import print_function
import sys
import time
sys.path.append(".")

# Import RTM module
import RTC
import OpenRTM_aist


# Import Service implementation class
# <rtc-template block="service_impl">

import shelf_controller

# </rtc-template>

# Import Service stub modules
# <rtc-template block="consumer_import">
# </rtc-template>


# This module's spesification
# <rtc-template block="module_spec">
shelf_controllertest_spec = ["implementation_id", "shelf_controllerTest", 
         "type_name",         "shelf_controllerTest", 
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
# @class shelf_controllerTest
# @brief ModuleDescription
# 
# 
# </rtc-template>
class shelf_controllerTest(OpenRTM_aist.DataFlowComponentBase):
    
    ##
    # @brief constructor
    # @param manager Maneger Object
    # 
    def __init__(self, manager):
        OpenRTM_aist.DataFlowComponentBase.__init__(self, manager)

        self._d_opeCmp = OpenRTM_aist.instantiateDataType(RTC.TimedLong)
        """
        """
        self._opeCmpIn = OpenRTM_aist.InPort("opeCmp", self._d_opeCmp)
        self._d_emgStop_cst = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
        """
        """
        self._emgStop_cstIn = OpenRTM_aist.InPort("emgStop_cst", self._d_emgStop_cst)
        self._d_emgStop_chg = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
        """
        """
        self._emgStop_chgIn = OpenRTM_aist.InPort("emgStop_chg", self._d_emgStop_chg)
        self._d_opeCmd = OpenRTM_aist.instantiateDataType(RTC.TimedLongSeq)
        """
        """
        self._opeCmdOut = OpenRTM_aist.OutPort("opeCmd", self._d_opeCmd)
        self._d_detectCust = OpenRTM_aist.instantiateDataType(RTC.TimedBoolean)
        """
        """
        self._detectCustOut = OpenRTM_aist.OutPort("detectCust", self._d_detectCust)


        


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
        self.addInPort("opeCmp",self._opeCmpIn)
        self.addInPort("emgStop_cst",self._emgStop_cstIn)
        self.addInPort("emgStop_chg",self._emgStop_chgIn)
        
        # Set OutPort buffers
        self.addOutPort("opeCmd",self._opeCmdOut)
        self.addOutPort("detectCust",self._detectCustOut)
        
        # Set service provider to Ports
        
        # Set service consumers to Ports
        
        # Set CORBA Service Ports
        
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
    
    #    ##
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
    
        return RTC.RTC_OK
    
    ###
    ##
    ## The aborting action when main logic error occurred.
    ##
    ## @param ec_id target ExecutionContext Id
    ##
    ## @return RTC::ReturnCode_t
    #    #
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
    
    def runTest(self):
        return True

def RunTest():
    manager = OpenRTM_aist.Manager.instance()
    comp = manager.getComponent("shelf_controllerTest0")
    if comp is None:
        print('Component get failed.', file=sys.stderr)
        return False
    return comp.runTest()

def shelf_controllerTestInit(manager):
    profile = OpenRTM_aist.Properties(defaults_str=shelf_controllertest_spec)
    manager.registerFactory(profile,
                            shelf_controllerTest,
                            OpenRTM_aist.Delete)

def MyModuleInit(manager):
    shelf_controllerTestInit(manager)
    shelf_controller.shelf_controllerInit(manager)

    # Create a component
    comp = manager.createComponent("shelf_controllerTest")

def main():
    mgr = OpenRTM_aist.Manager.init(sys.argv)
    mgr.setModuleInitProc(MyModuleInit)
    mgr.activateManager()
    mgr.runManager(True)

    ret = RunTest()
    mgr.shutdown()

    if ret:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

