# encoding: utf-8
"""
logging.py

Created by chichu on 2010-05-05.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

import logging

LOG_FILE = '/var/log/nginx/gamecard.app.log'

logger = logging.getLogger("gamecard_error_log")
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
fh = logging.FileHandler(LOG_FILE)
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)
       
def log_error(e):
    logger.error(e)

if "__name__" == "__main__":
    log_error("test")
