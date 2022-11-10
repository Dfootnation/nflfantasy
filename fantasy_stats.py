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
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week='', position='')


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
        query += f' Position = {position}'
    query += ' ORDER BY Fantasy_points Desc;'
    db = get_db()
    fantasy_stats = db.execute(query).fetchall()
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week=week, position=position)