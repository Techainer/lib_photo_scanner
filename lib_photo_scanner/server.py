from __future__ import absolute_import

from api import app, logger
import uvicorn

if __name__ == '__main__':
    uvicorn.run(app, 
        host="127.0.0.1", 
        port=8769, 
        log_level="info",
        access_log=False)