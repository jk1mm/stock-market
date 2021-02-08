from collections import Counter

import pandas as pd

from stock_market.data.reddit.trends import get_reddit_top_posts
from stock_market.model._classification import detect_ticker


class RedditSentiment(object):
    """Sentiment analysis on a subreddit's mentioned stocks

    Access a specified subreddit channel to identify most discussed tickers and the sentiments.

    Parameters
    ----------
    subreddit: str
        Subreddit channel name.

    num_post: int, default 10
        The number of top posts to analyze from the subreddit.

    time_period: str
        Time period of the top posts.

    Notes
    -----
    Reddit connection credentials must be specified in the .env file in the root level of stock_market.

    """

    def __init__(self, subreddit: str, num_post: int = 10, time_period: str = "day"):
        top_posts = get_reddit_top_posts(
            subreddit=subreddit, num_post=num_post, time_period=time_period
        )

        # Top posts
        self.posts = top_posts

        # Analysis from properties
        self._sentiment = None
        self._trending_stocks = None
        self._trending_charts = None

        # Supports
        self._ticker_classification = None

    @property
    def ticker_classification(self) -> list:
        """
        Classifies ticker of discussion for each subreddit posts.

        """
        # Checking for first time run
        if self._ticker_classification:
            return self._ticker_classification
        else:
            posts = self.posts
            classified_tickers = detect_ticker(text=posts["titles"], source="reddit")

            # Store classified tickers
            self._ticker_classification = classified_tickers

            return classified_tickers

    @property
    def trending_stocks(self) -> pd.DataFrame:
        """
        Ranks the stocks by most discussed.

        """
        # Checking for first time run
        if self._trending_stocks:
            return self._trending_stocks
        else:
            # Get classified ticker data
            ticker_classified = self.ticker_classification

            flattened_list = [
                item
                for sublist in list(filter(None, ticker_classified))
                for item in sublist
            ]

            trending_table = (
                pd.DataFrame(
                    {
                        "ticker": list(Counter(flattened_list).keys()),
                        "mentions": list(Counter(flattened_list).values()),
                    }
                )
                .sort_values(by="mentions", ascending=False)
                .reset_index(drop=True)
            )
            self._trending_stocks = trending_table

            return trending_table
