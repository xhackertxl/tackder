# -*- coding: utf-8 -*-


import tushare as ts


df = ts.get_tick_data('002570',date='2016-09-30')
df['time']= df['time'].str[:5]


df = df.groupby([df['time'], df['type']]).sum()





df.to_excel('/home/oracle/Desktop/002052.xlsx')


#直接保存
#df = ts.get_today_ticks('002570' ,date='2016-09-30')
#df.to_excel('/home/oracle/Desktop/002052.xlsx')

#df_hq = ts.get_index()

#df_hq = df_hq[df_hq['change'] <= 2 & df_hq['change'] >= -2 ]


#直接保存
#df.to_excel('/home/oracle/Desktop/002570.xlsx')