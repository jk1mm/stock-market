import importlib
import re

import bs4
import pandas as pd
import requests

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
        self._summary = None

    @property
    def summary(self):
        """
        High level summary of specified market index.
        1) Number of stocks by sector
        2) Periodic performance
        3) Annual performance
        4) Top performers

        """
        if self._summary is None:
            # Setup for metric population
            data = self.data
            sector_list = self.sector_list
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
            index_info["sector_count"] = sector_count

            self._summary = index_info

        # Populate sector count in pandas form
        sector_count = pd.DataFrame.from_dict(self._summary["sector_count"])

        return None


# Scraper for sp500
def _sp500():
    # URL
    index_url = "https://www.marketwatch.com/investing/index/spx"

    # Metrics
    performance_by_period = "performance"
    performance_top_stocks = "ByIndexGainers"
    performance_bottom_stocks = "ByIndexDecliners"

    # Search and store the following information
    ws_dict = dict()
    for metric in [
        performance_by_period,
        performance_top_stocks,
        performance_bottom_stocks,
    ]:
        # Regex search for the above metrics
        regex = re.compile(f"element element--table ({metric})")

        # Web Scraped data
        ws_metric = bs4.BeautifulSoup(
            requests.get(index_url).content, "html.parser"
        ).find("div", {"class": regex})

        # Check if data return requires a webscrape fix
        if len(ws_metric) == 0:
            print(f"The web-scrape metric name seems to be changed for {metric}.")
            return None

        ws_dict[metric] = ws_metric

    # Extract data points for each metric

    # 1) Performance per periods
    data_1 = dict()
    data = ws_dict[performance_by_period].find_all("td")
    for i in range(0, len(data), 2):
        # Every even index represents the info and odd index represents the value
        data_1[data[i].text.replace("\n", "")] = data[i + 1].text.replace("\n", "")
