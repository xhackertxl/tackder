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

thred=8                #指定并发个数
seq=(1 2 3 4 5 6 7 8 9 21 22 23 24 25 31 32 33 34 35) #创建任务列表

# 为并发线程创建相应个数的占位
{
for (( i = 1;i<=${thred};i++ ))
do
echo;                  #因为read命令一次读取一行，一个echo默认输出一个换行符，所以为每个线程输出一个占位换行
done
} >&4                #将占位信息写入管道



filelist=`cd /public/stock/tackder/history/day/data/ && ls *.csv`
for file in $filelist #从任务列表 seq 中按次序获取每一个任务 或者用：for id in ${seq}
do
    read                                                        #读取一行，即fd4中的一个占位符
    ({
    watch_jiangshi
    cp -r /public/stock/tackder/init_day_data.ctl /public/stock/tackder/init_day_data.ctl${file}
    sed -i "2s/^.*.*$/infile '${file}'/" /public/stock/tackder/init_day_data.ctl${file}
    sed -i "3s/^.*.*$/append   into   table DAY_${file:0:6}/" /public/stock/tackder/init_day_data.ctl${file}
    cd /public/stock/tackder/history/day/data
    sqlldr tacker/tacker@orcl control=/public/stock/tackder/init_day_data.ctl${file} log=log.log bad=bad.log errors=5000 rows=500
    rm -r /public/stock/tackder/init_day_data.ctl${file}

    } ;echo >&4 ) &       #在后台执行任务ur_command 并将任务 ${id} 赋给当前任务ur_command；任务执行完后在fd4种写入一个占位符 ，&表示该部分命令/任务 并行处理
done <&4                                                #指定fd4为整个for的标准输入


wait                                                         #等待所有在此shell脚本中启动的后台任务完成
exec 4>&-                                              #关闭管道

#s删除sed 临时文件
cd /public/stock/tackder
#>/dev/null  2>&1 将错误信息输出到空设备
rm -r sed* >/dev/null  2>&1

UPDATE_YESTERDAY_CLOSE_ALL


end=$(date +%s) && echo $(( $end - $start ))