import os

import matplotlib.pyplot as plt
import mplfinance as mpf


class ChartGenerator:
    """負責生成股票 K 線圖"""

    def __init__(self, save_path='chart.png'):
        self.chart_fig = save_path

    def generate_chart(self, ticker, price_data):
        """生成 K 線圖並存成圖片，並釋放記憶體"""
        mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
        s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
        kwargs = dict(type='candle', mav=(5, 20, 60), volume=True, title=f'{ticker} stock', style=s)

        fig, axlist = mpf.plot(price_data, **kwargs, returnfig=True)
        fig.savefig(self.chart_fig)  # 儲存圖表
        plt.close(fig)  # 釋放記憶體

    def is_chart_generated(self):
        """檢查圖表是否成功生成"""
        return os.path.exists(self.chart_fig)

    def remove_chart(self):
        """刪除生成的圖表"""
        if self.is_chart_generated():
            os.remove(self.chart_fig)
