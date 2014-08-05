import redis
import random
from Core import Core



class Redis(Core):


	def init_redis(self):
		redis_connect = redis.Redis()
		return redis_connect



	def flush_pattern(self, redis_connection, pattern):
		d_keys = redis_connection.keys(pattern)
		for k in d_keys:
			redis_connection.delete(k)



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




	def redis_aggregator(self, redis_connect, hash_prefix_src='src', hash_prefix_agg='agg'):
		src_keys = redis_connect.keys("""{}:{}""".format(hash_prefix_src,'*'))
		for id_string in src_keys:
			doc = redis_connect.hgetall(id_string)
			for ts in doc.keys():
				weekday, hour = self.timestamp_lookup(int(ts))
				timeslot = """{}_{}""".format(self.lookup_timeslot_day(weekday), hour)
				id = id_string.split("""{}:""".format(hash_prefix_src))[1]
				redis_connect.hincrby("""{}:{}""".format(hash_prefix_agg,id),timeslot,1)
				

if __name__ ==  "__main__":
	rd = Redis()
	r = rd.init_redis()
	rd.flush_pattern(r, 'agg*')