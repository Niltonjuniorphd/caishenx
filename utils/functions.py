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
    """
    original_is_multiindex = isinstance(df.columns, pd.MultiIndex)
    df = flatten_columns(df)

    # Single ticker case: simple columns (Open, High, Close...)
    if len(selected_stocks) == 1 and not original_is_multiindex:
        if "Close" not in df.columns:
            return pd.DataFrame()
        chart_df = df[["Close"]].copy()
        chart_df.columns = [selected_stocks[0]]
    # Multiple tickers: search for Close columns by ticker
    else:
        close_columns = []
        for col in df.columns:
            if "close" in col.lower():
                for stock in selected_stocks:
                    if stock.lower() in col.lower():
                        close_columns.append(col)
                        break
        if not close_columns:
            return pd.DataFrame()
        chart_df = df[close_columns].copy()
        rename_map = {}
        for col in chart_df.columns:
            for stock in selected_stocks:
                if stock.lower() in col.lower():
                    rename_map[col] = stock
                    break
        chart_df = chart_df.rename(columns=rename_map)
        available_cols = [s for s in selected_stocks if s in chart_df.columns]
        chart_df = chart_df.reindex(columns=available_cols)

    # Normalize index for Streamlit compatibility
    idx = chart_df.index
    if isinstance(idx, pd.PeriodIndex):
        chart_df.index = idx.to_timestamp()
    elif not isinstance(idx, pd.DatetimeIndex):
        chart_df.index = pd.to_datetime(idx)
    elif getattr(idx, "tz", None) is not None:
        chart_df.index = idx.tz_localize(None)

    return chart_df
