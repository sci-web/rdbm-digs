import config
import sys, time, re, getopt
from DBsql import DB
from DATAroll import query_execution, timeit


def main(argv):
    db_source = "vaxiom"
    # db_target = "vaxiom"
    db_target = "rockdental"
    DB(db_target, 0).sql_from_the_line("SET SESSION SQL_LOG_BIN=0;")
    
    fk_data_orgs = DB(db_source, 0).sql_from_the_file("fk_list_with_names_to_orgs.sql")
    fk_data = DB(db_source, 0).sql_from_the_file("fk_list_with_names.sql")

    show_tables = "show tables"
    source_tables = DB(db_source, 0).sql_from_the_line(show_tables)
    target_tables = DB(db_target, 0).sql_from_the_line(show_tables)


    print "performing records check:"
    if len(source_tables) != len(target_tables):
        print "tables aren't the same:"
        print db_source, "tables count:", str(len(source_tables))
        print db_target, "tables count:", str(len(target_tables))
        print "exit"
        sys.exit(2)

    DB(db_target, 0).sql_from_the_line("SET FOREIGN_KEY_CHECKS=0;")

    for source_t, target_t in zip(source_tables, target_tables):
        count_records = "select count(*) from " + source_t[0]
        source_t_records = DB(db_source, 0).sql_from_the_line(count_records)
        target_t_records = DB(db_target, 0).sql_from_the_line(count_records)
        if source_t_records[0][0] != target_t_records[0][0]:
            print source_t_records[0][0], "!=", target_t_records[0][0], "for", source_t[0]
            # sys.exit(2)

    fk_s_to_tbl = {}
    fk_s_to_refs = {}

    # NO NEED TO DROP FK AS THEY ARE NOT IN RESTORED db_target ANYMORE
    for item in fk_data:
        fk_s_to_tbl[item[0]] = item[1]
        fk_s_to_refs[item[0]] = item[2]
        this_t, this_c = item[1].split(".")
        sql = "ALTER TABLE " + this_t + " DROP FOREIGN KEY " + item[0]
        try:
            query_execution(query=DB(db_target, 0).sql_from_the_line, sql=sql)
        except Exception, e:
            print "doing this: " + sql
            print e

    fk_s_to_tbl_orgs = {}
    for item in fk_data_orgs:
        fk_s_to_tbl_orgs[item[0]] = item[1]

    num = 0
    print "starting deleting all records referenced to sys$organizations"
    for fk, tbl in fk_s_to_tbl_orgs.iteritems():
        this_t, this_c = tbl.split(".")
        ref_t, ref_c = fk_s_to_refs[fk].split(".")
        if this_t != "sys$organizations" and this_c != "parent_id" and ref_t != "sys$organizations" and ref_c != "id":
            sql_d = "DELETE FROM " + this_t + " WHERE " + this_c + "!=4 AND " + this_c + "!=51 AND " + this_c + "!=52 AND " + this_c + "!=53 AND " + this_c + "!=54 AND " + this_c + "!=55 AND " + this_c + "!=56 AND " + this_c + "!=57 AND " + this_c + "!=20582908 AND "+ this_c + "!=1574876422 AND "+ this_c + "!=34232731505 AND "+ this_c + "!=34232738277 AND "+ this_c + "!=36201581354"
        else:
            sql_d = "DELETE FROM " + this_t + " WHERE " + this_c + "!=4 AND " + this_c + "!=51 AND " + this_c + "!=52 AND " + this_c + "!=53 AND " + this_c + "!=54 AND " + this_c + "!=55 AND " + this_c + "!=56 AND " + this_c + "!=57 AND " + this_c + "!=20582908 AND "+ this_c + "!=1574876422 AND "+ this_c + "!=34232731505 AND "+ this_c + "!=34232738277 AND "+ this_c + "!=36201581354 AND " + this_c + "!=3"
            if this_c == 3:
                print "The record for " + ".".join(this_t,this_c) + "=3 self referenced to " + ".".join(tref_t,ref_c) + " IS KEPT"
        try:
            # changes = 1 to commit deletion
            query_execution(query=DB(db_target, 0).sql_from_the_line, sql=sql_d, changes=1)
        except Exception, e:
            print "doing this: " + sql_d
            print e
        num += 1
    print "records from " + str(num) + " tables are deleted"

    DB(db_target, 0).sql_from_the_line("SET FOREIGN_KEY_CHECKS=1;")


    for fk, tbl in fk_s_to_tbl.iteritems():
        this_t, this_c = tbl.split(".")
        ref_t, ref_c = fk_s_to_refs[fk].split(".")
        sql_a = "ALTER TABLE " + this_t + " ADD CONSTRAINT " + fk + " FOREIGN KEY (" + this_c + ") REFERENCES " + ref_t + "(" + ref_c + ")"
        try:
            query_execution(query=DB(db_target, 0).sql_from_the_line, sql=sql_a)
        except Exception, e:
            print "doing this: " + sql_a
            print e            

if __name__ == '__main__':
    main(sys.argv[1:])
