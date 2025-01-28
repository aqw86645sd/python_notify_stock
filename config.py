import os
from pathlib import Path

class Config:
    PROJECT_ROOT = Path(__file__).resolve().parent
    LINE_TOKEN_FILE_PATH = os.path.join(PROJECT_ROOT, "token/line_token")
    NEWS_API_KEY_FILE_PATH = os.path.join(PROJECT_ROOT, "token/news_api_key")
    LINE_TOKEN = open(LINE_TOKEN_FILE_PATH, "r").read()
    NEWS_TOKEN = open(NEWS_API_KEY_FILE_PATH, "r").read()

    # stock info
    ETF_SYMBOL = "VOO"
    PERIOD_LENGTH = "180d"
    NUM_STOCKS_TO_CHECK = 50
    TIMEZONE_OFFSET = 8

    # 策略參數
    STRATEGY_1_PRICE_LIMIT = 4
    STRATEGY_1_VOLUME_LIMIT = 2
    STRATEGY_2_SHORT_MA_PERIOD = 5
    STRATEGY_2_LONG_MA_PERIOD = 20
