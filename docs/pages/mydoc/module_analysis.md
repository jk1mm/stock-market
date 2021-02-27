---
title: Analysis
sidebar: mydoc_sidebar
permalink: module_analysis.html
folder: mydoc
---

Github: [analysis directory](https://github.com/jk1mm/stock-market/tree/release/stock_market/analysis)

## Market Index

The **IndexView** module within the analysis directory contains data views for
specified index of interest. The following features are shown in the code
snippet below.

```python
# Python

# Import module
from stock_market.analysis.index import IndexView

# Let's look at the SP500 index information
index_sp500 = IndexView(index = "SP500")

# Get the list of SP500 stocks with the industry
print(index_sp500.data)

# Get today's top and bottom stock performances from this index
top, bottom = index_sp500.summary_stocks_today
print(top)
print(bottom)

```

## Stock

The **stock_profit** function within the analysis directory contains net profit
view for a particular stock of interest.

The **stock_chart** function returns a stock chart (price & volume)
comparison between n number of requested stocks.

The following features are shown in the code snippet below.

```python
# Python

# Import module
from stock_market.analysis.stocks import stock_profit, stock_chart

# Get the supposed net profit if 100 AAPL stocks were purchased
# at market open on January 7 2021 and sold one week after before market close
print(
    stock_profit(ticker="AAPL", 
                 quantity=100, 
                 purchase_date="2021-01-07",
                 sell_date="2021-01-14",
                 purchase_time="Open",
                 sell_time="Close")
)

# Compare EV stocks: NIO, TSLA, NKLA for last year
stock_chart(stocks=["NIO", "TSLA", "NKLA"],
            start_date="2020-01-01",
            end_date="2020-12-31").show()

```

## IPO

The **RecentIPO** module within the analysis directory contains analytical functionalities
and data views for recently IPOed stocks. The following features are shown in the code
snippet below.

```python
# Python

# Import module
from stock_market.analysis.ipo import RecentIPO

# Get the overall summary of recently IPOed stocks
recent_ipo = RecentIPO()
print(recent_ipo.overall_summary)

# Get the individual summary of a recently IPOed stock
print(recent_ipo.individual_summary(ticker="ABNB"))

```

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
