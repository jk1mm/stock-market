from stock_market.data.constants import *
import validators


def test_constants():
    # Test URLs
    assert validators.url(IPO_URL)
    assert validators.url(SP500_URL)
