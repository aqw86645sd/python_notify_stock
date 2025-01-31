import requests

from config import Config
from utils.chart_generator import ChartGenerator
from utils.time_helper import TimeHelper


class Notifier:
    """負責發送 LINE Notify 通知"""

    def __init__(self, config, class_time_helper, class_chart_generator):
        self.config = config
        self.line_token = config.LINE_TOKEN
        self.time_helper = class_time_helper
        self.chart_generator = class_chart_generator

    def line_notify_message_text(self, msg):
        """發送純文字通知"""
        headers = {
            "Authorization": "Bearer " + self.line_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = {'message': msg}
        r = requests.post("https://notify-api.line.me/api/notify", headers=headers, params=payload)
        return r.status_code

    def send(self, ticker, strategy_results, price_data):
        """發送通知，包括文字與圖表"""
        notify_message = self.format_message(ticker, strategy_results)
        self.chart_generator.generate_chart(ticker, price_data)

        if self.chart_generator.is_chart_generated():
            self.line_notify_message(notify_message)
            self.chart_generator.remove_chart()
        else:
            print("Warning: Chart not found, skipping image attachment.")

    def format_message(self, ticker, strategy_results):
        """格式化通知訊息"""
        now = self.time_helper.get_timezone(self.config.TIMEZONE_OFFSET)
        strategy_text = "\n".join(strategy_results)
        return f"{now}\n{ticker}：{strategy_text}"

    def line_notify_message(self, msg):
        """發送帶圖片的通知"""
        url = 'https://notify-api.line.me/api/notify'
        headers = {"Authorization": "Bearer " + self.line_token}
        data = {'message': msg}

        with open(self.chart_generator.chart_fig, 'rb') as image:
            image_file = {'imageFile': image}
            requests.post(url, headers=headers, data=data, files=image_file)


if __name__ == "__main__":
    config = Config()
    time_helper = TimeHelper()
    chart_generator = ChartGenerator()
    notifier = Notifier(config, time_helper, chart_generator)

    notifier.line_notify_message_text("test")
