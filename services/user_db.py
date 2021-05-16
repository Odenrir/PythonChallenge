import os
from pysondb import db
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User


def login(username, password):
    database = db.getDb(os.getcwd() + '/db/users.json')
    query = database.getBy({'username': username})
    if not query:
        return None
    else:
        user_data = query[0]
        if check_password_hash(user_data['password'], password):
            return User(user_data['username'])
        else:
            return None


def create_user(username, password):
    database = db.getDb(os.getcwd() + '/db/users.json')
    if not database.getBy({'username': username}):
        password_hash = generate_password_hash(password)
        user_id = database.add({'username': username, 'password': password_hash})
        query = database.getBy({'id': user_id})
        user_data = query[0]
        return User(user_data['username'])
    else:
        return None
