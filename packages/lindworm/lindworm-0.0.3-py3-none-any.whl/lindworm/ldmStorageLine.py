#----------------------------------------------------------------------------
# Name:         ldmStorageLine.py
# Purpose:      storage for lines
#
# Author:       Walter Obweger
#
# Created:      20200104
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import logging
import traceback

from lindworm.ldmStorage import ldmStorage

class ldmStorageLine(ldmStorage):
    def __init__(self,iModeRev=0,sLogger='',iLv=1,iVerbose=0):
        """constructor
        ### parameter
            iModeRev    ... reverse processing
                    1   ... FILO, first in last out
                    0   ... FIFO, first in first out
            sLogger     ... log origin
            iLv         ... logging level
            iVerbose    ... higher values add more logs
        """
        ldmStorage.__init__(self,iModeRev=iModeRev,
                            sLogger=sLogger,iLv=iLv,
                            iVerbose=iVerbose)
        #self.__initDat__()
    def __initPrc__(self):
        """initialize data properties
        """
        try:
            ldmStorage.__initPrc__(self)
            # +++++ beg:initialize
            sOrg='ldmStorageFolder::__initDat__'
            self.oLog.debug('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:initialize data
            self.sEnc=None
            self.lLine=[]
            self.iCnt=0
            self.iAct=-1
            self.lMarker=[]
            # ----- end:initialize data
            self.oLog.debug('end:%s'%(sOrg))
        except:
            self.logTB()
            return -1
    def prcBeg(self,sDef,oRef=None,**kwargs):
        """processing begin, add file name and objects to stack
        ### parameter
            sFN     ... file name : str
            oDat    ... data object
            oRef    ... reference object
            kwargs  ... flexible keyword argument
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmStorageLine::prcBeg'
            # ----- end:initialize
            # +++++ beg:processing begin
            if self.iVerbose>0:
                self.oLog.debug('beg:%s sDef:%s'%(sOrg,sDef))
            dRef={
                'iAct':self.iAct,
                'oRef':oRef,
            }
            iRet=ldmStorage.prcBeg(self,sDef,oRef=dRef,**kwargs)
            if iRet>0:
                self.iAct=0
            if iRet>=0:
                self.lMarker.append([sDef,self.iCnt,self.iAct])
            if self.iVerbose>0:
                self.oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
            # ----- end:processing begin
            return iRet
        except:
            self.logTB()
            return -1
    def prcExc(self,**kwargs):
        """processing execution
        ### parameter
            **kwargs ... flexible keyword argument
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmStorageLine::prcExc'
            # ----- end:initialize
            # +++++ beg:
            iRet,sDef=self.getDef()
            if iRet<1:
                self.oLog.debug('skp:%s iRet:%d empty stack'%('ldmStorageLine::prcExc',iRet))
                return iRet
            self.oLog.debug('beg:%s sDef:%s'%(sOrg,sDef))
            if self.iVerbose>0:
                self.oLog.debug('    kwargs:%r'%(kwargs))
            iLine=0
            with open(sDef,'r',encoding=self.sEnc) as oFileIn:
                iLine=1
                for sLine in oFileIn:
                    # +++++ beg:process line
                    if self.iVerbose>50:
                        self.oLog.debug('  iLine:%04d sLine:>%s<'%(iLine,sLine))
                    iR,sL=self.prcLine(iLine,sLine,**kwargs)
                    if self.iVerbose>50:
                        self.oLog.debug('  iLine:%04d iR:%d sL:>%s<'%(iLine,iR,sL))
                    if iR>0:
                        self.addLine(sL)
                    iLine=iLine+1
                    # ----- end:process line
            self.oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
            # ----- end:
            return iRet
        except:
            self.logTB()
            return -1
    def prcEnd(self,**kwargs):
        """processing end
        ### parameter
            **kwargs ... flexible keyword argument
            
            use updated properties to access current properties to be finalized
            self.sDefEnd    ... definition
            self.oArgEnd    ... keyword arguments passed at prcBeg
            self.oDatEnd    ... data object
            self.oRefEnd    ... reference object
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmStorageLine::prcEnd'
            # ----- end:initialize
            # +++++ beg:processing end
            if self.iVerbose>0:
                self.oLog.debug('beg:%s len(lMarker):%d'%(sOrg,
                                len(self.lMarker)))
            iRet=ldmStorage.prcEnd(self,**kwargs)
            if iRet>0:
                #sMarkerFN,iMarkerCnt,iMarkerAct=self.lMarker[-1]
                #del self.lMarker[-1]
                #if sFN!=sMarkerFN:
                #    self.oLog.error('    %s sFN:%s sMarkerFN:%s mismatch'%('ldmStorageLine::prcEnd',
                #                    sFN,sMarkerFN))
                # +++++ beg:revert current file info
                #self.iAct=iMarkerAct    # revert current file line back
                # ----- end:revert current file info
                if self.iVerbose>5:
                    self.oLog.debug('    %s iAct:%5d iCnt:%6d sDefEnd:%s'%('ldmStorageLine::prcEnd',
                                    self.iAct,self.iCnt,self.sDefEnd))
            if self.iVerbose>0:
                self.oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
            # ----- end:processing end
            return iRet
        except:
            self.logTB()
            return -1
    def addLine(self,sLine):
        """add line to storage
        ### parameter
            sLine   ... line to add, including line feed character(s)
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            # ----- end:initialize
            # +++++ beg:add line to storage
            if sLine is not None:
                self.iAct=self.iAct+1
                self.lLine.append((self.iAct,sLine))
                self.iCnt=self.iCnt+1
                iRet=1
            if self.iVerbose>15:
                self.oLog.debug('%s iRet:%d iAct:%5d %-20s'%('ldmStorageLine::addLine',
                                iRet,self.iAct,sLine[:18]))
            # ----- end:add line to storage
            return iRet
        except:
            self.logTB()
            return -1
    def getLines(self):
        """add line to storage
        ### return
            lLine   ... list lines
            iCnt    ... line count
        """
        return self.lLine,self.iCnt
    def prcLine(self,iLine,sLine,**kwargs):
        """process line
        ### parameter
            iLine   ... line number : int
            sLine   ... line : str to process, including line feed character(s)
            **kwargs ... flexible keyword argument
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmStorageLine::prcLine'
            # ----- end:initialize
            # +++++ beg:process line
            if self.iVerbose>10:
                self.oLog.debug('beg:%s len(sLine):%d'%(sOrg,
                                iLine,len(sLine)))
            iRet=1
            if self.iVerbose>10:
                self.oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
            # ----- end:process line
            return iRet,sLine
        except:
            self.logTB()
            return -1,None
