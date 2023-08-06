#----------------------------------------------------------------------------
# Name:         lmdGUI.py
# Purpose:      OS class
#
# Author:       Walter Obweger
#
# Created:      20200403
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import sys
import os
import wx
import logging
import traceback

def getDN(sDN,oGui,sTitle,oLog=None):
    """get SHA limited
    ### parameter
        sDN     ... directory name
        oGui    ... GUI parent object
        sTitle  ... dialog title
        oLog    ... logging object
    ### return
        code
            >0  ... okay content read
            =0  ... okay no data
            <0  ... error
        directory
    """
    try:
        # +++++ beg:initialize
        iRet=0
        sRetDN=None
        # ----- end:initialize
        # +++++ beg:start directory
        if sDN is None:
            sDN=os.getcwd()
        else:
            if sDN in ['.','./','.\\']:
                sDN=os.getcwd()
        # ----- end:start directory
        # +++++ beg:show dialog
        dlgDN = wx.DirDialog(oGui, sTitle,
                        defaultPath=sDN,
                        style=wx.DD_DEFAULT_STYLE
                        #| wx.DD_DIR_MUST_EXIST
                        #| wx.DD_CHANGE_DIR
                        )
        if dlgDN.ShowModal() == wx.ID_OK:
            sRetDN=dlgDN.GetPath()
            iRet=1
            if oLog is not None:
                oLog.debug('ldmGUI::getDN sRetDN:%r'%(sRetDN))
        dlgDN.Destroy()
        # ----- end:show dialog
        return iRet,sRetDN
    except:
        if oLog is not None:
            oLog.error(traceback.format_exc())
        return -1,None
def getFN(sFN,oGui,sTitle,lWildCard=["All files (*.*)|*.*"],iOpen=1,oLog=None):
    """get file name
    ### parameter
        sFN     ... file name
        oGui    ... GUI parent object
        sTitle  ... dialog title
        oLog    ... logging object
    ### return
        code
            >0  ... okay content read
            =0  ... okay no data
            <0  ... error
        directory
    """
    try:
        # +++++ beg:initialize
        iRet=0
        sRetFN=None
        # ----- end:initialize
        # +++++ beg:start directory
        if sFN is None:
            sTmpDN=os.getcwd()
            sTmpFN=''
        else:
            #if sFN in ['.','./','.\\']:
            #    sDN=os.getcwd()
            sTmpDN,sTmpFN=os.path.split(sFN)
            if sTmpDN in ['','.','./','.\\']:
                sTmpDN=os.getcwd()
            
        # ----- end:start directory
        # +++++ beg:show dialog
        iStyle=wx.FD_DEFAULT_STYLE
        if iOpen==0:
            iStyle|=wx.FD_SAVE
        elif iOpen==1:
            iStyle|=wx.FD_OPEN
        elif iOpen>1:
            iStyle|=wx.FD_OPEN
            iStyle|=wx.FD_MULTIPLE
        else:
            iStyle|=wx.FD_OPEN
        dlgFN = wx.FileDialog(oGui, sTitle,
                        defaultDir=sTmpDN,
                        defaultFile=sTmpFN,
                        wildcard='|'.join(lWildCard),
                        style=iStyle)
        if dlgFN.ShowModal() == wx.ID_OK:
            if iOpen>1:
                oRetFN=dlgFN.GetPaths()
            else:
                oRetFN=dlgFN.GetPath()
            iRet=1
            if oLog is not None:
                oLog.logDbg('ldmGUI::getDN oRetFN:%r',oRetFN)
        dlgFN.Destroy()
        # ----- end:show dialog
        return iRet,oRetFN
    except:
        if oLog is not None:
            oLog.logTB()
        return -1,None
def getSplitFN(sFN):
    try:
        sTmpDN,sTmpFN=os.path.split(sFN)
        sDN=sTmpDN.replace('\\','/')
        return sDN,sTmpFN
    except:
        return None,None
