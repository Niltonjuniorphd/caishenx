import yfinance as yf
import pandas as pd

def get_data_from_yf(share):
    yf_data = yf.Ticker(share)

    return yf_data
