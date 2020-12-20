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
        if type(self._recent_ipo) is pd.DataFrame:
            return self._recent_ipo
        else:
            # Index 0 is recent_ipo
            ws_val = self._data_ws[0]

            # Extract data
            data = self.extract_data(ws_val)

            self._recent_ipo = data
            return data

    @property
    def upcoming_ipo(self):
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

            self._recent_ipo = data
            return data

    @property
    def future_ipo(self):
        # Check if this web scraping has already been run
        if type(self._future_ipo) is pd.DataFrame:
            return self._future_ipo
        else:
            # Index 3 is future_ipo
            ws_val = self._data_ws[3]

            # Extract data
            data = self.extract_data(
                ws_val, check_value=True, len_constraint=6, index_deletion=1
            )

            self._withdrawn_ipo = data
            return data

    @property
    def withdrawn_ipo(self):
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
        check_value: bool = False,
        len_constraint: int = None,
        index_deletion: int = None,
    ) -> pd.DataFrame:
        """
        Web scrape table header and values as pandas dataframe.

        Parameters
        ----------
        web_table: bs4.element.Tag
            The BeautifulSoup data containing table values.

        check_value: bool, default False
            Option to check value extraction, when webscraping can tend to output inconsistent values.

        len_constraint: int, default None
            Only applicable when check_value is True. The length to check for which is inconsistent with the column
            length.

        index_deletion: int, default None
            Only applicable when check_value is True. The index of the value to delete, when len_constraint number of
            values are detected.

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
        if check_value:
            for i in range(len(all_info)):
                ipo_info = all_info[i].text.strip().split("\n")

                # For future ipo stocks
                if len(ipo_info) == len_constraint:
                    del ipo_info[index_deletion]

                values.append(ipo_info)
        else:
            for i in range(len(all_info)):
                ipo_info = all_info[i].text.strip().split("\n")
                values.append(ipo_info)

        df = pd.DataFrame(values, columns=columns)

        return df
