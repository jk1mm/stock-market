import pandas as pd
import pytest

from stock_market.data import get_ticker, get_crypto


def test_get_ticker():
    # Working and correctly specified fields
    stock_data = get_ticker("AAPL", start_date="2020-01-01", end_date="2020-01-08")
    assert type(stock_data) is pd.DataFrame

    # Test different date format examples
    stock_data_c1 = get_ticker("AAPL", start_date="2020/01/01", end_date="2020/01/08")
    stock_data_c2 = get_ticker(
        "AAPL", start_date="January 1 2020", end_date="January 8 2020"
    )

    assert list(stock_data[["Value: Volume in Dollars"]]) == list(
        stock_data_c1[["Value: Volume in Dollars"]]
    )
    assert list(stock_data[["Value: Volume in Dollars"]]) == list(
        stock_data_c2[["Value: Volume in Dollars"]]
    )

    # Check default end date
    get_ticker("AAPL", start_date="2020-12-01")

    # Check invalid data call results in None
    assert get_ticker("ABNB", start_date="2019-12-10", end_date="2019-12-10") is None

    # Case valid for single day
    assert (
        get_ticker("ABNB", start_date="2020-12-10", end_date="2020-12-10").shape[0] == 1
    )


def test_get_crypto():
    # Invalid crypto currency - returns None
    assert (
        get_crypto(
            "NonExistent",
            start_date="2021-12-01",
            end_date="2021-12-08",
            currency_type="CAD",
        )
        is None
    )

    # Unsupported currency type
    with pytest.raises(Warning):
        get_crypto(
            "BTC", start_date="2021-12-01", end_date="2021-12-08", currency_type="EURO"
        )

    # Correctly specified fields
    crypto_data = get_crypto(
        "BTC", start_date="2021-12-01", end_date="2021-12-08", currency_type="CAD"
    )
    assert type(crypto_data) is pd.DataFrame
    assert crypto_data.shape[0] == 9
