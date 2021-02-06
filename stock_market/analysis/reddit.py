from typing import Union, List, Tuple, Optional


TICKER_LEN_MAX = 5


# TODO: Ticker recognizer
def detect_ticker(
    text: Union[str, List[str], Tuple[str]], count_max: int = 1
) -> Optional[List[str]]:
    # If one text specified as str
    if not isinstance(text, (list, tuple)):
        text = [text]


    return None


# TODO: use nlp models and ticker to perform sentiment analysis

# TODO: Given a ticker channel, sentiment analysis based on each articles (high level)
