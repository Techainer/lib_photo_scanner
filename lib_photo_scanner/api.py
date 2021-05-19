from __future__ import absolute_import

from fastapi import FastAPI, HTTPException, Depends, Request, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import time 
import os
from lib import Scanner, logger
import traceback
from typing import Optional

app = FastAPI()

def get_scanner(scanner_name: str = None):
    ls = Scanner()
    scanners = ls.getScanners()

    if scanner_name is None:
        if scanners is None or len(scanners) == 0:
            return None, [], {}, None 

        scanner_name = scanners[0]
    try: 
        ls.setScanner(scanner_name)
        ls.setDPI(300)
        ls.setPixelType("color")
        ls.close()
    except Exception as ex: 
        logger.error('Can not set Scanner: {0}'.format(ex))
        return None, scanners
    return ls, scanners, set(scanners), scanner_name

ls, scanners, scanners_set, scanner_name = get_scanner()
lock = False
last_lock = time.time()
LOCK_THRESHOLD = int(os.environ.get('LOCK_THRESHOLD', None)) if os.environ.get('LOCK_THRESHOLD', None) is not None else 3

@app.route('/')
def ping(request):
    start_time = time.time()

    output = {
        "output": "pong",
        "code": "SUCCESS", 
        "msg": "SUCCESS",
        "time": time.time() - start_time
    }

    return JSONResponse(status_code=status.HTTP_200_OK, content=output)

@app.route('/list')
def list_scanners(request):
    start_time = time.time()
    global scanners
    
    output = {
        "output": scanners,
        "code": "SUCCESS", 
        "msg": "SUCCESS",
        "time": time.time() - start_time
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=output)

@app.route('/scan')
def scanning(request, request_id: Optional[str] = None, scanner_name: Optional[str] = None):
    start_time = time.time()

    global ls
    global lock 
    global scanners
    global scanners_set

    if lock: 
        if last_lock + LOCK_THRESHOLD < time.time():
            lock = False 
        else:
            output = {
                    "request_id": request_id,
                    "output": False,
                    "code": "LOCK", 
                    "msg": "The scanner is locking, please wait",
                    "time": time.time() - start_time
                }
            return JSONResponse(status_code=status.HTTP_423_LOCKED, content=output)

    if scanner_name is not None: 
        if scanner_name not in scanners_set: 
            ls, scanners, scanners_set, scanner_name = get_scanner()

        if scanner_name not in scanners_set:
            output = {
                "request_id": request_id,
                "output": scanners,
                "code": "NOT_FOUND", 
                "msg": "Not found scanner {0}".format(scanner_name),
                "time": time.time() - start_time
            }
            return JSONResponse(status_code=status.HTTP_409_CONFLICT, content=output)
    else: 
        if len(scanners) == 0: 
            ls, scanners, scanners_set, scanner_name = get_scanner()
        
        if len(scanners) == 0:
            output = {
                "request_id": request_id,
                "output": False,
                "code": "NO_SCANNER", 
                "msg": "There's no plugin scanners, check your cable",
                "time": time.time() - start_time
            }
            return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=output)
        scanner_name = scanners[0]

    lock = True 
    last_lock = time.time()

    try:
        image = ls.scan(scanner_name=scanner_name, return_type="based64")
    except Exception as ex: 
        lock = False
        output = {
                "request_id": request_id,
                "error": "Scan Error",
                "code": "ERROR",
                "msg": "There's some error when scanner: {0}".format(traceback.format_exc()),
                "time": time.time() - start_time
            }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=output)

    lock = False

    if image is False or image is None:
        output = {
            "request_id": request_id,
            "error": "Scan Error",
            "code": "ERROR",
            "msg": "There's some error when scanner, I doesn't know.",
            "time": time.time() - start_time
        }
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=output)

    output = {
        "request_id": request_id,
        "output": image,
        "code": "SUCCESS", 
        "msg": "SUCCESS",
        "time": time.time() - start_time
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=output)