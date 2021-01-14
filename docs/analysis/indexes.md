## Index Analysis


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
