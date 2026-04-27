"""
Backend chart data transformation utilities.

Pure functions for preparing and reshaping stock data for visualization.
No Streamlit or UI dependencies.
"""

import pandas as pd
from backend.mappings import STOCK_NAMES


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


def transform_for_plotting(df, tickers):
    """Transform prepared chart data into long-format DataFrame ready for plotting.

    Args:
        df: DataFrame from prepare_chart_data() with ticker columns and DatetimeIndex
        tickers: List of ticker symbols (for validation/fallback)

    Returns:
        Long-format DataFrame with columns: Date, Ticker (friendly name), Close
    """
    if df.empty:
        return pd.DataFrame(columns=["Date", "Ticker", "Close"])

    # Ensure numeric and drop all-NA rows
    df = df.apply(pd.to_numeric, errors="coerce").dropna(how="all")
    if df.empty:
        return pd.DataFrame(columns=["Date", "Ticker", "Close"])

    # Reset index → rename → melt → dropna Close
    plot_df = df.reset_index().rename(
        columns={df.index.name or df.index.names[0] or 0: "Date"}
    )
    plot_df = plot_df.melt(
        id_vars="Date", var_name="Ticker", value_name="Close"
    ).dropna(subset=["Close"])

    # Map ticker codes → friendly names
    plot_df["Ticker"] = plot_df["Ticker"].map(lambda x: STOCK_NAMES.get(x, x))
    return plot_df


def compute_latest_stats(df, tickers):
    """Extract the most recent close price for each ticker from chart-ready data.

    Args:
        df: DataFrame from prepare_chart_data() (ticker columns, DatetimeIndex)
        tickers: List of ticker symbols

    Returns:
        pandas Series indexed by ticker with latest close prices, or empty Series
    """
    if df.empty:
        return pd.Series(dtype=float)
    df = df.apply(pd.to_numeric, errors="coerce").dropna(how="all")
    if df.empty:
        return pd.Series(dtype=float)
    last = df.iloc[-1]
    # Keep only tickers that actually exist in the row
    valid = {t: last[t] for t in tickers if t in last.index and pd.notna(last[t])}
    return pd.Series(valid)
