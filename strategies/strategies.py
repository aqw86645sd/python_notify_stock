from statistics import mean


class Strategy1:
    def __init__(self, class_config):
        self.config = class_config

    def exec(self, data):
        """ 檢查策略1是否符合條件 """
        if len(data) < 2 or len(data['Volume']) < self.config.STRATEGY_1_VOLUME_PERIOD:
            return None

        # 計算價格變動百分比
        close_today, close_yesterday = data['Close'].iloc[-1], data['Close'].iloc[-2]
        price_percent = round((close_today - close_yesterday) * 100 / close_yesterday, 2)

        # 計算成交量比率 (今日成交量 / 過去 n 日均量)
        volume_avg = mean(data['Volume'].iloc[-self.config.STRATEGY_1_VOLUME_PERIOD:])
        volume_today = data['Volume'].iloc[-1]
        volume_ratio = round(volume_today / volume_avg, 2)

        # 判斷是否符合策略條件
        if abs(price_percent) >= self.config.STRATEGY_1_PRICE_LIMIT and volume_ratio >= self.config.STRATEGY_1_VOLUME_LIMIT:
            return f"策略1 : 漲跌 {price_percent}%, 成交量比 {self.config.STRATEGY_1_VOLUME_PERIOD} 日平均增加 {volume_ratio} 倍"

        return None


class Strategy2:
    def __init__(self, config):
        self.config = config

    def exec(self, data):
        """ 檢查策略2是否符合條件 (短期與長期移動平均線的交叉) """
        if len(data) < self.config.STRATEGY_2_LONG_MA_PERIOD:
            return None

        # 計算短期與長期移動平均線
        short_ma = data['Close'].rolling(window=self.config.STRATEGY_2_SHORT_MA_PERIOD).mean()
        long_ma = data['Close'].rolling(window=self.config.STRATEGY_2_LONG_MA_PERIOD).mean()

        # 檢查是否有有效的移動平均線數據
        if short_ma.isna().sum() > 0 or long_ma.isna().sum() > 0:
            return None

        # 檢查買入和賣出信號
        if short_ma.iloc[-2] < long_ma.iloc[-2] and short_ma.iloc[-1] > long_ma.iloc[-1]:
            return "策略2 : 短期移動平均線上穿長期移動平均線，買入訊號"
        elif short_ma.iloc[-2] > long_ma.iloc[-2] and short_ma.iloc[-1] < long_ma.iloc[-1]:
            return "策略2 : 短期移動平均線下穿長期移動平均線，賣出訊號"

        return None
