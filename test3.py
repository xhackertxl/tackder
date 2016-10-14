# -*- coding: utf-8 -*-
import tushare as ts
import talib as ta
import numpy as np
import pandas as pd
import os, time, sys, re, datetime
import csv
import scipy
import smtplib
from email.mime.text import MIMEText

from public import *

# 获取股票列表
# code,代码 name,名称 industry,所属行业 area,地区 pe,市盈率 outstanding,流通股本 totals,总股本(万) totalAssets,总资产(万)liquidAssets,流动资产
# fixedAssets,固定资产 reserved,公积金 reservedPerShare,每股公积金 eps,每股收益 bvps,每股净资 pb,市净率 timeToMarket,上市日期
def Get_Stock_List():
    df = ts.get_stock_basics()
    return df


def load_csv_files(path):


    file_list = [f for f in os.listdir(path) if f.endswith('.csv')]

    df = pd.DataFrame

    df = pd.DataFrame(data=file_list, columns=['code'])

    df = df.set_index('code')

    return df
# 修改了的函数，按照多个指标进行分析

# 按照MACD，KDJ等进行分析
def Get_TA(df_Code, Dist , isLocal=False):
    operate_array1 = []
    operate_array2 = []
    operate_array3 = []

    count = 0

    df_Codes=df_Code.index


    for code in df_Codes:
        print(code)
        # index,0 - 6
        # 0 date：日期
        # 1 open：开盘价
        # 2 high：最高价
        # 3 close：收盘价
        # 4 low：最低价
        # 5 volume：成交量
        # 6 price_change：价格变动
        # 7 p_change：涨跌幅

        # 7-12 ma5：5日均价
        # 8 ma10：10日均价
        # 9 ma20:20日均价
        # 10    v_ma5:5日均量
        # 11    v_ma10:10日均量
        # 12    v_ma20:20日均量


        if isLocal == False:
            df = ts.get_hist_data(code, start='2014-11-20')
        else:
            csv_file_path = os.path.join(history_day_data_path,code)
            if os.path.exists(csv_file_path):
                try:
                    df = pd.read_csv(csv_file_path)
                    df.sort_values(['date'],inplace=True)
                except ValueError:
                    return

        dflen = df.shape[0]
        count = count + 1
        if dflen > 35:
            try:
                (df, operate1,date1) = Get_MACD(df)
                (df, operate2,date2) = Get_KDJ(df)
                (df, operate3,date3) = Get_RSI(df)
            except Exception as e:
                Write_Blog(e, Dist)
                pass
        operate_array1.append(operate1)  # round(df.iloc[(dflen-1),16],2)
        operate_array2.append(operate2)
        operate_array3.append(operate3)
        if count == 0:
            Write_Blog(str(count), Dist)
    df_Code['MACD'] = pd.Series(operate_array1, index=df_Codes)
    df_Code['KDJ'] = pd.Series(operate_array2, index=df_Codes)
    df_Code['RSI'] = pd.Series(operate_array3, index=df_Codes)
    return df_Code


# 通过MACD判断买入卖出
def Get_MACD(df):
    # 参数12,26,9
    macd, macdsignal, macdhist = ta.MACD(np.array(df['close']), fastperiod=12, slowperiod=26, signalperiod=9)

    SignalMA5 = ta.MA(macdsignal, timeperiod=5, matype=0)
    SignalMA10 = ta.MA(macdsignal, timeperiod=10, matype=0)
    SignalMA20 = ta.MA(macdsignal, timeperiod=20, matype=0)
    # 13-15 DIFF  DEA  DIFF-DEA
    df['macd'] = pd.Series(macd, index=df.index)  # DIFF
    df['macdsignal'] = pd.Series(macdsignal, index=df.index)  # DEA
    df['macdhist'] = pd.Series(macdhist, index=df.index)  # DIFF-DEA
    dflen = df.shape[0]
    MAlen = len(SignalMA5)
    operate = 0
    # 2个数组 1.DIFF、DEA均为正，DIFF向上突破DEA，买入信号。 2.DIFF、DEA均为负，DIFF向下跌破DEA，卖出信号。
    # 待修改
    if df.iloc[(dflen - 1)]['macd'] > 0:
        if df.iloc[(dflen - 1)]['macdsignal'] > 0:
            if df.iloc[(dflen - 1)]['macd'] > df.iloc[(dflen - 1)]['macdsignal'] and df.iloc[(dflen - 2)]['macd'] <= df.iloc[(dflen - 2)]['macdsignal']:
                operate = operate + 100  # 买入
    else:
        if df.iloc[(dflen - 1)]['macdsignal'] < 0:
            if df.iloc[(dflen - 1), 13 ] == df.iloc[(dflen-2)]['macdsignal']:
                operate = operate - 10  # 卖出

    # 3.DEA线与K线发生背离，行情反转信号。
    if df.iloc[(dflen - 1)]['MA5'] >= df.iloc[(dflen - 1)]['MA10'] and df.iloc[(dflen - 1)]['MA10'] >= df.iloc[(dflen - 1)]['MA20']:  # K线上涨
        if SignalMA5[MAlen - 1] <= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] <= SignalMA20[MAlen - 1]:  # DEA下降
            operate = operate - 1
    elif df.iloc[(dflen - 1)]['MA5'] <= df.iloc[(dflen - 1)]['MA10'] and df.iloc[(dflen - 1)]['MA10'] <= df.iloc[(dflen - 1)]['MA20']:  # K线下降
        if SignalMA5[MAlen - 1] >= SignalMA10[MAlen - 1] and SignalMA10[MAlen - 1] >= SignalMA20[MAlen - 1]:  # DEA上涨
            operate = operate + 1

    # 4.分析MACD柱状线，由负变正，买入信号。
    if df.iloc[(dflen - 1)]['macdhist'] > 0 and dflen > 30:
        for i in range(1, 26):
            if df.iloc[(dflen - 1 - i)]['macdhist'] <= 0:  #
                operate = operate + 5
                break
                # 由正变负，卖出信号
    if df.iloc[(dflen - 1)]['macdhist'] < 0 and dflen > 30:
        for i in range(1, 26):
            if df.iloc[(dflen - 1 - i)]['macdhist'] >= 0:  #
                operate = operate - 5
                break

    return (df, operate, df.iloc[(dflen - 1)]['date'])


# 通过KDJ判断买入卖出
def Get_KDJ(df):
    # 参数9,3,3
    slowk, slowd = ta.STOCH(np.array(df['high']), np.array(df['low']), np.array(df['close']), fastk_period=9,
                            slowk_period=3, slowk_matype=0, slowd_period=3, slowd_matype=0)

    slowkMA5 = ta.MA(slowk, timeperiod=5, matype=0)
    slowkMA10 = ta.MA(slowk, timeperiod=10, matype=0)
    slowkMA20 = ta.MA(slowk, timeperiod=20, matype=0)
    slowdMA5 = ta.MA(slowd, timeperiod=5, matype=0)
    slowdMA10 = ta.MA(slowd, timeperiod=10, matype=0)
    slowdMA20 = ta.MA(slowd, timeperiod=20, matype=0)

    # 16-17 K,D
    df['slowk'] = pd.Series(slowk, index=df.index)  # K
    df['slowd'] = pd.Series(slowd, index=df.index)  # D
    dflen = df.shape[0]
    MAlen = len(slowkMA5)
    operate = 0
    # 1.K线是快速确认线——数值在90以上为超买，数值在10以下为超卖；D大于80时，行情呈现超买现象。D小于20时，行情呈现超卖现象。
    if df.iloc[(dflen - 1)]['slowk'] >= 90:
        operate = operate - 3
    elif df.iloc[(dflen - 1)]['slowk'] <= 10:
        operate = operate + 30

    if df.iloc[(dflen - 1)]['slowd'] >= 80:
        operate = operate - 3
    elif df.iloc[(dflen - 1)]['slowd'] <= 20:
        operate = operate + 60

    # 2.上涨趋势中，K值大于D值，K线向上突破D线时，为买进信号。#待修改
    if df.iloc[(dflen - 1)]['slowk'] > df.iloc[(dflen - 1)]['slowd'] and df.iloc[(dflen - 2)]['slowk'] <= \
            df.iloc[(dflen - 2)]['slowd']:
        operate = operate + 10
    # 下跌趋势中，K小于D，K线向下跌破D线时，为卖出信号。#待修改
    elif df.iloc[(dflen - 1)]['slowk'] < df.iloc[(dflen - 1)]['slowd'] and df.iloc[(dflen - 2)]['slowk'] >= \
            df.iloc[(dflen - 2)]['slowd']:
        operate = operate - 10

    # 3.当随机指标与股价出现背离时，一般为转势的信号。
    if df.iloc[(dflen - 1)]['MA5'] >= df.iloc[(dflen - 1)]['MA10'] and df.iloc[(dflen - 1)]['MA10'] >= \
            df.iloc[(dflen - 1)]['MA20']:  # K线上涨
        if (slowkMA5[MAlen - 1] <= slowkMA10[MAlen - 1] and slowkMA10[MAlen - 1] <= slowkMA20[MAlen - 1]) or \
                (slowdMA5[MAlen - 1] <= slowdMA10[MAlen - 1] and slowdMA10[MAlen - 1] <= slowdMA20[MAlen - 1]):  # K,D下降
            operate = operate - 1
    elif df.iloc[(dflen - 1)]['MA5'] <= df.iloc[(dflen - 1)]['MA10'] and df.iloc[(dflen - 1)]['MA10'] <= \
            df.iloc[(dflen - 1)]['MA20']:  # K线下降
        if (slowkMA5[MAlen - 1] >= slowkMA10[MAlen - 1] and slowkMA10[MAlen - 1] >= slowkMA20[MAlen - 1]) or \
                (slowdMA5[MAlen - 1] >= slowdMA10[MAlen - 1] and slowdMA10[MAlen - 1] >= slowdMA20[MAlen - 1]):  # K,D上涨
            operate = operate + 1

    return (df, operate, df.iloc[(dflen - 1)]['date'])


# 通过RSI判断买入卖出
def Get_RSI(df):
    # 参数14,5
    slowreal = ta.RSI(np.array(df['close']), timeperiod=14)
    fastreal = ta.RSI(np.array(df['close']), timeperiod=5)

    slowrealMA5 = ta.MA(slowreal, timeperiod=5, matype=0)
    slowrealMA10 = ta.MA(slowreal, timeperiod=10, matype=0)
    slowrealMA20 = ta.MA(slowreal, timeperiod=20, matype=0)
    fastrealMA5 = ta.MA(fastreal, timeperiod=5, matype=0)
    fastrealMA10 = ta.MA(fastreal, timeperiod=10, matype=0)
    fastrealMA20 = ta.MA(fastreal, timeperiod=20, matype=0)
    # 18-19 慢速real，快速real
    df['slowreal'] = pd.Series(slowreal, index=df.index)  # 慢速real 18
    df['fastreal'] = pd.Series(fastreal, index=df.index)  # 快速real 19
    dflen = df.shape[0]
    MAlen = len(slowrealMA5)
    operate = 0
    # RSI>80为超买区，RSI<20为超卖区
    if df.iloc[(dflen - 1)]['slowreal'] > 80 or df.iloc[(dflen - 1)]['fastreal'] > 80:
        operate = operate - 2
    elif df.iloc[(dflen - 1)]['slowreal'] < 20 or df.iloc[(dflen - 1)]['fastreal'] < 20:
        operate = operate + 20

    # RSI上穿50分界线为买入信号，下破50分界线为卖出信号
    if (df.iloc[(dflen - 2)]['slowreal'] <= 50 and df.iloc[(dflen - 1)]['slowreal'] > 50) or (
            df.iloc[(dflen - 2)]['fastreal'] <= 50 and df.iloc[(dflen - 1)]['fastreal'] > 50):
        operate = operate + 4
    elif (df.iloc[(dflen - 2)]['slowreal'] >= 50 and df.iloc[(dflen - 1)]['slowreal'] < 50) or (
            df.iloc[(dflen - 2)]['fastreal'] >= 50 and df.iloc[(dflen - 1)]['fastreal'] < 50):
        operate = operate - 4

    # RSI掉头向下为卖出讯号，RSI掉头向上为买入信号
    if df.iloc[(dflen - 1)]['MA5'] >= df.iloc[(dflen - 1)]['MA10'] and df.iloc[(dflen - 1)]['MA10'] >= df.iloc[(dflen - 1)]['MA20']:  # K线上涨
        if (slowrealMA5[MAlen - 1] <= slowrealMA10[MAlen - 1] and slowrealMA10[MAlen - 1] <= slowrealMA20[MAlen - 1]) or \
                (fastrealMA5[MAlen - 1] <= fastrealMA10[MAlen - 1] and fastrealMA10[MAlen - 1] <= fastrealMA20[
                        MAlen - 1]):  # RSI下降
            operate = operate - 1
    elif df.iloc[(dflen - 1)]['MA5'] <= df.iloc[(dflen - 1)]['MA10'] and df.iloc[(dflen - 1)]['MA10'] <= df.iloc[(dflen - 1)]['MA20']:  # K线下降
        if (slowrealMA5[MAlen - 1] >= slowrealMA10[MAlen - 1] and slowrealMA10[MAlen - 1] >= slowrealMA20[MAlen - 1]) or \
                (fastrealMA5[MAlen - 1] >= fastrealMA10[MAlen - 1] and fastrealMA10[MAlen - 1] >= fastrealMA20[
                        MAlen - 1]):  # RSI上涨
            operate = operate + 1

    # 慢速线与快速线比较观察，若两线同向上，升势较强；若两线同向下，跌势较强；若快速线上穿慢速线为买入信号；若快速线下穿慢速线为卖出信号
    if df.iloc[(dflen - 1)]['fastreal'] > df.iloc[(dflen - 1)]['slowreal'] and df.iloc[(dflen - 2)]['fastreal'] <= df.iloc[(dflen - 2)]['slowreal']:
        operate = operate + 10
    elif df.iloc[(dflen - 1)]['fastreal'] < df.iloc[(dflen - 1)]['slowreal'] and df.iloc[(dflen - 2)]['fastreal'] >= df.iloc[(dflen - 2)]['slowreal']:
        operate = operate - 10

    return (df, operate, df.iloc[(dflen - 1)]['date'])


def Output_Csv(df, Dist):
    TODAY = datetime.date.today()
    CURRENTDAY = TODAY.strftime('%Y-%m-%d')
    df.to_csv(Dist + CURRENTDAY + 'stock.csv')  # 选择保存


def Close_machine():
    #o = "c:\\windows\\system32\\shutdown -s"  #########
    #os.system(o)  #########
    print('完成')


# 日志记录
def Write_Blog(strinput, Dist):
    TODAY = datetime.date.today()
    CURRENTDAY = TODAY.strftime('%Y-%m-%d')
    TIME = time.strftime("%H:%M:%S")
    # 写入本地文件
    fp = open(Dist + 'blog.txt', 'a')
    fp.write('------------------------------\n' + CURRENTDAY + " " + TIME + " " + strinput + '  \n')
    fp.close()
    time.sleep(1)




if 1==1: #从本地读取数据
    df = load_csv_files(history_day_data_path)

    df = Get_TA(df, history_day_data_path , isLocal=True )
    Output_Csv(df, history_day_log_path)
elif 1==2:
    df = Get_Stock_List()

    df = Get_TA(df, history_day_data_path)
    Output_Csv(df, history_day_log_path)
    time.sleep(1)
    Close_machine()
