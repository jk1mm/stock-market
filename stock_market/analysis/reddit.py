from typing import Union, List, Tuple, Optional


TICKER_LEN_MAX = 5
AVAILABLE_SOURCE = ["reddit"]


# TODO: Ticker recognizer
def detect_ticker(
    text: Union[str, List[str], Tuple[str]], source: str = "reddit"
) -> Optional[List[str]]:
    """
    Detects discussed ticker in a (list of) body of text.

    Parameters
    ----------
    text: Union[str, List[str], Tuple[str]]
        (List of) Body of text to detect presence of tickers.

    source: str, default "reddit"
        Source the body of text comes from. Logic of ticker detection may vary depending on source.

    Returns
    -------
    ticker_detection: Optional[List[str]]
        List of list of detected tickers for each body of text.

    """
    # Verify source is available
    if source.lower() not in AVAILABLE_SOURCE:
        return None

    # If one text specified as str
    if not isinstance(text, (list, tuple)):
        text = [text]

    # List of ticker detection
    ticker_detection = list()

    # For reddit source
    if source == "reddit":
        reddit_common = ["DD", "COVID", "WSB"]

        # Go through each phrases in text (list)
        for phrase in text:

            # Breakdown texts
            phrase_dec = phrase.split()

            # Rules:
            # R-1) Ticker starts with $. If at least one word is detected, move on to next phrase assuming that
            #      the user is consistent with their ticker mentions with $ beginning.
            if "$" in phrase_dec:
                phrase_dec.remove("$")
            r1 = list(filter(lambda word: word[0] == "$", phrase_dec))

            if r1:
                # Remove invalid len tickers
                r1 = [
                    ticker[1:].upper()
                    for ticker in r1
                    if len(ticker) <= TICKER_LEN_MAX + 1
                ]

                if r1:
                    # Add data and continue with loop
                    ticker_detection.append(r1)
                    continue

    return ticker_detection


# TODO: use nlp models and ticker to perform sentiment analysis

# TODO: Given a ticker channel, sentiment analysis based on each articles (high level)
