import importlib
import re
from typing import Optional, Tuple

import bs4
import pandas as pd
import requests

from stock_market.data.constants import (
    SP500_LINK,
    PERFORMANCE_PERIODIC,
    PERFORMANCE_TOP_STOCKS,
    PERFORMERS_BOTTOM_STOCKS,
)

AVAILABLE_INDEX = ["SP500"]


class IndexView(object):
    """
    Analysis on market indexes.

    Parameters
    ----------
    index: str
        The market index of interest for analysis. Currently supports the indexes in AVAILABLE_INDEX.

    """

    def __init__(self, index: str):

        # Check availability of index
        if (index_name := index.upper()) not in AVAILABLE_INDEX:
            raise Warning(
                f"Please select from the available indexes: {AVAILABLE_INDEX}"
            )

        # Extract specified index data
        data = getattr(importlib.import_module("stock_market.data"), index_name)

        # Column name constants
        self._column_names = {
            "ticker_symbol": "Ticker",
            "ticker_full": "Name",
            "ticker_sector": "Sector",
        }

        # Self stores
        self.data = data
        self.sector_list = list(set(data[self._column_names["ticker_sector"]]))

        # Value from property
        self._summary = dict()

    @property
    def summary_sector_view(self) -> pd.DataFrame:
        """
        Summary of number of stocks by sector.

        """
        if "sector_view" not in self._summary:
            # Setup for metric population
            data = self.data
            index_info = dict()
            ticker_symbol = self._column_names["ticker_symbol"]
            ticker_sector = self._column_names["ticker_sector"]

            # Number of stocks by sector
            sector_count = dict()
            sector_count["sector_count"] = (
                data[
                    [
                        ticker_symbol,
                        ticker_sector,
                    ]
                ]
                .groupby([ticker_sector])
                .count()
                .to_dict()[ticker_symbol]
            )

            self._summary["sector_view"] = sector_count

        # Populate sector count in pandas form
        sector_count = pd.DataFrame.from_dict(self._summary["sector_view"])

        return sector_count

    @property
    def summary_performance(self) -> pd.DataFrame:
        """
        High level summary of index's periodic performance.

        """
        if "performance" not in self._summary:
            # Run scrape function to extract all metrics in one go
            index_scrape = _sp500()
            self._summary["performance"] = index_scrape[PERFORMANCE_PERIODIC]
            self._summary["top_stocks"] = index_scrape[PERFORMANCE_TOP_STOCKS]
            self._summary["bottom_stocks"] = index_scrape[PERFORMERS_BOTTOM_STOCKS]

        periodic_performance = pd.DataFrame.from_dict(
            {"periodic_performance": self._summary["performance"]}
        )

        # TODO: Properly sort the periodic time periods

        return periodic_performance

    @property
    def summary_stocks_today(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Summary of today's top and bottom stock performances.

        """
        if ("top_stocks" not in self._summary) or (
            "bottom_stocks" not in self._summary
        ):
            # Run scrape function to extract all metrics in one go
            index_scrape = _sp500()
            self._summary["performance"] = index_scrape[PERFORMANCE_PERIODIC]
            self._summary["top_stocks"] = index_scrape[PERFORMANCE_TOP_STOCKS]
            self._summary["bottom_stocks"] = index_scrape[PERFORMERS_BOTTOM_STOCKS]

        return self._summary["top_stocks"], self._summary["bottom_stocks"]


# Scraper for sp500
def _sp500():
    # Search and store the following information
    ws_dict = dict()
    for metric in [
        PERFORMANCE_PERIODIC,
        PERFORMANCE_TOP_STOCKS,
        PERFORMERS_BOTTOM_STOCKS,
    ]:
        # Regex search for the above metrics
        regex = re.compile(f"element element--table ({metric})")

        # Web Scraped data
        ws_metric = bs4.BeautifulSoup(
            requests.get(SP500_LINK).content, "html.parser"
        ).find("div", {"class": regex})

        # Check if data return requires a webscrape fix
        if len(ws_metric) == 0:
            print(f"The web-scrape metric name seems to be changed for {metric}.")
            return None

        ws_dict[metric] = ws_metric

    # Extract data points for each metric
    metric_data = {}

    # 1) Performance per periods
    data_1 = dict()
    data = ws_dict[PERFORMANCE_PERIODIC].find_all("td")
    for i in range(0, len(data), 2):
        # Every even index represents the info and odd index represents the value
        data_1[data[i].text.replace("\n", "")] = data[i + 1].text.replace("\n", "")

    # 2) Top performing stocks today
    data_2 = _stock_performers_ws(data=ws_dict[PERFORMANCE_TOP_STOCKS])

    # 3) Bottom performing stocks today
    data_3 = _stock_performers_ws(data=ws_dict[PERFORMERS_BOTTOM_STOCKS])

    # All data store
    metric_data[PERFORMANCE_PERIODIC] = data_1
    metric_data[PERFORMANCE_TOP_STOCKS] = data_2
    metric_data[PERFORMERS_BOTTOM_STOCKS] = data_3

    return metric_data


# Helper function for _sp500()
def _stock_performers_ws(
    data: bs4.element.Tag,
) -> Optional[pd.DataFrame]:
    """
    Web scrapes the top and bottom performing stocks for an index in MarketWatch.

    """
    data_ws = data.find_all("tr")

    if len(data_ws) == 0:
        return None

    # Setup stock data
    stock_data = []

    # First row is the column names
    col_names = list(filter(None, data_ws[0].text.split("\n")))

    # Extract all other row info
    for row in range(1, len(data_ws)):
        stock_data.append(list(filter(None, data_ws[row].text.split("\n"))))

    # Form pandas dataframe
    data_df = pd.DataFrame(stock_data, columns=col_names)

    return data_df
