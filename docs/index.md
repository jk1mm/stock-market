---
title: "Stock Market Analysis"
sidebar: mydoc_sidebar
permalink: index.html
summary: High level overview of the stock-market package.
---

## Objective

Research & Analysis driven module, with the aim to help improve a trading
decision or optimize a stock portfolio. Market/trend data, market analysis,
and financial models are some upcoming work in the making.

{% include image.html file="overview_flowchart.png" caption="" %}


## Modules

### Data
 - **Stocks**: Get stocks performances for a date range given
               a ticker symbol
 - **IPO**: Get IPO related data from [MarketWatch](https://www.marketwatch.com/tools/ipo-calendar)
            and populate new metrics
 - **Index**: Get market indexes (e.g. S&P 500)
 - [**Reddit**](https://www.reddit.com/): Understand the general sentiment around most discussed stocks and topics


### Analysis
- **IPO**: Analysis on recent and upcoming IPO stocks
    - General success metrics on recent IPO bubble.
    - Optimal sell day analysis.
    - Individual stock performance views.


- **Index**: Analysis on a market index
    - Stock categorization summary by industry.
    - Index performance for different periodic times.
    - Today's top and bottom performing stocks.

- **Stocks**: Analysis on stocks
    - Stock net profit calculator: Supposed net gain on a stock for a
      buy and sell on a specified date period.
    - Stock chart comparison between a list of requested stocks to view.
      Provides quick and easy way to analyze the performance of each stock
      aligned by a date range.


- **Reddit**: Analysis on Reddit posts
    - Sentiment view of trending Reddit posts in a specified subreddit, leveraging
      ticker detection and sentiment model from [models](stock_market/model).


### Model
- **Classification**: Models relating to classification
    - Detect Stock: Identifies the ticker being discussed in a given text.


- **NLP**: Models relating to natural language processing
    - NLTK Sentiment: Leverages Vader Lexicon data to evaluate a given text's sentiment.

