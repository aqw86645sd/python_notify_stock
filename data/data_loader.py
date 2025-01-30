import re

import requests
import yfinance as yf


class DataLoader:
    def __init__(self, class_config, class_notifier):
        self.config = class_config
        self.notifier = class_notifier

    def get_etf_ticker_list(self):
        """ 取得 ETF 的股票清單 """
        url = f"https://www.zacks.com/funds/etf/{self.config.ETF_SYMBOL}/holding"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

        try:
            with requests.Session() as req:
                req.headers.update(headers)
                r = req.get(url)
                ticker_list = re.findall(r'etf\\\/(.*?)\\', r.text)

            return ticker_list

        except requests.exceptions.RequestException as e:
            self.notifier.line_notify_message_text(f"❌ 取得 ETF 股票清單失敗: {e}")
            return []  # 返回空列表以防止主程式崩潰

    def get_stock_data(self, ticker):
        """ 取得指定股票的數據 """
        try:
            stock_data = yf.Ticker(ticker.replace('.', '-')).history(period=self.config.PERIOD_LENGTH)
            if stock_data.empty:
                self.notifier.line_notify_message_text(f"⚠️ 無法獲取 {ticker} 的歷史數據")
            return stock_data

        except Exception as e:
            self.notifier.line_notify_message_text(f"❌ 無法取得 {ticker} 的股票數據: {e}")
            return None  # 返回 None 表示數據獲取失敗
