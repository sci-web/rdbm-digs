# -*- coding: utf-8 -*-
import config
import sys, time, re, getopt
from DBsql import DB
from dataservices import query_execution, timeit
from vzdia import VZ
import argparse

# python DATAroll.py --db1 vaxiom --sql1 "fk_list.sql" --nc=2 | grep "| appointments"

@timeit
def diagrams_generation(**kwargs):
  # kwargs['query'] = kwargs['dia']
  method = kwargs['query'](kwargs['tables'], kwargs['level'])
  return method


@timeit
def path_between(**kwargs):
  method = kwargs['query'](kwargs['tables'], kwargs['couple'])
  return method

def list_options():
  print """usage: %s --level, --way, --tables, --number, --depth, --clean, --help or -l, -w, -t, -n, -d, -c, -h
        --level,-l [number 1 or 2] (default: 1) 
          to generate PNG images of all tables along with the tables connected to a given table via foreign keys directly (1) or directly + next such connections (2)
        --way, -w [number 1 or -1] (default: 0)
          the direction of relationship: 
          1: for child to parent (from FK to parent column/table);
          -1: for parent to child
          0: draws nothing, outputs db basic statistics
        --tables, -t [two comma separated tables] 
          - draws full relationship path(s) between two given tables and outputs basic statistics on the database
        --number, -n [number] (default: 10)
          no greater than this maximum number of joints in the computed paths between given tables
        --depth, -d [depth] (default: 10)
          this value is opting for clustering, by default it assumes that a cluster's center has no less than 10 connections 
          (with parents and children tables) , the less is this number, the harder is load for the clusters graph calculations
        --clean, -c [cleaning a full DB snapshot ] (default: 0)
          if set 0, then draws full schema, 
          if set 1 — removes the annotations from cluster core tables, 
          if set 2 — removes the most connected table from the schema (to make other connections more perceptible)"""%sys.argv[0]


def main(argv):
  level = 1
  way = 0
  couple = []
  length = 10
  depth = 10
  clean = 0

  try:
    opts, arg = getopt.getopt(argv, "l:w:t:n:d:c:h:", ["level=", "way=", "tables=", "number=", "clean=", "help="])
  except getopt.GetoptError:
    # automatic execution:
    print "options are incorrect, should be: --level, --way, --tables, --number, --depth, --clean, --help or -l, -w, -t, -n, -d, -c, -h"
    list_options()
    sys.exit(2)
  # execution by input arguments:
  for opt, arg in opts:
    if opt in ("-h", "--help"):
      list_options()
      sys.exit(2)
    if opt in ("-l", "--level"):
      level = int(arg)
    if opt in ("-w", "--way"):
      way = int(arg)
    if opt in ("-t", "--tables"):
      couple = [e.strip() for e in arg.split(",")]
    if opt in ("-n", "--number"):
      length = int(arg)
    if opt in ("-d", "--depth"):
      depth = int(arg)
      if depth < 6:
        print "depth should be no less than", 6, "- setting default (10)"
        depth = 10
    if opt in ("-c", "--clean"):
      clean = int(arg)


  if level > 2: 
    print "too high level, level must be no more than 3"
    sys.exit(2)
  if way == 0 and len(couple) == 0:
    print "way of relationship propagation must be equal 1 or -1"
    sys.exit(2)

  fk_data = query_execution(query=DB("vaxiom", 0).sql_from_the_file, sql="fk_list.sql")
  tables = {}
  b_tables = {}
  for item in fk_data:
    if not re.search("^act_", item[0]):
      t_c, c_c = item[0].split(".")
      t_p, c_p = item[1].split(".")
      try:
        tables[t_c].update({c_c: [t_p, c_p]})
      except:
        tables[t_c] = {c_c: [t_p, c_p]}
      # to form unique dictionary keys: join parent column with child table through the arrow, then split in VZ.table_styling() 
      try:
        b_tables[t_p].update({u" \u2190 ".join([c_p, t_c]): [t_c, c_c]})
      except:
        b_tables[t_p] = {u" \u2190 ".join([c_p, t_c]): [t_c, c_c]}

  level_names = {1 : "1st_level_ERs/", 2: "2nd_level_ERs/"}        
  if way < 0:
    tables = b_tables
    level_names = {1 : "1st_level_ERs_back/", 2: "2nd_level_ERs_back/"}

  if len(couple) > 0 and way == 0:
    path = config.PDFPATH
    print "statistical data and calculating path(s) between", couple
    if len(couple) == 2:
      VZ(path, 0).paths_draw(tables, b_tables, couple, length, depth, clean)
    else:
      print "-t, --table option requires 2 tables, but has", len(couple)
  if way == 0 and len(couple) == 0:
    print "no tables to find connection path, no direction to draw FK connection"
  if way != 0:
    path = config.PNGPATH + level_names[level]
    print "writing diagrams into " + path
    diagrams_generation(query=VZ(path, way).diagram_draw, tables=tables, level=level)


if __name__ == '__main__':
    main(sys.argv[1:])
