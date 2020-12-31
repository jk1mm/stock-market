import pandas as pd
from pandas_datareader._utils import RemoteDataError

from stock_market.data import IPO, get_ticker


class RecentIPO(object):
    """
    Analysis on Recent IPO stocks (within 3 weeks).
    """

    # Get recent ipo data
    recent_ipo = IPO().recent_ipo

    # Helper variables
    _price_history = None  # Storing stock price history

    # Stats on different views
    _summary = None
    _individual_view = None

    @property
    def summary(self) -> pd.DataFrame:
        """
        High level summary of recent IPOs.
        1) Aggregate stock performance in one percentage.
        2) Total price shift per stocks since IPO
        3) Optimal sell day histogram

        """
        # Check if summary function has been run
        if self._summary is None:
            recent_ipo = self.recent_ipo
            today = pd.to_datetime("today")
            valid_stocks = []

            # Loop through each stock to see validity in US/CDN stock exchange
            for stock_i in range(len(recent_ipo)):
                try:
                    ticker = recent_ipo.iloc[stock_i, :].Ticker
                    ticker_data = get_ticker(
                        ticker=ticker, start_date=today - pd.Timedelta(days=30)
                    )
                except KeyError:
                    pass

    def price_history(self):
        """
        Stores all recent ipo historical data.
        """

        if self._price_history is None:
            _price_history = {}
            recent_ipo = self.recent_ipo
            today = pd.to_datetime("today")

            for stock_i in range(len(recent_ipo)):
                try:
                    ticker = recent_ipo.iloc[stock_i, :].Ticker
                    _price_history[ticker] = get_ticker(
                        ticker=ticker, start_date=today - pd.Timedelta(days=30)
                    )
                except RemoteDataError:
                    pass

            self._price_history = _price_history
