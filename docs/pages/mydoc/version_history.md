---
title: Version History
sidebar: mydoc_sidebar
permalink: version_history.html
folder: mydoc
---

## Versions

Below lists the history of changes made to this package.

### V1.0 +

#### 1.3.1
- Data health call, using [finviz](https://pypi.org/project/finviz/) api

#### 1.3.0
- IPO data module, fix several bugs
- isort addition

#### 1.2.1
- Update documentation to Jekyll format

#### 1.2.0
- Add Reddit data and analysis:
    - Add connection and get top post data
    - Sentiment analysis
- Add model directory:
    - NLP model
        - Add NLTK sentiment
    - Classification model:
        - Add ticker detector

#### 1.1.4
- Stock Analysis directory:
    - stock_chart: provide a quick and easy way to analyze the performance of each stock aligned by a date range
        - Price and volume comparison

#### 1.1.3
- Stock Analysis directory:
    - stock_profit: function to calculate net gain on a stock buy/sell scenario

#### 1.1.2
- Index Analysis: High level summary of index performance and sector categorization
    - Stock categorization summary by industry
    - Index performance for different periodic times
    - Today's top and bottom performing stocks
- Minor module name changes, relocating variables to constant folder, some test changes

#### 1.1.1
- IPO Analysis: Add individual_summary function
    - In depth report on a specified ticker
    - Plotly chart view on ticker
- Some variable name changes

#### 1.1.0
- Add Analysis directory
    - Recent IPO: Analysis on recent and upcoming IPO stocks
        - General success metrics on recent IPO bubble (general and individual view)
        - Optimal sell day analysis (general and individual views)

#### 1.0.2
- Restructure modules
- Update docs

#### 1.0.1
- Update on get_ticker:
    - Add new metrics: day to day change, within day change, day volatility (pct and value), dollar traded
- Store S&P 500 data
- Create constants file
- Create new directory(for future add on features)

#### 1.0.0
- Market data:
    - Stock data given ticker symbol
    - IPO information from MarketWatch

## Source

Version history on [Github](https://github.com/jk1mm/stock-market/releases).
