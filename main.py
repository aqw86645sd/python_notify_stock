from config import Config
from stock_data import StockData
from strategies import Strategy1, Strategy2
from notifier import Notifier


class Entrance:
    def __init__(self, stock_data, strategies, notifier):
        self.stock_data = stock_data
        self.strategies = strategies
        self.notifier = notifier

    def run(self):
        stock_list = self.stock_data.get_etf_ticker_list()

        for ticker in stock_list[:Config.NUM_STOCKS_TO_CHECK]:
            price_data = self.stock_data.get_stock_data(ticker)
            strategy_results = []

            for strategy in self.strategies:
                if strategy.check(price_data):
                    strategy_results.append(strategy.result(price_data))

            if strategy_results:
                self.notifier.send(ticker, strategy_results, price_data)


if __name__ == '__main__':
    config = Config()
    stock_data = StockData(config)
    strategies = [Strategy1(config), Strategy2(config)]
    notifier = Notifier(config)

    app = Entrance(stock_data, strategies, notifier)
    app.run()
