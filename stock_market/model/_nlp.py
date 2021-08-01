from pathlib import Path as _Path
from typing import Dict, List, Union

from nltk.sentiment.vader import SentimentIntensityAnalyzer


# nltk Vader Lexicon - Sentiment Analysis
def nltk_sentiment(
    text: Union[str, List[str]]
) -> Union[Dict[str, float], List[Dict[str, float]]]:
    """
    Sentiment analysis using Vader Lexicon (tuned for social media sentiments).

    Parameters
    ----------
    text: Union[str, List[str]]
        Sentence(s) to perform sentiment analysis on.

    Returns
    -------
    result: Union[Dict[str, float], List[Dict[str, float]]]
        Sentiment scores.

    """
    # Refer to lexicon data
    vader_sentiment = SentimentIntensityAnalyzer(
        lexicon_file=str(
            _Path(__file__).parent.parent / "data/_files/vader_lexicon.txt"
        ),
    )

    # Check input text
    if type(text) is list:
        result = list()
        for phrase in text:
            result.append(vader_sentiment.polarity_scores(phrase))

    else:
        result = vader_sentiment.polarity_scores(str(text))

    return result
