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
    stock_data.sort('date', inplace=True)


    # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
    for ma in ma_list:
        stock_data['MA_' + str(ma)] = pd.rolling_mean(stock_data['close'], ma)

    # 计算指数平滑移动平均线EMA
    for ma in ma_list:
        stock_data['EMA_' + str(ma)] = pd.ewma(stock_data['close'], span=ma)

    # 将数据按照交易日期从近到远排序
    stock_data.sort('date', ascending=False, inplace=True)

    return stock_data