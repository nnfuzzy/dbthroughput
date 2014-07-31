import time
import datetime
import random
from Core import Core
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



class Foundation(Core):
      

      def insert_timestamp_values(self, datetime_start='2013-01-01 00:00:00',
                            datetime_end='2014-01-01 00:00:00',
                            amount_ids=1000,
                            delay_sec=200,
                            drop=False):

	    ts_start =  self.datetime2timestamp(datetime_start)
	    ts_end =self. datetime2timestamp(datetime_end)

	    self.Base.metadata.create_all(engine)
	    Session = sessionmaker(bind=engine)
	    session = Session()    

	    while ts_start < ts_end:
		    add_src_data = Transaction(uid = random.randint(1, amount_ids), ts = ts_start)
		    session.add(add_src_data)
		    session.commit()
		    ts_start += delay_sec