## IPO data


Initial Public Offering is the offering of a company's shares into the stock market/exchange. 
IPO data is a fascinating topic as price volatility tends to be high due to the unexpected demands
or hype of companies. Proper analysis on this data can provide some meaningful signals for recent 
or upcoming IPOs.


The IPO module below is a python object, that webscrapes from
[MarketWatch](https://www.marketwatch.com/tools/ipo-calendar). The following data can be extracted
from this class:
1) Recent IPO
2) Upcoming IPO (within the next two weeks)
3) Future IPO (past the two weeks)
4) Withdrawn IPO


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
