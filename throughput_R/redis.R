library(rredis)
library(stringr)
library(lubridate)


flush_pattern_loop <- function(pattern){
  d_keys = redisKeys(pattern)
  for(k in d_keys){
  redisDelete(key = k)
  }
}


flush_pattern_vectorize <- function(pattern){
  d_keys = redisKeys(pattern)
  sapply(d_keys,function(k) redisDelete(key = k))
}


loop_insert_redis <- function(sequence,hash_prefix='src',UIDS,drop=TRUE){
  if(drop){
  flush_pattern_vectorize(sprintf('%s*',hash_prefix))
  }    
  for( dt in sequence){
    ts = as.numeric(dt)
    #key in hash is ts  , value for now only None. But could be more
    #in the future , i.e. smth like a json with k:v => transactions_data
    redisHSet(sprintf('%s:%s',hash_prefix,rndint(UIDS)),as.character(ts),"")
  }
}


#id_string <- 'src:429'
#d <- "1357120400"

loop_aggregation_redis <- function(hash_prefix_src='src',hash_prefix_agg='agg', drop=TRUE){
  if(drop){
    flush_pattern_vectorize(sprintf('%s*',hash_prefix_agg))
  }    
  src_keys <- redisKeys(sprintf('%s*',hash_prefix_src))
  for(id_string in src_keys){
    doc = redisHGetAll(key=id_string)
    print(doc)
    #doc is a list 
    doc_keys = names(doc)
    for (d in doc_keys){
      wd <- as.character(wday(as.POSIXct(as.numeric(d),origin = "1970-01-01"),label=TRUE)[1])
      hour <- as.character(hour(as.POSIXct(as.numeric(d),origin = "1970-01-01"))[1])
      tslot <- sprintf('%s_%s',wd,hour) 
      id <- str_split(id_string,':')[[1]][2]     
      print(sprintf('%s:%s',tslot,id))
      redisHIncrBy(sprintf("%s:%s",hash_prefix_agg,id),tslot,1)
    }
  }
}


