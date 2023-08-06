#----------------------------------------------------------------------------
# Name:         lndStorage.py
# Purpose:      storage base class
#
# Author:       Walter Obweger
#
# Created:      20200104
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import os
import logging
import traceback
import json

from lindworm.logUtil import logGet
from lindworm.logUtil import ldmUtilLog
import lindworm.ldmOS as ldmOS

class ldmStorage(ldmUtilLog):
    def __init__(self,iModeRev=0,sLogger='',iLv=1,iVerbose=0):
        """constructor
        ### parameter
            iModeRev    ... reverse processing
                    1   ... FILO, first in last out
                    0   ... FIFO, first in first out
            sLogger     ... log origin
            iLv         ... log level short
            iVerbose    ... higher values add more logs
        """
        ldmUtilLog.__init__(self,sLogger=sLogger,iLv=iLv,
                            iVerbose=iVerbose)
        #self.iVerbose=iVerbose
        #self.oLog=logGet(sLogger,iLevel)
        self.__initCfg__()
        self.__initDef__()
        self.__initDat__()
        self.__initPrc__()
        self.clrEnd()
        self.dCfgDft['iModeRev']=iModeRev
    def __initCfg__(self):
        """initialize configuration properties
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::__initCfg__'
            self.oLog.debug('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:initialize configuration attributes
            self.sCfgFN=''
            self.dCfg=None
            self.dCfgDft={
                'lAtr':['dDat']
                }
            # ----- end:initialize configuration attributes
            self.oLog.debug('end:%s'%(sOrg))
            return 1
        except:
            self.logTB()
            return -1
    def __initDef__(self):
        """initialize definition properties
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::__initDef__'
            self.oLog.debug('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:initialize data
            self.lDef=[]        # list definition been processed
            self.dArg={}        # arguments data
            self.dRef={}        # reference data
            # ----- end:initialize data
            self.oLog.debug('end:%s'%(sOrg))
            return 1
        except:
            self.logTB()
            return -1
    def __initDat__(self):
        """initialize data properties
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::__initDat__'
            self.oLog.debug('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:initialize data
            self.dDat={}        # dictionary processed files, performance
            # ----- end:initialize data
            self.oLog.debug('end:%s'%(sOrg))
            return 1
        except:
            self.logTB()
            return -1
    def __initPrc__(self):
        """initialize processing properties
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::__initPrc__'
            self.oLog.debug('beg:%s'%(sOrg))
            # ----- end:initialize
            # +++++ beg:initialize data
            self.iAct=-1                    # dictionary processed files, performance
            # ----- end:initialize data
            self.oLog.debug('end:%s'%(sOrg))
            return 1
        except:
            self.logTB()
            return -1
    def clrAll(self):
        """clear data properties
        """
        self.clrDef()
        self.clrDat()
        self.clrEnd()
        self.__initPrc__()
    def clrDef(self):
        """clear stored file names to process
        """
        iRet=len(self.lDef)
        self.lDef=[]
        return iRet
    def clrDat(self):
        """clear data properties
        """
        self.__initDat__()
    def clrEnd(self):
        """clear stored file names to process
        """
        self.sDefEnd=None
        self.oArgEnd=None
        self.oDatEnd=None
        self.oRefEnd=None
        return 1
    def getLstDef(self):
        """get definition list
        ### return
            []  ... list of definition stored
        """
        try:
            return self.lDef
        except:
            self.logTB()
            return []
    def getDef(self):
        """get current file name
        ### return
            iRet    ... return code
                >0  ... okay processing done
                =0  ... okay nop
                <0  ... error
            sFN     ... file name : str
        """
        try:
            if len(self.lDef)>0:
                if self.getCfg('iModeRev',sType='int',oDft=0)==1:
                    sDef=self.lDef[-1]
                else:
                    sDef=self.lDef[0]
                return 1,sDef
            return 0,None
        except:
            self.logTB()
            return -1,None
    def getDat(self,sDef=None):
        """current data object
        ### parameter
            sDef    ... definition to search, None = get current reference
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            if sDef is None:
                iRet,sDef=self.getDef()
            else:
                iRet=1
            if iRet>0:
                if sDef in self.dDat:
                    oDat=self.dDat[sDef]
                    return 1,oDat
            return 0,None
        except:
            self.logTB()
            return -1,None
    def getRef(self,sDef=None):
        """get current reference object
        ### parameter
            sDef    ... definition to search, None = get current reference
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            if sDef is None:
                iRet,sDef=self.getDef()
            else:
                iRet=1
            if iRet>0:
                if sDef in self.dDat:
                    oRef=self.dRef[sDef]
                    return 1,oRef
            return 0,None
        except:
            self.logTB()
            return -1,None
    def prcIsDone(self,sDef):
        """check definition has been queues/processed already  
        ### parameter
            sDef ... definition to check
        ### return
            >0  ... okay marked for processing done
            =0  ... okay unknown file name
            <0  ... error
        """
        try:
            if sDef in self.dDat:
                iRet=1
            else:
                iRet=0
            self.oLog.debug('%s sDef:%s iRet:%d'%('ldmStorage::prcIsDone',
                            sDef,iRet))
            return iRet
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
            sOrg='ldmStorage::bldDat'
            if self.iVerbose>5:
                self.oLog.debug('%s sDef:%s oRef:%r kwargs:%r'%(sOrg,sDef,oRef,kwargs))
            elif self.iVerbose>0:
                self.oLog.debug('%s sDef:%s'%(sOrg,oRef))
            return {}
        except:
            self.logTB()
            return None
    def prcBeg(self,sDef,oRef=None,**kwargs):
        """processing begin, add file name and objects to stack
        ### parameter
            sDef    ... definition name : str
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
            sOrg='ldmStorage::prcBeg'
            # ----- end:initialize
            # +++++ beg:add file name and auxillary objects to storage
            self.oLog.debug('beg:%s sDef:%s'%(sOrg,sDef))
            if self.prcIsDone(sDef)==0:
                self.lDef.append(sDef)
                self.dArg[sDef]=kwargs
                self.dRef[sDef]=oRef
                # +++++ beg:build data object
                oDat=self.bldDat(sDef,oRef=oRef,**kwargs)
                self.dDat[sDef]=oDat
                # ----- end:build data object
                iRet=1
            self.oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
            # ----- end:add file name and auxillary objects to storage
            return iRet
        except:
            self.logTB()
            return -1
    def prcExc(self,**kwargs):
        """processing end
        ### parameter
            kwargs  ... flexible keyword argument
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            # ----- end:initialize
            # +++++ beg:
            if len(self.lDef)<1:
                self.oLog.debug('skp:%s iRet:%d empty stack'%('ldmStorage::prcExc',iRet))
                return iRet
            iR,sDef=self.getDef()
            self.oLog.debug('beg:%s sDef:%s'%('ldmStorage::prcExc',sDef))
            if self.iVerbose>0:
                self.oLog.debug('    kwargs:%r'%(kwargs))
            self.oLog.debug('end:%s iRet:%d'%('ldmStorage::prcExc',iRet))
            # ----- end:
            return iRet
        except:
            self.logTB()
            return -1
    def prcEnd(self,**kwargs):
        """processing end
        ### parameter
            **kwargs ... flexible keyword argument
        ### return
            iRet    ... return code
                >0  ... okay processing done
                =0  ... okay nop
                <0  ... error
            sFN     ... filename
            oDat    ... data object
            oRef    ... reference object
        """
        try:
            # +++++ beg:initialize
            iRet=0
            self.clrEnd()
            # ----- end:initialize
            # +++++ beg:
            iCntDef=len(self.lDef)
            if iCntDef>0:
                if self.getCfg('iModeRev',sType='int',oDft=0)==1:
                    self.sDefEnd=self.lDef.pop()
                else:
                    self.sDefEnd=self.lDef[0]
                    del self.lDef[0]
                self.oArgEnd=self.dArg.get(self.sDefEnd,None)
                self.oDatEnd=self.dDat.get(self.sDefEnd,None)
                self.oRefEnd=self.dRef.get(self.sDefEnd,None)
                iRet=1
            # ----- end:
            return iRet
        except:
            self.logTB()
            return -1
    def saveJson(self,oDat,sFN,sDN=None,sSfx=None):
        """write object attribute data to json file
        ### parameter
            sFN     ... file name
            sDN     ... directory
            sSfx    ... suffix
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::saveJson'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            iRet=0
            # ----- end:initialize
            # +++++ beg:build file name
            iR,sFullFN=ldmOS.bldFN(sFN,sDN=sDN,
                                sExt='json',sSfx=sSfx,
                                oLog=self.oLog,iVerbose=1)
            self.oLog.debug('   :iR:%d sFullFN:%r'%(iR,sFullFN))
            if iR<=0:
                return 0
            iRet=1
            # ----- end:build file name
            # +++++ beg:save json
            with open(sFullFN,'w') as oFile:
                sDat=json.dumps(oDat)
                oFile.write(sDat)
            # ----- end:save json
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def loadJson(self,dDat,sK,sFN,sDN=None,iUpdate=0):
        """load directory list to json
        ### parameter
            dDat    ... dictionary
            sK      ... key to place loaded data
            sFN     ... file name
            sDN     ... optional directory
            iUpdate ... update dDat[sK]
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:build input file name
            sOrg='ldmStorage::loadJson'
            self.logDbg('beg:%s sK:%r sFN:%r sDN:%r iUpdate:%d',
                        sOrg,sK,sFN,sDN,iUpdate)
            iRet=0
            oVal=None
            if sDN is not None:
                sTmpFN=os.path.join(sDN,sFN)
            else:
                sTmpFN=sFN
            # ----- end:build input file name
            # +++++ beg:load info to json
            with open(sTmpFN,'r') as oFile:
                sDat=oFile.read()
                oVal=json.loads(sDat)
                if iUpdate>0:
                    if sK in dDat:
                        dDat[sK].update(oVal)
                    else:
                        dDat[sK]=oVal
                else:
                    dDat[sK]=oVal
            iRet=1
            # ----- end:load info to json
            self.logDbg('end:%s iRet:%d',sOrg,iRet)
            return iRet
        except:
            self.logTB()
            return -1
    def saveAtr(self,sFN,sDN=None,lAtr=None):
        """save object attribute data to json file
        ### parameter
            sFN     ... file name
            sDN     ... directory
            lAtr    ... attribute list
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::saveAtr'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            iRet=0
            # ----- end:initialize
            # +++++ beg:finalize
            if lAtr is None:
                iR,lAtr=self.getCfg('lAtr')
                if iR<=0:
                    self.oLog.error('   :getCfg problem iR:%d'%(iR))
                    lAtr=['dDat']
            for sAtr in lAtr:
                if sAtr in self.__dict__:
                    oAtr=self.__dict__[sAtr]
                    iR=self.saveJson(oAtr,sFN,sDN,sSfx=sAtr)
                    if iR>0:
                        iRet+=1
            # ----- end:read cfg file
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def saveDat(self,sFN,sDN=None,lKey=None,sAtr='dDat'):
        """save object data to json file
        ### parameter
            sFN     ... file name
            sDN     ... directory
            lKey    ... keys
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::saveDat'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            iRet=0
            # ----- end:initialize
            # +++++ beg:finalize
            if self.iVerbose>0:
                lAtr=list(self.__dict__.keys())
                self.oLog.debug('    sAtr:%s lAtr:%r lKey:%r'%(sAtr,lAtr,lKey))
            
            if sAtr in self.__dict__:
                if self.iVerbose>0:
                    self.oLog.debug('    sAtr:%s found lKey:%r'%(sAtr,lKey))
                oAtr=self.__dict__[sAtr]
                if lKey is not None:
                    iLenKey=len(lKey)
                    for sK in lKey:
                        oVal=oAtr[sK]
                        if iLenKey>1:
                            sSfx='.'.join([sAtr,sK])
                        else:
                            sSfx=None
                        iR=self.saveJson(oVal,sFN,sDN,sSfx=sSfx)
                        if iR>0:
                            iRet+=1
                else:
                    iR=self.saveJson(oAtr,sFN,sDN,sSfx=None)
                    if iR>0:
                        iRet+=1
            # ----- end:read cfg file
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def loadDat(self,sFN,sDN=None,sKey=None,sAtr='dDat'):
        """load object data to json file
        ### parameter
            sFN     ... file name
            sDN     ... directory
            lKey    ... keys
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::loadDat'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            iRet=0
            # ----- end:initialize
            # +++++ beg:finalize
            if self.iVerbose>0:
                lAtr=list(self.__dict__.keys())
                self.oLog.debug('    sAtr:%s lAtr:%r sKey:%r'%(sAtr,lAtr,sKey))
            
            if sAtr in self.__dict__:
                if self.iVerbose>0:
                    self.oLog.debug('    sAtr:%s found sKey:%r'%(sAtr,sKey))
                oAtr=self.__dict__[sAtr]
                if sKey is not None:
                    iR=self.loadJson(oAtr,sKey,sFN,sDN)
                    if iR>0:
                        iRet+=1
                else:
                    iR=self.loadJson(self.__dict__,sAtr,sFN,sDN,sSfx=None)
                    if iR>0:
                        iRet+=1
            else:
                iR=self.loadJson(self.__dict__,sAtr,sFN,sDN,sSfx=None)
                if iR>0:
                    iRet+=1
                        
            # ----- end:read cfg file
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def getCfg(self,sKey,sType=None,oDft=None):
        """get configuration value
        ### parameter
            sKey    ... configuration key
            sType   ... type enforcement
            oDft    ... default value
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            iRet=0
            oVal=oDft
            # ----- end:initialize
            # +++++ beg:find value
            if self.dCfg is not None:
                if sKey in self.dCfg:
                    iRet=2
                    oVal=self.dCfg[sKey]
            # ----- end:find value
            # +++++ beg:find default value
            if iRet==0:
                if self.dCfgDft is not None:
                    if sKey in self.dCfgDft:
                        iRet=1
                        oVal=self.dCfgDft[sKey]
            # ----- end:find default value
            # +++++ beg:type enforcement
            if iRet>0:
                if sType=='int':
                    try:
                        iVal=int(oVal)
                        return iRet,iVal
                    except:
                        iVal=oDft
                        return iRet,iVal
            # ----- end:type enforcement
            return iRet,oVal
        except:
            self.logTB()
            return -1,None
    def loadCfg(self,sCfgFN='cfg.json'):
        """read configuration file, given in json format
        ### parameter
            sCfgDN  ... configuration file name
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='ldmStorage::loadCfg'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            iRet=0
            # ----- end:initialize
            # +++++ beg:read cfg file
            self.sCfgFN=sCfgFN
            self.dCfg=None
            if os.path.exists(self.sCfgFN):
                with open(self.sCfgFN,'r') as oFile:
                    self.dCfg=json.loads(oFile.read())
                iRet=1
            # ----- end:read cfg file
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def __tpl(self):
        """
        ### parameter
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            # ----- end:
            # +++++ beg:initialize
            iRet=0
            sOrg='::'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            # ----- end:initialize
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
