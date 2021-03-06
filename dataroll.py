import config
import sys, time, re, getopt
import pytablewriter
from DBsql import DB
from dataservices import query_execution, timeit


def table_output(matrix, warning, header, t_name):
  writer = pytablewriter.MarkdownTableWriter()
  writer.table_name = t_name
  writer.header_list = list(range(0, len(header)))
  writer.value_matrix = matrix
  writer.margin = 1
  writer.write_table()  
  footer = pytablewriter.MarkdownTableWriter()
  footer.table_name = warning
  footer.value_matrix = tuple([[]])
  footer.margin = 0
  footer.write_table()  
  
def form_matrix(**kwargs):
    matrix = []
    result = query_execution(**kwargs)
    warning = "";
    header = ""
    if len(result) > 0:
      header = result[0]
      n = 0
      for l in result:
        row = []
        [row.append(str(i)) for i in l[0:len(l)]]
        matrix.append(tuple(row))
        n += 1
        if n > 1000:
          matrix.append(tuple([]))
          warning = "first 1000 records are shown: " + "\x1b[6;30;42m" + "more than 1000 records to display in STDOUT, try limit their number" + "\x1b[0m"
          break
      return table_output(matrix, warning, header, "query output:") 
    else:
      print "\n0 records are found: " + "\x1b[6;30;42m" + "perhaps you need to modify your SQL" + "\x1b[0m\n"


def list_options():
  print """usage: %s  --ln1, --ln2, --sql1, --sql2, --db1, --db2, --output, --pattern --help or -l, -m, -s, -t, -d, -b, -o, -p, -h
          example: 
          $ python dataroll.py --db1="1st DBNAME" --ln1="1st_SQL_QUERY"  --db2="2nd DBNAME" --ln2="2nd_SQL_QUERY" 
        --ln1,-l  
          1st query (one line of SQL)
        --ln2,-m
          2nd query (one line of SQL)
        --sql1, -s 
          1st SQL query from this file in sql/
        --sql2, -t
          2nd SQL query from this file in sql/
        --db1, -d
          1st database name
        --db2, -b
          2nd database name
        --output, -o
          output csv file with extracted records
        --pattern, -p
          pattern to be appended to a query"""%sys.argv[0]

    
def main(argv): 
  
  db1 = 'vaxiom'       
  db2 = 'vaxiom_o'
  output = ""
  pattern = ""
  try:
    opts, arg = getopt.getopt(argv, "l:m:s:t:d:b:o:p:h", ["ln1=", "ln2=", "sql1=", "sql2=",  "db1=", "db2=", "output=", "pattern=", "help=="])
  except getopt.GetoptError, e:
    print e
    print "options are incorrect, should be: --ln1, --ln2, --sql1, --sql2, --db1, --db2, --output, --pattern"
    sys.exit(2)
  # execution by input arguments:
  if len(opts) == 0:
    print "options are wrong, should be: --ln1, --ln2, --sql1, --sql2, --db1, --db2, --output, ---pattern or -l, -m, -s, -t, -d, -b, -o, -p, -h"
    list_options()
    sys.exit(2)

  for opt, arg in opts:
    if opt in ("-h", "--help"):
      list_options()
      sys.exit(2)
    if opt in ("-d", "--db1"):
      db1 = arg
    if opt in ("-b", "--db2"):
      db2 = arg

  for opt, arg in opts:
    if opt in ("-o", "--output"):
      output = arg

  for opt, arg in opts:
    if opt in ("-p", "--pattern"):
      pattern = arg

  for opt, arg in opts:  
    if opt in ("-l", "--ln1"):
      print "sql: ", arg
      form_matrix(query=DB(db1, 0).sql_from_the_line, sql=arg)
    elif opt in ("-s", "--sql1"):
      if output == "":
        if pattern == "":
          form_matrix(query=DB(db1, 0).sql_from_the_file, sql=arg)
        else:
          form_matrix(query=DB(db1, 0).sql_from_the_file_with_pattern, sql=arg, pattern=pattern)
      else:
        query_execution(query=DB(db1, 0).sql_from_the_file_to_csv, sql=arg, pattern=output)
    if opt in ("-m", "--ln2"):
      form_matrix(query=DB(db2, 0).sql_from_the_line, sql=arg)
    elif opt in ("-t", "--sql2"):
      form_matrix(query=DB(db2, 0).sql_from_the_file, sql=arg)

  # if (len(opts) == 0):  
  #   form_matrix(query=DB(db1, 0).detail_transactions_sql, num=column_num, sql='')
  #   form_matrix(query=DB(db1, 0).detail_payments_sql, sql='')
  
  print DB(0, 0).version()


if __name__ == '__main__':
    main(sys.argv[1:])
