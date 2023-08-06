#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#----------------------------------------------------------------------------
# Name:         ldmWidApp.py
# Purpose:      ldmWidApp.py
#               GUI for ldmWidApp
# Author:       Walter Obweger
#
# Created:      20200405
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import os
import logging
import traceback

from optparse import OptionParser

import wx
import wx.aui
import wx.html
import wx.grid

#import wx.lib.agw.aui as aui
#from wx.lib.agw.aui import aui_switcherdialog as ASD

from lindworm import __version__
from lindworm.ldmWidFrmAui import ldmWidFrmAui

class ldmWidApp(wx.App):
    def __init__(self,
                redirect=False,
                filename=None,
                useBestVisual=False,
                clearSigInt=True,
                clsFrm=None,
                kwargs=None):
        self.clsFrm=clsFrm
        self.kwargs=kwargs
        wx.App.__init__(self,redirect=redirect,
                    filename=filename,
                    useBestVisual=useBestVisual,
                    clearSigInt=clearSigInt)
    def OnInit(self):
        global opt
        if self.clsFrm is None:
            self.frmAui = ldmWidFrmAui(iLv=0,
                        sLogger='frmAui',
                        title="lindworm center",
                        ldmCfg=None)
        else:
            self.frmAui = self.clsFrm(iLv=0,
                        sLogger='frmAui',
                        title="lindworm center",
                        ldmCfg=None,
                        **self.kwargs)
        self.SetTopWindow(self.frmAui.GetWid())
        self.frmAui.GetWid().Show()
        return True

# end of class ldmWidApp

def main(args=None,clsFrm=None,**kwargs):
    # +++++ beg:
    # ----- end:
    
    # +++++ beg:init
    iRet=0
    iVerbose=5                                          # 20190624 wro:set default verbose level
    # ----- end:init
    # +++++ beg:define CLI arguments
    usage = "usage: %prog [options]"
    oParser=OptionParser(usage,version="%prog "+__version__)
    oParser.add_option('-c','--cfgFN',dest='sCfgFN',
            default='ldmStorageFolderCfg.json',
            help='configuration file',metavar='pyGatherMDCfg.json',
            )
    oParser.add_option('','--srcDN',dest='sSrcDN',
            default='./',
            help='source folder',metavar='path/to/folder/to/read',
            )
    oParser.add_option('','--bldDN',dest='sBldDN',
            default='./',
            help='build directory',metavar='path/to/output/folder',
            )
    oParser.add_option('','--bldFN',dest='sBldFN',
            default='',
            help='build file',metavar='sng.json',
            )
    oParser.add_option('-l','--log',dest='sLogFN',
            default='./log/ldmStorageFolder.log',
            help='log filename',metavar='./log/ldmStorageFolder.log')
    oParser.add_option("-v", action="store_true", dest="verbose", default=True)
    oParser.add_option("-q", action="store_false", dest="verbose", default=True)
    # ----- end:define CLI arguments
    # +++++ beg:parse command line
    (opt,args)=oParser.parse_args(args=args)
    if opt.verbose:
        print("config FN:     %r"%(opt.sCfgFN))
        print("source DN:     %r"%(opt.sSrcDN))
        print(" build DN:     %r"%(opt.sBldDN))
        print(" build FN:     %r"%(opt.sBldFN))
        iVerbose=20
    global gOpt
    gOpt=opt
    # ----- end:parse command line
    # +++++ beg:prepare logging
    if opt.sLogFN is not None:
        import lindworm.logUtil as logUtil
        logUtil.logInit(opt.sLogFN,iLevel=logging.DEBUG)
    # ----- end:prepare logging
    # +++++ beg:
    app = ldmWidApp(0,clsFrm=clsFrm,kwargs=kwargs)
    app.MainLoop()
    iRet+=1
    # ----- end:
    return iRet

if __name__ == "__main__":
    # +++++ beg:call entry point
    main(args=None)
    # ----- end:call entry point
