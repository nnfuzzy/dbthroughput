library(rmongodb)
library(lubridate)
library(plyr)
library(rbenchmark)
### Install dependencies
# install.packages("rmongodb")
# install.packages("lubridate")
# install.packages("rbenchmark")
# install.packages("rplyr")


source("mongothroughput_fun.R")

N_IDS <- 1000
STEPS_SECONDS <-  200

mongo <- mongo.create(db='throughput')


dt_sequence <- seq(from =as.POSIXct('2013-01-01 00:00:00',tz = '%Y-%m-%d %H:%M:%S',origin="1970-01-01"),
    to=as.POSIXct('2014-01-01 00:00:00',tz='%Y-%m-%d %H:%M:%S',origin="1970-01-01"),
    by=STEPS_SECONDS)

ns <- "throughput.r_throughput_src"

#insert loop 
#benchmark(loop_insert(dt_sequence=dt_sequence,N_IDS, mongo=mongo),replications = 1)
system.time(loop_insert(dt_sequence=dt_sequence,N_IDS, mongo=mongo))

# insert  vectorize solution
mongo.drop(mongo,ns)
#benchmark(sapply(dt_sequence,function(x) vectorize_insert(x,N_IDS = N_IDS)),replications = 1)
system.time(sapply(dt_sequence,function(x) vectorize_insert(x,N_IDS = N_IDS)))


#########################
#is there no lazy cursor?
system.time(rs <- mongo.find.all(mongo, "throughput.r_throughput_src",data.frame = T))
##########################

ns <- "throughput.r_throughput_agg"
system.time(loop_aggregation(rs = rs,mongo = mongo))
mongo.drop(mongo,ns)
system.time(d_ply(.data = rs,1,vectorize_aggregation))






