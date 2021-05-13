import hashlib
import sqlite3
import uuid
import getpass

database_filename = "tasker.db"

def database_write(sql, data=None):
    # Copy and paste the database_write() function from your server.py
    connection = sqlite3.connect(database_filename)
    connection.row_factory = sqlite3.Row
    db = connection.cursor()
    if data:
        rows_affected = db.execute(sql, data).rowcount
    else:
        rows_affected = db.execute(sql).rowcount
    connection.commit()
    db.close()
    connection.close()
    return rows_affected

def database_read(sql, data=None):
    # Copy and paste the database_read() function from your server.py
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

def create_account():
    userid = input("userid: ")
    email = input("email: ")
    name = input("name: ")
    password = getpass.getpass("Password: ")
    salt = str(uuid.uuid1())
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 10000).hex()
    sql = f"INSERT INTO accounts (userid, salt, password, email, name) VALUES (:userid, :salt, :password, :email, :name);"
    record = {
        "userid": userid,
        "salt": salt,
        "password": key,
        "email": email,
        "name": name
    }
    ok = database_write(sql, record)
    print(ok)

create_account()

