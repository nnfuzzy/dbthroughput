dbthroughput
============

This is a simple attempt comparing the throughput of different database products and client API. 
Actually I suffer on the slowness in  writes with mongodb regarding big data. In the first place I was 
interested if mongodb/pymongo is slower then others.  Data Mining is very often about meaningful 
recoding/aggregation  of transaction data. Finally I choose the timestamp->timeslot example , because it is universal 
and could be extended.

The realization for the different solutions might be not ideal. 


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

usage: Throughput.py [-h] [-d DELAY] [-a] [-i] [-uids UIDS] [--version]

Throughput

optional arguments:
  -h, --help  show this help message and exit
  -d DELAY    delay in seconds - density of data [200]
  -a          do aggregation [False]
  -i          do inserts [False]
  -uids UIDS  do inserts [1000]
  --version   show program's version number and exit


../mongothrouhput/mongothroughput_python (git)-[master] % ./Throughput.py -i -a    
Better than expected

#### Inserts 
0:00:20.792899
#### Upserts
0:00:15.371772


```

### mongothroughput_clojure
Bottleneck?

```
#### Inserts 
Elapsed time: 38.840 seconds
#### Upsert
Elapsed time: 64.443 seconds

```

### mongothroughput_R
Bottleneck?

../mongothrouhput/mongothroughput_R/Rscript throughput_R.R 1000 200


```
#### Inserts
Time difference of 3.374865 mins

#### Upsert
Time difference of 4.375968 mins


```



#### Author
* [Christian Schulz](https://twitter.com/nnfuzzy) 