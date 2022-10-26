from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from nflfantasy.db import get_db

bp = Blueprint('fantasy_stats', __name__)

@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    stats = db.execute(
        'SELECT * FROM fantasy_score ORDER BY Name'
    ).fetchall()
    return render_template('fantasy.html', stats=stats)

@bp.route('/', methods=['POST'])
def searchName():
    name = request.form['name']
    query = 'SELECT * FROM fantasy_score'
    if name:
        query += "WHERE Name LIKE '%%{}%%'".format(name)
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('fantasy.html', stats=stats, name=name)