#----------------------------------------------------------------------------
# Name:         ldmWidTree.py
# Purpose:      ldmWidTree.py
#               GUI widget respond on size change
# Author:       Walter Obweger
#
# Created:      20200405
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import wx
from lindworm.ldmWidCore import ldmWidCore

class ldmWidList(ldmWidCore):
    def __initCls__(self,**kwargs):
        self.clsWid=wx.ListCtrl
    def __initWid__(self,**kwargs):
        try:
            self.logDbg('__initWid__')
            style=wx.LC_HRULES | wx.LC_REPORT | wx.LC_VRULES
            self.IMG_EMPTY=-1
            if kwargs.get('bTreeButtons',1)>0:
                style|=wx.TR_HAS_BUTTONS
            if kwargs.get('bHideRoot',False)>0:
                style|=wx.TR_HIDE_ROOT
            if kwargs.get('single_sel',False)>0:
                style|=wx.LC_SINGLE_SEL
                self._bMultiple=False
            else:
                self._bMultiple=True
            _args,_kwargs=self.GetWidArgs(kwargs,
                        ['id','name','parent','pos','size','style'],
                        {'pos':(0,0),'size':(-1,-1),'style':style})
            self.wid=self.clsWid(*_args,**_kwargs)
            lCol=kwargs.get('lCol',None)
            if lCol is not None:
                for tCol in lCol:
                    if tCol[1] in ['l','lf']:
                        fmt=wx.LIST_FORMAT_LEFT
                    elif tCol[1] in ['r','rg']:
                        fmt=wx.LIST_FORMAT_RIGHT
                    elif tCol[1] in ['c','ct']:
                        fmt=wx.LIST_FORMAT_CENTER
                    else:
                        fmt=wx.LIST_FORMAT_LEFT
                    self.wid.AppendColumn(tCol[0],
                                    format=fmt,
                                    width=tCol[2])
        except:
            self.logTB()
