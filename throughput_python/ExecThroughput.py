#!/usr/bin/env python

import argparse
import datetime
from pythroughput import Mongo
from pythroughput import Redis
from pythroughput import Core



def main():
	parser = argparse.ArgumentParser(description="ExecThroughput", add_help=True)
	parser.add_argument('-d', action='store', dest='delay', type=int, default=2000,
	                    help='delay in seconds - density of data [%(default)s]')
	parser.add_argument('-uids', action='store', dest='uids', default=1000, type=int,
	                    help='number of uids [%(default)s]')

	parser.add_argument('-im', action='store_true', dest='insert_mongo', default=False,
	                    help='do inserts into mongodb [%(default)s]')

	parser.add_argument('-ir', action='store_true', dest='insert_redis', default=False,
	                    help='do inserts into redis[%(default)s]')

	parser.add_argument('-am', action='store_true', dest='aggregation_mongo', default=False,
	                    help='do aggregation in mongodb [%(default)s]')

	parser.add_argument('-ar', action='store_true', dest='aggregation_redis', default=False,
	                    help='do aggregation in redis [%(default)s]')



	parser.add_argument('--version', action='version', version='%(prog)s 0.1')


	options = parser.parse_args()

	thr_mongo = Mongo()
	thr_redis = Redis()


	if options.insert_mongo:
		throughput_src = thr_mongo.init_mongo()
		throughput_src.drop()
		thr_mongo.insert_timestamp_values(throughput_src, amount_ids=options.uids, delay_sec=options.delay)


	if options.aggregation_mongo:
		throughput_agg = thr_mongo.init_mongo(collection_name='python_throughput_agg')
		throughput_agg.drop()
		thr_mongo.mongo_aggregator(throughput_src, throughput_agg)


	if options.insert_redis:
		redis_connection= thr_redis.init_redis()
		thr_redis.flush_pattern(redis_connection, 'src*')
		thr_redis.insert_timestamp_values_redis(redis_connection)




if __name__ == "__main__":
	main()
