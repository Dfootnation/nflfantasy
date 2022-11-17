#FantasyFootball 
#imports
import sys
import csv
import sqlite3
from turtle import position        

class Player:
    def __init__(self, name) -> None:
        self.played = ''
        self.name = name
        self.team = ''
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
        self.avg = ''

class Average:
    def __init__(self, position) -> None:
        self.position = position
        self.average = ''

    def __repr__(self) -> str:
        return repr(self.__dict__)

def read_sqlite_table():
    connection = sqlite3.connect('instance/nflfantasy.sqlite')
    cursor = connection.cursor()
    #query1 = f'SELECT COUNT(DISTINCT (Week)) as Played, Name, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score WHERE Name = "{name1}" OR Name = "{name2}" GROUP BY Name LIMIT 10'
    query1 = f'SELECT COUNT(DISTINCT (Week)) as Played, Name, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score GROUP BY Name ORDER BY Fantasy_points DESC LIMIT 10'
    query2 = 'SELECT Position, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (playerid)),2) as Average FROM fantasy_score GROUP BY Position'
    cursor.execute(query1)
    player = cursor.fetchall()
    cursor.execute(query2)
    positionavg = cursor.fetchall()
    players = []
    for row in player:
        name = row[1]
        if name not in names:
          names[name] = []
        player = Player(name)
        names[name].append(player)
        player.played = row[0]
        player.team = row[2]
        player.pos = row[3]
        player.p_yards = row[4]
        player.p_tds = row[5]
        player.p_int = row[6]
        player.ru_yards = row[7]
        player.ru_tds = row[8]
        player.re_rec = row[9]
        player.re_yards = row[10]
        player.re_tds = row[11]
        player.ret_td = row[12]
        player.m_fumtd = row[13]
        player.m_2pt = row[14]
        player.fum_lost = row[15]
        player.fan_points = row[16]
        player.avg = row[17]
        players.append(row)
    avgs = []
    for row in positionavg:
        position = row[0]
        if position not in positions:
            positions[position] = []
        average = Average(position)
        positions[position].append(average)
        average.average = row[1]
        avgs.append(row)
    connection.close()

def print_players(names):
  for name, players in names.items():
    for player in players:
        print(f"{player.played}, {name}, {player.pos}, {player.fan_points}, {player.avg}")

def print_averages(avgs):
    for avgs in positions.items():
        for average in avgs:
            print(f"{average.position}, {average.average}")

def calculator(names, avgs):
    #compare players to average player of same position
    #give them scores where 1.0 is average
    #anything > 1.0 is above average
    #anything < 1.0 is below average
    for name, players in names.items():
        for player in players:
            if f'{player.pos}' == 'RB':
                {player.avg}
            {player.played}  

    for avgs in positions.items():
        for average in avgs:
            print(f"{average.position}, {average.average}")
    return

names = {}
positions ={}

read_sqlite_table()
#print_players(names)
#print_averages(avgs)