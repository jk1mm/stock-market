from typing import Dict, Optional, List

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from pandas_datareader._utils import RemoteDataError
from plotly.graph_objs._figure import Figure as go_Figure
from plotly.subplots import make_subplots

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

            # Sort by recency of entering into stock market
            ticker_agg_stats = ticker_agg_stats.sort_values(
                by=["Days_On_Exchange"], ascending=True
            ).reset_index(drop=True)

            # Store metrics, data and plots to _overall_summary
            _overall_summary["stats"] = ticker_agg_stats
            _overall_summary["overall_change"] = {
                "overall_pct": _avg(values=ticker_agg_stats["Pct_Overall_Change"]),
                "overall_osd": _avg(
                    values=ticker_agg_stats[ticker_agg_stats["OSD_Valid"] == True][
                        "OSD"
                    ]
                ),
            }

            # OSD matrix heatmap data
            sorted_ticker = list(
                ticker_agg_stats.sort_values(
                    by=["Pct_Overall_Change"], ascending=False
                )["Ticker"]
            )
            max_days = max(ticker_agg_stats["Days_On_Exchange"])
            sorted_lag_values = list()

            for ticker_i in range(len(sorted_ticker)):
                ticker_data = self.price_history[sorted_ticker[ticker_i]]
                start_price = ticker_data["Open"][0]
                close_price = list(ticker_data["Close"])

                # Performance per day
                ppd = [
                    _percent_change(start_value=start_price, end_value=x)
                    for x in close_price
                ]
                ppd += [None] * (max_days - len(ppd))

                # Add to lag values
                sorted_lag_values.append(ppd)

            heatmap_x_lab = list(range(0, max_days))

            try:
                individual_osd_map = plotly_matrix_heatmap(
                    data=sorted_lag_values,
                    x_categorical=heatmap_x_lab,
                    y_categorical=sorted_ticker,
                    plot_title="Performance of Stocks: N days after IPO",
                )
            except ValueError:
                individual_osd_map = None

            _overall_summary["plots"] = {
                "individual_pct_change": plotly_h_bar(
                    data=ticker_agg_stats,
                    x_numerical="Pct_Overall_Change",
                    y_categorical="Ticker",
                    plot_title="Percent (%) Change since IPO",
                ),
                "individual_osd_map": individual_osd_map,
            }

            self._overall_summary = _overall_summary

        # Output summary results
        overall_result = f"""
        Recent IPO Summary
        ------------------
        Overall percent change : {self._overall_summary["overall_change"]["overall_pct"]}%
        Overall optimal sell day : {self._overall_summary["overall_change"]["overall_osd"]}

        Notes: 
        - OSD refers to Optimal Sell Day after IPO
        - Any 'day' refers to stock exchange business day, 
          excluding weekends and holidays
        
        """

        individual_result = f"""
        Per Stock Summary
        -----------------
        """

        print(overall_result)
        print(individual_result)
        self._overall_summary["plots"]["individual_pct_change"].show()
        if self._overall_summary["plots"]["individual_osd_map"] is not None:
            self._overall_summary["plots"]["individual_osd_map"].show()

        return self._overall_summary["stats"]
        # TODO: Best OSD (using probability) by number of stocks and percent increase!!

    def individual_summary(self, ticker: str):
        """
        Individual summary of recent IPOs.

        Parameters
        ----------
        ticker: str
            Ticker to perform individual summary on.

        Returns
        -------
        ticker_data: pd.DataFrame
            Ticker performance relate information.

        """
        # Standardize ticker
        ticker = ticker.upper()

        # Check if ticker exists from recent ipo
        if ticker.upper() not in self.price_history.keys():
            raise Warning("Specified ticker is not part of the recent IPO.")

        # Call ticker data from price_history
        ticker_data = self.price_history[ticker].copy()

        # Populate required data before plotting
        ticker_data["Date"] = ticker_data.index
        ticker_ipo_open = ticker_data.iloc[0, :]["Open"]

        # Plot line/bar plot (showing market close price and volume)
        fig_ticker_performance = plotly_stock_history(
            data=ticker_data,
            date_col="Date",
            line_col="Close",
            bar_col="Volume",
            plot_title=f"{ticker} Performance Since IPO",
            line_label="Price",
            bar_label="Volume Traded",
            y_axis_label="Stock Close Price",
            add_tick_prefix="$",
            add_horizontal_line=ticker_ipo_open,
        )
        # Plot chart
        fig_ticker_performance.show()

        return ticker_data

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
                    _price_history[ticker.upper()] = get_ticker(
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


def _scale_value(target_value: float, value_list: List[float]) -> float:
    """
    Gets the scale value of a number based on the values from a list.

    Parameters
    ----------
    target_value: float
        Value to scale.

    value_list: List[float]
        List of values.

    Returns
    -------
    scale: Optional[float]
        The scaled value.

    """
    scale = abs((target_value - min(value_list)) / (max(value_list) - min(value_list)))

    return scale


# Plotly graphs


def plotly_h_bar(
    data: pd.DataFrame,
    x_numerical: str,
    y_categorical: str,
    plot_title: str = "",
) -> go_Figure:
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

    plot_title: str, default ""
        Plot title.

    Returns
    -------
    fig_bar: Figure
        The plotly graph object containing horizontal bar plot content.

    """
    # Constant parameters
    COLOR_BAR_POSITIVE = "rgb(102,194,165)"
    COLOR_BAR_NEGATIVE = "rgb(204,102,119)"
    COLOR_BAR_OUTLINE = "rgb(217, 217, 217)"
    XAXIS_END_SPACE = 75

    # Work off of a copy
    data = data.copy()
    data = data.sort_values(by=[x_numerical], ascending=True)
    data["Color"] = np.where(
        data[x_numerical] < 0, COLOR_BAR_NEGATIVE, COLOR_BAR_POSITIVE
    )
    value_range = [list(data[x_numerical])[0], list(data[x_numerical])[-1]]
    data_len = len(data)

    # Plot
    fig_bar = go.Figure()
    fig_bar.add_trace(
        go.Bar(
            x=data[x_numerical],
            y=data[y_categorical],
            orientation="h",
            text=data[x_numerical],
            textposition="outside",
            marker=dict(
                color=data["Color"], line=dict(color=COLOR_BAR_OUTLINE, width=1)
            ),
        )
    )

    fig_bar.update_layout(
        title=plot_title,
        yaxis_tickfont_size=10,
        xaxis={
            "range": [
                value_range[0] - XAXIS_END_SPACE,
                value_range[1] + XAXIS_END_SPACE,
            ]
        },
    )

    if data_len > 10:
        fig_bar.update_layout(height=data_len * 35.0)

    return fig_bar


def plotly_matrix_heatmap(
    data: List[List[Optional[float]]],
    x_categorical: List,
    y_categorical: List,
    plot_title: str = "",
) -> go_Figure:
    """
    Plots a matrix heatmap.

    Parameters
    ----------
    data: List[List[Optional[float]]]
        Matrix (List of Lists).

    x_categorical: List
        List of labels for each column.

    y_categorical: List
        List of labels for each row.

    plot_title: str, default ""
        Plot title.

    Returns
    -------
    fig_heatmap: Figure
        The plotly graph object containing heatmap content.

    """
    # Constant parameters

    # Rule setup for min and max colors
    # Percent decrease beyond

    # Tier Thresholds
    TIER_LOW_THRESH = -25
    TIER_MIDDLE_THRESH = 0
    TIER_HIGH_THRESH = 25

    # Tier colors
    TIER_LOW_COLOR = "rgba(255, 99, 71, 1)"
    TIER_MIDDLE_COLOR = "rgba(255, 99, 71, 0)"
    TIER_HIGH_COLOR = "rgba(0, 86, 0, 1)"

    # Flatten out matrix data
    flattened_data = [
        x for x in [val for sublist in data for val in sublist] if x is not None
    ]
    min_value = min(flattened_data)
    max_value = max(flattened_data)
    color_scale = list()

    # Populate lower end of the scale
    if min_value < 0 and max_value > 0:
        # 1) Lower threshold
        # Case 1: Lower end lower than threshold
        if min_value < TIER_LOW_THRESH:
            # Add equivalent color palette for beyond lowest and low threshold
            color_scale.append([0, TIER_LOW_COLOR])
            color_scale.append(
                [
                    _scale_value(
                        target_value=TIER_LOW_THRESH, value_list=flattened_data
                    ),
                    TIER_LOW_COLOR,
                ]
            )
        # Case 2: Between low threshold and 0
        else:
            # Modify color based on value relative to low threshold
            color_scale.append([0, f"rgba(255, 99, 71, {min_value/TIER_LOW_THRESH})"])

        # 2) Middle threshold
        color_scale.append(
            [
                _scale_value(
                    target_value=TIER_MIDDLE_THRESH, value_list=flattened_data
                ),
                TIER_MIDDLE_COLOR,
            ]
        )

        # 3) Upper threshold
        # Case 1: Upper end higher than threshold
        if max_value > TIER_HIGH_THRESH:
            # Add equivalent color palette for beyond upper and upper threshold
            color_scale.append(
                [
                    _scale_value(
                        target_value=TIER_HIGH_THRESH, value_list=flattened_data
                    ),
                    TIER_HIGH_COLOR,
                ]
            )
            color_scale.append([1, TIER_HIGH_COLOR])
        # Case 2: Between high threshold and 0
        else:
            # Modify color based on value relative to low threshold
            color_scale.append([1, f"rgba(0, 86, 0, {max_value/TIER_HIGH_THRESH})"])
    # TODO: Fix color scale
    # TODO: Add in other case checks

    # Plot
    fig_heatmap = go.Figure()
    fig_heatmap.add_trace(
        go.Heatmap(
            x=x_categorical,
            y=y_categorical,
            z=data,
            type="heatmap",
            colorscale=color_scale,
        )
    )

    # Add title
    fig_heatmap.update_layout(
        title=plot_title,
    )
    # TODO: Axis label

    return fig_heatmap


def plotly_stock_history(
    data: pd.DataFrame,
    date_col: str,
    line_col: str,
    bar_col: str,
    plot_title: str = "",
    line_label: str = "",
    bar_label: str = "",
    y_axis_label: str = "",
    add_tick_prefix: Optional[str] = "$",
    add_horizontal_line: Optional[float] = None,
) -> go_Figure:
    """
    Plots a line & bar graph, to show stock history performance.

    Parameters
    ----------
    data: pd.DataFrame
        Data with line and bar value information.

    date_col: str
        Date column in data.

    line_col: str
        Line column in data.

    bar_col: str
        Bar column in data.

    plot_title: str, default ""
        Plot title.

    line_label: str, default ""
        Label to display on line hover.

    bar_label: str, default ""
        Label to display on bar hover.

    y_axis_label: str, default ""
        Y axis name.

    add_tick_prefix: Optional[str], default "$"
        Option to add a prefix to line chart values.

    add_horizontal_line: Optional[float], default None
        Option to add a horizontal line.

    Returns
    -------
    fig_heatmap: Figure
        The plotly graph object containing heatmap content.

    """
    fig_stock_history = make_subplots(specs=[[{"secondary_y": True}]])

    fig_stock_history.add_trace(
        go.Scatter(
            x=data[date_col],
            y=data[line_col],
            name=line_label,
            line=dict(color="#5B84B1"),
            opacity=0.8,
        ),
        secondary_y=False,
    )

    fig_stock_history.add_trace(
        go.Bar(
            x=data[date_col],
            y=data[bar_col],
            name=bar_label,
            marker_color="#FC766A",
            opacity=0.8,
        ),
        secondary_y=True,
    )

    fig_stock_history.update_layout(
        dict(
            title={
                "text": plot_title,
                "font": dict(
                    family="Courier New, monospace",
                    size=25,
                ),
            },
            xaxis=dict(title="Date", ticklen=5, zeroline=False),
            yaxis=dict(title=y_axis_label),
            hovermode="x",
        ),
    )

    if add_tick_prefix:
        fig_stock_history.update_yaxes(tickprefix=add_tick_prefix, secondary_y=False)

    fig_stock_history.update_yaxes(
        showticklabels=False, secondary_y=True, range=[0, data[bar_col].max() * 3]
    )

    fig_stock_history.update_xaxes(rangeslider_visible=True)

    # Add a horizontal line for ipo open price
    if add_horizontal_line:
        fig_stock_history.add_shape(
            type="line",
            x0=min(data[date_col]),
            y0=add_horizontal_line,
            x1=max(data[date_col]),
            y1=add_horizontal_line,
            xref="x",
            yref="y",
            line=dict(
                color="#9199BE",
                width=2.5,
                dash="dashdot",
            ),
        )

    return fig_stock_history
