import string
from typing import List, Tuple, Union

from spellchecker import SpellChecker

TICKER_LEN_MAX = 5
AVAILABLE_SOURCE = ["reddit"]
PUNCTUATIONS = string.punctuation.replace("$", "") + "“"


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

    Notes - Logic and statistical aim behind NLP filtering
    ------------------------------------------------------
    - Minimizing false positives is crucial as incorrectly stating tickers can significantly skew
      towards a common word (e.g. auxiliary verbs, pronouns)
    - Given a larger sample size of posts, some tickers that are affected by false negatives are
      hopefully recognized correctly from other posts
    - Understand the derivation of ticker attributes (from North American market), which do not contain
      digits and have a prior known max ticker length

    Notes - Filters for different sources
    -------------------------------------
    Reddit Filters:
    - R1: Identifies words that are attached with a '$' mark, that have have no digits in the word
    - R2: Checks for capital words that are non-dictionary words (spelled wrong)

    """
    # Verify source is available
    source = source.lower()
    if source not in AVAILABLE_SOURCE:
        raise Warning(f"Choose from the current available sources: {AVAILABLE_SOURCE}")

    # If one text specified as str
    if not isinstance(text, (list, tuple)):
        text = [text]

    # Spell checking module
    spell_check = SpellChecker()

    # List of ticker detection
    ticker_detection = list()

    # For reddit source
    if source == "reddit":
        # Common reddit terms
        reddit_common = [
            "DD",
            "COVID",
            "WSB",
            "OTC",
            "ETF",
            "TLDR",
            "PT",
        ]

        # TODO: Controllable level of rule strictness

        # Go through each phrases in text (list)
        for phrase in text:

            # Breakdown texts
            phrase_dec = phrase.split()

            # Remove punctuations at the end of each words
            phrase_dec = [word.strip(PUNCTUATIONS) for word in phrase_dec]
            # Clean Nones
            phrase_dec = list(filter(None, phrase_dec))

            # Rules:
            # R-1) Ticker starts with $. If at least one word is detected, move on to next phrase assuming that
            #      the user is consistent with their ticker mentions with $ beginning.
            # Applying: $ check, digit check (phrase can refer to a $ amount)
            r1 = None

            if "$" in phrase:
                phrase_dec = list(filter(lambda word: "$" in word, phrase_dec))
                r1 = list(map(lambda word: word.strip("$"), phrase_dec))

            if r1:
                # Remove invalid length and digits inclusive tickers
                r1 = [
                    ticker.upper()
                    for ticker in r1
                    if (len(ticker) <= TICKER_LEN_MAX) and (not _check_digit(ticker))
                ]

                if r1:
                    # Add data and continue with loop
                    ticker_detection.append(r1)
                    continue

            # R-2) Look for cap locks
            # Applying: Reddit common check, spell checker
            r2 = [
                word
                for word in phrase_dec
                if word.isupper()
                and (len(word) <= TICKER_LEN_MAX)
                and (word not in reddit_common)
            ]

            if r2:
                # Check for dictionary words and if digit exists
                r2 = [
                    ticker.upper()
                    for ticker in spell_check.unknown(r2)
                    if (len(ticker) <= TICKER_LEN_MAX) and (not _check_digit(ticker))
                ]

                if r2:
                    # Add data and continue with loop
                    ticker_detection.append(r2)
                    continue

            # Append empty detection
            ticker_detection.append(None)

    return ticker_detection


def _check_digit(v: str) -> bool:
    """
    Checks if string value contains a digit.

    """
    return any(letter.isdigit() for letter in v)
