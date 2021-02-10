## NLP Model


1) **nltk_sentiment**

    - *Purpose*: Given a body of text, evaluate a sentiment score (-1,1) to the text using [Vader Lexicon](https://www.kaggle.com/nltkdata/vader-lexicon)
    - *Target data*: Specially targeted well for social media texts
    - *Logic*: Tries to understand the polarity and intensity of emotion in a given text, then distributes a score to 4
               categories: 
        1. Negative
        2. Neutral
        3. Positive
        4. Compound: (Final score based on a,b,c)

```python
# Python

# Import modules
from stock_market.model._nlp import nltk_sentiment

text = "AAPL will have a fantastic run this year!"
print(
    nltk_sentiment(text=text)
)
```
