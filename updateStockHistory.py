import os

import easyhistory
import datetime

#easyhistory.get_all_history(stock_code='000001',export='oracle')
starttime = datetime.datetime.now()

easyhistory.update()


#将数据导入数据库
#os.system('bash /public/stock/tackder/backupOracleDouble.sh')


endtime = datetime.datetime.now()
print ('执行时间为 ' + str( (endtime - starttime).seconds ) )