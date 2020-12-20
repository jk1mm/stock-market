import bs4
import pandas as pd
import requests

# URL with IPO information (from MarketWatch)
IPO_URL = "https://www.marketwatch.com/tools/ipo-calendar"


class IPO(object):
    """
    Extracts IPO related data from MarketWatch.
    """

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
    def recent_ipo(self) -> pd.DataFrame:
        """
        Extract list of recently priced IPOs.

        """
        # Check if this web scraping has already been run
        if type(self._recent_ipo) is pd.DataFrame:
            return self._recent_ipo
        else:
            # Index 0 is recent_ipo
            ws_val = self._data_ws[0]

            # Extract data
            data = self.extract_data(ws_val)

            # Data cleaning

            # Separate Ticker symbol and price change as separate columns
            data.insert(
                1, "Ticker", data["Symbol"].str.extract("([^\s]+)", expand=True)
            )
            data.insert(
                5, "Percent_Change", data["Symbol"].str.extract("\s(.*)\%", expand=True)
            )
            del data["Symbol"]

            # Removal of some characters in Price and Shares variable for type conversion
            data["Price"] = data["Price"].str.replace("$", "")
            data["Shares"] = data["Shares"].str.replace(",", "")

            # Data type conversion
            data = data.astype(
                {
                    "Percent_Change": "float",
                    "Shares": "int32",
                    "Price": "float",
                    "IPO_Date": "datetime64",
                }
            )

            self._recent_ipo = data
            return data

    @property
    def upcoming_ipo(self) -> pd.DataFrame:
        """
        Extract list of upcoming IPOs.

        """
        # Check if this web scraping has already been run
        if type(self._upcoming_ipo) is pd.DataFrame:
            return self._upcoming_ipo
        else:
            # Indexes 1 and 2 are upcoming_ipo
            ws_val_this_week = self._data_ws[1]
            ws_val_next_week = self._data_ws[2]

            # Extract data
            data = self.extract_data(ws_val_this_week)
            data1 = self.extract_data(ws_val_next_week)
            data["week"] = "This Week"
            data1["week"] = "Next Week"
            data.append(data1, ignore_index=True)

            self._upcoming_ipo = data
            return data

    @property
    def future_ipo(self) -> pd.DataFrame:
        """
        Extract list of future IPOs.

        """
        # Check if this web scraping has already been run
        if type(self._future_ipo) is pd.DataFrame:
            return self._future_ipo
        else:
            # Index 3 is future_ipo
            ws_val = self._data_ws[3]

            # Extract data
            data = self.extract_data(ws_val, index_deletion=1)

            self._future_ipo = data
            return data

    @property
    def withdrawn_ipo(self) -> pd.DataFrame:
        """
        Extract list of withdrawn IPOs.

        """
        # Check if this web scraping has already been run
        if type(self._withdrawn_ipo) is pd.DataFrame:
            return self._withdrawn_ipo
        else:
            # Index 3 is withdrawn_ipo
            ws_val = self._data_ws[4]

            # Extract data
            data = self.extract_data(ws_val)

            self._withdrawn_ipo = data
            return data

    @staticmethod
    def extract_data(
        web_table: bs4.element.Tag,
        index_deletion: int = None,
    ) -> pd.DataFrame:
        """
        Web scrape table header and values as pandas dataframe.

        Parameters
        ----------
        web_table: bs4.element.Tag
            The BeautifulSoup data containing table values.

        index_deletion: int, default None
            Option to delete an index of the webscraped values. If None, no index will be deleted.

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
        columns = [val.replace(" ", "_") for val in columns]
        del all_info[0]

        # Append values to rows in data
        values = []

        # Checking values
        if index_deletion:
            for i in range(len(all_info)):
                ipo_info = all_info[i].text.strip().split("\n")

                # For future ipo stocks
                if len(ipo_info) > index_deletion:
                    del ipo_info[index_deletion]

                values.append(ipo_info)
        else:
            for i in range(len(all_info)):
                ipo_info = all_info[i].text.strip().split("\n")
                values.append(ipo_info)

        df = pd.DataFrame(values, columns=columns)

        return df
