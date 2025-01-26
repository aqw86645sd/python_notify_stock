from config import Config
from data.data_loader import DataLoader
from strategies.strategies import Strategy1, Strategy2
from utils.notifier import Notifier


class Entrance:
    def __init__(self, data_loader, strategies, notifier):
        self.data_loader = data_loader
        self.strategies = strategies
        self.notifier = notifier

    def run(self):
        stock_list = self.data_loader.get_etf_ticker_list()

        for ticker in stock_list[:Config.NUM_STOCKS_TO_CHECK]:
            price_data = self.data_loader.get_stock_data(ticker)
            strategy_results = []

            for strategy in self.strategies:
                if strategy.check(price_data):
                    strategy_results.append(strategy.result(price_data))

            if strategy_results:
                self.notifier.send(ticker, strategy_results, price_data)


if __name__ == '__main__':
    config = Config()
    data_loader = DataLoader(config)
    strategies = [Strategy1(config), Strategy2(config)]
    notifier = Notifier(config)

    app = Entrance(data_loader, strategies, notifier)
    app.run()
