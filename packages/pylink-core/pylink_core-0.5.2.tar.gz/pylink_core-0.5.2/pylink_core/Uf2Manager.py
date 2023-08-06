import subprocess, signal, platform
import sys, os, time
import json
import logging
import threading
import locale
import shutil
import base64, re, requests
from io import BytesIO

from .ExecThread import *
from .uflash import copyHex, flash, getDisk

logger = logging.getLogger(__name__)


def uploadFirmTask(firmPath, ext, sendReq):
    def uploadProgress(p, total, prompt="#"):
        progress = int(p/total*100)
        sendReq("upload-status", {"text": prompt, "progress": progress})


    if firmPath.startswith("http"):
        # download firmware, todo: content-length is not set in gitpage deploy
        # r = requests.get(firmPath)
        # print(r.headers)
        # firmLen = int(r.headers['Content-Length'].strip())
        # iostream = BytesIO()
        # dbytes = 0
        # for buf in r.iter_content(1024):
        #     if buf:
        #         iostream.append(buf)
        #         dbytes += len(buf)
        #         uploadProgress(dbytes, firmLen, 'downloading')
        # firmPath = iostream
        firmPath = requests.get(firmPath).content

    (code, ret) = copyHex(firmPath, callback=uploadProgress)
    
    logger.info("upload return %s %s" %(code, ret))
    newVol = None
    sendReq("upload-status")
    if code != 0:
        sendReq("extension-method", {"extensionId": ext['id'], "func": "onFlashError", "msg": ret})
    else:
        # wait new thumbdisk show up
        if 'thumbdisk' in ext:
            DISKNAME = ext['thumbdisk']
            while not newVol:
                newVol = getDisk(DISKNAME)
                time.sleep(0.5)
        sendReq("extension-method", {"extensionId": ext['id'], "func": "onFlashDone", "msg": newVol})

def uploadUf2(ext, params, sendReq, userPath):

    sendReq("upload-status", {"text": "Uploading", "progress": "10"})
    if "code" in params:
        if "boardName" in params:
            firmware = ext["board"][params["boardName"]]["runtime"]
            firmPath = os.path.join(ext['fullpath'], firmware)
        else:
            firmPath = os.path.join(ext['fullpath'], ext['runtime'])
        logger.info("upload %s" %firmPath)
        pycode = bytes(params['code'], encoding = "utf8")
        (code, ret) = flash(path_to_runtime=firmPath, python_script=pycode)
        sendReq("upload-status")
    else:
        if "base64" in params:
            firmPath = params['base64']
        elif "url" in params:
            firmPath = params['url']
        else:
            firmPath = os.path.join(ext['fullpath'], ext['firmware'])
        th = threading.Thread(target=uploadFirmTask,args=(firmPath, ext, sendReq, ))
        th.start()
        
    