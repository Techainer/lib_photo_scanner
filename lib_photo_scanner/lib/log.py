import logging
from logging.handlers import RotatingFileHandler

rfh = RotatingFileHandler(
    filename='./lib_photo_scanner.log', 
    mode='a',
    maxBytes=100*1024,
    backupCount=2,
    encoding=None,
    delay=0
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(funcName)s(%(lineno)d) %(message)s",
    datefmt="%y-%m-%d %H:%M:%S",
    handlers=[
        rfh
    ]
)

logger = logging.getLogger('root')