#!/bin/bash

function watch_jiangshi()
{

echo "watch_jiangshi"  ${file:0:6}

sqlplus -S tacker/tacker@orcl <<EOF
call CREATE_CLEAR_CHECK_DAY_TABLE('DAY_${file:0:6}',2);
exit;
EOF
}


function UPDATE_YESTERDAY_CLOSE_ALL()
{

echo "watch_jiangshi"  ${file:0:6}
sqlplus -S tacker/tacker@orcl <<EOF
call UPDATE_YESTERDAY_CLOSE_ALL();
exit;
EOF
}


start=$(date +%s)

tmpfile=$$.fifo        #创建管道名称
mkfifo $tmpfile       #创建管道
exec 4<>$tmpfile   #创建文件标示4，以读写方式操作管道$tmpfile
rm $tmpfile            #将创建的管道文件清除


filelist=`cd /public/stock/tackder/history/day/data/ && ls *.csv`
file="000001.csv"

watch_jiangshi
cp -r /public/stock/tackder/init_day_data.ctl /public/stock/tackder/init_day_data.ctl${file}
sed -i "2s/^.*.*$/infile '${file}'/" /public/stock/tackder/init_day_data.ctl${file}
sed -i "3s/^.*.*$/append   into   table DAY_${file:0:6}/" /public/stock/tackder/init_day_data.ctl${file}
cd /public/stock/tackder/history/day/data
sqlldr tacker/tacker@orcl control=/public/stock/tackder/init_day_data.ctl${file} log=log.log bad=bad.log errors=5000 rows=500
rm -r /public/stock/tackder/init_day_data.ctl${file}


#s删除sed 临时文件
cd /public/stock/tackder
#>/dev/null  2>&1 将错误信息输出到空设备
rm -r sed* >/dev/null  2>&1


UPDATE_YESTERDAY_CLOSE_ALL


end=$(date +%s) && echo $(( $end - $start ))