#!/bin/bash
function watch_jiangshi()
{

echo "watch_jiangshi"  ${file:0:6}

sqlplus -S tacker/tacker@orcl <<EOF
call  CLEARTABLE();
exit;
EOF
}
start=$(date +%s)

watch_jiangshi
cd /public/stock/tackder && exp tacker/tacker inctype=cumulative file=tacker.dmp

end=$(date +%s) && echo $(( $end - $start ))