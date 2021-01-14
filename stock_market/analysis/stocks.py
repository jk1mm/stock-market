from stock_market.data import get_ticker
from typing import Optional


MARKET_TIME = ["open", "close"]


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

    None
