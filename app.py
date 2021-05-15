#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, request, redirect, jsonify, session
from services import user_db

app = Flask(__name__)
app.secret_key = 'jobsity'

@app.route('/newuser', methods=['POST'])
def new_user():
    info = json.loads(request.data)
    username = info.get('username', 'guest')
    password = info.get('password', '')
    user = user_db.create_user(username, password)
    if user:
        return jsonify({'status': 201, 'message': 'User created'})
    else:
        return jsonify({'status': 409, 'reason': 'User already exists'})

@app.route('/login', methods=['POST'])
def login():
    info = json.loads(request.data)
    username = info.get('username', 'guest')
    password = info.get('password', '')
    user = user_db.login(username, password)
    if user:
        session['user'] = user.to_json()
        return jsonify(user.to_json())
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


@app.route('/logout', methods=['POST'])
def logout():
    if 'user' in session:
        session.pop('user', None)
    return jsonify({'result': 200,
                    'data': {'message': 'logout success'}})


if __name__ == "__main__":
    app.run(port=8080, debug=True)
