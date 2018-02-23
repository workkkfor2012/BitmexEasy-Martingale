from os.path import join
import logging
import os
import alog

########################################################################################################################
# Connection/Auth
########################################################################################################################

# API URL.
BASE_URL = ''
if os.environ.get('RUN_ENV') == 'development':
    BASE_URL = "https://testnet.bitmex.com/api/v1/"
else:
    BASE_URL = "https://www.bitmex.com/api/v1/"

# The BitMEX API requires permanent API keys. Go to https://testnet.bitmex.com/api/apiKeys to fill these out.
#BITMEX_API_KEY = os.environ.get('BITMEX_API_KEY')
BITMEX_API_KEY = "VjcxqcfTxwBPPluMIYkp0H_9"
#BITMEX_API_SECRET = os.environ.get('BITMEX_API_SECRET')
BITMEX_API_SECRET = "5J_jfDms6Cdw34Y5d9NWleZW3Z0dMZ7Npqksc4IkqK3qQBfj"

# Available levels: logging.(DEBUG|INFO|WARN|ERROR)
# LOG_LEVEL = os.environ.get('LOG_LEVEL')

LOG_LEVEL = logging.INFO

alog.set_level(LOG_LEVEL)
