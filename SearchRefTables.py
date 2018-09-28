import config
import sys, time, re, getopt
from DBsql import DB
from dataroll import form_matrix
"""
some DB inspection
"""

def main(argv):
    db_source = "vaxiom"
    sql = "show full tables where Table_Type != 'VIEW'"
    tables = DB(db_source, 0).sql_from_the_line(sql)

    for t in tables:
        count_records = "select count(*) from " + t[0]
        source_t_records = DB(db_source, 0).sql_from_the_line(count_records)
        # ref_tables = DB(db_source, 0).sql_from_the_file_with_pattern("referenced_tables.sql", t[0])
        print "children tables for", t[0], "(1st column, FK is 2nd column)" 
        parent = form_matrix(query=DB(db_source, 0).sql_from_the_file_with_pattern, num=4, sql="referenced_tables.sql", pattern=t[0])
        sql_t = "select count(*) from " + t[0]
        cnt = DB(db_source, 0).sql_from_the_line(sql_t)
        if parent != 0:
            print "these are refs for", t[0], "with", cnt[0][0], "records"
        else:
            print "no refs for", t[0], "with", cnt[0][0], "records"
        print "parent tables for", t[0], "(3rd column) with FKs (2nd column)" 
        children = form_matrix(query=DB(db_source, 0).sql_from_the_file_with_pattern, num=4, sql="parent_tables.sql", pattern=t[0])
        if children != 0:
            print "these are parents for", t[0], "with", cnt[0][0], "children records"
        else:
            print "no parents for", t[0], "with", cnt[0][0], "children records"


if __name__ == '__main__':
    main(sys.argv[1:])
