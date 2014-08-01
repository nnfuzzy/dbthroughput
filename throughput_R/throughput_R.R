### Install dependencies
#install.packages(c("rmongodb","lubridate","rplyr","rbenchmarks"))
options(warn=-1)
library(rmongodb)
library(lubridate)
library(plyr)
library(rbenchmark)

path <- getwd()
source(sprintf('%s/%s',path,"throughput_R/mongothroughput_fun.R"))

args <- commandArgs(TRUE)
DELAY <- as.numeric(args[1])
UIDS <-  as.numeric(args[2])
INSERT_FLAG <- as.numeric(args[3])

mongo <- mongo.create(db='throughput')


if(INSERT_FLAG==1) {

dt_sequence <- seq(from =as.POSIXct('2013-01-01 00:00:00',tz = '%Y-%m-%d %H:%M:%S',origin="1970-01-01"),
to=as.POSIXct('2014-01-01 00:00:00',tz='%Y-%m-%d %H:%M:%S',origin="1970-01-01"),
by=DELAY)

mongo <- mongo.create(db='throughput')
ns <- "throughput.r_throughput_src"
#insert loop 
loop_insert(dt_sequence,UIDS,mongo,ns,TRUE)
} else {
#aggregation  
ns <- "throughput.r_throughput_agg"
mongo.index.create(mongo, ns, '{"id":1}')
loop_aggregation(mongo,ns_src="throughput.r_throughput_src",ns_agg="throughput.r_throughput_agg",drop=T)
}
