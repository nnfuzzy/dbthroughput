

rndint <- function(n) round(runif(1)*n,0)


loop_insert <- function(dt_sequence,N_IDS,mongo,ns="throughput.r_throughput_src",drop=T){
if(drop){
  mongo.drop(mongo,ns)
}
for(i in 1:(length(dt_sequence))){
  ts__ = as.numeric(dt_sequence[i])
  #dt = ymd_hms(as.POSIXct(ts,origin = "1970-01-01"))
  src_data <- mongo.bson.from.list(list(ts=ts__,id=rndint(N_IDS)))
  mongo.insert(mongo, ns,src_data)
}
}


vectorize_insert <- function(x,N_IDS,ns="throughput.r_throughput_src"){
  #dt = ymd_hms(as.POSIXct(x,origin = "1970-01-01"))
  ts__ = as.numeric(x)
  src_data <- mongo.bson.from.list(list(ts=ts__,id=rndint(N_IDS)))
  mongo.insert(mongo,ns,src_data)
  return(NULL)
}


loop_aggregation <- function(rs,mongo,ns="throughput.r_throughput_agg",drop=T){  
  if(drop){
    mongo.drop(mongo,ns)
  }  
for(i in 1:nrow(rs)){
  #print(rs[i,])
  wd <- as.character(wday(as.POSIXct(rs[i,1],origin = "1970-01-01"),label=T)[1])
  hour <- as.character(hour(as.POSIXct(rs[i,1],origin = "1970-01-01"))[1])
  tslot <- sprintf('%s_%s',wd,hour)  
  #prepare update
  buf <- mongo.bson.buffer.create()
  mongo.bson.buffer.append(buf, "id", round(rs[i,2],0))
  criteria <- mongo.bson.from.buffer(buf)
  buf <- mongo.bson.buffer.create()
  mongo.bson.buffer.start.object(buf, "$inc")
  mongo.bson.buffer.append(buf,as.character(tslot), 1L)
  mongo.bson.buffer.finish.object(buf)
  objNew <- mongo.bson.from.buffer(buf)
  mongo.update(mongo, ns,criteria,objNew,mongo.update.upsert) 
}
}

vectorize_aggregation <- function(x,ns="throughput.r_throughput_agg"){ 
    ts <- x$ts
    id <- x$id
    wd <- as.character(wday(as.POSIXct(ts,origin = "1970-01-01"),label=T)[1])
    hour <- as.character(hour(as.POSIXct(ts,origin = "1970-01-01"))[1])
    tslot <- sprintf('%s_%s',wd,hour)  
    #prepare update
    buf <- mongo.bson.buffer.create()
    mongo.bson.buffer.append(buf, "id", round(id,0))
    criteria <- mongo.bson.from.buffer(buf)
    buf <- mongo.bson.buffer.create()
    mongo.bson.buffer.start.object(buf, "$inc")
    mongo.bson.buffer.append(buf,as.character(tslot), 1L)
    mongo.bson.buffer.finish.object(buf)
    objNew <- mongo.bson.from.buffer(buf)
    mongo.update(mongo, ns,criteria,objNew,mongo.update.upsert) 
  }
