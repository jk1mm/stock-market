import pytest

from stock_market.analysis.stocks import stock_profit


def test_stock_profit():
    # TODO: Add edge case of potential start and end date convergence

    # Invalid market time raises exception
    with pytest.raises(Exception):
        stock_profit(
            ticker="AAPL",
            quantity=100,
            purchase_date="2020-12-10",
            purchase_time="Invalid time",
        )

    # Invalid date range
    assert (
        stock_profit(
            ticker="AAPL",
            quantity=100,
            purchase_date="2100-01-01",
            sell_date="2100-01-08",
        )
        is None
    )

    # Raise warning for non market date specification
    with pytest.warns(UserWarning):
        stock_profit(
            ticker="AAPL",
            quantity=100,
            purchase_date="2021-01-02",
            sell_date="2021-01-09",
        )

    # Raise warning for one day ticker history
    with pytest.warns(UserWarning):
        stock_profit(
            ticker="AAPL",
            quantity=100,
            purchase_date="2021-01-07",
            sell_date="2021-01-07",
        )

    # Check Value calculation results
    assert (
        stock_profit(ticker="aapl", quantity=1, purchase_date="2021-01-14")
        == -1.8899993896484375
    )
