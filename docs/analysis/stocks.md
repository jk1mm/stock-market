## Stock Analysis


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
