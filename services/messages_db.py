import os
from datetime import datetime
from pysondb import db


def save_msg(username, msg):
    time = datetime.now()
    timestamp = (time - datetime(1970, 1, 1)).total_seconds()
    database = db.getDb(os.getcwd() + '/db/messages.json')
    database.add({'username': username, 'msg': msg, 'timestamp': timestamp})
    return True
