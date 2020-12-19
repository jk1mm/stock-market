from stock_market.data.yahoo_finance import *


def test_get_ticker():
    # Working and correctly specified fields
    stock_data = get_ticker("AAPL", start_date="2020-01-01", end_date="2020-01-08")
    assert type(stock_data) is pd.DataFrame

    # Test different date format examples
    stock_data_c1 = get_ticker("AAPL", start_date="2020/01/01", end_date="2020/01/08")
    stock_data_c2 = get_ticker(
        "AAPL", start_date="January 1 2020", end_date="January 8 2020"
    )
    assert stock_data.equals(stock_data_c1)
    assert stock_data.equals(stock_data_c2)

    # Check default end date
    get_ticker("AAPL", start_date="2020-12-01")
