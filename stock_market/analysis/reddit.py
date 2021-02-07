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
        top_posts = get_reddit_top_posts(subreddit=subreddit, num_post=num_post)

        # Top posts
        self.posts = top_posts

        # Analysis from properties
        self._sentiment = None
        self._trending_stocks = None
        self._trending_charts = None

        # Supports
        self._ticker_classification = None

    @property
    def ticker_classification(self):
        # Checking for first time run
        if self._ticker_classification:
            return self._ticker_classification
        else:
            posts = self.posts
            classified_tickers = detect_ticker(text=posts["titles"], source="reddit")

            # Store classified tickers
            self._ticker_classification = classified_tickers

            return classified_tickers
