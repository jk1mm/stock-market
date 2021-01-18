from stock_market.data.constants import *
from urllib.parse import urlparse


def test_constants():
    # Test URLs
    assert urlparse(IPO_URL)
    assert urlparse(SP500_URL)
