# -*- coding: utf-8 -*-
"""
@author: www.yucezhe.com
@contact: QQ:2089973054 email:xjc@yucezhe.com

程序中运用到的样本数据可到这里下载：http://yucezhe.com/product?name=trading-data 其中包含了所有股票、从上市日起的全部交易数据。
"""


import pandas as pd

# 分别计算5日、20日、60日的移动平均线
#ma_list

def average(ma_list=[5, 20, 60], stock_data=[]):

    # 将数据按照交易日期从远到近排序
    stock_data.sort_values(['date'],inplace=True)

    # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
    for ma in ma_list:
        columsStr = 'MA_' + str(ma)
        if columsStr in stock_data.columns :
            del stock_data[columsStr]
        #stock_data['MA_' + str(ma)] = stock_data['close'].rolling(window=ma,center=False).mean()
        stock_data.insert(stock_data.columns.size,columsStr,stock_data['close'].rolling(window=ma,center=False).mean())

    # 计算指数平滑移动平均线EMA
    for ma in ma_list:
        #stock_data['EMA_' + str(ma)] = stock_data['close'].ewm(span=5, ignore_na=False, adjust=True, min_periods=0).mean()
        columsStr = 'EMA_' + str(ma)
        if columsStr in stock_data.columns :
            del stock_data[columsStr]
        stock_data.insert(stock_data.columns.size,columsStr, stock_data['close'].ewm(span=ma, ignore_na=False, adjust=True, min_periods=0).mean())


    # 将数据按照交易日期从近到远排序
    stock_data.sort_values(['date'], ascending=False, inplace=True)

    return stock_data