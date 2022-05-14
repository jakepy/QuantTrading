import numpy as np
import warnings
import pandas_datareader.data as web
import pandas as pd
import yfinance as yf
import datetime as dt
from yahoo_fin import stock_info as si
import pandas_ta as ta
warnings.filterwarnings('ignore')
yf.pdr_override()

## Set Params for downloading the data.
years = 1
start = dt.date.today() - dt.timedelta(days = int(365.25*years))
end = dt.date.today()

## Choose Tickers to Pull Data From
# dow_tickers = si.tickers_dow()
spy_tickers = si.tickers_sp500()
# nasdaq_tickers = si.tickers_nasdaq()

## Download data
history = web.get_data_yahoo(spy_tickers, start, end)['Adj Close'] ## Change parameter if needed to download the correct tickers
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

df = pd.DataFrame(get_top_abs_correlations(stock_returns))

## Saves to CSV File 
## ** MAKE SURE TO MANIPULATE THE CORRELATION TABLE NAME **
df.to_csv('corr_tables/spy_correlation.csv', header=False) ## Also make sure you have an appropriately named folder.

print(get_top_abs_correlations(stock_returns))
