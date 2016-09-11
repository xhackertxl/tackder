import cx_Oracle
import tushare as ts
from sqlalchemy import create_engine
from Average import  *

#create user tacker identified by tacker;
#grant session to tacker;//创建李四访问数据库权限
#grant connect,resource,dba to tacker;
#grant DBA to tacker
#报字段CLOB无法创建索引
#搜索return "CLOB" 修改为
#return "VARCHAR2(20)"
#gedit /public/tools/pyenv/versions/anaconda3-4.1.0/lib/python3.5/site-packages/sqlalchemy/sql/compiler.py


conn = cx_Oracle.connect('tacker/tacker@localhost:1521/orcl')

df = pd.read_sql(con=conn,sql="select *  from temp_temp")



cursor = conn.cursor()
cursor.execute("select * from dual")
row = cursor.fetchone()
print(row[0])
cursor.close()
conn.close()

#获取历史复权数据，分为前复权和后复权数据，接口提供股票上市以来所有历史数据，默认为前复权。如果不设定开始和结束日期，则返回近一年的复权数据，从性能上考虑，推荐设定开始日期和结束日期，而且最好不要超过三年以上，获取全部历史数据，请分年段分步获取，取到数据后，请及时在本地存储。获取个股首个上市日期，请参考以下方法：

engine = engine = create_engine('oracle+cx_oracle://tacker:tacker@orcl')

stock_codes = ts.get_stock_basics()

list = stock_codes.index
print(len(list))
df = stock_codes[stock_codes['timeToMarket'] != 0]
list = df.index
print(len(list))

print(len(list))

#for code in list:
#    print(code)






#'SELECT * FROM TABLE(F_STOCKS_LAST_DATA_TIME())'




#存入数据库
#df.to_sql('stock_code_list',engine)



#date = df.ix['600848']['timeToMarket'] #上市日期YYYYMMDD

#本接口还提供大盘指数的全部历史数据，调用时，请务必设定index参数为True,由于大盘指数不存在复权的问题，故可以忽略autype参数。

#df = ts.get_h_data('002337') #前复权

#存入数据库
#df.to_sql('days_002337',engine)

# ts.get_h_data('002337', autype='hfq') #后复权
# ts.get_h_data('002337', autype=None) #不复权
# ts.get_h_data('002337', start='2015-01-01', end='2015-03-16') #两个日期之间的前复权数据
# ts.get_h_data('399106', index=True) #深圳综合指数


#df = ts.get_tick_data('600848', date='2014-12-22')

#存入数据库
#df.to_sql('tick_data',engine)

# print('finish')

#追加数据到现有表
#df.to_sql('tick_data',engine,if_exists='append')