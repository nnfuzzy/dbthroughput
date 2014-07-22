Mongothroughput
===============

This is a simple attempt to compare the mongodb throughput with different client API's, because
I want to know if pymongo is slower then others. In the first place the different solutions might be not
optimized.


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



###  mongothroughput_python

```

pip install pymongo profilehooks --user

./mongothroughput_python/Throughput.py

#### Inserts 
16714687 function calls (16714686 primitive calls) in 27.489 seconds

#### Upserts
15928525 function calls (15928398 primitive calls) in 18.535 seconds


```

### mongothroughput_clojure

```


#### Inserts 
Elapsed time: 20.091 seconds
#### Upsert
Elapsed time: 26.470 seconds

```

### mongothroughput_R

```

#### Miss a lazy cursor to use it inside the aggregation
system.time(rs <- mongo.find.all(mongo, "throughput.r_throughput_src",data.frame = T))
       User      System verstrichen 
   1119.524       0.000    1118.145 


#### Inserts 
system.time(loop_insert(dt_sequence=dt_sequence,N_IDS, mongo=mongo))
       User      System verstrichen 
    120.798       8.761     152.246 
   

#### Upsert
system.time(loop_aggregation(rs = rs,mongo = mongo))
       User      System verstrichen 
    229.931      10.223     294.029 



```



#### Author

* [Christian Schulz](https://twitter.com/nnfuzzy) 
* [www.mining-facts.com](http://www.mining-facts.com)