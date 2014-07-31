import time
import datetime



class Timer(object):
	def __enter__(self):
		self.__start = time.time()

	def __exit__(self, type, value, traceback):
		# Error handling here
		self.__finish = time.time()

	def duration_in_seconds(self):
		return self.__finish - self.__start


class Core(object):


	def datetime2timestamp(self, datetime_str='2014-01-01'):
			timestamp = int(time.mktime(datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").timetuple()))
			return timestamp

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
