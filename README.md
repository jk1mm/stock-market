# Stock Market

Research & Analysis driven module, with the aim to help improve a trading
decision or optimize a stock portfolio. Market/trend data, market analysis, 
and financial models are some upcoming work in the making.


## Overview
<p align="center"><img src="https://github.com/jk1mm/stock-market/blob/release/docs/images/overview_flowchart.png"></p>


---
## Module Listing
 * [Data](https://github.com/jk1mm/stock-market#data)
 * [Analysis](https://github.com/jk1mm/stock-market#analysis)
 * [Model](https://github.com/jk1mm/stock-market#model)

---

## Modules

### Data

#### [Market data](stock_market/data)
 - **Stocks**: Get stocks performances for a date range given 
               a ticker symbol
 - **IPO**: Get IPO related data from [MarketWatch](https://www.marketwatch.com/tools/ipo-calendar)
            and populate new metrics
 - **Index**: Get market indexes (e.g. S&P 500) 
 - [**Reddit**](https://www.reddit.com/): Understand the general sentiment around most discussed stocks and topics


### Analysis

#### [Market analysis](stock_market/analysis)
- **IPO**: Analysis on recent and upcoming IPO stocks
    1) General success metrics on recent IPO bubble.
    2) Optimal sell day analysis.
    3) Individual stock performance views.
  

- **Index**: Analysis on a market index
    1) Stock categorization summary by industry.
    2) Index performance for different periodic times.
    3) Today's top and bottom performing stocks.


- **Stocks**: Analysis on stocks
    1) Stock net profit calculator: Supposed net gain on a stock for a 
       buy and sell on a specified date period.
    2) Stock chart comparison between a list of requested stocks to view. 
       Provides quick and easy way to analyze the performance of each stock
       aligned by a date range.


- **Reddit**: Analysis on Reddit posts
    1) Sentiment view of trending Reddit posts in a specified subreddit, leveraging 
       ticker detection and sentiment model from [models](stock_market/model).
       

### Model

#### [Statistical Models](stock_market/model)
- **Classification**: Models relating to classification
    1) Detect Stock: Identifies the ticker being discussed in a given text.


- **NLP**: Models relating to natural language processing
    1) NLTK Sentiment: Leverages Vader Lexicon data to evaluate a given text's sentiment.
