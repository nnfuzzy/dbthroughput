#!/usr/bin/env python

__author__ = 'nnfuzzy'

import datetime
import time
import pymongo
import random
import argparse
import redis
from profilehooks import profile


class Timer(object):
	def __enter__(self):
		self.__start = time.time()

	def __exit__(self, type, value, traceback):
		# Error handling here
		self.__finish = time.time()

	def duration_in_seconds(self):
		return self.__finish - self.__start


class Throughput(object):

	def init_mongo(self, db_name='throughput', collection_name='python_throughput_src'):
		try:
			c = pymongo.Connection()
			db= c[db_name]
			collection=db[collection_name]
			collection.drop()
		except Exception, e:
			print "Can't connect to mongodb!?"
		return collection


	def init_redis(self):
		redis_connect = redis.Redis()
		return redis_connect


	def datetime2timestamp(self, datetime_str='2014-01-01'):
		timestamp = int(time.mktime(datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").timetuple()))
		return timestamp


	def insert_timestamp_values(self, collection, datetime_start='2013-01-01 00:00:00',
	                            datetime_end='2014-01-01 00:00:00',
	                            amount_ids=1000,
	                            delay_sec=200,
	                            drop=False):
		if drop:
			collection.drop()

		ts_start = self.datetime2timestamp(datetime_start)
		ts_end = self.datetime2timestamp(datetime_end)

		while ts_start < ts_end:
			collection.insert({'id':random.randint(1, amount_ids), 'ts': ts_start})
			ts_start += delay_sec




	def lookup_timeslot_day(self, day):
		""" Recode number of the day into string repr.."""
		d = {0: 'mon', 1: 'tue', 2: 'wed', 3: 'thu', 4: 'fri',
		     5: 'sat', 6: 'sun'}
		return d.get(day)



	def timestamp_lookup(self, tstamp):
		""" Lookup from timestamp to day in the week and hour """
		if isinstance(tstamp, int):
			tstamp_ = float(tstamp)
		else:
			tstamp_ = tstamp
		t = datetime.datetime.fromtimestamp(tstamp_)
		d = (t.weekday(), t.hour)
		return d



	def insert_timestamp_values_redis(self, redis_connect, hash_prefix='src', datetime_start='2013-01-01 00:00:00',
	                            datetime_end='2014-01-01 00:00:00',
	                            amount_ids=1000,
	                            delay_sec=200,
	                            drop=False):

		""" ts_start = 1356994800  , ts_end=1388530800 """

		if drop:
			keys2delete = redis_connect.keys("""{}:{}""".format(hash_prefix,'*'))
			for h in keys2delete:
				redis_connect(h)

		ts_start = self.datetime2timestamp(datetime_start)
		ts_end = self.datetime2timestamp(datetime_end)

		while ts_start < ts_end:
			uid = random.randint(1, amount_ids)
			#key in hash is ts  , value for now only None. But could be more
			#in the future , i.e. smth like a json with k:v => transactions_data
			redis_connect.hset("""{}:{}""".format(hash_prefix, uid),ts_start,None)
			ts_start += delay_sec


	def mongo_updater(self, src_collection, agg_collection):
			agg_collection.ensure_index('id')
			cursor = src_collection.find()
			for doc in cursor:
				id, ts = doc.get('id'), doc.get('ts')
				weekday, hour = self.timestamp_lookup(ts)
				timeslot = """{}_{}""".format(self.lookup_timeslot_day(weekday), hour)
				agg_collection.update({'id': id}, {'$inc':{timeslot: 1}}, upsert=True)


	def redis_update(self, redis_connect, hash_prefix_src='src', hash_prefix_agg='agg'):
		src_keys = redis_connect.keys("""{}:{}""".format(hash_prefix_src,'*'))
		for id_string in src_keys:
			doc = redis_connect.hgetall(id_string)
			for ts in doc.keys():
				weekday, hour = self.timestamp_lookup(int(ts))
				timeslot = """{}_{}""".format(self.lookup_timeslot_day(weekday), hour)
				id = id_string.split("""{}:""".format(hash_prefix_src))[1]
				redis_connect.hincrby("""{}:{}""".format(hash_prefix_agg,id),timeslot,1)

	def main(self):
		parser = argparse.ArgumentParser(description="Throughput", add_help=True)
		parser.add_argument('-d', action='store', dest='delay', type=int, default=200,
		                    help='delay in seconds - density of data [%(default)s]')
		parser.add_argument('-uids', action='store', dest='uids', default=1000, type=int,
		                    help='number of uids [%(default)s]')

		parser.add_argument('-i', action='store_true', dest='insert', default=False,
		                    help='do inserts [%(default)s]')

		parser.add_argument('-ir', action='store_true', dest='insert_redis', default=False,
		                    help='do inserts into redis[%(default)s]')


		parser.add_argument('-a', action='store_true', dest='aggregation', default=False,
		                    help='do aggregation [%(default)s]')

		parser.add_argument('--version', action='version', version='%(prog)s 0.2')


		options = parser.parse_args()

		thr = Throughput()
		throughput_src = thr.init_mongo()
		throughput_agg = thr.init_mongo(collection_name='python_throughput_agg')

		if options.insert:
			throughput_src.drop()
			start_inserts = datetime.datetime.now()
			thr.insert_timestamp_values(throughput_src, amount_ids=options.uids, delay_sec=options.delay)
			stop_inserts = datetime.datetime.now()
			print str(stop_inserts - start_inserts)

		if options.aggregation:
			throughput_agg.drop()
			start_aggregation = datetime.datetime.now()
			thr.mongo_updater(throughput_src, throughput_agg)
			stop_aggregation = datetime.datetime.now()
			print str(stop_aggregation - start_aggregation)


		if options.insert_redis:
			redis_connect = thr.init_redis()
			start_inserts = datetime.datetime.now()
			thr.insert_timestamp_values_redis(redis_connect)
			stop_inserts = datetime.datetime.now()
			print str(stop_inserts - start_inserts)


if __name__ == "__main__":
	thr = Throughput()
	r = thr.init_redis()
	thr.redis_update(r)
	#thr.main()

