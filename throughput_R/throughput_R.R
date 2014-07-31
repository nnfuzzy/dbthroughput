### Install dependencies
#install.packages(c("rmongodb","lubridate","rplyr","rbenchmarks"))
options(warn=-1)
library(rmongodb)
library(lubridate)
library(plyr)
library(rbenchmark)



source("mongothroughput_fun.R")

args <- commandArgs(TRUE)
N_IDS <- as.numeric(args[1])
STEPS_SECONDS <- as.numeric(args[2])

#N_IDS <- 1000
#STEPS_SECONDS <-  200

mongo <- mongo.create(db='throughput')


dt_sequence <- seq(from =as.POSIXct('2013-01-01 00:00:00',tz = '%Y-%m-%d %H:%M:%S',origin="1970-01-01"),
    to=as.POSIXct('2014-01-01 00:00:00',tz='%Y-%m-%d %H:%M:%S',origin="1970-01-01"),
    by=STEPS_SECONDS)

ns <- "throughput.r_throughput_src"

#insert loop 
start_insert <- now()
loop_insert(dt_sequence=dt_sequence,N_IDS, mongo=mongo)
stop_insert <- now()



#aggregation  
mongo <- mongo.create(db='throughput')
ns <- "throughput.r_throughput_agg"
mongo.index.create(mongo, ns, '{"id":1}')
start_aggregation <- now()
loop_aggregation(mongo,ns_src="throughput.r_throughput_src",ns_agg="throughput.r_throughput_agg",drop=T)
stop_aggregation <- now()

print((stop_insert - start_insert))
print((stop_aggregation - start_aggregation))
