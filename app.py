import streamlit as st
import pandas as pd
from utils.load_data import get_data_from_yf

period_now = pd.Period.now(freq='D').strftime('%Y-%m-%d')

def main():

    st.title('Caishenx')

    stock = st.radio('Stock', ['ITUB4.SA', 'PETR4.SA'])

    stocks = st.multiselect('Stoks', ['ITUB4.SA', 'PETR4.SA'], default='ITUB4.SA')

    stok_data = get_data_from_yf(stocks)
    stock_price = stok_data.history(start = '2016-01-01', end = period_now)


    st.dataframe(stock_price)
    st.write(stock_price.columns)
    st.line_chart(stock_price.loc[:, [('Close', 'ITUB4.SA')]])




if __name__ == '__main__':
    main()