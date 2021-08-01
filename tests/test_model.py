import pytest

from stock_market.model._classification import _check_digit, detect_ticker
from stock_market.model._nlp import nltk_sentiment


class TestNlpModel:
    @staticmethod
    def test_nltk_sentiment():

        # Multiple sentences input
        input_text = ["This is the first sentence", "This is the second sentence"]
        assert type(nltk_sentiment(text=input_text)) is list

        # Single sentence input
        assert type(nltk_sentiment(text=input_text[0])) is dict


class TestClassificationModel:
    @staticmethod
    def test_detect_ticker():

        # Invalid case - invalid source
        with pytest.raises(Warning):
            detect_ticker(text="", source="invalid_source")

        # Valid case - multiple text input
        input_text = ["Identify ticker AAPL", "$MSFT"]
        multi_detect = detect_ticker(text=input_text, source="reddit")
        assert multi_detect == [["AAPL"], ["MSFT"]]

        # Valid case - single text input
        single_detect = detect_ticker(text=input_text[0], source="reddit")
        assert single_detect == [["AAPL"]]

        # Valid case - no detection
        input_no_ticker = ["No ticker her", "$3.2 is not a ticker"]
        assert detect_ticker(text=input_no_ticker, source="reddit") == [None, None]

    @staticmethod
    def test_helper_check_digit():
        # Check for digit
        val_digit = "mock1"
        val_non_digit = "mockone"

        assert _check_digit(val_digit)
        assert not _check_digit(val_non_digit)
