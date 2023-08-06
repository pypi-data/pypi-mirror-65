#----------------------------------------------------------------------------
# Name:         ldmWidSizeRspWid.py
# Purpose:      ldmWidSizeRspWid.py
#               GUI widget respond on size change
# Author:       Walter Obweger
#
# Created:      20200405
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import wx

class ldmWidSizeRspWid(wx.Control):
    def __init__(self, parent, id=-1,pos=None,size=None, mgr=None):
        wx.Control.__init__(self, parent, id,
                        pos or wx.DefaultPosition,
                        size or wx.DefaultSize,
                        style=wx.NO_BORDER)
        self.mgrGui = mgr

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        size = self.GetClientSize()


        dc.SetFont(wx.NORMAL_FONT)
        dc.SetBrush(wx.WHITE_BRUSH)
        dc.SetPen(wx.WHITE_PEN)
        
        iWdh=size.x
        iHgt=size.y
        iCtrX=iWdh/2
        iCtrY=iHgt/2
        iWdh-=1
        iHgt-=1
        
        dc.DrawRectangle(0, 0, iWdh, iHgt)
        dc.SetPen(wx.BLACK_PEN)
        #dc.DrawLine(0, 0, size.x, size.y)
        #dc.DrawLine(0, size.y, size.x, 0)
        #dc.SetPen(wx.LIGHT_GREY_PEN)
        iMrk=20
        dc.DrawPolygon([(0,0),(iMrk,0),(0,iMrk)])
        dc.DrawPolygon([(iWdh,0),(iWdh-iMrk,0),(iWdh,iMrk)])
        dc.DrawPolygon([(iWdh,iHgt),(iWdh-iMrk,iHgt),(iWdh,iHgt-iMrk)])
        dc.DrawPolygon([(0,iHgt),(iMrk,iHgt),(0,iHgt-iMrk)])
        
        dc.SetPen(wx.LIGHT_GREY_PEN)
        dc.DrawPolygon([
            (iMrk,iMrk),
            (iWdh-iMrk,iMrk),
            (iWdh-iMrk,iHgt-iMrk),
            (iMrk,iHgt-iMrk),
            ])
        dc.SetPen(wx.BLACK_PEN)
        lStr=[]
        def addStr(l,s,iHghGap=3):
            iWdhTxt, iHgtTxt = dc.GetTextExtent(s)
            iHgtTxt += iHghGap
            l.append([s,iWdhTxt, iHgtTxt])
        addStr(lStr,"Size: %d x %d"%(size.x, size.y))
        
        if self.mgrGui:
            pi = self.mgrGui.GetPane(self)
            addStr(lStr,"layer: %d"%(pi.dock_layer))
            addStr(lStr,"dock: %d row: %d pos: %d"%(pi.dock_direction,pi.dock_row,pi.dock_pos))
            addStr(lStr,"prop: %d"%(pi.dock_proportion))
        iHgtTxt=0
        for it in lStr:
            iHgtTxt+=it[2]
        iCtrY-=iHgtTxt>>1
        iHgtTxt=0
        for s,iWdhTxt,iHgtTxt in lStr:
            dc.DrawText(s, iCtrX - (iWdhTxt/2), iCtrY)
            iCtrY+=iHgtTxt
    def OnEraseBackground(self, event):
        pass
    def OnSize(self, event):
        self.Refresh()
