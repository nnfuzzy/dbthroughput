### Install dependencies
#install.packages(c("rmongodb","lubridate","rplyr","rbenchmarks"))
options(warn=-1)
library(rmongodb)
library(lubridate)
library(rredis)

#You have to run the starter script from path dbthroughput
path <- getwd()
source(sprintf('%s/%s',path,"throughput_R/core.R"))
source(sprintf('%s/%s',path,"throughput_R/mongo.R"))
source(sprintf('%s/%s',path,"throughput_R/redis.R"))


args <- commandArgs(TRUE)
DELAY <- as.numeric(args[1])
UIDS <-  as.numeric(args[2])
INSERT_FLAG <- as.numeric(args[3])
DB_FLAG <- args[4]


if(DB_FLAG == 'mongodb'){
  mongo <- mongo.create(db='throughput')
  if(INSERT_FLAG==1) {
    mongo <- mongo.create(db='throughput')
    ns <- "throughput.r_throughput_src"
    #insert loop 
    loop_insert_mongo(dt_sequence(DELAY),UIDS,mongo,ns,TRUE)
  } else {
    #aggregation  
    ns <- "throughput.r_throughput_agg"
    mongo.index.create(mongo, ns, '{"id":1}')
    loop_aggregation_mongo(mongo,ns_src="throughput.r_throughput_src",ns_agg="throughput.r_throughput_agg",drop=T)
  }
} 


if(DB_FLAG == 'redis'){
  redisConnect()
  if(INSERT_FLAG==1) {
    loop_insert_redis(dt_sequence(DELAY),hash_prefix ='src',UIDS=UIDS,drop=TRUE)
  } else {
    loop_aggregation_redis('src','agg')  
  }
} 

