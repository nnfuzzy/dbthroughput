import MySQLdb
from Core import Core
from random import randint


class MySQL(Core):
    
    def initMySQL(self, host, user, passwd, db,
                  port=3006, dictcursor=False, charset='utf8'):
        
        """ Create mysql connection  """
        
        if dictcursor:
            mysql = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port,
                                    cursorclass=MySQLdb.cursors.DictCursor)
        else:
            mysql = MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, port=port)
        return mysql



    def init_mysql_table(self, mysql_connection, tablename='src', drop=True):
        cur = mysql_connection.cursor()
        
        if  drop:
            cur.execute(""" Drop table if exists {} """.format(tablename))

        if tablename == 'src':
            q = """ Create table src ( id integer(10)  , tstamp bigint(10)) ENGINE=MyISAM; """
            cur.execute(q)   
            
        else:
            q =  """ Create table agg (id integer(10) , timeslot varchar(6), cnt int(10)) ENGINE=MyISAM; """
            cur.execute(q)
            cur.execute(""" Create UNIQUE INDEX agg_ix_1 on agg (id,timeslot) """)
        
        return
    

    def insert_timestamp_values_mysql(self, mysql_connection, datetime_start='2013-01-01 00:00:00',
                                datetime_end='2014-01-01 00:00:00',
                                amount_ids=1000,
                                delay_sec=200,
                                tablename = 'src'):

	    ts_start = self.datetime2timestamp(datetime_start)
	    ts_end = self.datetime2timestamp(datetime_end)
	    cur =mysql_connection.cursor()
	    
	    while ts_start < ts_end:
		q = """ Insert into {} (id,tstamp) VALUES (%s, %s) """.format(tablename)  %  (randint(1,amount_ids) , ts_start) 
		cur.execute(q)
		ts_start += delay_sec
		
	    
    def myql_aggregator(self, mysql_connection, src_table='src', agg_table='agg'):
	cur = mysql_connection.cursor()
	q = """ Select id, tstamp from {} """.format(src_table)
	cur.execute(q)
	for rec in cur.fetchall():
		id, ts , cnt = rec[0], rec[1], 1
		weekday, hour = self.timestamp_lookup(ts)
		timeslot = """{}_{}""".format(self.lookup_timeslot_day(weekday), hour)
		#u = """ Update{} set  timeslot=%s  , cnt = cnt +1  where id = %s """.format(agg_table)  %  (timeslot, id)
		u = """ Insert into {} (id,timeslot,cnt) VALUES (%s, '%s', %s)  ON DUPLICATE KEY UPDATE cnt = cnt +1 """.format(agg_table) % (id,timeslot,cnt)
		cur.execute(u)
	return
    
    
    
    
    