import os
from enum import Enum

API_KEY = "YOUR_API_KEY@AMER.OAUTHAP"
REDIRECT_URI = "http://localhost:8080/"
ACCOUNT_ID = "YOUR_ACCOUNT_ID"

DIRNAME = os.path.dirname(__file__)
TOKEN_PATH = os.path.join(DIRNAME, "token.pickle")
OUTPUT_PATH = os.path.dirname(__file__).replace("auth", "output")


class Actions(Enum):
    BUY = "BUY"
    SELL = "SELL"
    NONE = "NONE"


# Edit Values
# Rename to const.py
