import bs4
import pandas as pd
import requests

# URL with IPO information (from MarketWatch)
IPO_URL = "https://www.marketwatch.com/tools/ipo-calendar"


class IPO:
    # Web Scraped data
    _data_ws = bs4.BeautifulSoup(requests.get(IPO_URL).content, "html.parser").find(
        "div", class_="element__body j-tabPanes"
    )

    # 4 resulting ipo data sets
    recent_ipo = None
    upcoming_ipo = None
    future_ipo = None
    withdrawn_ipo = None

    def setup_dataframe(self, web_table: bs4.element.Tag) -> pd.DataFrame:
        """
        Initial data frame setup for each ipo data sets.

        Parameters
        ----------
        web_table: bs4.element.Tag
            The BeautifulSoup data containing table values.

        Returns
        -------
        df_setup: pd.DataFrame
            Initial data frame, with populated table headers.

        """
        # Ensure the headers are there at the minimum
        if len(web_table.find_all("th")) == 0:
            raise ValueError("There is no table header available for this data set.")

        # Extract header information
        columns = web_table.find_all("tr")[0].text.strip().split("\n")
        df_setup = pd.DataFrame(columns=columns)

        return df_setup
