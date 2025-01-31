from config import Config
from data.data_loader import DataLoader
from strategies.strategies import Strategy1, Strategy2
from utils.chart_generator import ChartGenerator
from utils.notifier import Notifier
from utils.time_helper import TimeHelper


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


if __name__ == '__main__':
    config = Config()
    time_helper = TimeHelper()
    chart_generator = ChartGenerator()
    notifier = Notifier(config, time_helper, chart_generator)
    data_loader = DataLoader(config, notifier)
    strategies = [Strategy1(config), Strategy2(config)]

    app = Entrance(data_loader, strategies, notifier)
    app.run()
