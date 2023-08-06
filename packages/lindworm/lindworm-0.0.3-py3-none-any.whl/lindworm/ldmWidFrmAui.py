#----------------------------------------------------------------------------
# Name:         ldmWidFrmAui.py
# Purpose:      ldmWidFrmAui.py
#               frame widget utilizing advanced user interface
# Author:       Walter Obweger
#
# Created:      20200405
# CVS-ID:       $Id$
# Copyright:    (c) 2020 by Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import wx
import wx.aui

from lindworm.ldmWidCore import ldmWidCore
from lindworm.ldmWidSizeRspWid import ldmWidSizeRspWid
from lindworm.ldmWidList import ldmWidList
from lindworm.ldmWidTree import ldmWidTree

#class ldmAuiMpw(aui.AuiMDIParentFrame):
class ldmWidFrmAui(ldmWidCore):
    ID_TBR_File=100
    ID_FILE_OPEN=101
    ID_FILE_SAVE=102
    ID_File_EXIT=190
    ID_EDIT_CUT=201
    ID_EDIT_COPY=202
    ID_EDIT_PASTE=203
    ID_DST=700
    def __initCls__(self,**kwargs):
        self.clsWid=wx.Frame
    def __initWid__(self,**kwargs):
        try:
            self.logDbg('__initWid__')
            # parent,iID,sTitle,oLdmCfg):
            tSz=(640,480)
            #aui.AuiMDIParentFrame.__init__(self, 
            style=wx.DEFAULT_FRAME_STYLE
            #'title','pos',
            self.logDbg('kw:%r',kwargs)
            lArg=['parent','id','title','pos','size','style']
            _args,_kwargs=self.GetWidArgs(kwargs,
                        ['id','name','parent','size','style','title'],
                        {'size':(640,480),'style':style},
                        lArg=lArg)
            #self.logDbg('arg:%r',_args)
            #self.logDbg('kw:%r',_kwargs)
            self.wid=self.clsWid(*_args,**_kwargs)
            self.oApi=wx.aui.AuiPaneInfo()
            self.mgrMain=wx.aui.AuiManager()
            self.mgrMain.SetManagedWindow(self.wid)
            # set frame icon
            #self.SetIcon(images.Mondrian.GetIcon())

            #mb = self.MakeMenuBar()
            #self.SetMenuBar(mb)
            self.__initMenuBar__(**kwargs)
            self.__initStatusBar__(**kwargs)
            self.__initToolBar__(**kwargs)
            self.oApi.Name("nbCenter")
            self.oApi.CenterPane()
            self.oApi.PaneBorder(False)
            self.oApi.Center()
            self.__initPanCt__(**kwargs)
            self.oApi.Left()
            self.__initPanLf__(**kwargs)
            self.oApi.Bottom()
            self.__initPanBt__(**kwargs)
            self.mgrMain.Update()
        except:
            self.logTB()
    def __initToolBar__(self,**kwargs):
        try:
            self.__initTbrFile__(**kwargs)
            self.__initTbrEdit__(**kwargs)
            self.__initTbrDst__(**kwargs)
        except:
            self.logTB()
    def __initTbrFile__(self,**kwargs):
        try:
            oSz=wx.Size(16, 16)
            iStyle =wx.aui.AUI_TB_DEFAULT_STYLE
            #iStyle|=wx.aui.AUI_TB_OVERFLOW
            tbr = wx.aui.AuiToolBar(self.GetWid(),
                        -1,
                        wx.DefaultPosition,
                        size=oSz or wx.DefaultSize,
                        style=iStyle)
            
            bmp=wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN,size=oSz)
            w=tbr.AddTool(self.ID_FILE_OPEN,
                        label="Open",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string='open json file')
            self.BindEvent('mn',self.OnFileOpen,w)
            bmp=wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,size=oSz)
            w=tbr.AddTool(self.ID_FILE_SAVE,
                        label="Save",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string='save json file')
            self.BindEvent('mn',self.OnFileSave,w)

            oApi=wx.aui.AuiPaneInfo().Name('tbrFile')
            oApi.Caption('file toolbar')
            oApi.ToolbarPane().Top()
            self.mgrMain.AddPane(tbr,oApi)
        except:
            self.logTB()
    def __initTbrEdit__(self,**kwargs):
        try:
            oSz=wx.Size(16, 16)
            iStyle =wx.aui.AUI_TB_DEFAULT_STYLE
            #iStyle|=wx.aui.AUI_TB_OVERFLOW
            tbr = wx.aui.AuiToolBar(self.GetWid(),
                        -1,
                        wx.DefaultPosition,
                        size=oSz or wx.DefaultSize,
                        style=iStyle)
            
            bmp=wx.ArtProvider.GetBitmap(wx.ART_CUT,size=oSz)
            w=tbr.AddTool(self.ID_EDIT_CUT,
                        label="Cut",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string='cut')
            self.BindEvent('mn',self.OnEditCut,w)
            bmp=wx.ArtProvider.GetBitmap(wx.ART_COPY,size=oSz)
            w=tbr.AddTool(self.ID_EDIT_COPY,
                        label="Copy",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string='copy')
            self.BindEvent('mn',self.OnEditCopy,w)
            bmp=wx.ArtProvider.GetBitmap(wx.ART_PASTE,size=oSz)
            w=tbr.AddTool(self.ID_EDIT_PASTE,
                        label="Paste",
                        bitmap=bmp,
                        kind=wx.ITEM_NORMAL,
                        short_help_string='paste')
            self.BindEvent('mn',self.OnEditPaste,w)
            
            oApi=wx.aui.AuiPaneInfo().Name('tbrEdit')
            oApi.Caption('edit toolbar')
            oApi.ToolbarPane().Top()
            self.mgrMain.AddPane(tbr,oApi)
        except:
            self.logTB()
    def __initTbrDst__(self,**kwargs):
        try:
            oSz=wx.Size(16, 16)
            iStyle =wx.aui.AUI_TB_DEFAULT_STYLE
            iStyle|=wx.aui.AUI_TB_VERTICAL
            tbr = wx.aui.AuiToolBar(self.GetWid(),
                        -1,
                        wx.DefaultPosition,
                        size=oSz or wx.DefaultSize,
                        style=iStyle)
            #tbr.SetToolBitmapSize(oSz)
            
            bmp=wx.ArtProvider.GetBitmap(wx.ART_HARDDISK,size=oSz)
            w=tbr.AddTool(self.ID_DST+0,
                        label="00",
                        bitmap=bmp,
                        kind=wx.ITEM_RADIO,
                        short_help_string='destination 00')
            self.BindEvent('mn',self.OnDst00,w)
            #AUI_BUTTON_STATE_NORMAL
            #AUI_BUTTON_STATE_HOVER
            #AUI_BUTTON_STATE_PRESSED
            #AUI_BUTTON_STATE_DISABLED
            #AUI_BUTTON_STATE_HIDDEN
            w.SetState(wx.aui.AUI_BUTTON_STATE_CHECKED)
            
            bmp=wx.ArtProvider.GetBitmap(wx.ART_HARDDISK,size=oSz)
            w=tbr.AddTool(self.ID_DST+1,
                        label="01",
                        bitmap=bmp,
                        kind=wx.ITEM_RADIO,
                        short_help_string='destination 01')
            self.BindEvent('mn',self.OnDst01,w)
            
            oApi=wx.aui.AuiPaneInfo().Name('tbrDst')
            oApi.Caption('destination toolbar')
            oApi.ToolbarPane().Right()
            oApi.GripperTop().TopDockable(False).BottomDockable(False)
            self.mgrMain.AddPane(tbr,oApi)
        except:
            self.logTB()
    def __initPanCt__(self,**kwargs):
        try:
            iStyle =wx.aui.AUI_NB_TOP | wx.aui.AUI_NB_TAB_SPLIT 
            iStyle|=wx.aui.AUI_NB_SCROLL_BUTTONS
            #iStyle|=wx.aui.AUI_NB_TAB_MOVE
            #iStyle|=wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB
            #iStyle|=wx.aui.AUI_NB_MIDDLE_CLICK_CLOSE
            wNb=wx.aui.AuiNotebook(self.GetWid(), -1, 
                        (0,0),
                        wx.Size(430, 200),
                        style=iStyle)
            self.mgrMain.AddPane(wNb,self.oApi)
            self.oApi.Name("nbCenter")
            self.oApi.CenterPane()
            self.oApi.PaneBorder(False)
            return wNb
            oWid=ldmWidSizeRspWid(wNb, -1,mgr=self.mgrMain)
            wNb.AddPage(oWid,'first',True)
        except:
            self.logTB()
        return None
    def __initPanLf__(self,**kwargs):
        try:
            oWid=ldmWidTree(parent=self.GetWid(),iLv=0,size=(200,120),sLogger='tr')
            self.oApi.Name('trDat')
            self.oApi.Caption("tree 0")
            self.oApi.Dockable(True)
            self.mgrMain.AddPane(oWid.GetWid(),self.oApi)
        except:
            self.logTB()
    def __initPanBt__(self,**kwargs):
        try:
            oWid=ldmWidList(parent=self.GetWid(),iLv=0,
                        size=(200,120),sLogger='lstLog',
                        lCol=[
                            ['No',      'lf',80],
                            ['Info',    'lf',250],
                            ['Status',  'rg',60],
                        ])
            self.oApi.Name('lstLog')
            self.oApi.Caption("logging")
            self.mgrMain.AddPane(oWid.GetWid(),self.oApi)
        except:
            self.logTB()
    def __initMenuBar__(self,**kwargs):
        try:
            mnBar = wx.MenuBar()

            mnFile=wx.Menu()
            mnFile.Append(self.ID_FILE_OPEN, "&Open\tCtrl+O")
            mnFile.Append(self.ID_FILE_SAVE, "&Save\tCtrl+S")
            w=mnFile.Append(wx.ID_EXIT, "Exit\tAlt+X")
            self.BindEvent('mn',self.OnExit,w)
            
            mnEdit=wx.Menu()
            mnEdit.Append(self.ID_EDIT_CUT, "Cut\tCtrl+X")
            mnEdit.Append(self.ID_EDIT_COPY, "Copy\tCtrl+C")
            mnEdit.Append(self.ID_EDIT_PASTE, "Paste\tCtrl+V")

            mnHelp=wx.Menu()
            mnHelp.Append(wx.ID_ABOUT, "About...")

            mnBar.Append(mnFile, "&File")
            mnBar.Append(mnEdit, "&Edit")
            mnBar.Append(mnHelp, "&Help")

            self.wid.SetMenuBar(mnBar)
        except:
            self.logTB()
    def __initStatusBar__(self,**kwargs):
        try:
            self.wid.CreateStatusBar()
        except:
            self.logTB()
    def __initEvt__(self,**kwargs):
        try:
            #self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.OnDropDownToolbarItem, id=ID_DropDownToolbarItem)
            #self.Bind(aui.EVT_AUI_PANE_CLOSE, self.OnPaneClose)
            #self.Bind(aui.EVT_AUINOTEBOOK_ALLOW_DND, self.OnAllowNotebookDnD)
            #self.Bind(aui.EVT_AUINOTEBOOK_PAGE_CLOSE, self.OnNotebookPageClose)

            #self.Bind(aui.EVT_AUI_PANE_FLOATING, self.OnFloatDock)
            #self.Bind(aui.EVT_AUI_PANE_FLOATED, self.OnFloatDock)
            #self.Bind(aui.EVT_AUI_PANE_DOCKING, self.OnFloatDock)
            #self.Bind(aui.EVT_AUI_PANE_DOCKED, self.OnFloatDock)
            
            self.wid.Bind(wx.EVT_ERASE_BACKGROUND, self.OnFrmEraseBackground)
            self.wid.Bind(wx.EVT_SIZE, self.OnFrmSize)
            self.wid.Bind(wx.EVT_CLOSE, self.OnFrmClose)
        except:
            self.logTB()
    def GetDockArt(self):
        return self.mgrMain.GetArtProvider()
    def OnFileOpen(self,evt):
        try:
            self.logDbg('OnFileOpen')
        except:
            self.logTB()
    def OnFileSave(self,evt):
        try:
            self.logDbg('OnFileSave')
        except:
            self.logTB()
    def OnEditCut(self,evt):
        try:
            self.logDbg('OnEditCut')
        except:
            self.logTB()
    def OnEditCopy(self,evt):
        try:
            self.logDbg('OnEditCopy')
        except:
            self.logTB()
    def OnEditPaste(self,evt):
        try:
            self.logDbg('OnEditPaste')
        except:
            self.logTB()
    def OnDst00(self,evt):
        try:
            self.logDbg('OnDst00')
        except:
            self.logTB()
    def OnDst01(self,evt):
        try:
            self.logDbg('OnDst01')
        except:
            self.logTB()
    def OnFrmEraseBackground(self, event):
        event.Skip()
    def OnFrmSize(self, event):
        event.Skip()
    def OnFrmClose(self, event):
        #self.timer.Stop()
        self.mgrMain.UnInit()
        event.Skip()
    def OnExit(self, event):
        try:
            self.logDbg('OnExit')
            self.wid.Close(True)
        except:
            self.logTB()
    def DoUpdate(self):
        self.mgrMain.Update()
        self.Refresh()
