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
        player = Player(name)
        weeks[week].append(player)

        player.team = row[2]
        player.against = row[3]
        player.pos = row[4]
        player.p_yards = row[5].replace('-', '0')
        player.p_tds = row[6].replace('-', '0')
        player.p_int = row[7].replace('-', '0')
        player.ru_yards = row[8].replace('-', '0')
        player.ru_tds = row[9].replace('-', '0')
        player.re_rec = row[10].replace('-', '0')
        player.re_yards = row[11].replace('-', '0')
        player.re_tds = row[12].replace('-', '0')
        player.ret_td = row[13].replace('-', '0')
        player.m_fumtd = row[14].replace('-', '0')
        player.m_2pt = row[15].replace('-', '0')
        player.fum_lost = row[16].replace('-', '0')
        player.fan_points = row[17].replace('-', '0')

def print_players(weeks):
  for week, players in weeks.items():
    for player in players:
      print(week + ', ' + player.name + ', ' + player.pos + ', ' + player.re_tds + ', ' + player.fan_points)

def create_sqlite_table(weeks):
    for week, players in weeks.items():
        for player in players:
            #create query
            table_query = '''CREATE TABLE if not Exists fantasy_scores
            (playerid INTEGER PRIMARY KEY AUTOINCREMENT, Week INTEGER, Name VARCHAR, Team VARCHAR, 
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
            ('NULL', {week}, '{player.name}', '{player.team}', '{player.against}', '{player.pos}', {player.p_yards}, {player.p_tds}, {player.p_int}, 
            {player.ru_yards}, {player.ru_tds}, {player.re_rec}, {player.re_yards}, {player.re_tds}, {player.ret_td}, {player.m_fumtd}, {player.m_2pt},
            {player.fum_lost}, {player.fan_points})'''
            #or
            #'''INSERT INTO fantasy_scores VALUES 
            #('NULL', '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', 
            #'{10}', '{11}', '{12}', '{13}', '{14}', '{15}', '{16}', '{17}')'''
            #.format(week, player.name, player.team, player.against, player.pos, player.p_yards, player.p_tds, player.p_int, player.ru_yards, player.ru_tds,
            # player.re_rec, player.re_yards, player.re_tds, player.ret_td, player.m_fumtd, player.m_2pt, player.fum_lost, player.fan_points)

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
#create_sqlite_table(weeks)
