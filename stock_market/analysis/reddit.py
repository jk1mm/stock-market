from stock_market.data.reddit.trends import get_reddit_top_posts


class RedditSentiment(object):
    """Sentiment analysis on a subreddit's mentioned stocks

    Access a specified subreddit channel to identify most discussed tickers and the sentiments.

    Parameters
    ----------
    subreddit: str
        Subreddit channel name.

    n: int, default 10
        The number of top posts to analyze from the subreddit.

    Notes
    -----
    Reddit connection credentials must be specified in the .env file in the root level of stock_market.

    """

    def __init__(
        self,
        subreddit: str,
        n: int = 10,
    ):
        top_posts = get_reddit_top_posts(subreddit=subreddit, limit=n)

        self.posts = top_posts

    # TODO: sentiment analysis
    # TODO: stock mentions
    # TODO: leveraging get_ticker
