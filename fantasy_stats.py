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
    print(query)
    db = get_db()
    fantasy_stats = db.execute(query).fetchall()
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week=week, position=position, name='')

@bp.route('/player', methods=['POST'])
def player():
    name = request.form['name']
    query1 = f'SELECT Name, Team, Position, SUM(Passing_yards), SUM(Passing_tds), SUM(Passing_int), SUM(Rushing_yards), SUM(Rushing_tds), SUM(Receiving_rec),SUM(Receiving_yards), SUM(Receiving_tds), SUM(Return_td), SUM(Misc_fumtd), SUM(Misc_2pt), SUM(Fum_lost), SUM(Fantasy_points) FROM fantasy_score WHERE Name = "{name}";'
    query2 = f'SELECT Name, Team, Position, AVG(Passing_yards), AVG(Passing_tds), AVG(Passing_int), AVG(Rushing_yards), AVG(Rushing_tds), AVG(Receiving_rec),AVG(Receiving_yards), AVG(Receiving_tds), AVG(Return_td), AVG(Misc_fumtd), AVG(Misc_2pt), AVG(Fum_lost), AVG(Fantasy_points) FROM fantasy_score WHERE Name = "{name}";'
    query3 = f'SELECT Name, Team, Position, MIN(Fantasy_points) FROM fantasy_score WHERE Name = "{name}";'
    query4 = f'SELECT Name, Team, Position, MAX(Fantasy_points) FROM fantasy_score WHERE Name = "{name}";'
    query5 = f'SELECT * FROM fantasy_score WHERE Name = "{name}";'
    print(query5)
    db = get_db()
    player_sum = db.execute(query1).fetchall()
    player_avg = db.execute(query2).fetchall()
    player_min = db.execute(query3).fetchall()
    player_max = db.execute(query4).fetchall()
    player = db.execute(query5).fetchall()
    return render_template('player.html', week='', position='', player=player, player_sum=player_sum, player_avg=player_avg, player_min=player_min, player_max=player_max, name=name)