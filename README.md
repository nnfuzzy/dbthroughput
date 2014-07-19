Mongothroughput
===============

This is a simple attempt to compare the mongodb throughput with different client API's, because
I want to know if pymongo is slower then others. 


###  mongothrouput_python

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
cd mongothroughput_clojure
lein run

#### Inserts 
Elapsed time: 20.091 seconds
#### Upsert
Elapsed time: 26.470 seconds

```


#### Author

* [Christian Schulz](https://twitter.com/nnfuzzy) 
