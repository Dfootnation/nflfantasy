from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from nflfantasy.db import get_db

bp = Blueprint('fantasy_stats', __name__)

@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    fantasy_stats = db.execute(
        'SELECT * FROM fantasy_score ORDER BY Fantasy_points Desc;'
    ).fetchall()
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week='', position='', name='')


@bp.route('/', methods=['POST'])
def search():
    week = request.form['week']
    position = request.form['position']
    query = 'SELECT * FROM fantasy_score'
    if week:
        query += f' WHERE Week = {week}'
    if position:
        if week:
            query += ' AND '
        else:
            query += ' WHERE '
        query += f' Position = "{position}"'
    query += ' ORDER BY Fantasy_points Desc;'
    #default params to show all not working
    #if week == 0 and position == 0:
        #query = 'SELECT * FROM fantasy_score ORDER BY Fantasy_points Desc;'
    db = get_db()
    fantasy_stats = db.execute(query).fetchall()
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week=week, position=position, name='')

@bp.route('/player', methods=['POST'])
def player():
    name = request.form['name']
    query1 = f'SELECT Name, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, SUM(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query2 = f'SELECT Name, Team, Position, AVG(Passing_yards) as Passing_yards, AVG(Passing_tds) as Passing_tds, AVG(Passing_int) as Passing_int, AVG(Rushing_yards) as Rushing_yards, AVG(Rushing_tds) as Rushing_tds, AVG(Receiving_rec) as Receiving_rec, AVG(Receiving_yards) as Receiving_yards, AVG(Receiving_tds) as Receiving_tds, AVG(Return_td) as Return_td, AVG(Misc_fumtd) as Misc_fumtd, AVG(Misc_2pt) as Misc_2pt, AVG(Fum_lost) as Fum_lost, AVG(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query3 = f'SELECT Name, Team, Position, MIN(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query4 = f'SELECT Name, Team, Position, MAX(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query5 = f'SELECT * FROM fantasy_score WHERE Name = "{name}";'
    query6 = f'SELECT Name, Team, Position, SUM(Passing_yards) / 25 as Passing_yards, SUM(Passing_tds) * 4 as Passing_tds, SUM(Passing_int) / 2 as Passing_int, SUM(Rushing_yards) / 10 as Rushing_yards, SUM(Rushing_tds) * 6 as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) / 10 as Receiving_yards, SUM(Receiving_tds) * 6 as Receiving_tds, SUM(Return_td) * 6 as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) * 2 as Misc_2pt, SUM(Fum_lost) * 2 as Fum_lost, SUM(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query7 = f'SELECT Name, Team, Position, AVG(Passing_yards) / 25 as Passing_yards, AVG(Passing_tds) * 4 as Passing_tds, AVG(Passing_int) / 2 as Passing_int, AVG(Rushing_yards) / 10 as Rushing_yards, AVG(Rushing_tds) * 6 as Rushing_tds, AVG(Receiving_rec) as Receiving_rec, AVG(Receiving_yards) / 10 as Receiving_yards, AVG(Receiving_tds) * 6 as Receiving_tds, AVG(Return_td) * 6 as Return_td, AVG(Misc_fumtd) as Misc_fumtd, AVG(Misc_2pt) * 2 as Misc_2pt, AVG(Fum_lost) * 2 as Fum_lost, AVG(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    db = get_db()
    player_sum = db.execute(query1).fetchall()
    player_avg = db.execute(query2).fetchall()
    player_min = db.execute(query3).fetchall()
    player_max = db.execute(query4).fetchall()
    player = db.execute(query5).fetchall()
    point_sum = db.execute(query6).fetchall()
    point_avg = db.execute(query7).fetchall()
    return render_template('player.html', week='', position='', player=player, player_sum=player_sum, player_avg=player_avg, player_min=player_min, player_max=player_max, point_sum=point_sum, point_avg=point_avg, name=name)