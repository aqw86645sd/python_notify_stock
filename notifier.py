import os
import datetime
import requests
import mplfinance as mpf

class Notifier:
    def __init__(self, config):
        self.config = config
        self.line_token = open(self.config.LINE_TOKEN_FILE, "r").read()
        self.chart_fig = 'chart.png'

    def send(self, ticker, strategy_results, price_data):
        """ 發送通知 """
        notify_message = self.format_message(ticker, strategy_results)

        mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
        s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
        kwargs = dict(type='candle', mav=(5, 20, 60), volume=True, title=ticker + ' stock', style=s)

        mpf.plot(price_data, **kwargs, savefig=self.chart_fig)


        if self.is_chart_generated():
            self.line_notify_message(notify_message)
            os.remove('./' + self.chart_fig)  # 確保圖片存在後再刪除
        else:
            print("Warning: Chart not found, skipping image attachment.")

    def format_message(self, ticker, strategy_results):
        """ 格式化訊息 """
        now = self.get_timezone(self.config.TIMEZONE_OFFSET)
        strategy_text = "\n".join(strategy_results)
        return f"{now}\n{ticker}：{strategy_text}"

    def line_notify_message(self, msg):
        url = 'https://notify-api.line.me/api/notify'
        headers = {"Authorization": "Bearer " + self.line_token}
        data = {'message': msg}
        image = open('./' + self.chart_fig, 'rb')
        image_file = {'imageFile': image}
        requests.post(url, headers=headers, data=data, files=image_file)

    def is_chart_generated(self):
        """ 檢查圖表文件是否存在 """
        return os.path.exists(self.chart_fig)

    @staticmethod
    def get_timezone(offset):
        gmt = datetime.timezone(datetime.timedelta(hours=offset))
        return datetime.datetime.now(tz=gmt).strftime('%Y/%m/%d %H:%M:%S')
