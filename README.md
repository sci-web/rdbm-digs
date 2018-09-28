**MySQL data digging and vizualization tools**

* All necessary installations commands are in needed_installs.txt
* This DB-talking code obeys the following convention: *all queries are to be kept in one place*, `DBsql.py` manages all the queries

---

## How it works

looking from the main directory:

1. ./sql/ — all *.sql are to be put here, they can be full SQLs or partial with params appended through the var param in this way (see `DBsql.py`):
`q = self.readSQL(self.sql_file(name), 'WHERE pa.human_id=13688')`

2. query can be put also directly as a string parameter (see 'DBsql.py'):
`return "Database version : %s" % self.q_fetch_one("SELECT VERSION()")`

3. config.py is a config file, where DB connector's parameters and the path to *.sql files are readed from

4. all *.sql files have conventional names according to the method where they are called to: i.e.
`DB('').detail_payments_sql()` from anywhere calls `def detail_payments_sql(self)` in DBsql.py which uses `detail_payments.sql` from `config.SQLPATH`

5. entity-relationships discovery and visualization (example of usage):

`$ python schemaviz.py -l 2 -w 1`
`$ python schemaviz.py -t table_A,table_B -n5 -d8 -c2`
`$ python schemaviz.py -h` — lists options

6. the digger:
`$ python dataroll.py -h` — lists options

7. `dataroll.py` can be launched with params for one DB or to compare two queries from the same or different DBs:
`:/axpm/data-mine# python dataroll.py --db1="1st DBNAME" --ln1="1st_SQL_QUERY"  --db2="2nd DBNAME" --ln2="2nd_SQL_QUERY" --nc=number-of-columns-in-output``
---


