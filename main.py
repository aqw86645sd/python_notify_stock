import os

from config import Config
from data.data_loader import DataLoader
from strategies.strategies import Strategy1, Strategy2
from utils.chart_generator import ChartGenerator
from utils.notifier import Notifier
from utils.time_helper import TimeHelper

try:
    import functions_framework
except ImportError:
    functions_framework = None


class Entrance:
    def __init__(self, class_data_loader, class_strategies, class_notifier):
        self.data_loader = class_data_loader
        self.strategies = class_strategies
        self.notifier = class_notifier

    def run(self):
        stock_list = self.data_loader.get_etf_ticker_list()

        for ticker in stock_list[:Config.NUM_STOCKS_TO_CHECK]:
            price_data = self.data_loader.get_stock_data(ticker)

            strategy_results = [
                msg for strategy in self.strategies if (msg := strategy.exec(price_data))
            ]

            if strategy_results:
                self.notifier.send(ticker, strategy_results, price_data)


def run_app():
    """統一的應用邏輯，不論在 Cloud Functions 還是本地執行"""
    config = Config()
    time_helper = TimeHelper()
    chart_generator = ChartGenerator()
    notifier = Notifier(config, time_helper, chart_generator)
    data_loader = DataLoader(config, notifier)
    strategies = [Strategy1(config), Strategy2(config)]

    app = Entrance(data_loader, strategies, notifier)
    app.run()


# Cloud Functions 入口（Pub/Sub 觸發）
if functions_framework:
    @functions_framework.cloud_event
    def hello_pubsub(cloud_event):
        print(f"Received Pub/Sub message: {cloud_event.data}")
        run_app()

# 本地測試入口
if __name__ == "__main__":
    if os.getenv("GOOGLE_CLOUD_PROJECT"):
        print("在 Google Cloud Functions 環境，請透過 Pub/Sub 觸發")
    else:
        print("本地測試模式")
        run_app()
