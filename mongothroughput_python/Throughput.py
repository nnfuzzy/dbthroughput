__author__ = 'nnfuzzy'

import datetime
import time
import pymongo
import random
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

    def init_mongo(self, db_name='test', collection_name='throughput_src'):
        try:
            c = pymongo.Connection()
            db= c[db_name]
            collection=db[collection_name]
        except Exception , e:
            print "Can't connect to mongodb!?"
        return collection


    def datetime2timestamp(self, datetime_str='2014-01-01'):
        timestamp = int(time.mktime(datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").timetuple()))
        return timestamp


    def insert_timestamp_values(self, collection,
                                datetime_start='2013-01-01 00:00:00',
                                datetime_end='2014-01-01 00:00:00',
                                amount_ids=1000,
                                delay_sec=10,
                                truncate=False):
        if truncate:
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



    @profile()
    def mongo_updater(self, src_collection, agg_collection):
        cursor = src_collection.find().sort('ts', 1)
        for doc in cursor:
            id, ts = doc.get('id'), doc.get('ts')
            weekday, hour = self.timestamp_lookup(ts)
            timeslot = "{}_{}".format(self.lookup_timeslot_day(weekday), hour)
            agg_collection.update({'id':id},
                              {
                                  '$inc':{timeslot: 1}
                              }, upsert=True)



if __name__ == '__main__':
    thr = Throughput()
    throughput_src = thr.init_mongo()
    throughput_agg = thr.init_mongo(collection_name='throughput_agg')
    throughput_src.drop()
    throughput_agg.drop()
    thr.insert_timestamp_values(throughput_src,delay_sec=3600)
    thr.mongo_updater(throughput_src, throughput_agg)






