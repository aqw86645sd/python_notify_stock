from statistics import mean

class Strategy1:
    def __init__(self, config):
        self.config = config

    def check(self, data):
        """ 檢查策略1是否符合條件 """
        close_list = data['Close'].tolist()

        if len(close_list) < 2:
            return False

        close_today = close_list[-1]
        close_yesterday = close_list[-2]
        price_percent = round((close_today - close_yesterday) * 100 / close_yesterday, 2)

        volume_list = data['Volume'].tolist()
        volume_avg_20 = mean(volume_list)
        volume_avg_5 = mean(volume_list[-5:])
        volume_time = round(volume_avg_5 / volume_avg_20, 2)

        return abs(price_percent) >= self.config.STRATEGY_1_PRICE_LIMIT and volume_time >= self.config.STRATEGY_1_VOLUME_LIMIT

    def result(self, data):
        close_list = data['Close'].tolist()
        close_today = close_list[-1]
        close_yesterday = close_list[-2]
        price_percent = round((close_today - close_yesterday) * 100 / close_yesterday, 2)

        volume_list = data['Volume'].tolist()
        volume_avg_20 = mean(volume_list)
        volume_avg_5 = mean(volume_list[-5:])
        volume_time = round(volume_avg_5 / volume_avg_20, 2)

        return f"策略1 : 漲跌 {price_percent}%, 成交量增加 {volume_time} 倍"


class Strategy2:
    def __init__(self, config):
        self.config = config

    def check(self, data):
        """ 檢查策略2是否符合條件 (短期與長期移動平均線的交叉) """
        short_ma = data['Close'].rolling(window=self.config.STRATEGY_2_SHORT_MA_PERIOD).mean()
        long_ma = data['Close'].rolling(window=self.config.STRATEGY_2_LONG_MA_PERIOD).mean()

        if len(short_ma) < 2 or len(long_ma) < 2:
            return False

        return (short_ma.iloc[-2] < long_ma.iloc[-2] and short_ma.iloc[-1] > long_ma.iloc[-1]) or \
               (short_ma.iloc[-2] > long_ma.iloc[-2] and short_ma.iloc[-1] < long_ma.iloc[-1])

    def result(self, data):
        short_ma = data['Close'].rolling(window=self.config.STRATEGY_2_SHORT_MA_PERIOD).mean()
        long_ma = data['Close'].rolling(window=self.config.STRATEGY_2_LONG_MA_PERIOD).mean()

        if short_ma.iloc[-2] < long_ma.iloc[-2] and short_ma.iloc[-1] > long_ma.iloc[-1]:
            return "策略2 : 短期移動平均線上穿長期移動平均線，買入訊號"

        if short_ma.iloc[-2] > long_ma.iloc[-2] and short_ma.iloc[-1] < long_ma.iloc[-1]:
            return "策略2 : 短期移動平均線下穿長期移動平均線，賣出訊號"
