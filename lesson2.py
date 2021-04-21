from flask import Flask, render_template, redirect
import flask_login

app = Flask(__name__)

@app.route('/')
def index_page():
    return "Index page"

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
def feed_page():
    return render_template("main.html")

@app.route("/profile/<userid>")
def profile_page(userid):
    return f'Profile page for {userid}'

app.run(host='0.0.0.0', port=80, debug=True)

