# -*- coding: utf-8 -*-
import tushare as ts
from datetime import datetime
from multiprocessing.pool import ThreadPool
import pandas as pd




class Day_CELUE:


    def update(self,stock_s=None):
        pool = ThreadPool(1)
        # stock_codes = ['000501']
        pool.map(self.update_single_code, stock_s)


    def update_single_code( self,stock=None ):
        #'002052'
        print(stock)

        df = ts.get_tick_data(stock , date)
        df['time']= df['time'].str[:5]
        #df= df[df['time'] <= '11:20']


        dfs = df.groupby(df['time']).agg({'volume':'sum'})

        price_count = df.groupby(df.price)
        df__500 = dfs[dfs.volume <= 500]
        df5_1000 = dfs[ (dfs.volume <= 1000) &  (dfs.volume > 500) ]
        df1_2000 = dfs[ (dfs.volume <= 2000) &  (dfs.volume > 1000) ]
        df2_4000 = dfs[ (dfs.volume <= 4000) &  (dfs.volume > 2000) ]
        df4_6000 = dfs[ (dfs.volume <= 6000) &  (dfs.volume > 4000) ]
        df6_10000 = dfs[ (dfs.volume <= 10000) &  (dfs.volume > 6000) ]
        df__100000 = dfs[ dfs.volume > 10000 ]

        data = [stock,len(price_count),len(df__500),len(df5_1000),len(df1_2000),len(df2_4000),len(df4_6000),len(df6_10000),len(df__100000)]



        dict_rows.append(dict(zip(COLUMNS, data)))


        if len(price_count) <= 10 :
            len(price_count)
            print(price_count)
            print(data)

stock_s = ts.get_today_all()
#stock_s = ts.get_stock_basics()
stock_changepercent = stock_s[ ( stock_s.changepercent >= -3 ) & ( stock_s.changepercent  <= 2) ]

code = stock_changepercent['code']
#code = ['601700']
dict_rows = []
shishidata = pd.DataFrame()
COLUMNS = [ 'code' ,'price_count','df__500', 'df5_1000','df1_2000','df2_4000','df4_6000','df6_10000','df__100000']


now = datetime.now()
date = now.strftime('%Y-%m-%d')
date = '2016-10-11'
Day_CELUE().update(stock_s=code)


now2 = datetime.now()
date2 = now.strftime('HHmm')


shishidata.append( data=dict_rows ,columns=COLUMNS)

shishidata.to_excel('/home/oracle/Desktop/shishidata.xlsx')



#dfs.to_excel('/home/oracle/Desktop/002052.xlsx')
#dfs = df.groupby(df['price']).agg({'time':'min','price':'min','volume':'sum'})


#dfs.to_excel('/home/oracle/Desktop/002052-p.xlsx')
#df.to_excel('/home/oracle/Desktop/002052-3.xlsx')
#直接保存
#df = ts.get_today_ticks('002570' ,date='2016-09-30')
#df.to_excel('/home/oracle/Desktop/002052.xlsx')
#df_hq = ts.get_index()
#df_hq = df_hq[df_hq['change'] <= 2 & df_hq['change'] >= -2 ]
#直接保存
#df.to_excel('/home/oracle/Desktop/002570.xlsx')