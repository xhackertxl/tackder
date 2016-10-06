# -*- coding: utf-8 -*-
"""
@量化交流QQ群:461470781，欢迎交流
"""
import pandas as pd


import os
def get_his(stock_code, parse_dates=['date']):
    #当前小牧绝对路径'/public/stock/tackder/海龟交易法则'
    #homedir = os.getcwd()
    csv_file_path = os.path.join('/public/stock/tackder/','history', 'day', 'data', '{}.csv'.format(stock_code))

    if os.path.exists(csv_file_path):
        try:
            his = pd.read_csv(csv_file_path , parse_dates= parse_dates)
            return his
        except ValueError:
            return

# ==========导入上证指数的原始数据data
# 注意：这里请填写数据文件在您电脑中的路径，并注意路径中斜杠的方向
index_data = get_his('000001', parse_dates=['date'])


# 保留这几个需要的字段：'date', 'high', 'low', 'close', 'change'
index_data = index_data[['date', 'high', 'low', 'close']]
# 对数据按照【date】交易日期从小到大排序
index_data.sort('date', inplace=True)
index_data['change'] = index_data['close'].pct_change() * 100



# ==========计算海龟交易法则的买卖点
# 设定海龟交易法则的两个参数，当收盘价大于最近N1天的最高价时买入，当收盘价低于最近N2天的最低价时卖出
# 这两个参数可以自行调整大小，但是一般N1 > N2
N1 = 20
N2 = 10

# 通过rolling_max方法计算最近N1个交易日的最高价
index_data['最近N1个交易日的最高点'] =  pd.rolling_max(index_data['high'], N1)
# 对于上市不足N1天的数据，取上市至今的最高价
index_data['最近N1个交易日的最高点'].fillna(value=pd.expanding_max(index_data['high']), inplace=True)

# 通过相似的方法计算最近N2个交易日的最低价
index_data['最近N2个交易日的最低点'] =  pd.rolling_min(index_data['low'], N1)
index_data['最近N2个交易日的最低点'].fillna(value=pd.expanding_min(index_data['low']), inplace=True)

# 当当天的【close】> 昨天的【最近N1个交易日的最高点】时，将【收盘发出的信号】设定为1
buy_index = index_data[index_data['close'] > index_data['最近N1个交易日的最高点'].shift(1)].index
index_data.loc[buy_index, '收盘发出的信号'] = 1
# 当当天的【close】< 昨天的【最近N2个交易日的最低点】时，将【收盘发出的信号】设定为0
sell_index = index_data[index_data['close'] < index_data['最近N2个交易日的最低点'].shift(1)].index
index_data.loc[sell_index, '收盘发出的信号'] = 0

# 计算每天的仓位，当天持有上证指数时，仓位为1，当天不持有上证指数时，仓位为0
index_data['当天的仓位'] = index_data['收盘发出的信号'].shift(1)
index_data['当天的仓位'].fillna(method='ffill', inplace=True)

# 取1992年之后的数据，排出较早的数据
index_data = index_data[index_data['date'] >= pd.to_datetime('19930101')]

# 当仓位为1时，买入上证指数，当仓位为0时，空仓。计算从19920101至今的资金指数
index_data['资金指数'] = (index_data['change'] * index_data['当天的仓位'] + 1.0).cumprod()
initial_idx = index_data.iloc[0]['close'] / (1 + index_data.iloc[0]['change'])
index_data['资金指数'] *= initial_idx

# 输出数据到指定文件
index_data[['date', 'high', 'low', 'close', 'change', '最近N1个交易日的最高点',
            '最近N2个交易日的最低点', '当天的仓位', '资金指数']].to_csv('turtle.csv', index=False, encoding='gbk')


# ==========计算每年指数的收益以及海龟交易法则的收益
index_data['海龟法则每日涨跌幅'] = index_data['change'] * index_data['当天的仓位']
year_rtn = index_data.set_index('date')[['change', '海龟法则每日涨跌幅']].\
               resample('A', how=lambda x: (x+1.0).prod() - 1.0) * 100
print(year_rtn)