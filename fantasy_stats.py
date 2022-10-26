from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from nflfantasy.db import get_db

bp = Blueprint('fantasy_stats', __name__)

@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    fantasy_stats = db.execute(
        'SELECT * FROM fantasy_score ORDER BY Fantasy_points Desc'
    ).fetchall()
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week='')

@bp.route('/', methods=['POST'])
def selectweek():
    week = request.form['week']
    query = 'SELECT * FROM fantasy_score'
    if week:
        query += " WHERE Week = '%%{}%%'".format(week)
    db = get_db()
    fantasy_stats = db.execute(query).fetchall()
    return render_template('fantasy.html', fantasy_stats=fantasy_stats, week=week)