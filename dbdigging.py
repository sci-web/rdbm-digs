import config
import sys, time, re, getopt
from DBsql import DB
from DATAroll import query_execution, timeit


def main(argv):
    fk_data_orgs = query_execution(query=DB("vaxiom", 0).sql_from_the_file, sql="fk_list_with_names_to_orgs.sql")
    fk_data = query_execution(query=DB("vaxiom", 0).sql_from_the_file, sql="fk_list_with_names.sql")
    fk_s_to_tbl = {}
    fk_s_to_refs = {}
    for item in fk_data:
        fk_s_to_tbl[item[0]] = item[1]
        fk_s_to_refs[item[0]] = item[2]

    fk_back_refs = {}
    fk_refs = {}
    for fk, tbl in fk_s_to_tbl.iteritems():
        this_t, this_c = tbl.split(".")
        ref_t, ref_c = fk_s_to_refs[fk].split(".")
        fk_back_refs[ref_t] = this_t
        fk_refs[this_t] = ref_t	
    j = 0
    l = 0
    n = 0
    k = 0
    for ta in query_execution(query=DB("vaxiom", 0).sql_from_the_line, sql="SHOW TABLES"):
        ta = ta[0]
        try:
            print fk_back_refs[ta], fk_refs[ta]
            n += 1
        except:
        	pass
        try:
            print fk_back_refs[ta] 
            k += 1
        except:
        	pass 
        try:
            print fk_refs[ta]
            j += 1
        except:
			pass

    print j, l, n, k



if __name__ == '__main__':
    main(sys.argv[1:])