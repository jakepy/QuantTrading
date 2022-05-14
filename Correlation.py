## Best to run this in an IPYNB Environment.
import numpy as np
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime as dt

import matplotlib.pyplot as plt
import seaborn as sns

## Correlation
start = dt(2017,1,1)
symbol_list = ['SPY', 'QQQ', 'DIA', 'IWM', 'UVXY']

symbols = []
for symbol in symbol_list:
    s = web.DataReader(symbol, 'yahoo', start)
    s['Symbol'] = symbol
    symbols.append(s)

df = pd.concat(symbols)
df = df.reset_index()
df = df[['Date', 'Close', 'Symbol']]
df_pivot = df.pivot('Date', 'Symbol', 'Close').reset_index()

corr_df = df_pivot.corr(method='pearson')
corr_df.reset_index()
corr_df = corr_df.rename_axis(None, axis=1)
corr_df.head(10)

mask = np.zeros_like(corr_df)
mask[np.triu_indices_from(mask)] = True

## Plot Correlation
sns.heatmap(corr_df,
            cmap='RdYlGn',
            vmax=1.0,
            vmin=-1.0,
            mask=mask,
            linewidths=2.5,
            annot=True)
plt.yticks(rotation=0)
plt.xticks(rotation=90)
plt.show()
