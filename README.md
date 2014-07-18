Mongothroughput
===============

This is a simple attempt to compare the mongodb throughput with different client API's, because
I want to know if pymongo is slower then others. 


###  mongothrouput_python dependencies

```

pip install pymongo profilehooks --user

./mongothroughput_python/Throughput.py

#### Inserts 
16714498 function calls in 31.777 seconds

#### Upserts
15928525 function calls in 22.442 seconds

```

```

### mongothroughput_clojure
cd mongothroughput_clojure
lein run

#### Inserts 
"Elapsed time: 19066.944037 msecs"
#### Upsert
"Elapsed time: 50970.906349 msecs"

```

#### Author

* [Christian Schulz](https://twitter.com/nnfuzzy) 
