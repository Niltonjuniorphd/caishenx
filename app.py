import streamlit as st
import pandas as pd
import plotly.express as px
from utils.functions import fetch_stock_data, flatten_columns, prepare_chart_data
from utils.stock_mappings import STOCK_NAMES

period_now = pd.Period.now(freq="D").strftime("%Y-%m-%d")


def render_chart(stock_price, tickers, title, colors=None):
    """Render a line chart for the given tickers. Returns True if rendered.
    
    Args:
        colors: Optional list of colors to use for lines (e.g., hot colors like red, orange, yellow)
    """
    df = prepare_chart_data(stock_price, tickers)
    if not isinstance(df, pd.DataFrame):
        try:
            df = pd.DataFrame(df)
        except Exception:
            df = pd.DataFrame()
    if df.empty:
        st.warning(f"No data available for {', '.join(tickers)}")
        return False
    df = df.apply(pd.to_numeric, errors="coerce").dropna(how="all")
    if df.empty:
        st.warning(f"No valid numeric data for {', '.join(tickers)}")
        return False
    plot_df = df.reset_index().rename(
        columns={df.index.name or df.index.names[0] or 0: "Date"}
    )
    plot_df = plot_df.melt(id_vars="Date", var_name="Ticker", value_name="Close").dropna(
        subset=["Close"]
    )
    
    # Replace ticker codes with friendly names for legend display
    plot_df["Ticker"] = plot_df["Ticker"].map(lambda x: STOCK_NAMES.get(x, x))
    
    # Use Plotly for custom colors if provided
    if colors:
        fig = px.line(
            plot_df, 
            x="Date", 
            y="Close", 
            color="Ticker",
            title=title,
            height=400,
            color_discrete_sequence=colors
        )
    else:
        fig = px.line(
            plot_df, 
            x="Date", 
            y="Close", 
            color="Ticker",
            title=title,
            height=400
        )
    
    st.plotly_chart(fig, width='stretch')
    return True


def main():
    st.set_page_config(page_title="Caishenx", layout="centered")
    st.title("Caishenx")

    # ── Ticker selection ──
    st.subheader("Select Tickers")
    all_options = list(STOCK_NAMES.keys())
    left_ticker = "^BVSP"
    right_tickers = st.multiselect(
        "Other stocks to plot (right chart)",
        options=[opt for opt in all_options if opt != left_ticker],
        default=["PETR4.SA"],
        format_func=lambda x: STOCK_NAMES.get(x, x),
        help="Choose one or more stocks to compare with Ibovespa.",
    )
    st.markdown("---")

    # High-contrast palette for clear line differentiation
    # Using Plotly's qualitative colors: blue, red, green, purple, orange, cyan
    hot_colors = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A", "#19D3F3"]

    # ── Fetch once ──
    fetch_all = [left_ticker] + right_tickers
    try:
        stock_price = fetch_stock_data(tuple(fetch_all), "2016-01-01", period_now)
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
        col1, col2 = st.columns([1, 1], gap="medium")
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
        stats = prepare_chart_data(stock_price, fetch_all)
        stats = stats.apply(pd.to_numeric, errors="coerce").dropna(how="all")
        if not stats.empty:
            last = stats.iloc[-1]
            n_cols = min(4, len(last))
            cols = st.columns(n_cols)
            i = 0
            for ticker, price in last.items():
                if i < n_cols:
                    label = STOCK_NAMES.get(ticker, ticker)
                    with cols[i]:
                        st.metric(
                            label=label,
                            value=f"{price:,.2f}",
                        )
                        i += 1

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
