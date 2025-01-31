from datetime import datetime, timedelta

import pytz
from newsapi import NewsApiClient

from config import Config


class NewsAPI:
    def __init__(self, class_config):
        self.api_token = class_config.NEWS_TOKEN

    def get_news(self, ticker):
        date = self.get_new_york_yesterday()

        newsapi = NewsApiClient(api_key=self.api_token)

        articles = newsapi.get_everything(
            q=ticker,
            from_param=date,
            sort_by='publishedAt'
        )

        print(articles)


    @staticmethod
    def get_new_york_today():
        new_york_timezone = pytz.timezone("America/New_York")
        new_york_time = datetime.now(new_york_timezone)
        new_york_date_str = new_york_time.strftime("%Y-%m-%d")
        return new_york_date_str

    @staticmethod
    def get_new_york_yesterday():
        new_york_timezone = pytz.timezone("America/New_York")
        new_york_time = datetime.now(new_york_timezone) - timedelta(days=1)
        new_york_yesterday_str = new_york_time.strftime("%Y-%m-%d")
        return new_york_yesterday_str


if __name__ == "__main__":
    config = Config()
    news_api = NewsAPI(config)
    news_api.get_news("MSFT")
