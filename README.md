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
Elapsed time: 38.840 seconds
#### Upsert
Elapsed time: 64.443 seconds

```

### mongothroughput_R

```

#### This is not a lazy cursor to use it inside the aggregation


#### Inserts 
   

#### Upsert



```



#### Author

* [Christian Schulz](https://twitter.com/nnfuzzy) 
* [www.mining-facts.com](http://www.mining-facts.com)