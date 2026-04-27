"""Utility functions for stock data fetching and chart preparation."""

import streamlit as st
import pandas as pd
from utils.load_data import get_data_from_yf


@st.cache_data(ttl=3600)
def fetch_stock_data(stocks_tuple, start, end):
    """Fetch historical stock data with caching."""
    tickers = get_data_from_yf(list(stocks_tuple))
    return tickers.history(start=start, end=end, group_by="ticker")


def flatten_columns(df):
    """Flatten MultiIndex columns by joining levels with underscore."""
    df = df.copy()
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [
            "_".join([str(level).strip() for level in col if level is not None])
            for col in df.columns
        ]
    else:
        df.columns = [str(col).strip() for col in df.columns]
    return df


def prepare_chart_data(df, selected_stocks):
    """Prepare dataframe for plotting.

    Handles:
    - single ticker (simple columns)
    - multiple tickers (MultiIndex columns)

    Rules:
    - Flatten MultiIndex columns
    - Keep only Close columns
    - Filter only selected stocks
    - Normalize index to naive DatetimeIndex

    IMPORTANT: Avoids duplicate column names by using exact ticker-prefix
    matching (not substring), so PETR4.SA and PETR3.SA are distinguished.
    """
    original_is_multiindex = isinstance(df.columns, pd.MultiIndex)

    if original_is_multiindex:
        # MultiIndex: (ticker, field). Build a clean single-ticker Close series dict.
        close_series = {}
        for ticker in selected_stocks:
            try:
                col_tuple = (ticker, "Close")
                if col_tuple in df.columns:
                    close_series[ticker] = df[col_tuple].dropna()
            except Exception:
                pass
        if not close_series:
            return pd.DataFrame()
        chart_df = pd.DataFrame(close_series)
    else:
        # Already flattened (single-level columns from flatten_columns).
        # Column names are exactly: "{ticker}_{field}" e.g. "PETR4.SA_Close"
        if len(selected_stocks) == 1:
            ticker = selected_stocks[0]
            target = f"{ticker}_Close"
            if target not in df.columns:
                return pd.DataFrame()
            chart_df = df[[target]].copy()
            chart_df.columns = [ticker]
        else:
            series_dict = {}
            for ticker in selected_stocks:
                target = f"{ticker}_Close"
                if target in df.columns:
                    series_dict[ticker] = df[target].dropna()
            if not series_dict:
                return pd.DataFrame()
            chart_df = pd.DataFrame(series_dict)

    # Normalize index for Streamlit compatibility
    idx = chart_df.index
    if isinstance(idx, pd.PeriodIndex):
        chart_df.index = idx.to_timestamp()
    elif not isinstance(idx, pd.DatetimeIndex):
        chart_df.index = pd.to_datetime(idx)
    elif getattr(idx, "tz", None) is not None:
        chart_df.index = idx.tz_localize(None)

    return chart_df
