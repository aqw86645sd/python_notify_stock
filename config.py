import os

from dotenv import load_dotenv


class Config:
    # 加载 .env 文件
    load_dotenv()

    LINE_TOKEN = os.getenv("LINE_TOKEN")
    NEWS_TOKEN = os.getenv("NEWS_API_TOKEN")

    # stock info
    ETF_SYMBOL = "VOO"
    PERIOD_LENGTH = "180d"
    NUM_STOCKS_TO_CHECK = 50
    TIMEZONE_OFFSET = 8

    # 策略參數
    STRATEGY_1_PRICE_LIMIT = 4
    STRATEGY_1_VOLUME_PERIOD = 20  # 成交量平均
    STRATEGY_1_VOLUME_LIMIT = 2
    STRATEGY_2_SHORT_MA_PERIOD = 5
    STRATEGY_2_LONG_MA_PERIOD = 20
