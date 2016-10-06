# -*- coding: utf-8 -*-
#此例子采用Talib提供的MACD指标作为买入/卖出信号。
#当MACD信号小于0卖出。
#当MACD信号大于0买入。
import talib


# 定义MACD函数
def MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    参数设置:
        fastperiod = 12
        slowperiod = 26
        signalperiod = 9

    返回: macd - signal
    '''
    macd, signal, hist = talib.MACD(prices,
                                    fastperiod=fastperiod,
                                    slowperiod=slowperiod,
                                    signalperiod=signalperiod)
    return macd[-1] - signal[-1]



# 定义MACD函数
def MACDS(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    参数设置:
        fastperiod = 12
        slowperiod = 26
        signalperiod = 9

    返回: macd - signal
    '''
    macd, signal, hist = talib.MACD(prices,
                                    fastperiod=fastperiod,
                                    slowperiod=slowperiod,
                                    signalperiod=signalperiod)




    return macd, signal, hist


import numpy as np

def KDJ(date,N=9,M1=3,M2=3):
    datelen=len(date)
    array=np.array(date)
    kdjarr=[]
    for i in range(datelen):
        if i-N<0:
            b=0
        else:
            b=i-N+1
        rsvarr=array[b:i+1,0:5]
        rsv=(float(rsvarr[-1,-1])-float(min(rsvarr[:,3])))/(float(max(rsvarr[:,2]))-float(min(rsvarr[:,3])))*100
        if i==0:
            k=rsv
            d=rsv
        else:
            k=1/float(M1)*rsv+(float(M1)-1)/M1*float(kdjarr[-1][2])
            d=1/float(M2)*k+(float(M2)-1)/M2*float(kdjarr[-1][3])
        j=3*k-2*d
        kdjarr.append(list((rsvarr[-1,0],rsv,k,d,j)))
    return kdjarr
