import os
from enum import Enum

# TDA API Info
API_KEY = "YOUR_API_KEY@AMER.OAUTHAP"
REDIRECT_URI = "http://localhost:8080/"
ACCOUNT_ID = "YOUR_ACCOUNT_ID"

# Alpaca API Info
APCA_API_KEY_ID = "KEY"
APCA_API_SECRET_KEY = "SECRET KEY"

DIRNAME = os.path.dirname(__file__)
TOKEN_PATH = os.path.join(DIRNAME, "token.pickle")
OUTPUT_PATH = os.path.dirname(__file__).replace("auth", "output")


# Twitter keys
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


class Actions(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"


# Edit Values
# Rename to const.py
