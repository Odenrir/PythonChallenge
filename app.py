#!/usr/bin/env python
# encoding: utf-8
import json
import threading
from flask import Flask, request, jsonify, render_template, url_for
from flask_socketio import SocketIO, send
from flask_login import LoginManager, login_user, login_required, current_user
from services import user_db, rabbitmq

app = Flask(__name__)
app.secret_key = 'jobsity'

socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ''


@login_manager.user_loader
def load_user(username):
    return user_db.get_user(username)


@app.before_first_request
def activate_job():
    thread = threading.Thread(target=rabbitmq.consume_message, args=(socketio,))
    thread.start()


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


@socketio.on('connect')
@login_required
def connect():
    msg = current_user.username + ' joined'
    send(msg, broadcast=True)


@socketio.on('disconnect')
@login_required
def disconnect():
    msg = current_user.username + ' leave'
    send(msg, broadcast=True)


@socketio.on('message')
@login_required
def handle_message(data):
    if data.startswith('/'):
        rabbitmq.publish_message(data)
    else:
        msg = current_user.username + ': ' + str(data)
        send(msg, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0')
