## Stock data


The **get_ticker** function retrieves a stock's price history for a specified date range. 
It leverages the **pandas_datareader** module to extract data from Yahoo finance, and provides
additional (self-added) metrics for future analytics.

```python
# Python

# Import module
from stock_market.data import get_ticker

# Get Airbnb's performance from December 10th
abnb = get_ticker(ticker="ABNB",
                  start_date="2020-12-10")
print(abnb)
```
