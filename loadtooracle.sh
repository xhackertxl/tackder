#!/bin/bash


function watch_jiangshi()
{

echo "watch_jiangshi"  ${file:0:6}

sqlplus -S tacker/tacker@orcl <<EOF
call CREATE_CLEAR_CHECK_DAY_TABLE('DAY_${file:0:6}',2);
exit;
EOF
}
start=$(date +%s)

filelist=`cd /public/stock/tackder/history/day/data/ && ls *.csv`
for file in $filelist
do

    {
    watch_jiangshi
    sed -i "2s/^.*.*$/infile '${file}'/" /public/stock/tackder/init_day_data.ctl
    sed -i "3s/^.*.*$/append   into   table DAY_${file:0:6}/" /public/stock/tackder/init_day_data.ctl
    cd /public/stock/tackder/history/day/data
    \sqlldr tacker/tacker@orcl control=/public/stock/tackder/init_day_data.ctl log=log.log bad=bad.log errors=5000 rows=500
    }&
done

end=$(date +%s) && echo $(( $end - $start ))


#还原数据库
#imp tacker/tacker inctype=RESTORE FULL=y FILE=tacker.dmp