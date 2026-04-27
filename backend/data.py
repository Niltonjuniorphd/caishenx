"""
Backend data layer — yfinance integration and caching.

Note: fetch_stock_data uses Streamlit's cache_data decorator for performance.
This is acceptable infrastructure coupling for a Streamlit-native application.
"""

import streamlit as st
import pandas as pd
import yfinance as yf


def get_data_from_yf(share):
    """Create yfinance Tickers object for the given share symbols."""
    return yf.Tickers(share)


@st.cache_data(ttl=3600)
def fetch_stock_data(stocks_tuple, start, end):
    """Fetch historical stock data with caching.

    Args:
        stocks_tuple: Tuple of ticker strings
        start: Start date string (YYYY-MM-DD)
        end: End date string (YYYY-MM-DD)

    Returns:
        pandas DataFrame with multi-index columns (ticker, field)
    """
    tickers = get_data_from_yf(list(stocks_tuple))
    return tickers.history(start=start, end=end, group_by="ticker")
