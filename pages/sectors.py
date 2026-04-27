"""Sectors page — one chart per sector, independent of main page selections.

This page fetches its own data from yfinance for all sector tickers and renders
a time-series plot per sector with all stocks in that sector overlay-plotted.
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date, timedelta
from utils.functions import fetch_stock_data, prepare_chart_data
from utils.stock_mappings import STOCK_NAMES, SECTOR_GROUPS

st.title("Sectors Overview")

# ── Date range selection ──
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input(
        "Start date",
        value=date.today() - timedelta(days=3*365),
        help=" Earliest date to fetch stock data"
    )
with col2:
    end_date = st.date_input(
        "End date",
        value=date.today(),
        help="Latest date to fetch stock data"
    )

start_str = start_date.strftime("%Y-%m-%d")
end_str = end_date.strftime("%Y-%m-%d")

if start_date >= end_date:
    st.error("Start date must be before end date.")
    st.stop()

# Use all tickers defined per sector (no per-sector filtering).
# Build the union of all tickers we will fetch.
all_needed_tickers = set()
for tickers in SECTOR_GROUPS.values():
    all_needed_tickers.update(tickers)

if not all_needed_tickers:
    st.warning("No tickers defined in any sector.")
    st.stop()

tickers_list = sorted(all_needed_tickers)
st.caption(f"Fetching data for {len(tickers_list)} tickers...")

# ── Fetch sector data once ──
try:
    stock_price = fetch_stock_data(tuple(tickers_list), start_str, end_str)
    if not isinstance(stock_price, pd.DataFrame):
        raise TypeError("Fetched data is not a DataFrame")
    if stock_price.empty:
        st.warning("No historical data available for the selected tickers.")
        st.stop()
except Exception as e:
    st.error(f"Failed to fetch stock data: {e}")
    st.stop()

st.success(f"Loaded {len(stock_price)} trading days of data.")

# ── Color palette ──
sector_palette = [
    "#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
    "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"
]

st.markdown("Each chart shows all tickers in that sector overlayed on the same time-series plot.")
st.markdown("---")

# ── Render charts ──
palette_len = len(sector_palette)
pci = 0  # palette color index cycling

for idx, (sector_name, tickers) in enumerate(SECTOR_GROUPS.items()):
    if not tickers:
        continue

    st.subheader(sector_name)

    # Prepare data
    df = prepare_chart_data(stock_price, tickers)
    if df.empty:
        st.warning(f"No data available for {sector_name}.")
        continue

    df = df.apply(pd.to_numeric, errors="coerce").dropna(how="all")
    if df.empty:
        st.warning(f"No numeric data for {sector_name}.")
        continue

    plot_df = df.reset_index().rename(
        columns={df.index.name or df.index.names[0] or 0: "Date"}
    )
    plot_df = plot_df.melt(
        id_vars="Date", var_name="Ticker", value_name="Close"
    ).dropna(subset=["Close"])

    # Friendly names
    plot_df["Ticker"] = plot_df["Ticker"].map(lambda x: STOCK_NAMES.get(x, x))

    # Use rotating colors across the tickers in this sector
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.set_style("darkgrid")

    for i, (ticker, group) in enumerate(plot_df.groupby("Ticker")):
        color_idx = (pci + i) % palette_len
        ax.plot(
            group["Date"],
            group["Close"],
            label=ticker,
            color=sector_palette[color_idx],
            linewidth=2,
        )

    ax.set_title(f"{sector_name} — Price History", fontsize=14, pad=10)
    ax.set_xlabel("Date", fontsize=11)
    ax.set_ylabel("Close Price (BRL)", fontsize=11)
    ax.legend(loc="best", fontsize=9, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    pci = (pci + 1) % palette_len

    if idx < len(SECTOR_GROUPS) - 1:
        st.markdown("---")
