# -*- coding: utf-8 -*-
import tushare as ts

# df = ts.get_realtime_quotes('002628') #Single stock symbol
# df[['code','name','price','bid','ask','volume','amount','time']]
# print(df)
#
# df = ts.get_tick_data('002628',date='2016-09-20')
# df.head(10)
# print(df)
#
# df = ts.get_today_ticks('601333')
# df.head(10)
# print(df)


df = ts.get_h_data('300035') #前复权
print(df)