import warnings
from typing import Optional, List

import pandas as pd
import plotly.graph_objects as go
from pandas_datareader._utils import RemoteDataError
from plotly.subplots import make_subplots

from stock_market.data import get_ticker

MARKET_TIME = [
    "open",  # at market open
    "close",  # at market close
    "high",  # at day high price
    "low",  # at day low price
]


def stock_profit(
    ticker: str,
    quantity: int,
    purchase_date: str,
    sell_date: str = None,
    purchase_time: str = "open",
    sell_time: str = "close",
) -> Optional[float]:
    """
    Stock calculator, to understand the net profit from buying and selling n number of stocks on a
    certain period of time.

    Parameters
    ----------
    ticker: str
        Stock ticker symbol.

    quantity: int
        Number of stocks purchased/sold.

    purchase_date: str
        Date of stock purchase.

    sell_date: str, default None
        Date of stock sell. If None, use current date.

    purchase_time: str, default "open"
        Time of purchase.

    sell_time: str, default "close"
        Time of sell.

    Returns
    -------
    net_profit: Optional[float]
        Net profit, in the respective exchange currency.

    """
    # Check if purchase or sell time is valid
    purchase_time = purchase_time.lower()
    sell_time = sell_time.lower()
    if purchase_time not in MARKET_TIME or sell_time not in MARKET_TIME:
        raise Exception(f"Populate valid time metrics: {MARKET_TIME}")

    # TODO: Think of a more efficient way to do this

    # Call the ticker data
    ticker_history = get_ticker(
        ticker=ticker, start_date=purchase_date, end_date=sell_date, new_metrics=False
    )

    # If no data is returned (from invalid date range)
    if ticker_history is None:
        print("No stock history for requested date range.")
        return None

    # Checking validity of the requested days

    # For buy date, shift to next nearest day if invalid
    if pd.to_datetime(purchase_date) != ticker_history.index[0]:
        warnings.warn("Purchase date has been shifted to the next stock in market day.")

    # For sell date, shift to previous nearest day
    if pd.to_datetime(sell_date) != ticker_history.index[-1]:
        warnings.warn(
            "Sell date has been shifted back to the previous stock in market day."
        )

    # Re-format column names for standardization
    ticker_history.columns = ["high", "low", "open", "close", "volume", "adj close"]

    # Calculation

    # Edge case: for length == 1, raise warning for potential inaccurate results
    if len(ticker_history) == 1:
        warnings.warn(
            "Result may be inaccurate since buying and selling happens on the same day."
        )

    # Calculate
    net_profit = (ticker_history.loc[:, sell_time][-1] * quantity) - (
        ticker_history.loc[:, purchase_time][0] * quantity
    )

    return net_profit


def stock_chart(
    stocks: List[str],
    start_date: str,
    end_date: str = None,
):
    """
    View stock performance chart for requested list of stock(s).

    Parameters
    ----------
    stocks: List[str]
        List of stocks to see performance charts.

    start_date: str
        Start date of stock information. (e.g. 2020-01-01, 2020/01/01, January 1 2020)

    end_date: str, default None
        End date of stock information. If None, use current date.

    Returns
    -------
    stock_view:

    """
    # Constant parameters
    OPACITY = 0.8
    BAR_SHRINKAGE = 3
    YAXIS_RANGE_EXTENSION = 0.4

    # Unique list of stocks (lower cased)
    stocks = list(set([stock.lower() for stock in stocks]))
    stock_price_col = "Close"
    stock_volume_col = "Volume"

    # Setup: storing stock information
    stocks_info = dict()
    invalid_stocks = list()

    # First check validity of tickers in list. Ticker is invalid if:
    #  - Invalid ticker (KeyError)
    #  - Ticker is not in the market within the date range requested (return None)
    for stock in stocks:
        try:
            # Attempt stock data call
            stock_pd = get_ticker(
                ticker=stock, start_date=start_date, end_date=end_date
            )[[stock_price_col, stock_volume_col]]

            # Date range is invalid (but stock exists)
            if stock_pd is None:
                invalid_stocks.append(stock)  # Add stock to invalid list
                continue

            # If valid, add data to stock info
            stocks_info[stock] = stock_pd

        # Invalid ticker
        except RemoteDataError:
            invalid_stocks.append(stock)

    # Case when all stocks are invalid
    valid_tickers = list(stocks_info.keys())
    valid_ticker_count = len(valid_tickers)
    if valid_ticker_count == 0:
        raise Exception(
            "All stock(s) specified are either invalid or was not in the market for requested"
            "date range. Please re-specify with valid parameters."
        )

    # Warning raise for presence of some invalid cases (but some are valid)
    if len(invalid_stocks) > 0:
        warnings.warn(
            f"The following list of stock(s) were skipped due to invalid ticker or "
            f"date range: {invalid_stocks}"
        )

    # Setup specs
    specs = list()
    for i in range(valid_ticker_count):
        specs.append([{"secondary_y": True}])

    # Setup the plot grid
    chart_grid = make_subplots(
        rows=valid_ticker_count,
        cols=1,
        shared_xaxes=True,
        specs=specs,
    )

    # Add charts one by one
    for i in range(1, valid_ticker_count + 1):
        ticker_name = valid_tickers[i - 1]
        data = stocks_info[ticker_name]

        # Line chart: Price
        chart_grid.add_trace(
            go.Scatter(
                x=data.index, y=data[stock_price_col], name=f"{ticker_name}".upper()
            ),
            row=i,
            col=1,
            secondary_y=False,
        )

        # Bar chart: Volume
        chart_grid.add_trace(
            go.Bar(
                x=data.index,
                y=data[stock_volume_col],
                marker_color="#FC766A",
                opacity=OPACITY,
            ),
            row=i,
            col=1,
            secondary_y=True,
        )

        # Y-axis modifier
        line_val_extend = (
            max(data[stock_price_col]) - min(data[stock_price_col])
        ) * YAXIS_RANGE_EXTENSION

        yaxis_update_max = max(data[stock_price_col]) + line_val_extend
        yaxis_update_min = min(data[stock_price_col]) - line_val_extend
        if yaxis_update_min < 0:
            yaxis_update_min = 0

        # Line modifier
        chart_grid.update_yaxes(
            title_text="Price",
            range=[yaxis_update_min, yaxis_update_max],
            row=i,
            col=1,
            secondary_y=False,
        )

        # Bar modifier
        chart_grid.update_yaxes(
            showticklabels=False,
            secondary_y=True,
            range=[0, data[stock_volume_col].max() * BAR_SHRINKAGE],
        )

    # Formats
    chart_grid.update_layout(
        xaxis_showticklabels=True, xaxis2_showticklabels=True
    )  # Date axis populate for each charts
    chart_grid.update_yaxes(tickprefix="$", secondary_y=False,)

    # Drop down menu to change metric views

    # TODO: Use rbc work example for rfm pie chart
    # For the ones with the same y axis values, make another plot/chart

    return chart_grid.show()
