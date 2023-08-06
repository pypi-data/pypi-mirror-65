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

import logging
import traceback

from lindworm.logUtil import logGet

class ldmStorage:
    def __init__(self,sLogger='',iLevel=logging.DEBUG,iVerbose=0):
        """constructor
        """
        self.iVerbose=iVerbose
        self.__initDat__()
        self.oLog=logGet(sLogger,iLevel)
    def __initDat__(self):
        """initialize data properties
        """
        self.lFN=[]         # list files been processed
        self.dFN={}         # dictionary processed files, performance
    def clr(self):
        self.__initDat__()
    def prcIsDone(self,sFN):
        """check file name has been processed already  
        return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        if sFN in self.dFN:
            iRet=1
        else:
            iRet=0
        self.oLog.debug('%s sFN:%s iRet:%d'%('ldmStorage::prcIsDone',
                        sFN,iRet))
        return iRet
    def _tpl(self,iVerbose=-1):
        """
        return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            logging.debug('beg: iVerbose:%d'%(iVerbose))
            iRet=0
            # ----- end:
            # +++++ beg:
            # ----- end:
            # +++++ beg:
            logging.debug('end:  iRet:%d'%(iRet))
            # ----- end:
            return iRet
        except:
            logging.error(traceback.format_exc())
            return -1
    def _tpl2(self):
        """
        return
            >0  ... okay processing done
            =0  ... okay nop
            <0  ... error
        """
        try:
            # +++++ beg:
            if self.iVerbose>0:
                self.oLog.debug('beg: iVerbose:%d'%(self.iVerbose))
            iRet=0
            # ----- end:
            # +++++ beg:
            # ----- end:
            # +++++ beg:
            if self.iVerbose>0:
                self.oLog.debug('end:  iRet:%d'%(iRet))
            # ----- end:
            return iRet
        except:
            self.oLog.error(traceback.format_exc())
            return -1
