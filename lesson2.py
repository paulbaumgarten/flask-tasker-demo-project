"""
1. Write HTML main.html and login.html
2. Use render_template() to send the HTML files
3. Redirect index -> login
"""

from flask import Flask, render_template, redirect, request
import flask_login
from datetime import datetime
import json

app = Flask(__name__)

@app.route('/')
def index_page():
    print("[index_page] Got visited by someone at "+request.remote_addr)
    print(request.host)
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
    id = 3
    if 'id' in request.values:
        id = int(request.values['id'])
    folderid = 3
    if 'folderid' in request.values:
        folderid = int(request.values['folderid'])
    folders = ["CompSci", "Economics", "English", "History", "Math", "Science"]
    user = { 'name': 'Paul Baumgarten' }
    items = []
    with open("demo.json") as f:
        items = json.loads(f.read())
    return render_template("main.html", folders=folders, tasks=items, user=user, folderid=folderid, id=id)

@app.route("/profile/<userid>")
def profile_page(userid):
    return f'Profile page for {userid}'


app.run(host='0.0.0.0', port=80, debug=True)

