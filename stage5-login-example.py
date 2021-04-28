from flask import Flask, request, redirect, send_file
from flask.templating import render_template
import flask_login

# Setup

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some random code here. this is used to cryptographically sign your data'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Login system

### Our mock database.
users = {'foo': {'password': 'secret'}}

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def load_user(userid):
    if userid not in users:
        return None
    user = User()
    user.id = userid
    return user

"""
@login_manager.request_loader
def request_loader(request):
    userid = request.form.get('userid')
    if userid not in users:
        return None
    user = User()
    user.id = userid
    user.is_authenticated = request.form['password'] == users[userid]['password']
    return user
"""

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

# Page routes

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
    if userid in users and request.form['password'] == users[userid]['password']:
        user = User()
        user.id = userid
        flask_login.login_user(user)
        return redirect('/main')
    return render_template("login.html", alert="Bad login attempt. Try again.")

@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect('/')

@app.route("/main")
@flask_login.login_required
def main_page():
    iam = flask_login.current_user.id
    return render_template("main.html")

@app.route("/profile/<userid>")
@flask_login.login_required
def profile_page(userid):
    return f'Profile page for {userid}'

# Start the app

app.run(host='0.0.0.0', port=80, debug=True)

