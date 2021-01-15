from stock_market.data import get_ticker
from typing import Optional
import pandas as pd
import warnings


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
