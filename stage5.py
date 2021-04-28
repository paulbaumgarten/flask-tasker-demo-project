from flask import Flask, render_template, redirect, request
import flask_login
from datetime import datetime
import csv
import sqlite3
import uuid

app = Flask(__name__)
database_filename = "tasker.db"
app.config['SECRET_KEY'] = 'some random code here. this is used to cryptographically sign your data'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    def __init__(self, userid, email, name):
        self.id = userid
        self.email = email
        self.name = name
    
    def get_dict(self):
        return {"userid": self.id, "email": self.email, "name": self.name}

@login_manager.user_loader
def load_user(userid):
    users = database_read("SELECT * FROM accounts WHERE userid=?", (userid,))
    if len(users) != 1:
        return None
    user = User(users[0]['userid'], users[0]['email'], users[0]['name'])
    user.id = userid
    return user

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

def database_read(sql, data=None):
    connection = sqlite3.connect(database_filename)
    connection.row_factory = sqlite3.Row
    db = connection.cursor()
    if data:
        db.execute(sql, data)
    else:
        db.execute(sql)
    records = db.fetchall()
    rows = [dict(record) for record in records]
    db.close()
    connection.close()
    return rows

@app.route('/')
def index_page():
    print("[index_page] Got visited by someone at "+request.remote_addr)
    if flask_login.current_user.is_authenticated:
        return redirect('/main')
    else:
        return redirect('/login')

@app.route("/register")
def register_page():
    return "Registration page"

@app.route("/login", methods=['GET'])
def login_page():
    return render_template("login.html", alert="")

@app.route("/login", methods=['POST'])
def login_request():
    userid = request.form['userid']
    possible_passwd = request.form['password']
    users = database_read("SELECT * FROM accounts WHERE userid=? AND password=?", (userid,possible_passwd))
    if len(users) == 1:
        user = User(users[0]['userid'], users[0]['email'], users[0]['name'])
        user.id = userid
        flask_login.login_user(user)
        return redirect('/main')
    return render_template("login.html", alert="Bad login attempt. Try again.")

@app.route("/logout")
def logout_page():
    flask_login.logout_user()
    return redirect("/")

@app.route("/main")
@flask_login.login_required
def main_page():
    id = '3'
    if 'id' in request.values:
        id = request.values['id']
    folderid = '3'
    if 'folderid' in request.values:
        folderid = request.values['folderid']
    user = flask_login.current_user.get_dict()
    folders = database_read("SELECT * FROM folders ORDER BY name;")
    items = database_read(f"SELECT * FROM tasks WHERE folderid='{folderid}' AND status != 'Completed';")
    maintask = database_read(f"SELECT * FROM tasks WHERE id='{id}';")[0]
    print("main_page sending: ",maintask)
    return render_template("main-stage4.html", folders=folders, tasks=items, maintask=maintask, user=user, folderid=folderid, id=id)

@app.route("/save_task", methods=['POST'])
@flask_login.login_required
def task_update():
    form = dict(request.values)
    print("task_update received: ", form)
    id = form['id']
    folderid = form['folderid']
    if "submit-delete" in form:
        database_write(f"DELETE FROM tasks WHERE id={id} AND userid={flask_login.current_user.id};")
        return redirect("/main")
    if "submit-close" in form:
        form['status'] = "Completed"
    # New task or update to an existing?
    if id == "": # New task
        id = str(uuid.uuid1())
        form['link'] = ""
        form['id'] = id
        form['userid'] = flask_login.current_user.id
        sql = "INSERT INTO tasks (userid,folderid,id,title,due,reminder,created,category,priority,status,notes,link) VALUES (:userid,:folderid,:id,:title,:due,:reminder,:created,:category,:priority,:status,:notes,:link);"
        ok = database_write(sql, form)
        if ok == 1:
            return redirect(f"/main?folderid={folderid}&id={id}")
        else:
            return redirect(f"/error?msg=Unable%20to%20save")
    else: # Update existing
        form['link'] = ""
        form['userid'] = flask_login.current_user.id
        sql = "UPDATE tasks SET title=:title,due=:due,reminder=:reminder,category=:category,priority=:priority,status=:status,notes=:notes,link=:link WHERE id=:id;"
        ok = database_write(sql, form)
        if ok == 1:
            return redirect(f"/main?folderid={folderid}&id={id}")
        else:
            return redirect(f"/error?msg=Unable%20to%20save")

@app.route("/new_folder", methods=["POST"])
@flask_login.login_required
def folder_new():
    form = dict(request.values)
    print("folder_new received: ", form)
    id = str(uuid.uuid1())
    form['id'] = id
    form['userid'] = flask_login.current_user.id
    sql = "INSERT INTO folders (userid,id,name) VALUES (:userid,:id,:name);"
    ok = database_write(sql, form)
    if ok == 1:
        return f"Folder created with id {id}"
    else:
        return "Error creating folder"

@app.route("/profile/<userid>")
@flask_login.login_required
def profile_page(userid):
    return f'Profile page for {userid}'

app.run(host='0.0.0.0', port=80, debug=True)

