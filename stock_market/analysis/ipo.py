import pandas as pd

from stock_market.data import IPO


class RecentIPO(object):
    """
    Analysis on Recent IPO stocks (within 3 weeks).
    """

    # Get recent ipo data
    recent_ipo = IPO().recent_ipo

    # Stats on different views
    _summary = None
    _individual_view = None

    @property
    def summary(self) -> pd.DataFrame:
        """
        High level summary of recent IPOs.

        """
        # Check if summary function has been run
        if type(self._summary) is not None:
            return self._summary
        else:
            # Loop through each stock to see validity in US/CDN stock exchange
            None


# TODO: FutureIPO
