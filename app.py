#!/usr/bin/env python
# encoding: utf-8
import json

from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_socketio import SocketIO
from flask_login import LoginManager, login_user, login_required, current_user

from models.user import User
from services import user_db

app = Flask(__name__)
app.secret_key = 'jobsity'
socketio = SocketIO(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''

@login_manager.user_loader
def load_user(username):
    return user_db.get_user(username)

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/chat', methods=['GET'])
@login_required
def chat():
    return render_template('chat.html')


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
        login_user(user)
        result = {'url': url_for('chat')}
        return jsonify(result)
    else:
        return jsonify({"status": 401,
                        "reason": "Username or Password Error"})


@app.route('/logout', methods=['POST'])
@login_required
def logout():
    user = current_user
    user.authenticated = False
    return jsonify({'result': 200,
                    'data': {'message': 'logout success'}})


'''-----------------Socket events-------------------------'''


@socketio.on('join')
@login_required
def join():
    print(current_user.username + ' join the room')


@socketio.on('message')
@login_required
def handle_message(data):
    print(current_user.username + ': ' + str(data))


if __name__ == "__main__":
    # app.run(port=8080, debug=True)
    #socketio.run(app, async_mode='eventlet')
    socketio.run(app)
