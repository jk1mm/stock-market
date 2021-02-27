---
title: Data
sidebar: mydoc_sidebar
permalink: module_data.html
folder: mydoc
---

Github: [data directory](https://github.com/jk1mm/stock-market/tree/release/stock_market/data)

## Market Index

Market index data will be stored within the data module to perform
various analytics on market trends and formation of recommendation models.

Currently available index(es):
 - S&P500

```python
# Python

# Import data
from stock_market.data import SP500

# View S&P 500 data
print(SP500)

```

## Stocks

The **get_ticker** function retrieves a stock's price history for a specified date range.
It leverages the **pandas_datareader** module to extract data from Yahoo finance, and provides
additional (self-added) metrics for future analytics.

```python
# Python

# Import module
from stock_market.data import get_ticker

# Get Airbnb's performance from December 10th
abnb = get_ticker(
    ticker="ABNB",
    start_date="2020-12-10"
)

# View Airbnb's stock performance
print(abnb)

```

## IPO

Initial Public Offering is the offering of a company's shares into the stock market/exchange.
IPO data is a fascinating topic as price volatility tends to be high due to the unexpected demands
or hype of companies. Proper analysis on this data can provide some meaningful signals for recent
or upcoming IPOs.

The IPO module below is a python object, that webscrapes from
[MarketWatch](https://www.marketwatch.com/tools/ipo-calendar). The following data can be extracted
from this class:
1. Recent IPO
2. Upcoming IPO (within the next two weeks)
3. Future IPO (past the two weeks)
4. Withdrawn IPO


```python
# Python

# Import module
from stock_market.data import IPO

market_ipo = IPO()

# 1) Recent IPO
print(market_ipo.recent_ipo)

# 2) Upcoming IPO
print(market_ipo.upcoming_ipo)

# 3) Future IPO
print(market_ipo.future_ipo)

# 4) Withdrawn IPO
print(market_ipo.withdrawn_ipo)

```

## Reddit

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

