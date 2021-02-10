## Reddit data


Reddit posting data for a given subreddit channel. This data can be used
for various NLP related analysis to understand trending stocks and sentiments
behind certain stock.

```python
# Python

# Import modules
from stock_market.data.reddit import load_reddit_credentials
from stock_market.data import get_reddit_top_posts


# Load your Reddit account credentials to env
load_reddit_credentials(
    client_id="reddit_id",
    client_secret="reddit_secret_key",
    username="reddit_username",
    password="reddit_password"
)

# Get top 100 posts for "wallstreetbets" channel for today
print(
    get_reddit_top_posts(
        subreddit="wallstreetbets",
        num_post=100,
        time_period="day"
    )
)
```
