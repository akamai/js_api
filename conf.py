#!/usr/bin/env python
import os

WORKING_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(WORKING_DIR, 'src')
TEMPLATE_FOLDER = os.path.join(SRC, 'templates')
STATIC_FOLDER = os.path.join(SRC, 'static')
TEMP_FOLDER = os.path.join(WORKING_DIR, 'temp')
HISTORY_RESULT = os.path.join(WORKING_DIR, 'history')

TIMEOUT = 10  # 10 minutes

# Log
LOG_FOLDER = os.path.join(WORKING_DIR, 'logs')
LOGGER_FILE = os.path.join(LOG_FOLDER, 'js-api.log')
LOGGER_NAME = 'js-api'
LOG_FILE_SIZE = 10 * 1000000  # 10 MB
LOG_FILE_NUMBER = 5

# MODEL TRAINED

MODEL_TRAINED = os.path.join(WORKING_DIR, 'ressources', 'model_trained_akamai')

# Credentials

VT_KEY = 'VT'
PUBLICWWW_KEY = 'PUBLICWWW'
API_CREDENTIALS = os.path.join(WORKING_DIR, 'credentials.json')

# CRAWLER

DOWNLOAD_FOLDER = os.path.join(WORKING_DIR, 'download')
TIMEOUT_THREAD_CRAWL = 60 * 20  # 20min should be enough to crawl 1000 URLS
TIMEOUT_CRAWL = 20
TIMEOUT_DOWNLOAD = 100
TIMEOUT_CRAWL_FULL_URL = 420  # 7min
DEPTH_MAX = 10
THREADS_MAX = 1000
MAX_LEN_URL = 247  # to avoid OSError: [Errno 63] File name too long.
EXCLUDE_LIST = ['']
LINKS = 'links'
INLINE = 'inline'
UNKNOWN = 'unknown'
MIN_CHARACTER_LEN_JS = 120  # We increase the min len to avoid small scripts

# AST

TO_PROCESS = 'to_process'

# TEST

TEST_FOLDER = os.path.join(WORKING_DIR, 'test')

# METADATA

VT_UPLOAD_MAX_TIME = 500
SLEEP_STEP = 20