#----------------------------------------------------------------------------
# Name:         pyGatherMD.py
# Purpose:      python gather markdown
#
# Author:       Walter Obweger
#
# Created:      20191102
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import os
import os.path
import logging
import logging.handlers
import traceback
import shutil
import json

from optparse import OptionParser

from lindworm import __version__
from lindworm.ldmStorageLine import ldmStorageLine
from lindworm.ldmMD import ldmMD

class pyGatherMD(ldmStorageLine):
    def __init__(self,sLogger='srgMD',iLv=1,iVerbose=0):
        """constructor
        ### parameter
            iLv         ... logging level
            sLogger     ... log origin
            iLv         ... logging level
            iVerbose    ... higher values add more logs
        """
        self.sFN=None
        #self.oSrgMD=ldmStorageLine(sLogger='srgMD',iVerbose=iVerbose-10)
        ldmStorageLine.__init__(self,sLogger='srgMD',
                            iLv=1,
                            iVerbose=iVerbose-10)
        self.__initDat__()
    def __initCfg__(self):
        """initialize configuration properties
        """
        try:
            # +++++ beg:
            ldmStorageLine.__initCfg__(self)
            # ----- end:
            # +++++ beg:
            # ----- end:
        except:
            self.logTB()
            return -1
    def __initDat__(self):
        """initialize data properties
        """
        try:
            # +++++ beg:
            ldmStorageLine.__initDat__(self)
            # ----- end:
            # +++++ beg:
            self.sInFN=''
            self.sOtFN=''
            self.lHdrLv=[]
            self.lMarkDownFN=[]
            self.dMarkDown={}
            self.dImgFiles={}
            self.dStatus={
                'oky':{},
                'err':{},
                'skp':{},
                'wrn':{},
                }
            self.oFileBld=None
            # ----- end:
        except:
            self.logTB()
            return -1
    def _tpl(self,iVerbose=-1):
        """
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            sOrg='::'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,iVerbose))
            iRet=0
            # ----- end:
            # +++++ beg:
            # ----- end:
            # +++++ beg:
            self.oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
            # ----- end:
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
            sOrg='pyGatherMD::bldDat'
            if self.iVerbose>0:
                self.oLog.debug('beg:%s sDef:%s oRef:%r kwargs:%r'%(sOrg,sDef,oRef,kwargs))
            oDat=kwargs.get('oDat',self)
            if self.iVerbose>0:
                self.oLog.debug('end:%s sDef:%s oDat:%r'%(sOrg,sDef,oDat))
            return oDat
        except:
            self.logTB()
            return None
    def chgLv(self,iHdrLvCur,iHdrLvNxt,iVerbose=-1):
        """change header level
        ### parameter
            iHdrLvCur   ...
            iHdrLcNxt   ...
            iVerbose    ... verbose level
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
            -11 ... header level mismatch
        """
        try:
            # +++++ beg:
            self.oLog.debug('beg:chgLv iVerbose:%d'%(iVerbose))
            iRet=0
            # ----- end:
            # +++++ beg:
            dLvNxt={
                'name':'',
                'iLv':iHdrLvNxt,
                }
            if len(self.lHdrLv)>0:
                dLvPrv=self.lHdrLv[-1]
                while dLvPrv['iLv']>=dLvNxt['iLv']:
                    del self.lHdrLv[-1]
                    if len(self.lHdrLv)>0:
                        dLvPrv=self.lHdrLv[-1]
                    else:
                        break
            if len(self.lHdrLv)>0:
                dLvPrv=self.lHdrLv[-1]
                if dLvPrv['iLv']==(dLvNxt['iLv']-1):
                    iRet=1
                else:
                    self.oLog.error('  hdr lv mismatch prv:%d nxt:%d'%(dLvPrv['iLv'],dLvNxt['iLv']))
                    iRet=-11
            self.lHdrLv.append(dLvNxt)
            # ----- end:
            # +++++ beg:
            self.oLog.debug('end:chgLv  iRet:%d'%(iRet))
            # ----- end:
            return iRet
        except:
            logging.error(traceback.format_exc())
            return -1
    def loadCfg(self,sCfgFN='pyGatherMDCfg.json'):
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
            sOrg='pyGatherMD::loadCfg'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            iRet=0
            self.__initCfg__()
            # ----- end:initialize
            # +++++ beg:read cfg file
            self.sCfgFN=sCfgFN
            with open(self.sCfgFN,'r') as oFile:
                self.dCfg=json.loads(oFile.read())
            # ----- end:read cfg file
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            return -1
    def validateDatPrm(self,sInFN='README.md',
                  sBldDN='./build',
                  sOtFN=None):
        """validate data parameter
        ### parameter
            sInFN   ... file name to process
            sBldDN  ... build directory name
            sOtFN   ... output file name
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:initialize
            sOrg='pyGatherMD::validateDatPrm'
            if self.iVerbose>0:
                self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
                self.oLog.debug('  sInFN:%r'%(sInFN))
                self.oLog.debug(' sBldDN:%r'%(sBldDN))
                self.oLog.debug('  sOtFN:%r'%(sOtFN))
            iRet=0
            self.__initDat__()
            # ----- end:initialize
            # +++++ beg:check call parameters
            sTmpInDN,sTmpInFN=os.path.split(sInFN)
            if self.iVerbose>5:
                self.oLog.debug('  sInFN:%r -> DN:%r FN:%r'%(sInFN,sTmpInDN,sTmpInFN))
            if sTmpInDN is None:
                sTmpInDN='./'
            if sOtFN is None:
                if sBldDN is None:
                    self.oLog.error('no output filename provided, no build directory given')
                    self.oLog.error('input file will not be overwritten, abort')
                    return -10
                sBldFN=os.path.join(sBldDN,sTmpInFN)
            else:
                if sBldDN is None:
                    if sTmpInFN==sOtFN:
                        self.oLog.error('output filename provided, no build directory given')
                        self.oLog.error('input file will not be overwritten, abort')
                        return -11
                    sTmpOtDN,sTmpOtFN=os.path.split(sOtFN)
                    if sTmpOtDN is None:
                        sTmpOtDN='./'
                    sBldDN=sTmpOtDN#os.path.join(sTmpInDN,sOtFN)
                    sBldFN=sOtFN#sTmpOtDN
                else:
                    self.oLog.debug('  sOtFN:%r'%(sOtFN))
                    self.oLog.debug(' sBldDN:%r sOtFN:%r'%(sBldDN,sOtFN))
                    sBldFN=os.path.join(sBldDN,sOtFN)
            if sBldFN==sInFN:
                self.oLog.error('build FN:%r and input FN:%r identical'%(sBldFN,sInFN))
                self.oLog.error('input file will not be overwritten, abort')
                return -19
            # ----- end:check call parameters
            # +++++ beg:validate adjusted
            sAbsInFN=os.path.abspath(sInFN)
            sAbsOtFN=os.path.abspath(sBldFN)
            if sAbsInFN==sAbsOtFN:
                return -15
            if os.path.exists(sInFN):
                iRet=1
            self.sInFN=sInFN
            self.sBldDN=sBldDN
            self.sBldFN=sBldFN
            # ----- end:validate adjusted
            # +++++ beg:
            if self.iVerbose>0:
                self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:
            return iRet
        except:
            self.logTB()
            return -1
    def copyImage(self,sCurDN,sImgFN):
        """copy image
        ### parameter
            sCurDN  ... current directory name
            sImgFN  ... image file name
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            if sCurDN is None:
                sCurDN=self.sCurDN
            self.oLog.debug('beg:copyImage:%s sCurDN:%s'%(sImgFN,sCurDN))
            iRet=0
            # ----- end:
            # +++++ beg:
            if sImgFN.startswith('./'):
                sTmpDN,sTmpFN=os.path.split(sImgFN)
                sSrcImgDN=sCurDN+sTmpDN[1:]
                sDstImgDN=self.sBldDN+sTmpDN[1:]
                sImgFN=sTmpFN
            else:
                sSrcImgDN=sCurDN+'/'
                sDstImgDN=self.sBldDN
            self.oLog.debug('  sSrcDN:%s'%(sSrcImgDN))
            self.oLog.debug('  sDstDN:%s'%(sDstImgDN))
            sSrcFullFN=os.path.join(sSrcImgDN,sImgFN)
            sDstFullFN=os.path.join(sDstImgDN,sImgFN)
            self.oLog.debug('  sSrcFullFN:%s'%(sSrcFullFN))
            self.oLog.debug('  sDstFullFN:%s'%(sDstFullFN))
            if sSrcFullFN in self.dImgFiles:
                self.oLog.warning('file:%s already copied'%(sSrcFullFN))
                return 0
            # ----- end:
            # +++++ beg:
            if os.path.exists(sDstImgDN)==False:
                try:
                    os.makedirs(sDstImgDN)
                except:
                    self.logTB()
            # ----- end:
        except:
            self.logTB()
            return -1
        try:
            # +++++ beg:
            self.dImgFiles[sSrcFullFN]=sDstFullFN
            shutil.copyfile(sSrcFullFN,sDstFullFN)
            self.dStatus['oky'][sSrcFullFN]=sDstFullFN
            # ----- end:
            # +++++ beg:
            self.oLog.debug('end:copyImage:%s  iRet:%d'%(sImgFN,iRet))
            # ----- end:
            return iRet
        except:
            self.logTB()
            self.dStatus['err'][sSrcFullFN]='copy to >%s< failed'%(sDstFullFN)
            #self.dImgFiles[sSrcFullFN]
            return -2
    def walkMD(self,sInFN='README.md',
                  sBldDN='./build',
                  sOtFN=None):
        """
        ### parameter
            sInFN   ... file name to process
            sBldDN  ... build directory
            sOtFN   ... output file name
        ### return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
            -5  ... build directory does not exit
        """
        try:
            # +++++ beg:initialize
            sOrg='pyGatherMD::walkMD'
            self.oLog.debug('beg:%s iVerbose:%d'%(sOrg,self.iVerbose))
            self.oLog.debug('  sInFN:%r'%(sInFN))
            self.oLog.debug(' sBldDN:%r'%(sBldDN))
            self.oLog.debug('  sOtFN:%r'%(sOtFN))
            iRet=0
            self.lLineOut=[]
            self.lMarkerMD=[]
            # ----- end:initialize
            # +++++ beg:validate parameter
            iRet=self.validateDatPrm(sInFN=sInFN,
                            sBldDN=sBldDN,
                            sOtFN=sOtFN)
            self.oLog.debug('    validateDatPrm iRet:%d'%(iRet))
            if iRet<0:
                logging.debug('end:%s  iRet:%d'%(sOrg,iRet))
                return iRet
            self.oLog.debug('  sInFN:%r'%(self.sInFN))
            self.oLog.debug(' sBldDN:%r'%(self.sBldDN))
            self.oLog.debug('  sOtFN:%r'%(self.sOtFN))
            # ----- end:validate parameter
            # +++++ beg:create build DN
            if os.path.exists(self.sBldDN)==False:
                try:
                    os.makedirs(self.sBldDN)
                except:
                    self.logTB()
            if os.path.exists(self.sBldDN)==False:
                self.oLog.error("end:%s return -5 sBldDN:%s "
                                "directory does not exist, "
                                "can't be created"%(sOrg,sBldDN))
                return -5
            # ----- end:create build DN
            # +++++ beg:create build file
            self.oLog.info(' sBldFN:%r'%(self.sBldFN))
            if self.sEnc is None:
                self.oFileBld=open(self.sBldFN,'w')
            else:
                self.oFileBld=open(self.sBldFN,'w',encoding=self.sEnc)
            # ----- end:create build file
            # +++++ beg:memorize file name
            sAbsInFN=os.path.abspath(self.sInFN)
            self.sCurDN,self.sCurFN=os.path.split(sAbsInFN)
            if self.iVerbose>5:
                self.oLog.debug('  sCurDN:%r sCurFN:%r'%(self.sCurDN,self.sCurFN))
            if self.sCurDN is None:
                self.sCurDN='./'
            if len(self.sCurDN)==0:
                self.sCurDN='./'
            # ----- end:memorize file name
            # +++++ beg:determine base file name to skip
            sTmpDN,sTmpFN=os.path.split(sAbsInFN)
            if sTmpDN is None:
                iSkipDN=-1
            else:
                iSkipDN=len(sTmpDN)+1
            # ----- end:determine base file name to skip
            # +++++ beg:process input file
            oMD=ldmMD(sAbsInFN,sLogger='oMD',iSkipDN=iSkipDN,
                      iVerbose=self.iVerbose)
            #oMD.prcBeg(sAbsInFN,oDat=oMD,oRef=None)
            oMD.prcBeg(sAbsInFN,oRef=None)
            oMD.prcExc(oGtrMD=self)
            iRetMD=oMD.prcEnd()
            # ----- end:process input file
            # +++++ beg:write output
            for iLine,sLine in oMD.lLine:
                self.oFileBld.write(sLine)
            # ----- end:write output
            # +++++ beg:close output
            if self.oFileBld is not None: 
                self.oFileBld.close()
            # ----- end:close output
            # +++++ beg:finalize
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,iRet))
            # ----- end:finalize
            return iRet
        except:
            self.logTB()
            self.oLog.debug('end:%s  iRet:%d'%(sOrg,-1))
            return -1

def execMain(sInFN='README.md',
                sBldDN='./build',
                sOtFN=None,
                sCfgFN=None,
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
        oGather=pyGatherMD(iVerbose=iVerbose)
        iRet=oGather.loadCfg(sCfgFN)
        iRet=oGather.walkMD(sInFN=sInFN,
                  sBldDN=sBldDN,
                  sOtFN=sOtFN)
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
            default='pyGatherMDCfg.json',
            help='configuration file',metavar='pyGatherMDCfg.json',
            )
    oParser.add_option('-i','--inFN',dest='sInFN',
            default='README.md',
            help='markdown file to start',metavar='README.md',
            )
    oParser.add_option('-b','--buildDN',dest='sBldDN',
            default='./build',
            help='build directory',metavar='./build',
            )
    oParser.add_option('-o','--otFN',dest='sOtFN',
            default=None,
            help='output file',metavar='sng.md',
            )
    oParser.add_option('-l','--log',dest='sLogFN',
            default='./log/pyGatherMD.log',
            help='log filename',metavar='./log/pyGatherMD.log')
    oParser.add_option("-v", action="store_true", dest="verbose", default=True)
    oParser.add_option("-q", action="store_false", dest="verbose", default=True)
    # ----- end:define CLI arguments
    # +++++ beg:parse command line
    (opt,args)=oParser.parse_args(args=args)
    if opt.verbose:
        print("config FN:     %r"%(opt.sCfgFN))
        print(" input FN:     %r"%(opt.sInFN))
        print(" build DN:     %r"%(opt.sBldDN))
        print("output FN:     %r"%(opt.sOtFN))
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
    iRet=execMain(sInFN=opt.sInFN,
                sBldDN=opt.sBldDN,
                sOtFN=opt.sOtFN,
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
