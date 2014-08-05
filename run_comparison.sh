#!/bin/bash

filename='throughput_timing_results_new.txt'
cpu=$(grep "model name" /proc/cpuinfo | uniq | sed 's/\s//g' | sed 's/modelname://g')
hd=$(sudo lshw |  fgrep 'disk' -A 3 | fgrep 'Produkt' | sed 's/Produkt: //g' | sed 's/\s//g')
os=$(uname -a | sed 's/\s/;/g' | awk -F";" '{ print $1,$3}')

delay=$1
uids=$2

#clojure_mongo

meta="$(date +%Y-%m-%d);$cpu;$hd;$os;clojure_mongodb_inserts;$delay;$uids;%e"
`\time -f "$meta" -a -o  $filename   throughput_clojure/target/mongothroughput_clojure-1.0.0-SNAPSHOT -i -d $delay -u $uids`


meta="$(date +%Y-%m-%d);$cpu;$hd;$os;clojure_mongodb_aggregate;$delay;$uids;%e"
`\time -f "$meta" -a -o  $filename   throughput_clojure/target/mongothroughput_clojure-1.0.0-SNAPSHOT -a -d $delay -u $uids`

#python_mongo

meta="$(date +%Y-%m-%d);$cpu;$hd;$os;python_mongodb_inserts;$delay;$uids;%e"
`\time -f "$meta" -a -o  $filename throughput_python/ExecThroughput.py -im -d $delay -u $uids`

meta="$(date +%Y-%m-%d);$cpu;$hd;$os;python_mongodb_aggregate;$delay;$uids;%e"
`\time -f "$meta" -a -o  $filename throughput_python/ExecThroughput.py -am -d $delay -u $uids`

#python_redis
meta="$(date +%Y-%m-%d);$cpu;$hd;$os;python_redis_inserts;$delay;$uids;%e"
`\time -f "$meta" -a -o $filename throughput_python/ExecThroughput.py -ir  -d $delay -u $uids`
meta="$(date +%Y-%m-%d);$cpu;$hd;$os;python_redis_aggregate;$delay;$uids;%e"
`\time -f "$meta" -a -o $filename throughput_python/ExecThroughput.py -ar  -d $delay -u $uids`


#python_mysql
meta="$(date +%Y-%m-%d);$cpu;$hd;$os;python_mysql_inserts;$delay;$uids;%e"
`\time -f "$meta" -a -o $filename throughput_python/ExecThroughput.py -is  -d $delay -u $uids`
meta="$(date +%Y-%m-%d);$cpu;$hd;$os;python_mysql_aggregate;$delay;$uids;%e"
`\time -f "$meta" -a -o $filename throughput_python/ExecThroughput.py -as -d $delay -u $uids`

#R_mongo
meta="$(date +%Y-%m-%d);$cpu;$hd;$os;r_mongo_inserts;$delay;$uids;%e"
`\time -f "$meta" -a -o $filename Rscript throughput_R/throughput_R.R $delay $uids 1 mongodb`

meta="$(date +%Y-%m-%d);$cpu;$hd;$os;r_mongo_aggregate;$delay;$uids;%e"
`\time -f "$meta" -a -o $filename Rscript throughput_R/throughput_R.R $delay $uids 0 mongodb`

#R_redis
meta="$(date +%Y-%m-%d);$cpu;$hd;$os;r_redis_inserts;$delay;$uids;%e"
`\time -f "$meta" -a -o $filename Rscript throughput_R/throughput_R.R $delay $uids 1 redis`
meta="$(date +%Y-%m-%d);$cpu;$hd;$os;r_redis_aggregate;$delay;$uids;%e"
`\time -f "$meta" -a -o $filename Rscript throughput_R/throughput_R.R $delay $uids 0 redis`
