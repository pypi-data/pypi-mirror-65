#----------------------------------------------------------------------------
# Name:         ldmStorageFolder.py
# Purpose:      storage folder content
#
# Author:       Walter Obweger
#
# Created:      20200322
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import logging
import traceback

import os

from optparse import OptionParser

from lindworm import __version__
from lindworm.ldmStorage import ldmStorage
from lindworm.ldmOS import getSha

class ldmStorageFolder(ldmStorage):
    def __init__(self,iModeRev=0,sLogger='srgFld',iLv=0,iVerbose=0):
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
        #self.__initCfg__()
    def __initCfg__(self):
        """initialize configuration properties
        """
        try:
            ldmStorage.__initCfg__(self)
            # +++++ beg:initialize
            sOrg='ldmStorage::__initCfg__'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:default configuration
            self.dCfgDft['lSkipDN']=['CVS','.git']
            # ----- end:default configuration
            self.logDbg('end:%s',sOrg)
            return 1
        except:
            self.logTB()
            return -1
    def __initPrc__(self):
        """initialize processing properties
        """
        try:
            ldmStorage.__initPrc__(self)
            # +++++ beg:initialize
            sOrg='ldmStorageFolder::__initDat__'
            self.logDbg('beg:%s',sOrg)
            # ----- end:initialize
            # +++++ beg:initialize data
            self.iCnt=0             # count of directories
            self.iAct=0             # 
            self.iSrcLen=0          # source DN length, used to build relative
            self.lCnt=[]            # files in relative DN
            self.lFdr=[]            # folder list as they arrived, relative DN
            self.dFolder={}         # content cache, relative DN
            # ----- end:initialize data
            self.logDbg('end:%s',sOrg)
            return 1
        except:
            self.logTB()
            return -1
    def clrEnd(self):
        """clear stored file names to process
        """
        iRet=ldmStorage.clrEnd(self)
        self.dCntEnd=None
        return iRet
    def getDatRel(self,sRelDN,sBaseDN=None):
        """get relative content from data
        ### parameter
            sRelDN  ... relative DN
            sBaseDN ... base DN
        ### return
            iRet
                >0  ... okay processing done
                =0  ... okay nop
                <0  ... error
            dDN ... directory content
                dict  ... {'.':...}
                None  ... invalid content
        """
        try:
            # +++++ beg:get relative path list
            iR,dDN=self.getDat(sDef=sBaseDN)
            if iR<1:
                self.oLog.error('getDatRel: sFN:%s iR:%d dDat:%r'%(sBaseDN,iR,self.dDat))
                return -1,None
            if sRelDN=='./':
                lRelDN=['.']
            else:
                lRelDN=sRelDN.split('/')
            #if self.iVerbose>0:
            #    self.logDbg('            lRelDN:%r',lRelDN)
            # ----- end:get relative path list
            # +++++ beg:get dDN storage
            for sDN in lRelDN[1:]:
                if sDN not in dDN:
                    return 0,None
                dDN=dDN[sDN]
            return 1,dDN
            # ----- end:get dDN storage
        except:
            self.logTB()
            return -1,None
    def getDatContent(self,sRoot):
        """get content from data
        ### parameter
            sRoot   ... directory
        ### return
            sCurDN  ... current directory name, relative
            sDN     ... directory content
            sFN     ... file content
        """
        try:
            if self.iVerbose>90:
                self.logDbg('        sRoot:%s',sRoot)
            # +++++ beg:calc relative DN posix style
            sCurDN=sRoot[self.iSrcLen:].replace(os.sep,'/')
            if sCurDN=='':
                sCurDN='./'
            elif sCurDN[0]=='/':
                sCurDN='.'+sCurDN
            else:
                sCurDN='./'+sCurDN
            if self.iVerbose>0:
                self.logDbg('        sCurDN:%s',sCurDN)
            # ----- end:calc relative DN posix style
            # +++++ beg:prepare dDN storage
            iR,dDN=self.getDat()
            if iR<1:
                self.oLog.error('getDat() iR:%d dDN:%r'%(iR,dDN))
                dDN={}
            else:
                if self.iVerbose>0:
                    lKey=list(dDN.keys())
                    lKey.sort()
                    self.logDbg('            getDat() iR:%d dDN keys:%r',iR,lKey)
                if self.iVerbose>95:
                    self.logDbg('            getDat() iR:%d dDN:%r',iR,dDN)
            if sCurDN=='./':
                lCurDN=['.']
                if '.' not in dDN:
                    dDN['.']={}
            else:
                lCurDN=sCurDN.split('/')
            if self.iVerbose>0:
                self.logDbg('            lCurDN:%r',lCurDN)
            # ----- end:prepare dDN storage
            # +++++ beg:get dDN storage
            for sDN in lCurDN[1:]:
                if sDN not in dDN:
                    dDN[sDN]={'.':{}}
                dDN=dDN[sDN]
            dFN=dDN['.']
            # ----- end:get dDN storage
            # +++++ beg:build cache
            self.iCnt+=1
            self.lFdr.append(sCurDN)
            self.dFolder[sCurDN]=dDN
            # ----- end:build cache
            return sCurDN,dDN,dFN
        except:
            self.logTB()
            return None,None,None
    def prcBeg(self,sDef,oRef=None,**kwargs):
        """processing begin, add file name and objects to stack
        ### parameter
            sSrcDN  ... source directory name : str
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
            sOrg='ldmStorageFolder::prcBeg'
            # ----- end:initialize
            # +++++ beg:processing begin
            self.logDbg('beg:%s sDef:%s',sOrg,sDef)
            if self.iVerbose>0:
                self.logDbg('    oRef:%r kwargs:%r',oRef,kwargs)
            dRef={
                'iAct':self.iAct,
                'oRef':oRef,
            }
            iRet=ldmStorage.prcBeg(self,sDef,oRef=dRef,**kwargs)
            if iRet>0:
                self.iAct=0
            self.logDbg('end:%s iRet:%d',sOrg,iRet)
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
            sOrg='ldmStorageFolder::prcExc'
            # ----- end:initialize
            # +++++ beg:get definition
            iRet,sDef=self.getDef()
            if iRet<1:
                self.logDbg('skp:%s iRet:%d empty stack',sOrg,iRet)
                return iRet
            self.logDbg('beg:%s sDef:%s',sOrg,sDef)
            if self.iVerbose>0:
                self.logDbg('    kwargs:%r',kwargs)
            self.iSrcLen=len(sDef)
            # ----- end:get definition
            # +++++ beg:get folder list to skip
            iR,lSkipDN=self.getCfg('lSkipDN')
            if self.iVerbose>0:
                self.logDbg('    iR:%d lSkipDN:%r',iR,lSkipDN)
            # ----- end:get folder list to skip
            # +++++ beg:walk through directory recursive
            for sRoot,lDN,lFN in os.walk(sDef):
                #sCurDN='./'+sRoot[iSrcLen:].replace(os.sep,'/')
                if self.iVerbose>90:
                    self.logDbg('        sRoot:%s',sRoot)
                sCurDN,dDN,dFN=self.getDatContent(sRoot)
                #if self.iVerbose>0:
                #    self.logDbg('        sCurDN:%s',sCurDN)
                #dFiles={}
                #dContent={'.':dFiles}
                #self.lFdr.append(sCurDN)
                #self.dFolder[sCurDN]=dContent
                if dFN is not None:
                    for sFN in lFN:
                        iR,oRef=self.getRef()
                        iR,dStat=self.getStat(sRoot,sFN,oRef,**kwargs)
                        if iR>0:
                            if self.iVerbose>0:
                                self.logDbg('          sFN:%s dStat:%r',sFN,dStat)
                            dFN[sFN]=dStat
                if self.iVerbose>5:
                    iLenFN=len(dFN)
                    self.logDbg('        sCurDN:%s iLenFN:%r',sCurDN,iLenFN)
                for sSkipDN in lSkipDN:
                    if sSkipDN in lDN:
                        lDN.remove(sSkipDN)
            # ----- end:walk through directory recursive
            # +++++ beg:finalize
            if self.iVerbose>90:
                self.logDbg('   :%s sDef:%s dDat:%r',sOrg,sDef,self.dDat)
            self.logDbg('end:%s iRet:%d',sOrg,iRet)
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def prcEnd(self,**kwargs):
        """processing end
        ### parameter
            *kwargs ... flexible keyword argument
            
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
            sOrg='ldmStorageFolder::prcEnd'
            # ----- end:initialize
            # +++++ beg:processing end
            self.logDbg('beg:%s len(lFdr):%d kwargs:%r',sOrg,
                                len(self.lFdr),kwargs)
            iRet=ldmStorage.prcEnd(self,**kwargs)
            if iRet>0:
                # +++++ beg:revert current file info
                #self.iAct=iMarkerAct    # revert current file line back
                # ----- end:revert current file info
                if self.iVerbose>5:
                    self.logDbg('    %s iAct:%5d iCnt:%6d sDefEnd:%s',sOrg,
                                    self.iAct,self.iCnt,self.sDefEnd)
                if self.iVerbose>95:
                    self.logDbg('   :%s oDatEnd:%r',sOrg,
                                    self.oDatEnd)
                # +++++ beg:loop through folders
                iOfsFdr=0
                lCntKey=['sz','iDN','iFN',]
                dCntDef={
                    'sz':0,
                    'iDN':0,
                    'iFN':0,
                }
                for sRelDN in self.lFdr:
                    iR,dDN=self.getDatRel(sRelDN,sBaseDN=self.sDefEnd)
                    if self.iVerbose>5:
                        self.logDbg('   :%s sRelDN:%s iR:%d sDefEnd:%r',sOrg,
                                        sRelDN,iR,self.sDefEnd)
                    iSz=0
                    iLenFN=0
                    iLenDN=0
                    if iR>0:
                        if self.iVerbose>5:
                            self.logDbg('   :%s sRelDN:%s iR:%d len(dDN):%d',sOrg,
                                            sRelDN,iR,len(dDN))
                        if self.iVerbose>95:
                            self.logDbg('   :%s sRelDN:%s iR:%d dDN:%r',sOrg,
                                            sRelDN,iR,dDN)
                        dFN=dDN.get('.',None)
                        iLenDN=len(dDN)-1
                        if dFN is not None:
                            for sFN,dStat in dFN.items():
                                iSz+=dStat.get('sz',0)
                                iLenFN+=1
                    dCnt={
                        'sRelDN':sRelDN,
                        'sz':iSz,
                        'iDN':iLenDN,
                        'iFN':iLenFN,
                        }
                    self.lCnt.append(dCnt)
                    # +++++ beg:update count total
                    for sK in lCntKey:
                        dCntDef[sK]=dCntDef[sK]+dCnt[sK]
                    # ----- end:update count total
                    iOfsFdr+=1
                # ----- end:loop through folders
                # +++++ beg:post processing
                self.dCntEnd=dCntDef
                iR=self.prcPost(**kwargs)
                # ----- end:post processing
                if self.iVerbose>5:
                    self.logDbg('   :%s lCnt:%r',sOrg,self.lCnt)
            self.logDbg('end:%s iRet:%d',sOrg,iRet)
            # ----- end:processing end
            return iRet
        except:
            self.logTB()
            return -1
    def prcPost(self,**kwargs):
        """processing end
            **kwargs ... flexible keyword argument
                iShaMB  ... data to calculate sha in MB 
        ### return
            iRet    ... return code
                >0  ... okay processing done
                =0  ... okay nop
                <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            sOrg='ldmStorageFolder::prcPost'
            iShaMB=kwargs.get('iShaMB',0)
            # ----- end:initialize
            if self.sDefEnd is None:
                self.logDbg('skp:%s iRet:%d empty definition,'
                                'prcEnd has to be call before',sOrg,iRet)
                return iRet
            # +++++ beg:folder post processing
            iOfsFld=-1
            iCntFN=0
            self.logDbg('beg:%s sDefEnd:%s len(lFdr):%d kwargs:%r',sOrg,
                                self.sDefEnd,len(self.lFdr),kwargs)
            oNty=kwargs.get('oNty',None)
            if oNty is not None:
                self.logDbg('    dCntEnd:%r',self.dCntEnd)
                oNty.SetMax(self.dCntEnd['iFN'])
            for sRelDN in self.lFdr:
                iOfsFld+=1
                if sRelDN in self.dFolder:
                    if oNty is not None:
                        oNty.SetStatus(sRelDN)
                        oNty.IncStatus()
                    sDN='/'.join([self.sDefEnd,sRelDN])
                    dDN=self.dFolder[sRelDN]
                    if self.iVerbose>5:
                        self.logDbg('   :%s sRelDN:%s len(dDN):%d',sOrg,
                                        sRelDN,len(dDN))
                    if self.iVerbose>9:
                        self.logDbg('    dDN:%r',dDN)
                    if '.' in dDN:
                        dFN=dDN['.']
                        # +++++ beg:calc sha fingerprint
                        for sFN,dStat in dFN.items():
                            iCntFN+=1
                            if oNty is not None:
                                #oNty.SetStatus(sFN)
                                #oNty.IncStatus()
                                oNty.SetVal(iCntFN)
                            sSha=getSha(sFN,iMB=iShaMB,
                                        sDN=sDN,
                                        oLog=self.oLog)
                            if self.iVerbose>5:
                                self.logDbg('      sFN:%s sha:%s',sFN,
                                                sSha)
                            dStat['sha']=sSha
                        # ----- end:calc sha fingerprint
            # ----- end:folder post processing
            #if oNty is not None:
            #S    oNty.clrStatus()
            self.logDbg('end:%s iRet:%d',sOrg,iRet)
            return iRet
        except:
            self.logTB()
            return -1
    def getStatDct(self,sFN,oStat,dStat,oRef,**kwargs):
        return 0
    def getStat(self,sDN,sFN,oRef,**kwargs):
        try:
            if sDN is not None:
                sTmpFN=os.path.join(sDN,sFN)
            else:
                sTmpFN=sFN
            if os.path.exists(sTmpFN):
                # +++++ beg:read file status information
                oStat=os.stat(sTmpFN)
                # ----- end:read file status information
                # +++++ beg:
                dStat={
                    'sz':oStat.st_size,
                }
                iR=self.getStatDct(sTmpFN,oStat,dStat,oRef,**kwargs)
                return 1,dStat
            return 0,None
        except:
            self.logTB()
            return -1,None

def execMain(sSrcDN='.',
                sBldDN=None,
                sBldFN=None,
                sCfgFN=None,
                iShaMB=1,
                iVerbose=0):
    """main function to perform conversion
    """
    try:
        # +++++ beg:
        # ----- end:
        # +++++ beg:
        logging.debug('beg:execMain')
        iRet=0
        # ----- end:
        # +++++ beg:
        oFld=ldmStorageFolder(iVerbose=iVerbose)
        iRet=oFld.loadCfg(sCfgFN)
        # ----- end:
        # +++++ beg:
        oFld.prcBeg(sSrcDN,oRef=None)
        oFld.prcExc()#(oGtrMD=self)
        iRetFdr=oFld.prcEnd(iShaMB=iShaMB)
        if iRetFdr>0:
            iRet+=1
        # ----- end:
        # +++++ beg:
        if iRetFdr>0:
            iRetSave=oFld.saveDat(sBldFN,sDN=sBldDN,
                                lKey=[oFld.sDefEnd],
                                sAtr='dDat')
        # ----- end:
        # +++++ beg:
        logging.debug('end:execMain iRet:%d'%(iRet))
        # ----- end:
        return iRet
    except:
        logging.error(traceback.format_exc())
        return -1

def main(args=None):
    # +++++ beg:
    # ----- end:
    
    # +++++ beg:init
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
            default='.',
            help='source folder',metavar='path/to/folder/to/read',
            )
    oParser.add_option('','--bldDN',dest='sBldDN',
            default=None,
            help='build directory',metavar='path/to/output/folder',
            )
    oParser.add_option('','--otBldFN',dest='sBldFN',
            default=None,
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
    # ----- end:parse command line
    # +++++ beg:prepare logging
    import lindworm.logUtil as logUtil
    logUtil.logInit(opt.sLogFN,iLevel=logging.DEBUG)
    # ----- end:prepare logging
    # +++++ beg:status
    print('logging file:%r'%(opt.sLogFN))
    # ----- end:status
    # +++++ beg:perform main action
    iRet=execMain(sSrcDN=opt.sSrcDN,
                sBldDN=opt.sBldDN,
                sBldFN=opt.sBldFN,
                sCfgFN=opt.sCfgFN,
                iVerbose=iVerbose)
    # ----- end:perform main action
    # +++++ beg:finished
    print('\nend processing')
    print('   iRet:%r'%(iRet))
    # ----- end:finished

if __name__=='__main__':
    # +++++ beg:call entry point
    main(args=None)
    # ----- end:call entry point
