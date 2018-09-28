#!/usr/bin/python
import config
import MySQLdb as mdb
import sys, re, inspect
from warnings import filterwarnings
"""
Class to query MySQL DB
"""

class DB(object):
  def __init__(self, db, w):
    db = config.DB['dbname'] if db == 0 else db
    try:
      self.con = mdb.connect(config.DB['host'], config.DB['user'], config.DB['password'], db)
      self.cur = self.con.cursor()
      if w == 0:
        filterwarnings('ignore', category = mdb.Warning)
    except mdb.Error, e:
      print "Error %d: %s" % (e.args[0],e.args[1])
      # sys.exit(1)
    # and connection closes on the MySQLdb side

  def version(self):
    return "Database version : %s" % self.q_fetch_one("SELECT VERSION()")

  def detail_payments_sql(self):
    name = inspect.stack()[0][3]
    q = self.readSQL( self.sql_file(name), 'LIMIT 5' ) # 'WHERE pa.human_id=13688'
    return self.q_fetch_all(q)

  def detail_transactions_sql(self):
    name = inspect.stack()[0][3]
    q = self.readSQL( self.sql_file(name), 'WHERE pa.human_id=13688', 0)
    return self.q_fetch_all(q)
    
  def sql_from_the_line(self, line):
    return self.q_fetch_all(line)

  def sql_from_the_line_no_commit(self, line):
    return self.q_fetch_all_no_commit(line)

  def sql_from_the_file(self, file):
    f = file if re.search("/", file) else "".join( [config.SQLPATH, file] )
    q = self.readSQL( f, '', 0 )
    try:
      return self.q_fetch_all(q)
    except mdb.Error, e:
      print e
      # sys.exit(1)

  def sql_from_the_file_with_pattern(self, file, pattern):
    f = file if re.search("/", file) else "".join( [config.SQLPATH, file] )
    q = self.readSQL( f, pattern, 1 )
    return self.q_fetch_all(q)

  def sql_from_the_file_to_csv(self, file, csv):
    # csv = "/var/lib/mysql-files/test_ex.csv"
    f = file if re.search("/", file) else "".join( [config.SQLPATH, file] )
    try:
      q = self.readSQL( f, "into outfile '"+ csv+"' fields terminated by ', ' escaped by '' enclosed by '\"' lines terminated by '\r\n' ", 1)
    except:
      return "could not form the SQL"
    try: 
      return self.q_fetch_all(q)
    except mdb.Error, e:
      print e
      sys.exit(1)

# reading SQL from file
  def readSQL(self, sql, params, replace_pattern):
    try:
      with open(sql, "r") as f:
        fc = f.read()
        if replace_pattern == 1 and re.search("[$$]", fc):
          return fc.replace("[$$]", params)
        else: 
          return "%s %s;" % (fc, params)
    except Exception, e:
      print "Ooops! missed sql?", e
      sys.exit(1)
# fetch query results or return error (log error)
  def q_fetch_one(self, q):
    self.cur.execute(q)
    self.con.commit()
    try:
      return self.cur.fetchone()
    except mdb.Error, e:
      print e

  def q_fetch_all_no_commit(self, q):
      self.cur.execute(q)
      try:
        return self.cur.fetchall()
      except mdb.Error, e:
        return e
        # sys.exit(1)

  def q_fetch_all(self, q):
    self.cur.execute(q)
    self.con.commit()
    try:
      return self.cur.fetchall()
    except mdb.Error, e:
      print e
      # sys.exit(1)

# services
  def rreplace(self, s, old, new, occurrence):
    return new.join(s.rsplit(old, occurrence))
  
  def sql_file(self, name):
    return "".join( [config.SQLPATH, self.rreplace(name, '_', '.', 1)] )

  def sql_file(self, name):
    return "".join( [config.SQLPATH, self.rreplace(name, '_', '.', 1)] ) 
