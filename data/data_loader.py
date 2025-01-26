import re

import requests
import yfinance as yf


class DataLoader:
    def __init__(self, config):
        self.config = config

    def get_etf_ticker_list(self):
        """ 取得 ETF 的股票清單 """
        url = f"https://www.zacks.com/funds/etf/{self.config.VOO_ETF_SYMBOL}/holding"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

        with requests.Session() as req:
            req.headers.update(headers)
            r = req.get(url)
            ticker_list = re.findall(r'etf\\\/(.*?)\\', r.text)

        return ticker_list

    def get_stock_data(self, ticker):
        """ 取得指定股票的數據 """
        return yf.Ticker(ticker.replace('.', '-')).history(period=self.config.PERIOD_LENGTH)
