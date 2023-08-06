#----------------------------------------------------------------------------
# Name:         lmdGuiNty.py
# Purpose:      gui notify class
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

from six.moves import _thread as sixThd

from lindworm.logUtil import ldmUtilLog

class ldmGuiNty:
    def __init__(self,iVal=0,iMin=0,iMax=100):
        self.sPhase=''
        self.sStatus=''
        self.iVal=iVal
        self.iMin=iMin
        self.iMax=iMax
        self.iSchedule=0
        self.iStatus=0
    def clrSchedule(self):
        """
        ### parameter
        ### return
            actions scheduled
        """
        self.iSchedule=0
    def finStatus(self):
        """finalize status, property iStatus set to -2,
        to ensure final notification to be posted.
        IsActive set iStatus to -1.
        """
        self.iStatus=-2
    def clrStatus(self):
        """clear status, notification turned off.
        """
        self.iStatus=-1
    def IsActive(self,iHndFin=1):
        """check notification still active.
        event handler is supposed to use methode to prevent
        unnecessary notifications.
        """
        if self.iStatus>=0:
            return 1
        else:
            if self.iStatus==-2:
                if iHndFin>0:
                    self.clrStatus()
                return 1
            return 0
    def IncSchedule(self):
        """increment schedule counter.
        """
        self.iSchedule+=1
        self.iStatus=0
    def IncStatus(self):
        """increment status counter.
        """
        self.iStatus+=1
    def GetStatusOfs(self):
        """get string with schedule and status counter formated.
        schedule 2 digits,
        status 6 digits, or 'fin   ' in case iStatus==-2
        counter overflow is handled here.
        """
        if self.iSchedule>99:
            self.iSchedule=0
        if self.iStatus>999990:
            self.iStatus=0
        elif self.iStatus==-2:
            return '%02d.fin    '%(self.iSchedule)
        return '%02d.%06d'%(self.iSchedule,self.iStatus)
    def SetPhase(self,sPhase):
        """set phase
        ### parameter
            sPhase      ... phase : string
        """
        self.sPhase=sPhase
    def GetPhase(self):
        """get phase
        ### return
            sPhase      ... phase : string
        """
        return self.sPhase
    def SetStatus(self,sStatus):
        """set sStatus
        ### parameter
            sStatus     ... status : string
        """
        self.sStatus=sStatus
    def GetStatus(self):
        """get sStatus
        ### return
            sStatus     ... status : string
        """
        return self.sStatus
    def SetVal(self,iVal,iMax=None):
        """set value
        ### parameter
            iVal    ... value : int
            iMax    ... maximum : int
        """
        self.iVal=iVal
        if iMax is not None:
            self.iMax=iMax
    def SetMin(self,iMin):
        """set minimum
        ### parameter
            iMin    ... minimum : int
        """
        self.iMin=iMin
    def SetMax(self,iMax):
        """set maximum
        ### parameter
            iMax    ... maximum : int
        """
        self.iMax=iMax
    def GetNormalized(self,rScale=1000):
        """get normalized value scaled between 0 to rScale.
        ### parameter
            rScale  ... scale limit
        ### return
            rVal    ... normalized value (min/max),
                        0 <= rVal <= rScale
        """
        try:
            if self.iVal<self.iMin:
                self.iVal=self.iMin
            if self.iVal>self.iMax:
                self.iVal=self.iMax
            rVal=(self.iVal-self.iMin)/(self.iMax-self.iMin)
            return rVal*rScale
        except:
            return 12
