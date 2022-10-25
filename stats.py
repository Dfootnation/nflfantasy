from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from NFL-fantasy.db import get_db

bp = Blueprint('stats', __name__)

@bp.route('/', methods=['GET'])
def index():
    db = get_db()
    stats = db.execute(
        'SELECT * FROM account ORDER BY tag'
    ).fetchall()
    return render_template('stats/index.html', stats=stats, tag='')

@bp.route('/', methods=['POST'])
def search():
    tag = request.form['tag']
    query = 'SELECT * FROM account'
    if tag:
        query += " WHERE tag LIKE '%%{}%%'".format(tag)
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/index.html', stats=stats, tag=tag)


@bp.route('/settings', methods=['GET'])
def settings():
    query = 'SELECT * FROM settings'
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/settings.html', stats=stats, ign='')

@bp.route('/settings', methods=['POST'])
def settingssearch():
    ign = request.form['ign']
    query = 'SELECT * FROM account'
    if ign:
        query += " WHERE tag LIKE '%%{}%%'".format(ign)
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/settings.html', stats=stats, ign=ign)

@bp.route('/roster', methods=['GET'])
def roster():
    query = "SELECT * FROM settings;"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/roster.html', stats=stats, ign='')

@bp.route('/players', methods=['GET'])
def players():
    query = "SELECT * FROM settings;"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players.html', stats=stats, ign='')

@bp.route('/players/walsh', methods=['GET'])
def walsh():
    query = "SELECT * FROM settings WHERE ign = 'Walsh';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/walsh.html', stats=stats, ign='')

@bp.route('/players/croll', methods=['GET'])
def croll():
    query = "SELECT * FROM settings WHERE ign = 'Croll';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/croll.html', stats=stats, ign='')

@bp.route('/players/dfootnation', methods=['GET'])
def dfootnation():
    query = "SELECT * FROM settings WHERE ign = 'Dfootnation';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/dfootnation.html', stats=stats, ign='')

@bp.route('/players/festy', methods=['GET'])
def festy():
    query = "SELECT * FROM settings WHERE ign = 'festy';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/festy.html', stats=stats, ign='')

@bp.route('/players/mish', methods=['GET'])
def mish():
    query = "SELECT * FROM settings WHERE ign = 'Mish';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/mish.html', stats=stats, ign='')

@bp.route('/players/bino', methods=['GET'])
def bino():
    query = "SELECT * FROM settings WHERE ign = 'bino';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/bino.html', stats=stats, ign='')

@bp.route('/players/borddinho', methods=['GET'])
def borddinho():
    query = "SELECT * FROM settings WHERE ign = 'Borddinho';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/borddinho.html', stats=stats, ign='')

@bp.route('/players/thiccthigh', methods=['GET'])
def thiccthigh():
    query = "SELECT * FROM settings WHERE ign = 'Thiccthigh';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/thiccthigh.html', stats=stats, ign='')

@bp.route('/players/kek', methods=['GET'])
def kek():
    query = "SELECT * FROM settings WHERE ign = 'Kek';"
    db = get_db()
    stats = db.execute(query).fetchall()
    return render_template('stats/players/kek.html', stats=stats, ign='')