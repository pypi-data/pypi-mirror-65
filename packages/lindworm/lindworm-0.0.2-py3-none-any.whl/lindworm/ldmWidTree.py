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

class ldmWidTree(ldmWidCore):
    def __initCls__(self,**kwargs):
        self.clsWid=wx.TreeCtrl
    def __initWid__(self,**kwargs):
        try:
            self.logDbg('__initWid__')
            style=0
            self.IMG_EMPTY=-1
            if kwargs.get('bTreeButtons',1)>0:
                style|=wx.TR_HAS_BUTTONS
            if kwargs.get('bHideRoot',False)>0:
                style|=wx.TR_HIDE_ROOT
            if kwargs.get('multiple_sel',False)>0:
                style|=wx.TR_MULTIPLE
                self._bMultiple=True
            else:
                self._bMultiple=False
            _args,_kwargs=self.GetWidArgs(kwargs,
                        ['id','name','parent','pos','size','style'],
                        {'pos':(0,0),'size':(-1,-1),'style':style})
            self.wid=self.clsWid(*_args,**_kwargs)
        except:
            self.logTB()
