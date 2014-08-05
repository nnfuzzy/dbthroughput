dbthroughput
============

This is a simple attempt comparing the throughput of different database products and client API. 
Actually I suffer on the slowness in  writes with mongodb regarding big data. In the first place I was 
interested if mongodb/pymongo is slower then others.  Data Mining is very often about meaningful 
recoding/aggregation  of transaction data. Finally I choose the timestamp->timeslot example , because it is universal 
and could be extended.

The realization for the different solutions might be not ideal yet.


### Task

* Insert some timestamps for a specified amount of ids

```

{
    "_id" : ObjectId("53ca0890628ab01f35935529"),
    "id" : 526,
    "ts" : 1356994800
}

```

* Read and aggregate this timestamps by one of the 168 week timeslots

```

{
    "_id" : ObjectId("53ce604d4bee4d2dc5d70ed0"),
    "id" : 140,
    "Tues_1" : 1,
    "Wed_18" : 1,
    "Sun_21" : 1,
    "Thurs_23" : 1,
    "Wed_12" : 1,
    "Fri_10" : 1,
    "Tues_16" : 1,
    "Sat_12" : 1,
    "Fri_4" : 1,
    "Sun_19" : 1,
    "Wed_6" : 1,
    "Fri_1" : 1,
    "Wed_1" : 1,
    "Sat_17" : 1
}


```
#### Results
Isolation isn't perfect, helper functions and delete operations are in the timings included.

* R/Redis: What's wrong here ~ 24 ops/second? It is well-known that loops are bad in R. As well the deletes are very bad. With python it takes < 1 second.
* Python/MySQL: RDBMS are difficult with dynamic table designs (flat table) , because repeated 'alter table' commands are not approriate.
So I decided using an "aggregated" transaction result table.




<img src="http://i.imgur.com/DL3L4CT.png">

#### Contributors
* [Christian Schulz](https://twitter.com/nnfuzzy) 