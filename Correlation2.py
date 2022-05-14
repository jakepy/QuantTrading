# Author: https://towardsdatascience.com/find-highly-correlated-stocks-with-python-77eba4fd061b
import numpy as np
import warnings
import pandas_datareader.data as web
import pandas as pd
import yfinance as yf
import datetime as dt
from yahoo_fin import stock_info as si
pd.set_option('display.max_rows', None)
warnings.filterwarnings('ignore')
yf.pdr_override()

years = 1 # Adjust as needed, or use days
start = dt.date.today() - dt.timedelta(days = int(365.25*years))
end = dt.date.today()

tickers = si.tickers_dow()

history = web.get_data_yahoo(tickers, start, end)['Adj Close']
stock_returns = np.log(history/history.shift(1))
corr_matrix = stock_returns.corr()

def get_redundant_pairs(df):
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr

print('Top Absolute Correlations')
print(get_top_abs_correlations(stock_returns))
