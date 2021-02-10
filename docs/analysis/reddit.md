## Reddit Analysis


The **RedditSentiment** module within the analysis directory contains analytical functionalities
to detect top trending stocks along with a sentiment score, to understand bearish/bullish news 
behind certain tickers. The following features are shown in the code snippet below.

```python
# Python

# Import module
from stock_market.data.reddit import load_reddit_credentials
from stock_market.analysis.reddit import RedditSentiment

# Load your Reddit account credentials to env
load_reddit_credentials(
    client_id="reddit_id",
    client_secret="reddit_secret_key",
    username="reddit_username",
    password="reddit_password"
)

# Perform sentiment analysis for "wallstreetbets" channel
wsb_sentiment = RedditSentiment(
    subreddit="wallstreetbets",
    num_post=100,
    time_period="day"
)
print(wsb_sentiment.posts)  # See the actual posts and number of comments

print(wsb_sentiment.sentiment)  # View ranked sentiment scores
```
