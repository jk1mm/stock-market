import pytest

from stock_market.analysis.stocks import stock_profit, stock_chart, _unique_ordered_list
from plotly.graph_objs._figure import Figure as go_Figure


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
        stock_profit(
            ticker="aapl",
            quantity=1,
            purchase_date="2021-01-14",
            sell_date="2021-01-14",
        )
        == -1.8899993896484375
    )


def test_stock_chart():
    # Exception: No stocks are valid
    with pytest.raises(Exception):
        stock_chart(
            stocks=[
                "abnb",
            ],
            start_date="2015-01-01",
            end_date="2015-01-08",
        )

    # Warning: Some valid and some invalid stocks
    with pytest.warns(UserWarning):
        stock_chart(
            stocks=["tsla", "invalid1", "invalid2"],
            start_date="2020-01-01",
            end_date="2020-01-08",
        )

    # Valid case: return output check
    valid_chart_obj = stock_chart(
        stocks=["nio"],
        start_date="2020-05-01",
        end_date="2020-08-25",
    )
    assert type(valid_chart_obj) == go_Figure


def test_helper_functions():
    # Test _unique_ordered_list
    duplicate_list = ["tsla", "nio", "tsla", "xpev", "nkla"]

    assert _unique_ordered_list(duplicate_list) == ["tsla", "nio", "xpev", "nkla"]
