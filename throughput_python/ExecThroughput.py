#!/usr/bin/env python

import argparse
import datetime
from pythroughput import Mongo
from pythroughput import Redis
from pythroughput import Core
from pythroughput import MySQL


def main():
	parser = argparse.ArgumentParser(description="ExecThroughput", add_help=True)
	parser.add_argument('-d', action='store', dest='delay', type=int, default=2000,
	                    help='delay in seconds - density of data [%(default)s]')
	parser.add_argument('-u', action='store', dest='uids', default=1000, type=int,
	                    help='number of uids [%(default)s]')

	parser.add_argument('-im', action='store_true', dest='insert_mongo', default=False,
	                    help='do inserts into mongodb [%(default)s]')

	parser.add_argument('-ir', action='store_true', dest='insert_redis', default=False,
	                    help='do inserts into redis[%(default)s]')

	parser.add_argument('-is', action='store_true', dest='insert_mysql', default=False,
	                    help='do inserts into mysql[%(default)s]')

	parser.add_argument('-am', action='store_true', dest='aggregation_mongo', default=False,
	                    help='do aggregation in mongodb [%(default)s]')

	parser.add_argument('-ar', action='store_true', dest='aggregation_redis', default=False,
	                    help='do aggregation in redis [%(default)s]')

	parser.add_argument('-as', action='store_true', dest='aggregation_mysql', default=False,
	                    help='do aggregation in mysql [%(default)s]')


	parser.add_argument('--version', action='version', version='%(prog)s 0.1')


	options = parser.parse_args()

	thr_mongo = Mongo()
	thr_redis = Redis()


	if options.insert_mongo:
		throughput_src = thr_mongo.init_mongo()
		throughput_src.drop()
		thr_mongo.insert_timestamp_values_mongo(throughput_src, amount_ids=options.uids, delay_sec=options.delay)


	if options.aggregation_mongo:
		throughput_src = thr_mongo.init_mongo()
		throughput_agg = thr_mongo.init_mongo(collection_name='python_throughput_agg')
		throughput_agg.drop()
		thr_mongo.mongo_aggregator(throughput_src, throughput_agg)


	if options.insert_redis:
		redis_connect= thr_redis.init_redis()
		thr_redis.flush_pattern(redis_connect, 'src*')
		thr_redis.insert_timestamp_values_redis(redis_connect, hash_prefix='src', 
		                                       datetime_start='2013-01-01 00:00:00', 
		                                       datetime_end='2014-01-01 00:00:00', 
		                                       amount_ids=options.uids, 
		                                       delay_sec=options.delay, 
		                                       drop=True)

	if options.aggregation_redis:
		redis_connect=thr_redis.init_redis()
		thr_redis.redis_aggregator(redis_connect, hash_prefix_src='src', 
		                          hash_prefix_agg='agg')


	if options.insert_mysql:
		my = MySQL()
		mysql_connection = my.initMySQL('localhost', 'dbthroughput', 'test', 'dbthroughput')
		mysql_connection.autocommit = True
		my.init_mysql_table(mysql_connection, tablename='src',  drop=True)
		my.insert_timestamp_values_mysql(mysql_connection, 
		                                datetime_start='2013-01-01 00:00:00', 
		                                datetime_end='2014-01-01 00:00:00', 
		                                amount_ids=options.uids, 
		                                delay_sec=options.delay, 
		                                tablename='src')		
		
	if options.aggregation_mysql:
		my = MySQL()
		mysql_connection = my.initMySQL('localhost', 'dbthroughput', 'test', 'dbthroughput')
		mysql_connection.autocommit = True
		my.init_mysql_table(mysql_connection, tablename='agg',  drop=True)
		my.myql_aggregator(mysql_connection, src_table='src', agg_table='agg')


if __name__ == "__main__":
	main()
