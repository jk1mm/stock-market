import bs4
import pandas as pd
import requests

# URL with IPO information (from MarketWatch)
IPO_URL = "https://www.marketwatch.com/tools/ipo-calendar"


class IPO(object):
    # Web Scraped data
    _data_ws = (
        bs4.BeautifulSoup(requests.get(IPO_URL).content, "html.parser")
        .find("div", class_="element__body j-tabPanes")
        .find_all("table")
    )

    # 4 resulting ipo data sets
    _recent_ipo = None
    _upcoming_ipo = None
    _future_ipo = None
    _withdrawn_ipo = None

    @property
    def recent_ipo(self):
        # Check if this web scraping has already been run
        if self._recent_ipo:
            return self._recent_ipo
        else:
            # First index is recent_ipo
            ws_val = self._data_ws[0]

            # Extract data
            data = self.extract_data(ws_val)

            self._recent_ipo = data
            return data

    @property
    def upcoming_ipo(self):
        # Check if this web scraping has already been run
        if self._upcoming_ipo:
            return self._upcoming_ipo
        else:
            # First index is recent_ipo
            ws_val_this_week = self._data_ws[1]
            ws_val_next_week = self._data_ws[2]

            # Extract data
            data = self.extract_data(ws_val_this_week)
            data1 = self.extract_data(ws_val_next_week)
            data["week"] = "This Week"
            data1["week"] = "Next Week"
            data.append(data1, ignore_index=True)

            self._recent_ipo = data
            return data

    @staticmethod
    def extract_data(web_table: bs4.element.Tag) -> pd.DataFrame:
        """
        Web scrape table header and values as pandas dataframe.

        Parameters
        ----------
        web_table: bs4.element.Tag
            The BeautifulSoup data containing table values.

        Returns
        -------
        df: pd.DataFrame
            Pandas dataframe with proper column and values.

        """
        # Ensure the headers are there at the minimum
        if len(web_table.find_all("th")) == 0:
            raise ValueError("There is no table header available for this data set.")

        # Find all headers
        all_info = web_table.find_all("tr")

        # Extract header information
        columns = all_info[0].text.strip().split("\n")
        del all_info[0]

        # Append values to rows in data
        values = []
        for i in range(len(all_info)):
            ipo_info = all_info[i].text.strip().split("\n")
            values.append(ipo_info)

        df = pd.DataFrame(values, columns=columns)

        return df
