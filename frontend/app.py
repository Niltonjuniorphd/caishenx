import streamlit as st
import pandas as pd
import plotly.express as px
from backend.data import fetch_stock_data
from backend.chart_utils import prepare_chart_data, transform_for_plotting, compute_latest_stats
from frontend.charts import render_chart
from backend.mappings import STOCK_NAMES
from backend.constants import DEFAULT_LEFT_TICKER, DEFAULT_RIGHT_TICKERS, DEFAULT_START_DATE, HOT_COLORS, COLUMN_RATIO

period_now = pd.Period.now(freq="D").strftime("%Y-%m-%d")


def main():
    st.set_page_config(page_title="Caishenx", layout="centered")
    st.title("Caishenx")

    # ── Ticker selection ──
    st.subheader("Select Tickers")
    all_options = list(STOCK_NAMES.keys())
    left_ticker = DEFAULT_LEFT_TICKER
    right_tickers = st.multiselect(
        "Other stocks to plot (right chart)",
        options=[opt for opt in all_options if opt != left_ticker],
        default=DEFAULT_RIGHT_TICKERS,
        format_func=lambda x: STOCK_NAMES.get(x, x),
        help="Choose one or more stocks to compare with Ibovespa.",
    )
    st.markdown("---")

    # High-contrast palette for clear line differentiation
    hot_colors = HOT_COLORS

    # ── Fetch once ──
    fetch_all = [left_ticker] + right_tickers
    try:
        stock_price = fetch_stock_data(tuple(fetch_all), DEFAULT_START_DATE, period_now)
        if not isinstance(stock_price, pd.DataFrame):
            raise TypeError("Fetched data is not a DataFrame")
        if stock_price.empty:
            st.warning("No historical data available for the selected tickers.")
            st.stop()
    except Exception as e:
        st.error(f"Failed to fetch stock data: {e}")
        st.stop()

    # Save for debug page
    st.session_state["stock_price"] = stock_price
    st.session_state["stocks"] = fetch_all

    # ── Mobile-first layout: stack on narrow screens, side-by-side on wide ──
    has_right = bool(right_tickers)

    if has_right:
        col1, col2 = st.columns(COLUMN_RATIO, gap="medium")
    else:
        col1 = st.container()
        col2 = None

    # ── Left column: BVSP ──
    with col1:
        left_name = STOCK_NAMES.get(left_ticker, left_ticker)
        st.markdown(f"**{left_name}** — Ibovespa index")
        render_chart(stock_price, [left_ticker], title=f"{left_name} Price")

    # ── Right column: selected stocks ──
    if col2:
        with col2:
            names = [STOCK_NAMES.get(t, t) for t in right_tickers]
            st.markdown(f"**{' + '.join(names)}**")
            render_chart(stock_price, right_tickers, title="Selected Stocks", colors=hot_colors)

    # ── Mobile stats cards ──
    if has_right:
        st.markdown("---")
        st.subheader("Latest Close Prices")
        stats_series = compute_latest_stats(prepare_chart_data(stock_price, fetch_all), fetch_all)
        if not stats_series.empty:
            n_cols = min(4, len(stats_series))
            cols = st.columns(n_cols)
            for i, (ticker, price) in enumerate(stats_series.items()):
                if i < n_cols:
                    label = STOCK_NAMES.get(ticker, ticker)
                    with cols[i]:
                        st.metric(label=label, value=f"{price:,.2f}")

    # ── Single-stock detail shown below charts on mobile ──
    if has_right and len(right_tickers) == 1:
        st.markdown("---")
        single = right_tickers[0]
        single_name = STOCK_NAMES.get(single, single)
        st.subheader(f"{single_name} — Price Summary")
        df = prepare_chart_data(stock_price, [single])
        if not df.empty:
            df = df.apply(pd.to_numeric, errors="coerce").dropna()
            if not df.empty:
                c1, c2, c3 = st.columns(3)
                latest_date = df.index[-1].strftime("%Y-%m-%d")
                c1.metric("Min", f"{df.min().iloc[0]:,.2f}")
                c2.metric("Max", f"{df.max().iloc[0]:,.2f}")
                c3.metric("Latest", f"{df.iloc[-1].iloc[0]:,.2f}", delta=f"as of {latest_date}")


if __name__ == "__main__":
    main()
