import pandas_datareader.data as web
import numpy as np
import pandas as pd

import datetime

#### inputs
# investment
investment_eur = 1000
# pick tickers
# 'IVV' = S&P500 Core, 'DE' = DAX Core, 'XWD.TO' = MSCI World Core
stocks = ['IVV', 'DE', 'AMZN']
# pf weights
# weights = [0.5,0.5]
weights = [0.3333,0.3333, 0.3333]


#### output
# retrieve data
data = web.DataReader(stocks,data_source="yahoo",start='01/01/2018')['Adj Close']
data.sort_index(inplace=True)
# create pf value
data["pf_raw"] = data.dot(weights)
# calc absolute pf value
data["pf_abs"] = data["pf_raw"] * investment_eur / data["pf_raw"][0]
# create daily pf return
data["pf_ret"] = data["pf_abs"].pct_change()
# create rolling pf return
data["pf_ret30"] = data["pf_ret"].rolling(30).mean()
# create helper cols
data["assets"] = str(stocks)
data["weights"] = str(weights)
data["date"] = list(data.index)
data.tail(5)


#### plot return
from plotnine import ggplot, geom_point, geom_line, aes, stat_smooth, facet_wrap, theme_bw, theme, element_text, ggtitle

# plot
(ggplot(data, aes(x="date", y='pf_abs'))
 + geom_line() + theme_bw() + theme(axis_text_x=element_text(rotation=45, hjust=1))) + ggtitle(f"total pf return over time horizon: {round((data['pf_abs'][-1]/data['pf_abs'][0])*100, 2)}% \n assets: {str(stocks)}, weights: {str(weights)}")