#----------------------------------------------------------------------------
# Name:         lmdGuiThread.py
# Purpose:      gui thread class
#
# Author:       Walter Obweger
#
# Created:      20200404
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import time
import wx
import wx.lib.newevent

from six.moves import _thread as sixThd

from lindworm.logUtil import ldmUtilLog
from lindworm.ldmGuiNty import ldmGuiNty

# +++++ beg:create event class and binder function
(ldmGuiNotifyEvt, EVT_LDM_GUI_NOTIFY) = wx.lib.newevent.NewEvent()
# ----- end:initialize

class ldmGuiThd(ldmUtilLog):
    def __init__(self,oGui,rDly=0.200,sLogger='ldmGuiThd',iLv=0,iVerbose=0):
        """constructor
        ### parameter
            oGui        ... GUI object
            rDly        ... delay between processing [s], yield GIL
            sLogger     ... log origin
            iLv         ... log level short
            iVerbose    ... higher values add more logs
        """
        ldmUtilLog.__init__(self,sLogger=sLogger,iLv=iLv,
                            iVerbose=iVerbose)
        self.oGui=oGui
        self.iKeepRun=0
        self.iRunning=0
        self.rDly=max(rDly,0.01)
        self.lCall=[]
        self.oNty=ldmGuiNty()
    def BindEvtNty(self,funcOnNty):
        """bind event function to oGui object
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            if self.oGui is not None:
                self.oGui.Bind(EVT_LDM_GUI_NOTIFY, funcOnNty)
                return 1
            else:
                return 0
        except:
            self.logTB()
            return -1
    def GetNty(self):
        """get notify object
        ### parameter
        ### return
            !=None  ... okay processing done
            ==None  ... okay nop
        """
        return self.oNty
    def Do(self,sPhase,func,*args,**kwargs):
        """schedule callable
        ### parameter
            sPhase  ... phase name
            fun     ... callable
            args    ... argument
            kwargs  ... keyword arguments
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmGuiThd::'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            # ----- end:initialize
            # +++++ beg:
            self.oNty.IncSchedule()
            self.lCall.append((sPhase,func,args,kwargs))
            # ----- end:
            # +++++ beg:
            if self.iKeepRun<1:
                self.Start()
                iRet=2
            else:
                iRet=1
            # ----- end:
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def Start(self):
        self.iKeepRun=1
        self.iRunning=1
        self.iRunExc=1
        sixThd.start_new_thread(self._runNotify,())
        sixThd.start_new_thread(self._runExc,())
    def Stop(self):
        self.iKeepRun=0
    def _runNotify(self):
        """
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmGuiThd::_runNotify'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            # ----- end:initialize
            # +++++ beg:
            while (self.iKeepRun>0) and (self.iRunExc>0):
                if self.oGui is not None:
                    evt = ldmGuiNotifyEvt(oNty = self.oNty)
                    wx.PostEvent(self.oGui, evt)
                if self.iVerbose>0:
                    self.oLog.debug('    %s sleep:%4.3f'%(sOrg,self.rDly))
                time.sleep(self.rDly)
            # ----- end:
            # +++++ beg:
            #if self.oGui is not None:
                #self.oNty.SetStatus('stopped')
            #    evt = ldmGuiNotifyEvt(oNty = self.oNty)
            #    wx.PostEvent(self.oGui, evt)
            #    time.sleep(self.rDly)
            self.iRunning=0
            # ----- end:
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def delay(self,iCnt=1):
        time.sleep(self.rDly)
        while iCnt>0:
            time.sleep(self.rDly)
            iCnt-=1
    def _runExc(self):
        """
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmGuiThd::_runExc'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            # ----- end:initialize
            # +++++ beg:
            while self.iKeepRun>0:
                if len(self.lCall)>0:
                    try:
                        sPhase,func,args,kwargs=self.lCall.pop(0)
                        self.oNty.SetPhase(sPhase)
                        oRetCall=func(*args,**kwargs)
                        self.oLog.debug('    %s oRetCall:%r'%(sOrg,oRetCall))
                    except:
                        self.logTB()
                if self.iVerbose>0:
                    self.oLog.debug('    %s sleep:%4.3f'%(sOrg,self.rDly))
                time.sleep(self.rDly)
            # +++++ beg:
            self.iRunExc=0
            # ----- end:
            # ----- end:
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def __tpl(self):
        """
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            iRet=0
            sOrg='::'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            # ----- end:initialize
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
