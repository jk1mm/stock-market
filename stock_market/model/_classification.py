from typing import Union, List, Tuple

TICKER_LEN_MAX = 5
AVAILABLE_SOURCE = ["reddit"]


def detect_ticker(
    text: Union[str, List[str], Tuple[str]], source: str = "reddit"
) -> List[Union[None, List[str]]]:
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
    ticker_detection: List[Union[None, List[str]]]
        List of list of detected tickers for each body of text.

    """
    # Verify source is available
    source = source.lower()
    if source not in AVAILABLE_SOURCE:
        raise Warning(f"Choose from the current available sources: {AVAILABLE_SOURCE}")

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
                phrase_dec = list(filter(lambda word: word != "$", phrase_dec))
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

            # R-2) Look for cap locks
            r2 = [
                word
                for word in phrase_dec
                if word.isupper()
                and (len(word) <= TICKER_LEN_MAX)
                and (word not in reddit_common)
            ]

            if r2:
                # TODO: Removing auxiliary words
                # Add data and continue with loop
                ticker_detection.append(r2)
                continue

            # Append empty detection
            ticker_detection.append(None)

    return ticker_detection
