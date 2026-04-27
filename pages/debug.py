"""Debug page – inspect the data fetched and passed to the chart."""

import streamlit as st
import pandas as pd
from utils.functions import flatten_columns, prepare_chart_data

st.title("Debug Inspector")

# Check if data exists in session state
if "stock_price" not in st.session_state or "stocks" not in st.session_state:
    st.info("No data available. Go to the main page and fetch data first.")
    st.stop()

stock_price = st.session_state["stock_price"]
stocks = st.session_state["stocks"]

st.header("Fetched Data (raw API response)")
st.dataframe(stock_price)
st.write("Shape:", stock_price.shape)
st.write("Columns:", stock_price.columns.tolist())

st.header("Flattened Columns")
flattened = flatten_columns(stock_price)
st.dataframe(flattened)
st.write("Flattened columns:", flattened.columns.tolist())

st.header("Chart Data (input to plot transformation)")
chart_data = prepare_chart_data(stock_price, stocks)
st.dataframe(chart_data.head())
st.write("Chart data shape:", chart_data.shape)
st.write("Chart data columns:", chart_data.columns.tolist())
st.write("Chart data index:", chart_data.index)

# Show the final plot-ready dataframe as well
if not chart_data.empty:
    st.header("Plot-Ready DataFrame (long format)")
    plot_df = chart_data.reset_index().rename(
        columns={chart_data.index.name or chart_data.index.names[0] or 0: "Date"}
    )
    plot_df = plot_df.melt(
        id_vars="Date", var_name="Ticker", value_name="Close"
    )
    plot_df = plot_df.dropna(subset=["Close"])
    st.dataframe(plot_df.head())
    st.write("Plot DF shape:", plot_df.shape)
