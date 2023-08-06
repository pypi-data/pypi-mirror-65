#----------------------------------------------------------------------------
# Name:         lndMD.py
# Purpose:      MD class
#
# Author:       Walter Obweger
#
# Created:      20200108
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import logging
import traceback
import os.path

from lindworm.ldmStorageLine import ldmStorageLine
from lindworm.ldmStr import ldmStr

class ldmMD(ldmStorageLine):
    SEP_HDR='.'
    def __init__(self,sFN,sLogger='',iLv=1,
                 iSkipDN=-1,iVerbose=0):
        """constructor
        ### parameter
            iModeRev    ... reverse processing
                    1   ... FILO, first in last out
                    0   ... FIFO, first in first out
            sLogger     ... log origin
            iLv         ... logging level
            iVerbose    ... higher values add more logs
        """
        ldmStorageLine.__init__(self,
                    iModeRev=0,
                    sLogger=sLogger,
                    iLv=iLv,
                    iVerbose=iVerbose)
        self.sFullFN=sFN
        self.oStr=ldmStr()
        sTmpDN,sTmpFN=os.path.split(sFN)
        self.sDN=sTmpDN
        self.sFN=sTmpFN
        self.iSkipDN=iSkipDN
    def __initDat__(self):
        """initialize data properties
        """
        try:
            sOrg='ldmStorage::__initDat__'
            self.oLog.debug('beg:%s'%(sOrg))
            # +++++ beg:initialize parent
            ldmStorageLine.__initDat__(self)
            # ----- end:initialize parent
            # +++++ beg:initialize data
            self.lHdr=[]        # list header per level during processing
            self.dHdr={}        # dictionary header 
            self.lHdrNavLv=[]   # list header navigation and level
            # ----- end:initialize data
            self.oLog.debug('end:%s'%(sOrg))
            return 1
        except:
            self.logTB()
            return -1
    #def clr(self):
    #    """clear data properties
    #    """
    #    self.__initDat__()
    def getHdrNavLv(self,iOfs=0):
        """get header level, maximal 6 allowed
        ### parameter
            iOfs    ... offset to header
        ### return
            sNav    ... navigation data
            sHdr    ... header
            iLv     ... level, 1 to 6, -1= out of range
        """
        try:
            if len(self.lHdrNavLv)>iOfs:
                return self.lHdrNavLv[iOfs]
            return '','',-1
        except:
            self.logTB()
            return '','',-1
    def getHdrLv(self,sLine):
        """get header level, maximal 6 allowed
        ### return
            >0  ... okay header found
            =0  ... okay nop
            <0  ... error
        """
        try:
            sTmp=sLine.strip()
            iLen=min(6,len(sTmp))
            for iOfs in range(iLen):
                if sTmp[iOfs]!='#':
                    return iOfs
            return 0
        except:
            self.logTB()
            return -1
    def bldDat(self,sDef,oRef=None,**kwargs):
        """check definition has been queues/processed already  
        ### parameter
            sDef    ... definition to check
            oRef    ... reference object
            kwargs  ... flexible keyword argument
        ### return
            oDat    ... okay marked for processing done
        """
        try:
            sOrg='ldmMD::bldDat'
            if self.iVerbose>0:
                self.oLog.debug('beg:%s sDef:%s oRef:%r kwargs:%r'%(sOrg,sDef,oRef,kwargs))
            oDat=kwargs.get('oDat',self)
            if self.iVerbose>0:
                self.oLog.debug('end:%s sDef:%s oDat:%r'%(sOrg,sDef,oDat))
            return oDat
        except:
            self.logTB()
            return None
    def handleLink(self,sLink,oGtrMD=None):
        """handle link
        ### parameter
            sLink   ... link data
            oGtrMD  ... global storage
        ### return
            ''      ... changed string
            None    ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmMD::handleLink'
            iVerboseLmt=5
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('beg:%s sLink:%s'%(sOrg,sLink))
            iRet=0
            sNav=None
            oMD=None
            # ----- end:initialize
            # +++++ beg:
            sTmpFN=sLink.lower()
            if sTmpFN.endswith('.md'):
                sFullFN=os.path.join(self.sDN,sLink)
                if os.path.exists(sFullFN)==False:
                    self.oLog.warning("    handleLink return -5 sFullFN:%s file does not exist, skip"%(sFullFN))
                    iRet=-5
                else:
                    sAbsFullFN=os.path.abspath(sFullFN)
                    oMD=ldmMD(sAbsFullFN,
                            sLogger='oMD',
                            iSkipDN=self.iSkipDN,
                            iVerbose=self.iVerbose)
                    if oGtrMD is not None:
                        iRetDone=oGtrMD.prcIsDone(sAbsFullFN)
                        if iRetDone==0:
                            oGtrMD.prcBeg(sAbsFullFN,oDat=oMD,oRef=None)
                        elif iRetDone>0:
                            iRetMD,oMD=oGtrMD.getDat(sAbsFullFN)
                        else:
                            oMD=None
                    else:
                        iRetDone=self.prcIsDone(sAbsFullFN)
                        if iRetDone>0:
                            iRetMD,oMD=self.getDat(sAbsFullFN)
                    if iRetDone==0:
                        iRet=self.prcBeg(sAbsFullFN,oDat=oMD,oRef=None)
                        if iRet>0:
                            # +++++ beg:process sub file
                            oMD.prcBeg(sAbsFullFN,oDat=oMD,oRef=None)
                            oMD.prcExc(oGtrMD=oGtrMD)
                            oMD.prcEnd()
                            # ----- end:process sub file
                    if iRetDone>=0:
                        # +++++ beg:process sub file
                        sNav,sHdr,iLv=oMD.getHdrNavLv()
                        if self.iVerbose>iVerboseLmt:
                            self.oLog.debug('    %s sNav:%r sHdr:%r iLv:%d'%(sOrg,sNav,sHdr,iLv))
                        # ----- end:process sub file
            # ----- end:
            # +++++ beg:finalize
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return sNav
        except:
            self.logTB()
            return None
    def getHdrPrefix(self):
        """get header prefix, reflect origin
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:find file extension
            iPosExt=self.sFN.rfind('.')
            if iPosExt<0:
                iPosExt=len(self.sFN)
                sFN=self.sFN[:iPosExt]
            else:
                sFN=self.sFN
            # ----- end:find file extension
            # +++++ beg:
            sPart1=self.sDN+self.SEP_HDR+sFN
            sPart1=self.oStr.replaceIgnore(sPart1[self.iSkipDN:])
            # ----- end:
            return sPart1
        except:
            self.logTB()
            return ''
    def getHdrIdf(self,sHdr):
        """get header path as string separated by SEP_HDR
        ### parameter
            sHdr    ... header
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iVerboseLmt=10
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('beg: sHdr:%s'%(sHdr))
            iRet=0
            # ----- end:initialize
            # +++++ beg:
            if sHdr is None:
                sHdr=self.SEP_HDR.join(self.lHdr)
            #else:
            #    sHdr=sHdr.strip()
            sHdr=self.oStr.replaceIgnore(sHdr)
            # ----- end:
            # +++++ beg:finalize
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('end: sHdr:%s'%(sHdr))
            # ----- end:finalize
            return sHdr
        except:
            self.logTB()
            return ''
    def setHdr(self,iHdr,sHdr):
        """store heading at proper header location
        ### parameter
            iHdr    ... header level
            sHdr    ... header
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iVerboseLmt=10
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('beg: iHdr:%d sHdr:%s'%(iHdr,sHdr))
            iRet=0
            # ----- end:initialize
            # +++++ beg:update header stack
            iLenHdr=len(self.lHdr)
            if iLenHdr>=iHdr:
                self.lHdr=self.lHdr[:iHdr]
            else:
                for iOfs in range(iLenHdr,iHdr):
                    self.lHdr.append('')
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('     iHdr:%d %d lHdr:%r'%(iHdr,
                                iLenHdr,self.lHdr))
            self.lHdr[iHdr-1]=sHdr
            iRet=iHdr
            # ----- end:update header stack
            # +++++ beg:finalize
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('end: lHdr:%r'%(self.lHdr))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def prcLine(self,iLine,sLine,**kwargs):
        """add line to storage
        ### parameter
            iLine   ... line number : int
            sLine   ... line : str
            oGtrMD   ... gather object
            **kwargs ... flexible keyword argument
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmMD::prcLine'
            iVerboseLmt=0
            iRet=0
            iPosBeg=0
            iIsHdr=0
            iIsLink=0
            iIsImage=0
            iPosLblBeg=-1
            iPosLblEnd=-1
            iPosDatBeg=-1
            iPosDatEnd=-1
            iLen=len(sLine)
            iPosLF=sLine.rfind('\n')
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('beg:%s iLine:%6d sLine:%s'%(sOrg,iLine,sLine[:iPosLF]))
            oGtrMD=kwargs.get('oGtrMD',None)
            # ----- end:initialize
            # +++++ beg:check header
            iHdr=self.getHdrLv(sLine)
            if iHdr>0:
                # +++++ beg:
                iPosLblBeg=iHdr+1
                iPosLblBeg=self.oStr.findWhiteSpace(sLine,iLen,iPosLblBeg,iMode=0)
                iPosLblEnd=self.oStr.findWhiteSpace(sLine,iLen,iPosLblBeg,iMode=1)
                if self.iVerbose>iVerboseLmt:
                    self.oLog.debug('    iHdr:%d iPosLblBeg:%d iPosLblEnd:%d'%(iHdr,iPosLblBeg,iPosLblEnd))
                iPosDatBeg,iPosDatEnd=self.oStr.findBegEnd(sLine,iLen,
                                                    iPosBeg,'{','}')
                if self.iVerbose>iVerboseLmt:
                    self.oLog.debug('    iHdr:%d iPosDatBeg:%d iPosDatEnd:%d'%(iHdr,iPosDatBeg,iPosDatEnd))
                if iPosDatBeg<0:
                    iPosLblEnd=sLine.rfind('\r')
                    if iPosLblEnd<0:
                        iPosLblEnd=iPosLF
                if iPosLblBeg>0:
                    #if iPosLblEnd<0:
                    #    iPosLblEnd=sLine.rfind('\r')
                    #    if iPosLblEnd<0:
                    #        iPosLblEnd=iPosLF
                    if iPosLblEnd>0:
                        sHdr=sLine[iPosLblBeg:iPosLblEnd]
                self.setHdr(iHdr,sHdr)
                # ----- end:
                # +++++ beg:
                #iPosDatBeg=iHdr+1
                if self.iVerbose>iVerboseLmt:
                    self.oLog.debug('    iHdr:%d sHdr:%s'%(iHdr,sHdr))
                if iPosDatBeg>0:
                    iPosLblEnd=iPosDatBeg-1
                    if iPosDatEnd>0:
                        iPosDatBeg=iPosDatBeg+1
                        sTmpDat=sLine[iPosDatBeg:iPosDatEnd]
                        sHdrNav='{#%s}'%(sTmpDat)
                        self.lHdrNavLv.append((sHdrNav[1:-1],sHdr,iHdr))
                    else:
                        self.lHdrNavLv.append((sHdr,sHdr,iHdr))
                else:
                    iPosLblEnd=sLine.rfind('\r')
                    if iPosLblEnd<0:
                        iPosLblEnd=iPosLF
                    sTmpDat=None
                    #sHdr=sLine[iPosDatBeg:iPosLblEnd]
                    sHdrNav='{#%s%s%s}'%(self.getHdrPrefix(),self.SEP_HDR,self.getHdrIdf(sTmpDat))
                    sLine=sLine[:iPosLblEnd]+sHdrNav+sLine[iPosLF:]
                    self.lHdrNavLv.append((sHdrNav[1:-1],sHdr,iHdr))
                iPosBeg=-1
                iIsHdr=1
                # ----- end:
            # ----- end:check header
            # +++++ beg:check link
            while iPosBeg>=0:
                # +++++ beg:clear loop variables
                iIsLink=0
                iIsImage=0
                iPosLblBeg=-1
                iPosLblEnd=-1
                iPosDatBeg=-1
                iPosDatEnd=-1
                # ----- end:clear loop variables
                # +++++ beg:find link start
                iPosLblBeg,iPosLblEnd=self.oStr.findBegEnd(sLine,iLen,
                                                    iPosBeg,'[',']')
                #iPosLblBeg=sLine.find('[',iPosBeg)
                if self.iVerbose>iVerboseLmt:
                    self.oLog.debug('  iPosBeg:%d iPosLblBeg:%d iPosLblEnd:%d '%(iPosBeg,iPosLblBeg,iPosLblEnd))
                if iPosLblBeg>0:
                    if sLine[iPosLblBeg-1]=='!':
                        iIsImage=1
                    else:
                        iIsImage=0
                    if self.iVerbose>iVerboseLmt:
                        self.oLog.debug('  lnk beg found iPosLblBeg:%d iPosLblEnd:%d '
                                        'iIsImage:%d'%(iPosLblBeg,iPosLblEnd,iIsImage))
                # ----- end:find link start
                if iPosLblBeg>=0:
                    # +++++ beg:find link parts
                    #iPosLblEnd=sLine.find(']',iPosLblBeg)
                    if iPosLblEnd>0:
                        iPosDatBeg,iPosDatEnd=self.oStr.findBegEnd(sLine,iLen,
                                                    iPosLblEnd,'(',')')
                        if self.iVerbose>iVerboseLmt:
                            self.oLog.debug('  lnk beg found iPosDatBeg:%d iPosDatEnd:%d '
                                            'iIsImage:%d'%(iPosDatBeg,iPosDatEnd,iIsImage))
                        #iPosDatBeg=sLine.find('(',iPosLblEnd)
                        if iPosDatBeg>0:
                            #iPosDatEnd=sLine.find(')',iPosDatBeg)
                            if iPosDatEnd>0:
                                # found
                                iIsLink=1
                            else:
                                iPosBeg=-1
                        else:
                            if iLen>(iPosLblEnd+2):
                                if sLine[iPosLblEnd+1]==':':
                                    # +++++ beg:find second link part
                                    iPosBeg=-1
                                    iPosDatBeg=self.oStr.findWhiteSpace(sLine,iLen,
                                                        iPosLblEnd+2,
                                                        iMode=0)
                                    if iPosDatBeg>0:
                                        iPosDatEnd=self.oStr.findWhiteSpace(sLine,iLen,
                                                        iPosDatBeg,
                                                        iMode=1)
                                        if iPosDatEnd>0:
                                            # found
                                            iIsLink=1
                                        else:
                                            iPosBeg=-1
                                    else:
                                        iPosBeg=-1
                                    # ----- end:find second link part
                                else:
                                    iPosBeg=-1
                            else:
                                iPosBeg=-1
                    else:
                        iPosBeg=-1
                    # ----- end:find link parts
                else:
                    iPosBeg=-1
                # ----- end:check link
                # +++++ beg:process link
                if self.iVerbose>20:
                    self.oLog.debug('  iPosBeg:%d iIsLink:%d iIsImage:%d'
                                    ''%(iPosBeg,iIsLink,iIsImage))
                if iIsLink>0:
                    # +++++ beg:link info
                    if self.iVerbose>20:
                        self.oLog.debug('  iPosBeg:%d iPosLblBeg:%d iPosLblEnd:%d '
                                    'iPosDatBeg:%d iPosDatEnd:%d'%(iPosBeg,iPosLblBeg,iPosLblEnd,
                                    iPosDatBeg,iPosDatEnd))
                    iPosLblBeg=iPosLblBeg+1
                    iPosDatBeg=iPosDatBeg+1
                    sTmpLbl=sLine[iPosLblBeg:iPosLblEnd]
                    sTmpDat=sLine[iPosDatBeg:iPosDatEnd]
                    if self.iVerbose>5:
                        self.oLog.debug('  sLbl:%s sDat:%s'%(sTmpLbl,sTmpDat))
                    # ----- end:link info
                    # +++++ beg:
                    if iIsImage==0:
                        # +++++ beg:handle link
                        if self.iVerbose>(iVerboseLmt+5):
                            self.oLog.debug('  link found:%s'%(sTmpDat))
                        sReplDat=self.handleLink(sTmpDat,oGtrMD)
                        if sReplDat is not None:
                            sLine=sLine[:iPosDatBeg]+sReplDat+sLine[iPosDatEnd:]
                            iPosDatEnd=iPosDatEnd+(len(sTmpDat)-len(sReplDat))
                            #iPosBeg=iPosDatEnd+1
                        iPosBeg=iPosDatEnd+1
                        # ----- end:handle link
                    else:
                        # +++++ beg:handle link to image
                        if self.iVerbose>(iVerboseLmt+5):
                            self.oLog.debug('  image found:%s'%(sTmpDat))
                        oGtrMD.copyImage(self.sDN,sTmpDat)
                        iPosBeg=iPosDatEnd+1
                        # ----- end:handle link to image
                    # ----- end:
                # ----- end:process link
            # ----- end:check line
            iRet=1
        except:
            self.logTB()
        try:
            # +++++ beg:finalize
            iPosLF=sLine.rfind('\n')
            if self.iVerbose>10:
                self.oLog.debug('  sLine:>%s<'%(sLine[:iPosLF]))
            if self.iVerbose>0:
                self.oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet,sLine
        except:
            self.logTB()
            return -1,sLine
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
            sOrg='ldmMD::prcExc'
            iVerboseLmt=0
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('beg:%s len(lMarker):%d'%(sOrg,
                                len(self.lMarker)))
            if self.iVerbose>0:
                self.oLog.debug('    kwargs:%r'%(kwargs))
            oGtrMD=kwargs.get('oGtrMD',None)
            # ----- end:initialize
            # +++++ beg:memorize file name
            self.sCurDN,self.sCurFN=os.path.split(self.sFN)
            if self.iVerbose>(iVerboseLmt+5):
                self.oLog.debug('    sCurDN:%r sCurFN:%r'%(self.sCurDN,self.sCurFN))
            if self.sCurDN is None:
                self.sCurDN='./'
            if len(self.sCurDN)==0:
                self.sCurDN='./'
            # ----- end:memorize file name
            # +++++ beg:processing end
            iRet=ldmStorageLine.prcExc(self,oGtrMD=oGtrMD)
            if self.iVerbose>(iVerboseLmt+5):
                self.oLog.debug('    %s iRet:%d iCnt:%d iAct:%d len(lLine):%d'%(sOrg,
                            iRet,self.iCnt,self.iAct,len(self.lLine)))
            ldmStorageLine.prcEnd(self)
            # +++++ beg:process referenced files
            lSubFN=self.getLstDef()
            if lSubFN is not None:
                for sSubFN in lSubFN:
                    self.addLine('\r\n')
                    # +++++ beg:get object to process referenced file
                    if oGtrMD is None:
                        iRetMD,oMD=self.getDat(sSubFN)
                    else:
                        iRetMD,oMD=oGtrMD.getDat(sSubFN)
                    if self.iVerbose>0:
                        self.oLog.debug('    %s oGtrMD:%r iRetMD:%d oMD:%r'%(sOrg,oGtrMD,iRetMD,oMD))
                    # ----- end:get object to process referenced file
                    # +++++ beg:process referenced file
                    if iRetMD>0:
                        # +++++ beg:process sub file
                        oMD.prcBeg(sSubFN,oDat=oMD,oRef=None)
                        iR=oMD.prcExc(oGtrMD=oGtrMD)
                        if iR>0:
                            iRet=iRet+1
                        oMD.prcEnd()
                        # ----- end:process sub file
                        # +++++ beg:add lines
                        lLines,iCnt=oMD.getLines()
                        for iAct,sL in lLines:
                            self.addLine(sL)
                        # ----- end:add lines
                    # ----- end:process referenced file
                #iR,sTmpFN,oTmpDat,oTmpRef=oMD.prcEnd()
            iR=self.clrDef()
            # ----- end:process referenced files
            if self.iVerbose>iVerboseLmt:
                self.oLog.debug('end:%s iRet:%d iCnt:%d'%(sOrg,
                                iRet,self.iCnt))
            # ----- end:processing end
            return iRet
        except:
            self.logTB()
            return -1
