import streamlit as st
import pandas as pd
from utils.load_data import get_data_from_yf

period_now = pd.Period.now(freq='D').strftime('%Y-%m-%d')

def main():

    st.title('Caishenx')

    stock = st.radio('Stock', ['ITUB4.SA'])

    stok_data = get_data_from_yf(stock)
    stock_price = stok_data.history(start = '2016-01-01', end = period_now)

    st.dataframe(stock_price)
    st.line_chart(stock_price[['High', 'Low', 'Close']])


if __name__ == '__main__':
    main()