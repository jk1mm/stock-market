---
title: Classification
sidebar: mydoc_sidebar
permalink: model_module_classification.html
folder: mydoc
---

Github: [model directory](https://github.com/jk1mm/stock-market/tree/release/stock_market/model)

## detect_ticker

- *Purpose*: Given a body of text, correctly identify the set of ticker(s) being discussed
- *Target data*: Reddit (or similar social media data)
- *Logic*: Refer to github [code](https://github.com/jk1mm/stock-market/blob/release/stock_market/model/_classification.py)
- *Statistical Reasoning*:
    1. <ins>Minimizing false positives</ins> is crucial as incorrectly stating tickers can significantly skew
       towards a common word (e.g. auxiliary verbs, pronouns)
    2. Given a <ins>larger sample size</ins> of posts, some tickers that are affected by false negatives are
       hopefully recognized correctly from other posts
    3. Understand the <ins>derivation</ins> of ticker attributes (from North American market), which do not contain
       digits and have a prior known max ticker length

```python
# Python

# Import module
from stock_market.model._classification import detect_ticker

text = "AAPL will have a fantastic run this year!"
print(
   detect_ticker(text=text, source="reddit")
)

```
