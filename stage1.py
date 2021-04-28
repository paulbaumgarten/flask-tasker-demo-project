from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def index_page():
    print("[index_page] Got visited by someone at "+request.remote_addr)
    return "Index page"

@app.route("/register")
def register_page():
    return "Registration page"

@app.route("/login")
def login_page():
    return 'Login page'

@app.route("/logout")
def logout_page():
    return 'Logout page'

@app.route("/main")
def main_page():
    return 'Main page'

@app.route("/profile/<userid>")
def profile_page(userid):
    return f'Profile page for {userid}'

app.run(host='0.0.0.0', port=80, debug=True)

