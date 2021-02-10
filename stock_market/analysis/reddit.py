import pandas as pd

from stock_market.data.reddit.trends import get_reddit_top_posts
from stock_market.model._classification import detect_ticker
from stock_market.model._nlp import nltk_sentiment


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
    def sentiment(self):
        # Checking for first time run
        if self._sentiment:
            return self._sentiment
        else:
            # Get classified ticker data
            ticker_classified = self.ticker_classification
            valid_index = [
                i for i, v in enumerate(ticker_classified) if v
            ]  # Valid indexes
            valid_tickers = [ticker_classified[i] for i in valid_index]

            # Get posts
            # TODO: Incorporate num_comments
            posts = self.posts["titles"]
            valid_posts = [posts[i] for i in valid_index]

            # Perform sentiment
            sentiment_res = nltk_sentiment(valid_posts)

            # Compute avg compound scores
            sentiment_agg = dict()
            for i in range(len(valid_tickers)):
                for ticker in valid_tickers[i]:
                    # Check if ticker exists
                    if sentiment_agg.get(ticker):
                        sentiment_agg[ticker].append(sentiment_res[i]["compound"])
                    else:
                        sentiment_agg[ticker] = [sentiment_res[i]["compound"]]

            # Prepare table with
            sentiment_table = {
                "ticker": list(),
                "mentions": list(),
                "sentiment": list(),
            }
            for ticker in sentiment_agg.keys():
                # Append ticker
                sentiment_table["ticker"].append(ticker)

                # Append number of mentions
                sentiment_table["mentions"].append(len(sentiment_agg[ticker]))

                # Append sentiment scores
                current_score = [sc for sc in sentiment_agg[ticker] if sc != 0.0]
                if current_score:
                    current_score = sum(current_score) / len(current_score)
                else:
                    current_score = 0.0
                sentiment_table["sentiment"].append(current_score)

            sentiment_table = (
                pd.DataFrame(sentiment_table)
                .sort_values(by="sentiment", ascending=False)
                .reset_index(drop=True)
            )

            self._sentiment = sentiment_table

            return sentiment_table
