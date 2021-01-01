from typing import Dict, Optional, List

import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pandas_datareader._utils import RemoteDataError
from plotly.graph_objs._figure import Figure

from stock_market.data import IPO, get_ticker

OSD_THRESH = 3


class RecentIPO(object):
    """
    Analysis on Recent IPO stocks (within 3 weeks).
    """

    # Get recent ipo data
    recent_ipo = IPO().recent_ipo

    # Helper variables
    _price_history = None  # Storing stock price history

    # Stats on different views
    _overall_summary = None
    _individual_summary = None

    @property
    def overall_summary(self) -> pd.DataFrame:
        """
        High level summary of recent IPOs.
        1) Aggregate stock performance in one percentage.
        2) Total price shift per stocks since IPO
        3) Optimal sell day (Number of market days since IPO where stock price was at highest)

        """
        # Check if summary function has been run
        if self._overall_summary is None:
            # Setup for metric population
            data = self.price_history
            _overall_summary = {}
            ticker_agg_stats = pd.DataFrame()

            # Loop through each tickers
            for ticker in data.keys():
                ticker_data = data[ticker]
                ticker_market_days = len(ticker_data)
                ticker_open = ticker_data.iloc[0, :].Open

                # Calculate Optimal Sell Day (OSD)
                ticker_high = list(ticker_data["High"])
                osd = ticker_high.index(max(ticker_high))

                # Add ticker stats to aggregated stats
                ticker_stats = {
                    "Ticker": ticker,
                    "Days_On_Exchange": ticker_market_days,
                    "Pct_Overall_Change": _percent_change(
                        start_value=ticker_open,
                        end_value=ticker_data.iloc[ticker_market_days - 1, :].Close,
                    ),
                    "OSD": osd,
                    "OSD_Max_Pct_Gain": _percent_change(
                        start_value=ticker_open, end_value=max(ticker_high)
                    ),
                    "OSD_Valid": True
                    if ticker_market_days - OSD_THRESH > osd
                    else False,
                }
                ticker_agg_stats = ticker_agg_stats.append(
                    pd.DataFrame(ticker_stats, index=[0])
                )

            ticker_agg_stats = ticker_agg_stats.reset_index(drop=True)

            _overall_summary["stats"] = ticker_agg_stats
            _overall_summary["overall_change"] = {
                "overall_pct": _avg(values=ticker_agg_stats["Pct_Overall_Change"]),
                "overall_osd": _avg(
                    values=ticker_agg_stats[ticker_agg_stats["OSD_Valid"] == True][
                        "OSD"
                    ]
                ),
            }
            self._overall_summary = _overall_summary

        # Output summary results
        print_statistics = f"""
        Recent IPO Summary
        ------------------
        Overall percent change : {self._overall_summary["overall_change"]["overall_pct"]}%
        Overall optimal sell day : {self._overall_summary["overall_change"]["overall_osd"]}

        Notes: 
        - OSD refers to Optimal Sell Day after IPO
        - Any 'day' refers to stock exchange business day, 
          excluding weekends and holidays

               
        Individual statistics
        ---------------------
        """

        print(print_statistics)
        return self._overall_summary["stats"]
        # TODO: Best OSD (using probability) by number of stocks and percent increase!!

    @property
    def price_history(self) -> Dict[str, pd.DataFrame]:
        """
        Stores all recent ipo historical data.
        """

        if self._price_history is None:
            _price_history = {}
            recent_ipo = self.recent_ipo
            today = pd.to_datetime("today")

            for stock_i in range(len(recent_ipo)):
                # Loop through each stock to see validity in US/CDN stock exchange
                try:
                    ticker = recent_ipo.iloc[stock_i, :].Ticker
                    _price_history[ticker] = get_ticker(
                        ticker=ticker, start_date=today - pd.Timedelta(days=30)
                    )
                except RemoteDataError:
                    pass

            self._price_history = _price_history

        return self._price_history


# Helper function


def _percent_change(
    start_value: float,
    end_value: float,
    to_percent: bool = True,
    round_digits: Optional[int] = 3,
) -> float:
    """
    Calculates percent change of two values.

    Parameters
    ----------
    start_value: float
        Start value.

    end_value: str
        End value.

    to_percent: bool;, default True
        Option to output value as percentage.

    round_digits: Optional[int], default 3
        Option to round return value to n decimal places.

    Returns
    -------
    percent_change: float
        Percent change between start and end value.

    """
    # Percent or decimal value
    multiplier = 100.0 if to_percent else 1.0

    # Calculation
    percent_change = (end_value - start_value) / start_value * multiplier

    return (
        percent_change if round_digits is None else round(percent_change, round_digits)
    )


def _avg(values: List[float], round_digits: Optional[int] = 3) -> Optional[float]:
    """
    Calculates the mean of the list of values.

    Parameters
    ----------
    values: List[float]
        List of numerical values.

    round_digits: Optional[int], default 3
        Option to round return value to n decimal places.

    Returns
    -------
    mean_value: Optional[float]
        The mean value of the input list.

    """
    len_values = len(values)

    if len_values == 0:
        return None

    mean_value = sum(values) / len_values

    return mean_value if round_digits is None else round(mean_value, round_digits)


# Plotly graphs


def plotly_hbar(
    data: pd.DataFrame,
    x_numerical: str,
    y_categorical: str,

) -> Figure:
    """
    Plots a sorted and re-formatted horizontal bar chart.

    Parameters
    ----------
    data: pd.DataFrame
        Data with the categorical and numerical values for horizontal bar plot.

    y_categorical: str
        Column name of data, with categorical values.

    x_numerical: str
        Column name of data, with numerical values.


    Returns
    -------
    fig_bar: Figure
        The plotly graph object containing horizontal bar plot content.

    """
    # Constant parameters
    None
