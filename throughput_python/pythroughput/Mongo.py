import pymongo
import random
from  Core import Core


class Mongo(Core):

	def init_mongo(self, db_name='throughput', collection_name='python_throughput_src', drop=False):
			try:
				c = pymongo.Connection()
				db= c[db_name]
				collection=db[collection_name]
				if drop:
					collection.drop()
			except Exception, e:
				print "Can't connect to mongodb!?"
			return collection



	def insert_timestamp_values_mongo(self, collection, datetime_start='2013-01-01 00:00:00',
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



	def mongo_aggregator(self, src_collection, agg_collection):
		agg_collection.ensure_index('id')
		cursor = src_collection.find()
		for doc in cursor:
			id, ts = doc.get('id'), doc.get('ts')
			weekday, hour = self.timestamp_lookup(ts)
			timeslot = """{}_{}""".format(self.lookup_timeslot_day(weekday), hour)
			agg_collection.update({'id': id}, {'$inc':{timeslot: 1}}, upsert=True)