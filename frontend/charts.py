"""
Frontend chart rendering components.

This module contains Streamlit-coupled chart rendering functions.
Backend data transformations live in backend.chart_utils.
"""

import streamlit as st
import plotly.express as px
from backend.chart_utils import prepare_chart_data, transform_for_plotting
from backend.constants import CHART_HEIGHT, PLOTLY_WIDTH
from backend.mappings import STOCK_NAMES


def render_chart(stock_price, tickers, title, colors=None):
    """Render a Plotly line chart for the given tickers.

    Args:
        stock_price: Raw DataFrame from yfinance (multi-index or flattened)
        tickers: List of ticker symbols to plot
        title: Chart title displayed above the plot
        colors: Optional list of color hex codes for line colors

    Returns:
        True if chart was rendered, False if no data available
    """
    df = prepare_chart_data(stock_price, tickers)
    plot_df = transform_for_plotting(df, tickers)

    if plot_df.empty:
        st.warning(f"No data available for {', '.join(tickers)}")
        return False

    fig = px.line(
        plot_df,
        x="Date",
        y="Close",
        color="Ticker",
        title=title,
        height=CHART_HEIGHT,
        color_discrete_sequence=colors,
    )

    st.plotly_chart(fig, width=PLOTLY_WIDTH)
    return True
