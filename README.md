# flask-igcse-2021
Flask lessons for igcse class 2021

Project progression:
* 1 - Basic routing
*   - login.html, login.css
        1. Create basic Flask outline
        2. Get first Flask server working 
*   - main.html, main.css
* 2 - Rendering template with demo data
        1. Write HTML main.html and login.html
        2. Use render_template() to send the HTML files
        3. Redirect index -> login
        4. Load demo.csv data for render_template()
*   - tasker.db
        * create tables, fields, keys
        * enter test data
* 3 - Rendering template from database
        * main.html folder listing, loop.index0 to folder.id
        * main.html: task['preview'] to task['notes'][:50]
        * main.html: tasks[id] to maintask
* 4 - Update existing and add new records to database
        * Update task
        * New task
        * New folder
        * Includes some Javascript (add the src ref to the html)
* 5 - Login system
        * app.config secret key
        * login_manager
        * User class
        * load_user
        * request_loader
        * unauthorised_handler
        * add @flask_login.login_required to secure routes
        * logout ->... flask_login.logout_user()
        * add to index:;;; 
            if flask_login.current_user.is_authenticated:
                return redirect('/main')
            else:
                return redirect('/login')
        * login route:::::
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

        * Update SQLs to only use session userid not browser supplied

## Lesson 1 - A web server

Introduce project & unit

Theory

* show understanding of the role of the browser
    * show understanding of the role of an Internet Service Provider (ISP)
    * show understanding of what is meant by hypertext transfer protocol (http and https) and HTML
* show understanding of the concepts of MAC address, 
    * How to find your MAC address (console)
* Internet Protocol (IP) address, 
    * IP4 v IP6
    * How to find your IP address (console)
* Uniform Resource Locator (URL) 
* cookies
    * How to see the cookies and storage on your system (chrome dev tools/application/storage)
* DNS
    * Query a domain name (console)
* URL - parts

```python
import uuid
import socket

mac = uuid.getnode()
ip = socket.gethostbyname(socket.gethostname())

print("Mac address: ", mac)
print("As hex     : ", hex(mac))
print("IP address : ", ip)
```

Project

* Setup environment
* Install Flask library
* lesson1.py - basic routes

## Lesson 2 - HTML

Theory

* distinguish between HTML structure and presentation
* Differentiate between HTML, CSS and Javascript

Practical

* Brief introductory exercises into all HTML & CSS via the login form
* You don't need to be able to read & write HTML. Recognise it, yes, but that's all
* Find a good reference and use it while you learn a project

https://cssreference.io/
https://htmlreference.io/

The link between html class and the . in css
The link between html id and the # in css
Unprefixed CSS is an element
Some other controls available eg :hover
 

## Lesson 3 - HTML template

Practical

* lesson2.py
* Create the main.html
* Create a few key elements of the css layout (3 column grid, the grid on the form)
* Give the rest of the CSS ?

## Lesson 4 - Jinga2

Templating language

* Benefits
* Basics - provide reference doc

## Lesson 5 - Get form data

Different HTTP requests - GET, POST, PUSH, get
* Different ways of encoding the data sent (not immediately visible doesn't mean it is hidden/secret/private)

## Lesson 6 - Database ideas

Candidates should be able to:
* define a single-table database from given data storage requirements
* choose and specify suitable data types
* choose a suitable primary key for a database table
* perform a query-by-example from given search criteria

## Lesson 7 - Create a database

Theory

* Tables, columns, fields, database types
* Primary key
* Insert records
* SQL to query the database

Practical

* Install DB Browser SQL lite
* Create a database - tasker
* Use the query-by-example tool

## Lesson 8 - Read/write database via Python

Create a quick & dirty stand alone Python script to demonstrate

```python
database_write("INSERT INTO table (field1,field2,field3) VALUES (?,?,?);", ["a","b","c"])
```

## Lesson 9 - Add databasing to Tasker

## Lesson 10 - Securing the user information

•• show understanding of the security aspects of using the Internet and understand what methods are available
to help minimise the risks
•• show understanding of the Internet risks associated with malware, including viruses, spyware and hacking
•• explain how anti-virus and other protection software helps to protect the user from security risks

Salting and hashing the password

Chrome inspection, view the network data and the cookies

Firewall - prventing you from viewing your neighbours Flask



