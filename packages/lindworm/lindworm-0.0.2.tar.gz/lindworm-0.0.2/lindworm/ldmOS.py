#----------------------------------------------------------------------------
# Name:         lmdOS.py
# Purpose:      OS class
#
# Author:       Walter Obweger
#
# Created:      20200322
# CVS-ID:       $Id$
# Copyright:    Walter Obweger
# Licence:      MIT
#----------------------------------------------------------------------------

import sys
import os
import os.path
import time
import stat
import traceback

def newSha():
    """python 3 change fix
    """
    if sys.version_info  >= (2,6,0):
        import hashlib
        return hashlib.sha1()
    else:
        import sha
        return sha.new()

def getSha(sFN,iMB=-1,iBlk=4096,sDN=None,oLog=None,iVerbose=0):
    """get SHA limited
    ### parameter
        sFN     ... file name
        iMB     ... max size to read
                    + <=0 all data
                    + >0 up to maximum in MB
        iBlk    ... block size
        oLog    ... logging object
    ### return
        >0  ... okay content read
        =0  ... okay no data
        <0  ... error
    """
    try:
        if sDN is not None:
            sFullFN=os.path.join(sDN,sFN)
        else:
            sFullFN=sFN
        if oLog is None:
            iVerbose=0
        with open(sFullFN,'rb') as oFile:
            if iVerbose>0:
                oLog.debug('sFullFN:%s'%(sFullFN))
            # +++++ beg:initialize
            oStat=os.stat(sFullFN)
            oSha=newSha()
            if iBlk<64:
                iBlk=64
            if iMB==0:
                iSz=0
            elif iMB<=0:
                iSz=oStat.st_size
                iBlkSz=4096
            else:
                iSz=iMB<<20
                if iSz>oStat.st_size:
                    iSz=oStat.st_size
            if iSz==0:
                iEnd=2
            else:
                iEnd=0
            # ----- end:initialize
            # +++++ beg:read file data
            iPrv=0
            iCur=0
            while iEnd==0:
                try:
                    iPrv=iCur
                    if iVerbose>0:
                        oLog.debug('iBlk:%d iPrv:%d'%(iBlk,iPrv))
                    sDat=oFile.read(iBlk)
                    iCur=oFile.tell()
                    iRd=iCur-iPrv
                    if iVerbose>0:
                        oLog.debug('iRd:%d iCur:%d'%(iRd,iCur))
                    if iRd>0:
                        oSha.update(sDat)
                        if iRd<iBlk:
                            iEnd=1
                        if iCur>iSz:
                            iEnd=3
                    else:
                        iEnd=2
                except:
                    if oLog is not None:
                        oLog.error(traceback.format_exc())
                    iEnd=-1
            # ----- end:read file data
            # +++++ beg:deliver fingerprint value
            if iEnd==1:         # regular
                return oSha.hexdigest()
            elif iEnd==2:       # empty
                return "---"
            elif iEnd==3:       # limit reached
                return oSha.hexdigest()
            elif iEnd==-1:      # exception
                return '!!!'
            return '???'        # you're not supposed to be here
            # ----- end:deliver fingerprint value
    except:
        if oLog is not None:
            oLog.error(traceback.format_exc())
        return '???!!!'

def getNow(iUTC=1,sFmt='%Y%m%d_%H%M%S'):
    """get string current time
    ### parameter
        iUTC    ... in universal time cooradinated
        sFmt    ... format
    ### return
        str ... string representing current time
    """
    if iUTC>0:
        zNow=time.gmtime(time.time())
    else:
        zNow=time.localtime(time.time())
    sNow=time.strftime(sFmt,zNow)
    return sNow

def getNiceFN(sFN,iKind=0,oLog=None):
    """build file name and create required directories
    ### parameter
        sFN     ... file name
    ### return
        >0  ... okay content read
        =0  ... okay no data
        <0  ... error
    """
    try:
        # +++++ beg:initialize
        iRet=0
        iLen=len(sFN)
        lRet=[]
        # ----- end:initialize
        for s in sFN:
            iFound=0
            iOrd=ord(s)
            if (iOrd>=65) and (iOrd<=90):
                iFound=1
            elif (iOrd>=97) and (iOrd<=122):
                iFound=1
            elif (iOrd>=48) and (iOrd<=57):
                iFound=1
            elif s in ['.',',','_','-']:
                iFound=1
            else:
                pass
            if iFound>0:
                lRet.append(s)
            else:
                if iKind==0:
                    lRet.append('_')
        return ''.join(lRet)
    except:
        if oLog is not None:
            oLog.error(traceback.format_exc())
        return -1,None
    
def bldFN(sFN,sDN=None,sExt='json',sSfx=None,oLog=None,iVerbose=0):
    """build file name and create required directories
    ### parameter
        sFN     ... file name
        sDN     ... directory name
        sExt    ... file name extension
        sSfx    ... suffix
        oLog    ... logging object
        iVerbose .. verbose detail level
    ### return
        >0  ... okay content read
        =0  ... okay no data
        <0  ... error
    """
    try:
        # +++++ beg:initialize
        iRet=0
        iVrb=0
        if oLog is not None:
            if iVerbose>0:
                sOrg='ldmOS::bldFN'
                oLog.debug('beg:%s iVerbose:%d'%(sOrg,iVerbose))
                iVrb=1
        # ----- end:initialize
        # +++++ beg:ensure file name
        if sFN is None:
            sFN=getNow()
        elif sFN==0:
            sFN=getNow(iUTC=0)
        elif sFN==1:
            sFN=getNow(iUTC=1)
        # ----- end:ensure file name
        # +++++ beg:build file name
        if sDN is not None:
            sFullFN=os.path.join(sDN,sFN)
        else:
            sFullFN=sFN
        if sExt is not None:
            iLenExt=len(sExt)+1
            if sFullFN.endswith(sExt):
                lFN=[sFullFN[:-iLenExt]]
            else:
                lFN=[sFullFN]
        else:
            lFN=[sFullFN]
        if sSfx is not None:
            sSfxNice=getNiceFN(sSfx)
            lFN.append(sSfxNice)
        if sExt is not None:
            lFN.append(sExt)
        sFullFN='.'.join(lFN)
        if iVrb>0:
            oLog.debug('   :sFullFN:%s'%(sFullFN))
        # ----- end:build file name
        # +++++ beg:create folder
        try:
            sTmpDN,sTmpFN=os.path.split(sFullFN)
            if len(sTmpDN)>0:
                if os.path.exists(sTmpDN)==False:
                    os.makedirs(sTmpDN)
            iRet=1    
        except:
            if oLog is not None:
                oLog.error(traceback.format_exc())
        # ----- end:create folder
        # +++++ beg:finalize
        if iVrb>0:
            oLog.debug('end:%s iRet:%d'%(sOrg,iRet))
        # ----- end:finalize
        return iRet,sFullFN
    except:
        if oLog is not None:
            oLog.error(traceback.format_exc())
        return -1,None
