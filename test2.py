
import easyhistory
import talib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def myMACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
    ewma12 = pd.ewma(price,span=fastperiod)
    ewma60 = pd.ewma(price,span=slowperiod)
    dif = ewma12-ewma60
    dea = pd.ewma(dif,span=signalperiod)
    bar = (dif-dea) #有些地方的bar = (dif-dea)*2，但是talib中MACD的计算是bar = (dif-dea)*1
    return dif,dea,bar


his = easyhistory.History(dtype='D' , stock_code='000001' )

CLOSE=his.market['close'].values
macd, signal, hist = talib.MACD( CLOSE,fastperiod=12, slowperiod=26, signalperiod=9)
mydif,mydea,mybar = myMACD(CLOSE, fastperiod=12, slowperiod=26, signalperiod=9)

fig = plt.figure(figsize=[18,5])
plt.plot(CLOSE,macd,label='macd dif')
plt.plot(CLOSE,signal,label='signal dea')
plt.plot(CLOSE,hist,label='hist bar')
plt.plot(CLOSE,mydif,label='my dif')
plt.plot(CLOSE,mydea,label='my dea')
plt.plot(CLOSE,mybar,label='my bar')
plt.legend(loc='best')
plt.show()