import sqlite3

class Start(object):
  con = None
  cur = None
  def __init__(dat):
    con = sqlite3.connect(dat)
    cur = con.cursor()
    table_sql = "CREATE TABLE IF NOT EXISTS info (name TEXT NOT NULL UNIQUE, val TEXT NOT NULL)"
    cur.execute(table_sql)
  def set(name, data):
    in_sql = "INSERT INTO info(name, val) VALUES (?, ?)"
    cur.execute(in_sql, (name, data))
  def get(name):
    out_sql = "SELECT FROM info WHERE name=?"
    cur.execute(out_sql, (name))
    rows = cur.fetchall()
    for row in rows:
      return row
