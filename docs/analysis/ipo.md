## IPO Analysis


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
