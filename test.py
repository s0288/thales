import pandas_datareader.data as web
import numpy as np
import pandas as pd

# pick tickers
stocks = ['IVV', 'DE']
# pf weights
weights = np.asarray([0.5,0.5])

# retrieve data
data = web.DataReader(stocks,data_source="yahoo",start='01/10/2019')['Adj Close']
data.sort_index(inplace=True)
# create pf value
data["pf_abs"] = data.dot(weights)
# create daily pf return
data["pf_ret"] = data["pf_abs"].pct_change()
# create rolling pf return
data["pf_avg14"] = data["pf_ret"].rolling(14).mean()


#### plot return
from plotnine import ggplot, geom_point, geom_line, aes, stat_smooth, facet_wrap, theme_bw

# create Date col
data["date"] = list(data.index)

# plot
(ggplot(data, aes(x="date", y='pf_ret'))
 + geom_point() + geom_line(aes(y='pf_avg14')) + theme_bw())