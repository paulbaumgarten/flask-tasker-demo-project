import hashlib
import sqlite3
import uuid
import getpass

# Based on
# https://docs.python.org/3/library/hashlib.html
# https://nitratine.net/blog/post/how-to-hash-passwords-in-python/

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

def create_account():
    userid = input("UserID: ")
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    password2 = getpass.getpass("Repeat password: ")
    while password != password2:
        print("Passwords don't match. Please try agian")
        password = getpass.getpass("Password: ")
        password2 = getpass.getpass("Repeat password: ")
    salt = str(uuid.uuid1())
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    print("Salt:",salt)
    print("Hash",key)

def verify_account():
    salt = input("Salt: ")
    valid_key = input("Key: ")
    password = getpass.getpass("Password: ")
    attempted_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex()
    if valid_key == attempted_key:
        print("Password is correct")
    else:
        print(attempted_key)

create_account()
verify_account()
