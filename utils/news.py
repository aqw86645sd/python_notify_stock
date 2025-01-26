from datetime import datetime

import pytz
from newsapi import NewsApiClient

from config import Config


class NewsAPI:
    def __init__(self, config):
        self.api_token = config.NEWS_TOKEN

    def get_news(self, ticker):
        date = self.get_new_york_date()

        newsapi = NewsApiClient(api_key=self.api_token)

        # /v2/top-headlines
        all_articles = newsapi.get_everything(q=ticker,
                                              sources='bbc-news,the-verge',
                                              domains='bbc.co.uk,techcrunch.com',
                                              from_param=date,
                                              to=date,
                                              language='en',
                                              sort_by='publishedAt',
                                              page=2)

        print(all_articles)

    @staticmethod
    def get_new_york_date():
        new_york_timezone = pytz.timezone("America/New_York")
        new_york_time = datetime.now(new_york_timezone)
        new_york_date_str = new_york_time.strftime("%Y-%m-%d")
        return new_york_date_str


if __name__ == "__main__":
    config = Config()
    news_api = NewsAPI(config)
    news_api.get_news("MSFT")
