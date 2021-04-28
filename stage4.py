from flask import Flask, render_template, redirect, request
import flask_login
from datetime import datetime
import csv
import sqlite3
import uuid

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
    items = database_read(f"SELECT * FROM tasks WHERE folderid='{folderid}' AND status != 'Completed';")
    maintask = database_read(f"SELECT * FROM tasks WHERE id='{id}';")[0]
    print("main_page sending: ",maintask)
    return render_template("main-stage4.html", folders=folders, tasks=items, maintask=maintask, user=user, folderid=folderid, id=id)

@app.route("/save_task", methods=['POST'])
def task_update():
    form = dict(request.values)
    print("task_update received: ", form)
    id = form['id']
    folderid = form['folderid']
    if "submit-close" in form:
        form['status'] = "Completed"
    if "submit-delete" in form:
        database_write(f"DELETE FROM tasks WHERE id={id};")
        return redirect("/main")
    # New task or update to an existing?
    if id == "": # New task
        id = str(uuid.uuid1())
        form['link'] = ""
        form['id'] = id
        sql = "INSERT INTO tasks (userid,folderid,id,title,due,reminder,created,category,priority,status,notes,link) VALUES (:userid,:folderid,:id,:title,:due,:reminder,:created,:category,:priority,:status,:notes,:link);"
        ok = database_write(sql, form)
        if ok == 1:
            return redirect(f"/main?folderid={folderid}&id={id}")
        else:
            return redirect(f"/error?msg=Unable%20to%20save")
    else: # Update existing
        form['link'] = ""
        sql = "UPDATE tasks SET title=:title,due=:due,reminder=:reminder,category=:category,priority=:priority,status=:status,notes=:notes,link=:link WHERE id=:id;"
        ok = database_write(sql, form)
        if ok == 1:
            return redirect(f"/main?folderid={folderid}&id={id}")
        else:
            return redirect(f"/error?msg=Unable%20to%20save")

@app.route("/new_folder", methods=["POST"])
def folder_new():
    form = dict(request.values)
    print("folder_new received: ", form)
    id = str(uuid.uuid1())
    form['id'] = id
    sql = "INSERT INTO folders (userid,id,name) VALUES (:userid,:id,:name);"
    ok = database_write(sql, form)
    if ok == 1:
        return f"Folder created with id {id}"
    else:
        return "Error creating folder"


@app.route("/profile/<userid>")
def profile_page(userid):
    return f'Profile page for {userid}'

app.run(host='0.0.0.0', port=80, debug=True)

