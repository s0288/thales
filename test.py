import pandas_datareader.data as web
import numpy as np
import pandas as pd

####
# Necessary adjustments:
# - add points of time for investment (have one col as 'total_funds' and one as 'added_funds') and calculate 'weights' as result of shifting 'total_funds'  
# --> pf["date", "pf_abs", "pf_ret", "pf_ret30", "original_funds", "assets" ARRAY["name_stock1", "name_stock2", "name_stock3"], "weights" ARRAY["weight_stock1", "weight_stock2", "weight_stock3"]]

# pick tickers
stocks = ['IVV', 'DE']
# pf weights
weights = np.asarray([0.5,0.5])

# retrieve data
data = web.DataReader(stocks,data_source="yahoo",start='01/01/2019')['Adj Close']
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