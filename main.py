# -- coding: utf-8 --
import requests
import yfinance as yf
import re
import mplfinance as mpf
import os
import datetime
from statistics import mean

# 定義 token 檔案名稱
file_path = "token/line_token"


class Entrance:
    def __init__(self):
        # variable
        # strategy 1
        self.strategy_1_price_percent_limit = 4  # 漲跌百分比限制
        self.strategy_1_volume_percent_limit = 2  # 交易量百分比限制

        # fixed value
        self.news_url_format_cnbc = 'https://www.cnbc.com/quotes/{}?tab=news'  # CNBC 新聞網站
        self.news_url_format_cnyes = 'https://www.cnyes.com/search/news?keyword={}'  # 鉅亨 新聞網站
        self.line_token = open(file_path, "r").read()  # 跟line申請權杖
        self.chart_fig = 'chart.png'

    def run(self):

        # VOO list
        stock_list = self.get_etf_ticker_list("VOO")

        for ticker in stock_list[:50]:

            is_show = False

            strategy_text = "\n"

            # 標的相關資訊
            yf_data = yf.Ticker(ticker.replace('.', '-'))

            # 執行策略
            strategy_1_is_show, strategy_1_content = self.strategy_1(yf_data)

            if strategy_1_is_show:
                is_show = True
                strategy_text += strategy_1_content + "\n"

            # 其中一個符合
            if is_show:

                yf_info = yf_data.info

                # generate image
                if self.get_stock_chart(ticker):
                    stock_info = ticker + '：' + yf_info['shortName'] + ', ' + yf_info['industry'] + strategy_text
                    news_url_cnbc = self.news_url_format_cnbc.format(ticker)
                    news_url_cnyes = self.news_url_format_cnyes.format(ticker)

                    now = self.get_timezone(8)
                    notify_message = str(now) + '\n' + stock_info + '\n' + news_url_cnbc + '\n' + news_url_cnyes  # 訊息

                    self.line_notify_message(notify_message)

                    # 刪除 image 檔案
                    os.remove('./' + self.chart_fig)

    @staticmethod
    def get_etf_ticker_list(etf_symbol):
        """ getting holdings data from Zacks for the given ticker """
        url = "https://www.zacks.com/funds/etf/{}/holding".format(etf_symbol)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"
        }

        with requests.Session() as req:
            req.headers.update(headers)
            r = req.get(url)
            ticker_list = re.findall(r'etf\\\/(.*?)\\', r.text)

        return ticker_list

    def get_stock_chart(self, p_ticker):
        """
        將 chart 存成圖
        :param p_ticker: 標的
        :return:
        """
        ticker_yahoo_data = yf.Ticker(p_ticker.replace('.', '-'))
        ticker_period_data = ticker_yahoo_data.history(period="100d")

        mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
        s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
        kwargs = dict(type='candle', mav=(5, 20, 60), volume=True, title=p_ticker + ' stock', style=s)

        mpf.plot(ticker_period_data, **kwargs, savefig=self.chart_fig)

        return True

    def line_notify_message(self, msg):
        # 跟line申請權杖
        token = self.line_token

        url = 'https://notify-api.line.me/api/notify'

        headers = {
            "Authorization": "Bearer " + token
        }

        data = {
            'message': msg
        }

        image = open('./' + self.chart_fig, 'rb')
        image_file = {'imageFile': image}

        r = requests.post(url, headers=headers, data=data, files=image_file)
        return r.status_code

    @staticmethod
    def get_timezone(h):
        """
        回傳時區時間
        :return:
        """
        gmt = datetime.timezone(datetime.timedelta(hours=h))  # 取得時區
        return datetime.datetime.now(tz=gmt).strftime('%Y/%m/%d %H:%M:%S')  # 回傳該時區的時間

    def strategy_1(self, yf_data):
        """
            策略一
            當日漲跌要超過一定數值
            偵測近期成交量與
        """
        is_show = False  # 符合
        content = ""  # 內容

        """ 收盤價 """
        close_list = yf_data.history(period="2d")['Close'].tolist()

        if len(close_list) != 2:
            return False, ""

        close_today = close_list[1]
        close_yesterday = close_list[0]

        price_percent = round((close_today - close_yesterday) * 100 / close_yesterday, 2)

        """ 交易量 """
        volume_list = yf_data.history(period="20d")['Volume'].tolist()

        if len(volume_list) != 20:
            return False, ""

        volume_avg_20 = mean(volume_list)

        volume_avg_5 = mean(volume_list[:5])

        volume_time = round(volume_avg_5 / volume_avg_20, 2)

        """ 邏輯條件 """
        if abs(price_percent) >= self.strategy_1_price_percent_limit and volume_time >= self.strategy_1_volume_percent_limit:
            is_show = True
            content = "策略1 : 漲跌 {}%, 成交量增加 {} 倍".format(str(price_percent), str(volume_time))

        return is_show, content


if __name__ == '__main__':
    # 檢查檔案是否存在
    if not os.path.exists(file_path):
        # 如果檔案不存在，創建一個新檔案
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 建立檔案
        with open(file_path, 'w') as file:
            file.write('')  # 可以在這裡寫入初始內容

        print(f"已創建新的 line_token 檔案，請填入 Line taken。")
    else:
        execute = Entrance()
        execute.run()
