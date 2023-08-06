# Python template for logging
from pathlib import Path

'''Setup for logging.  Note that basic config can only be used once per module, and opens logs for append.'''
import logging

logDir = Path.home().joinpath('Documents/Logs')
logName = Path(__name__).stem + '.log'
logFile = str(logDir.joinpath(logName))
logging.basicConfig(filename=logFile, level=logging.DEBUG, format='{asctime} {filename} {levelname} {message}',
    style='{', datefmt='%H:%M:%S',  # Can't find how to use '{' format in datefmt parameter
    filemode ='w')                  # 'w' is overwrite, 'a' is append
logger = logging.getLogger(logFile)


def func(myfile):
    try:
        logger.info("message")
        return
    except OSError as e:
        logger.error("error message ", exc_info=True)
        logger.warning("a warning message")
    finally:
        logger.debug("the function is done for the file %s", myfile)[...]

