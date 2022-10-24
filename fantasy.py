#FantasyFootball 
#imports
import sys
import csv
import sqlite3

class Player:
    def __init__(self, name) -> None:
        self.week = ''
        self.name = name
        self.team = ''
        self.against = ''
        self.pos = ''
        self.p_yards = ''
        self.p_tds = ''
        self.p_int = ''
        self.ru_yards = ''
        self.ru_tds = ''
        self.re_rec = ''
        self.re_yards = ''
        self.re_tds = ''
        self.ret_td = ''
        self.m_fumtd = ''
        self.m_2pt = ''
        self.fum_lost = ''
        self.fan_points = ''

    def __repr__(self) -> str:
        return repr(self.__dict__)


#parse csv data
def parse_file(reader, weeks):
      next(reader)
      for row in reader:
        week = row[0]
        name = row[1].strip()
        if week not in weeks:
          weeks[week] = []
        ent = Player(name)
        weeks[week].append(ent)

        ent.team = row[2]
        ent.against = row[3]
        ent.pos = row[4]
        ent.p_yards = row[5].replace('-', '0')
        ent.p_tds = row[6].replace('-', '0')
        ent.p_int = row[7].replace('-', '0')
        ent.ru_yards = row[8].replace('-', '0')
        ent.ru_tds = row[9].replace('-', '0')
        ent.re_rec = row[10].replace('-', '0')
        ent.re_yards = row[11].replace('-', '0')
        ent.re_tds = row[12].replace('-', '0')
        ent.ret_td = row[13].replace('-', '0')
        ent.m_fumtd = row[14].replace('-', '0')
        ent.m_2pt = row[15].replace('-', '0')
        ent.fum_lost = row[16].replace('-', '0')
        ent.fan_points = row[17].replace('-', '0')

def print_players(weeks):
  for week, players in weeks.items():
    for ent in players:
      print(week + ', ' + ent.name + ', ' + ent.pos + ', ' + ent.re_tds + ', ' + ent.fan_points)

def create_sqlite_table(weeks):
#create query
  table_query = '''CREATE TABLE if not Exists fantasy_scores
  (playerid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, Week INTEGER, Name VARCHAR, Team VARCHAR, 
  Against VARCHAR, Position VARCHAR, Passing_yards INTEGER, Passing_tds INTEGER, Passing_int INTEGER, 
  Rushing_yards INTEGER, Rushing_tds, Receiving_rec INTEGER, Receiving_yards INTEGER, Receiving_tds INTEGER, 
  Return td INTEGER, Misc_fumtd INTEGER, Misc_2pt INTEGER, Fum_lost INTEGER, Fantasy_points DOUBLE)'''

  #create database
  connection = sqlite3.connect('fantasy_football')
  cursor = connection.cursor()
  #create table
  cursor.execute(table_query)

  #create insert query
  #insertquery = '''INSERT INTO fantasy_scores VALUES 
  #('NULL', '{week}', '{name}', '{team}', '{against}', '{pos}', '{p_yards}', '{p_tds}', '{p_int}', '{ru_yards}', '{ru_tds}', 
  #'{re_rec}', '{re_yards}', '{re_tds}', '{ret_td}', '{m_fumtd}', '{m_2pt}', '{fum_lost}', '{fan_points}')'''

  insertquery = '''INSERT INTO fantasy_scores VALUES 
  ('NULL', '{ent.week}', '{ent.name}', '{ent.team}', '{ent.against}', '{ent.pos}', '{ent.p_yards}', '{ent.p_tds}', '{ent.p_int}', 
  '{ent.ru_yards}', '{ent.ru_tds}', '{ent.re_rec}', '{ent.re_yards}', '{ent.re_tds}', '{ent.ret_td}', '{ent.m_fumtd}', '{ent.m_2pt}',
  '{ent.fum_lost}', '{ent.fan_points}')'''
  #or
  #'''INSERT INTO fantasy_scores VALUES 
  #('NULL', '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', 
  #'{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}')'''
  #.format(ent.week, ent.name, ent.team, ent.against, ent.pos, ent.p_yards, ent.p_tds, ent.p_int, ent.ru_yards, ent.ru_tds,
  # ent.re_rec, ent.re_yards, ent.re_tds, ent.ret_td, ent.m_fumtd, ent.m_2pt, ent.fum_lost, ent.fan_points)

  #execute query
  cursor.execute(insertquery)
  #view all the information from the csv
  for row in cursor.execute('SELECT * FROM fantasy_scores'):
      print(row)

  select_all = "SELECT * FROM fantasy_scores"
  rows = cursor.execute(select_all.fetchall())
  # Output to the console screen
  for r in rows:
      print(r)

  #commit changes
  connection.commit()
  #close connection
  connection.close()


weeks = {}

#read the csv
for filename in sys.argv[1:]:
    csvfile = open(filename, 'r')
    reader = csv.reader(csvfile, delimiter=',')
    parse_file(reader, weeks)

print_players(weeks)
create_sqlite_table(weeks)
