"""
1. Read from database
"""

from flask import Flask, render_template, redirect, request
import flask_login
from datetime import datetime
import csv
import sqlite3

app = Flask(__name__)
database_filename = "tasker.db"

def database_write(sql, data=None):
    connection = sqlite3.connect(database_filename)
    connection.row_factory = sqlite3.Row
    db = connection.cursor()
    rows_affected = 0
    if data:
        rows_affected = db.execute(sql, data).rowcount
    else:
        rows_affected = db.execute(sql).rowcount
    connection.commit()
    db.close()
    connection.close()
    return rows_affected

def database_read(sql):
    connection = sqlite3.connect(database_filename)
    connection.row_factory = sqlite3.Row
    db = connection.cursor()
    db.execute(sql)
    records = db.fetchall()
    rows = [dict(record) for record in records]
    db.close()
    connection.close()
    return rows

@app.route('/')
def index_page():
    print("[index_page] Got visited by someone at "+request.remote_addr)
    print(request.host)
    database_read("SELECT * FROM accounts;")
    return redirect("/login")

@app.route("/register")
def register_page():
    return "Registration page"

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/logout")
def logout_page():
    return 'Logout page'

@app.route("/main")
def main_page():
    id = '3'
    if 'id' in request.values:
        id = request.values['id']
    folderid = '3'
    if 'folderid' in request.values:
        folderid = request.values['folderid']
    user = { 'name': 'Paul Baumgarten', "userid": "pbaumgarten" }
    folders = database_read("SELECT * FROM folders ORDER BY name;")
    items = database_read(f"SELECT * FROM tasks WHERE folderid='{folderid}';")
    maintask = database_read(f"SELECT * FROM tasks WHERE id='{id}';")[0]
    print(maintask)
    return render_template("main-stage3.html", folders=folders, tasks=items, maintask=maintask, user=user, folderid=folderid, id=id)

@app.route("/profile/<userid>")
def profile_page(userid):
    return f'Profile page for {userid}'

app.run(host='0.0.0.0', port=80, debug=True)

