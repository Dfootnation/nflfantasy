from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from nflfantasy.db import get_db

bp = Blueprint('fantasy_stats', __name__)

@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    fantasy_stats = db.execute(
        'SELECT ROW_NUMBER() OVER(ORDER BY Fantasy_points DESC) as Rank, fantasy_score.* FROM fantasy_score ORDER BY Fantasy_points Desc LIMIT 100;'
    ).fetchall()
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week='', position='', name='')


@bp.route('/', methods=['POST'])
def search():
    week = request.form['week']
    position = request.form['position']
    query = 'SELECT ROW_NUMBER() OVER(ORDER BY Fantasy_points DESC) as Rank, fantasy_score.* FROM fantasy_score'
    if week:
        query += f' WHERE Week = {week}'
    if position:
        if week:
            query += ' AND '
        else:
            query += ' WHERE '
        query += f' Position = "{position}"'
    query += ' ORDER BY Fantasy_points Desc;'
    db = get_db()
    fantasy_stats = db.execute(query).fetchall()
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week=week, position=position, name='')

@bp.route('/player', methods=['POST'])
def player():
    name = request.form['name']
    query1 = f'SELECT Name, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query2 = f'SELECT Name, Team, Position, ROUND(AVG(Passing_yards),2) as Passing_yards, ROUND(AVG(Passing_tds),2) as Passing_tds, ROUND(AVG(Passing_int),2) as Passing_int, ROUND(AVG(Rushing_yards),2) as Rushing_yards, ROUND(AVG(Rushing_tds),2) as Rushing_tds, ROUND(AVG(Receiving_rec),2) as Receiving_rec, ROUND(AVG(Receiving_yards),2) as Receiving_yards, ROUND(AVG(Receiving_tds),2) as Receiving_tds, ROUND(AVG(Return_td),2) as Return_td, ROUND(AVG(Misc_fumtd),2) as Misc_fumtd, ROUND(AVG(Misc_2pt),2) as Misc_2pt, ROUND(AVG(Fum_lost),2) as Fum_lost, ROUND(AVG(Fantasy_points),2) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query3 = f'SELECT Name, Team, Position, MIN(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query4 = f'SELECT Name, Team, Position, MAX(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query5 = f'SELECT * FROM fantasy_score WHERE Name = "{name}";'
    query6 = f'SELECT Name, Team, Position, ROUND(SUM(Passing_yards) / 25) as Passing_yards, ROUND(SUM(Passing_tds) * 4) as Passing_tds, ROUND(SUM(Passing_int) / 2) as Passing_int, ROUND(SUM(Rushing_yards) / 10,2) as Rushing_yards, ROUND(SUM(Rushing_tds) * 6) as Rushing_tds, ROUND(SUM(Receiving_rec)) as Receiving_rec, ROUND(SUM(Receiving_yards) / 10) as Receiving_yards, SUM(Receiving_tds) * 6 as Receiving_tds, ROUND(SUM(Return_td) * 6) as Return_td, ROUND(SUM(Misc_fumtd)) as Misc_fumtd, ROUND(SUM(Misc_2pt) * 2) as Misc_2pt, ROUND(SUM(Fum_lost) * 2) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query7 = f'SELECT Name, Team, Position, ROUND(AVG(Passing_yards) / 25) as Passing_yards, ROUND(AVG(Passing_tds) * 4) as Passing_tds, ROUND(AVG(Passing_int) / 2) as Passing_int, ROUND(AVG(Rushing_yards) / 10,2) as Rushing_yards, ROUND(AVG(Rushing_tds) * 6,2) as Rushing_tds, ROUND(AVG(Receiving_rec),2) as Receiving_rec, ROUND(AVG(Receiving_yards) / 10,2) as Receiving_yards, ROUND(AVG(Receiving_tds) * 6,2) as Receiving_tds, ROUND(AVG(Return_td) * 6) as Return_td, ROUND(AVG(Misc_fumtd)) as Misc_fumtd, ROUND(AVG(Misc_2pt) * 2) as Misc_2pt, ROUND(AVG(Fum_lost) * 2) as Fum_lost, ROUND(AVG(Fantasy_points),2) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    query8 = f'SELECT Name, Team, Position, COUNT(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}" AND Fantasy_points > 30;'
    query9 = f'SELECT Name, Team, Position, COUNT(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}" AND Fantasy_points > 20;'
    query10 = f'SELECT Name, Team, Position, COUNT(Fantasy_points) as Fantasy_points FROM fantasy_score WHERE Name = "{name}";'
    db = get_db()
    player_sum = db.execute(query1).fetchall()
    player_avg = db.execute(query2).fetchall()
    player_min = db.execute(query3).fetchall()
    player_max = db.execute(query4).fetchall()
    player = db.execute(query5).fetchall()
    point_sum = db.execute(query6).fetchall()
    point_avg = db.execute(query7).fetchall()
    thirtyplus = db.execute(query8).fetchall()
    twentyplus = db.execute(query9).fetchall()
    profile = db.execute(query10).fetchall()
    return render_template('player.html', week='', position='', player=player, player_sum=player_sum, player_avg=player_avg, player_min=player_min, player_max=player_max, point_sum=point_sum, point_avg=point_avg, thirtyplus=thirtyplus, twentyplus=twentyplus, profile=profile, name=name)

@bp.route('/season', methods=['GET'])
def season():
    db = get_db()
    fantasy_stats = db.execute(
        'SELECT ROW_NUMBER() OVER(ORDER BY SUM(Fantasy_points) DESC) as Rank, COUNT(DISTINCT (Week)) as Played, Name, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(AVG(Fantasy_points),2) as Average FROM fantasy_score GROUP BY Name ORDER BY Fantasy_points DESC LIMIT 100 ;'
    ).fetchall()
    return render_template('season.html', fantasy_stats=fantasy_stats, week='', position='', name='')

@bp.route('/season', methods=['POST'])
def seasonbyposition():
    position = request.form['position']
    query = 'SELECT ROW_NUMBER() OVER(ORDER BY SUM(Fantasy_points) DESC) as Rank, COUNT(DISTINCT (Week)) as Played, Name, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(AVG(Fantasy_points),2) as Average FROM fantasy_score' 
    if position:
        query += f' WHERE Position = "{position}"'
    query += ' GROUP BY Name ORDER BY Fantasy_points DESC LIMIT 100 ;'
    db = get_db()
    fantasy_stats = db.execute(query).fetchall()
    return render_template('season.html', fantasy_stats=fantasy_stats, position=position, name='')

@bp.route('/team', methods=['GET'])
def team():
    db = get_db()
    fantasy_stats = db.execute(
        'SELECT ROW_NUMBER() OVER(ORDER BY SUM(Fantasy_points) DESC) as Rank, COUNT(DISTINCT (Week)) as Played, COUNT(DISTINCT(Name)) as Players, Team, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score GROUP BY Team ORDER BY Fantasy_points DESC;'
    ).fetchall()
    return render_template('team.html', fantasy_stats=fantasy_stats, week='', position='', name='')

@bp.route('/team', methods=['POST'])
def teambyposition():
    position = request.form['position']
    query = 'SELECT ROW_NUMBER() OVER(ORDER BY SUM(Fantasy_points) DESC) as Rank, COUNT(DISTINCT (Week)) as Played, COUNT(DISTINCT(Name)) as Players, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score'
    if position:
        query += f' WHERE Position = "{position}"'
    query += ' GROUP BY Team ORDER BY Fantasy_points DESC;'
    db = get_db()
    fantasy_stats = db.execute(query).fetchall()
    return render_template('team.html', fantasy_stats=fantasy_stats, position=position, name='')

@bp.route('/against', methods=['GET'])
def against():
    db = get_db()
    fantasy_stats = db.execute(
        'SELECT ROW_NUMBER() OVER(ORDER BY SUM(Fantasy_points) DESC) as Rank, COUNT(DISTINCT (Week)) as Played, COUNT(DISTINCT(Name)) as Players, Against, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score GROUP BY Against ORDER BY Fantasy_points DESC;'
    ).fetchall()
    return render_template('against.html', fantasy_stats=fantasy_stats, week='', position='', name='')

@bp.route('/against', methods=['POST'])
def againstbyposition():
    position = request.form['position']
    query = 'SELECT ROW_NUMBER() OVER(ORDER BY SUM(Fantasy_points) DESC) as Rank, COUNT(DISTINCT (Week)) as Played, COUNT(DISTINCT(Name)) as Players, Against, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score'
    if position:
        query += f' WHERE Position = "{position}"'
    query += ' GROUP BY Team ORDER BY Fantasy_points DESC;'
    db = get_db()
    fantasy_stats = db.execute(query).fetchall()
    return render_template('against.html', fantasy_stats=fantasy_stats, position=position, name='')

@bp.route('/compare', methods=['GET'])
def compare():
    db = get_db()
    fantasy_stats = db.execute(
        'SELECT COUNT(DISTINCT (Week)) as Played, COUNT(DISTINCT(Name)) as Players, Against, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score GROUP BY Name ORDER BY Fantasy_points DESC;'
    ).fetchall()
    return render_template('compare.html', fantasy_stats=fantasy_stats, week='', position='', name1='', name2='')

@bp.route('/compare', methods=['POST'])
def comparebyname():
    name1 = request.form['name1']
    name2 = request.form['name2']
    query1 = 'SELECT COUNT(DISTINCT (Week)) as Played, Name, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score'
    if name1:
        query1 += f' WHERE Name = "{name1}"'
    query1 += ' GROUP BY Name ORDER BY Fantasy_points DESC;'
    
    query2 = 'SELECT COUNT(DISTINCT (Week)) as Played, Name, Team, Position, SUM(Passing_yards) as Passing_yards, SUM(Passing_tds) as Passing_tds, SUM(Passing_int) as Passing_int, SUM(Rushing_yards) as Rushing_yards, SUM(Rushing_tds) as Rushing_tds, SUM(Receiving_rec) as Receiving_rec, SUM(Receiving_yards) as Receiving_yards, SUM(Receiving_tds) as Receiving_tds, SUM(Return_td) as Return_td, SUM(Misc_fumtd) as Misc_fumtd, SUM(Misc_2pt) as Misc_2pt, SUM(Fum_lost) as Fum_lost, ROUND(SUM(Fantasy_points),2) as Fantasy_points, ROUND(SUM(Fantasy_points)/COUNT(DISTINCT (Week)),2) as Average FROM fantasy_score'
    if name2:
        query2 += f' WHERE Name = "{name2}"'
    query2 += ' GROUP BY Name ORDER BY Fantasy_points DESC;'
    print(query1)
    print(query2)
    db = get_db()
    player1 = db.execute(query1).fetchall()
    player2 = db.execute(query2).fetchall()
    return render_template('compare.html', player1=player1, player2=player2, week='', position='', name1=name1, name2=name2)