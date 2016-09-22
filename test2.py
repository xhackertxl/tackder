import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.graphics.api as smg
import patsy

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas import Series,DataFrame
from scipy import stats
import seaborn as sns
import tushare as ts
import datetime
start = datetime.datetime(2016,1,1)
end = datetime.datetime(2016,9,20)

from pandas.io.data import DataReader
datass = ts.get_realtime_quotes('sh')
datajqr = ts.get_h_data('002337')
datass.head()
datajqr.head()
close_ss = datass["pre_close"]
close_jqr = datajqr["close"]
close_ss.describe()
close_jqr.describe()
close_ss=close_ss.astype(float)
close_jqr=close_jqr.astype(float)

fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(15,6))
close_ss.plot(ax=ax[0])
ax[0].set_title("SZZZ")
close_jqr.plot(ax=ax[1])
ax[1].set_title("JQR")
stock = pd.merge(datass,datajqr,left_index = True, right_index = True)
#stock = stock[["Close_x","Close_y"]]
stock.columns = ["SZZZ","JQR"]
stock.head()

daily_return = (stock.diff()/stock.shift(periods = 1)).dropna()
daily_return.head()

daily_return.describe()

daily_return[daily_return["JQR"] > 0.105]

fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(15,6))
daily_return["SZZZ"].plot(ax=ax[0])
ax[0].set_title("SZZZ")
daily_return["JQR"].plot(ax=ax[1])
ax[1].set_title("JQR")

fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(15,6))
sns.distplot(daily_return["SZZZ"],ax=ax[0])
ax[0].set_title("SZZZ")
sns.distplot(daily_return["JQR"],ax=ax[1])
ax[1].set_title("JQR")


fig,ax = plt.subplots(nrows=1,ncols=1,figsize=(12,6))
plt.scatter(daily_return["JQR"],daily_return["SZZZ"])
plt.title("Scatter Plot of daily return between JQR and SZZZ")


import statsmodels.api as sm
daily_return["intercept"]=1.0
model = sm.OLS(daily_return["JQR"],daily_return[["SZZZ","intercept"]])
results = model.fit()
results.summary()