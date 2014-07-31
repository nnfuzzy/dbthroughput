#!/usr/bin/env python

import time
import datetime
import random
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref


engine = create_engine("foundationdb+psycopg2://@localhost:15432/")
Base = declarative_base()


class Transaction(Base):
      __tablename__ = 'trans'

      id = Column(Integer, primary_key=True)
      uid = Column(Integer)
      ts = Column(Integer)

      def __repr__(self):
         return "<Customer(uid='%s', ts='%s')>" % (
                              self.uid, self.ts)


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()



def datetime2timestamp(datetime_str='2014-01-01'):
	timestamp = int(time.mktime(datetime.datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S").timetuple()))
	return timestamp


def insert_timestamp_values(datetime_start='2013-01-01 00:00:00',
                            datetime_end='2014-01-01 00:00:00',
                            amount_ids=1000,
                            delay_sec=200,
                            drop=False):

	ts_start = datetime2timestamp(datetime_start)
	ts_end = datetime2timestamp(datetime_end)

	while ts_start < ts_end:
		add_src_data = Transaction(uid = random.randint(1, amount_ids), ts = ts_start)
		session.add(add_src_data)
		session.commit()
		ts_start += delay_sec



start_inserts = datetime.datetime.now()
insert_timestamp_values()
stop_inserts = datetime.datetime.now()
print str(stop_inserts - start_inserts)
