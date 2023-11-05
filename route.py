import subprocess
import tkinter as tk
from flask import Flask, render_template, url_for, flash, redirect, request, session, url_for
from flask_socketio import join_room, leave_room, send, SocketIO
from forms import RegistrationForm, LoginForm
import random
from string import ascii_uppercase

import os
#import util
app = Flask(__name__)
app.config['SECRET_KEY'] = 'krishna'
socketio = SocketIO(app)

rooms = {}

def generate_room_code(length):
    code = ""
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
        
        if code not in rooms:
            break
        
    return code


@app.route("/")
def home():
    return "Hello World!"

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/chatroom-home", methods=['POST', 'GET'])
def chatroom_home():
    if request.method == 'POST':
        name = request.form.get('name') #diff functions return diff attributes for name (ex. create, join)
        code = request.form.get('code')
        join = request.form.get('join', False)
        create = request.form.get('create', False)

        if not name:
            return render_template('chatroom-home.html', error="Make sure to enter a name!", code=code, name=name)
        
        if join != False and (not code or code not in rooms):
            return render_template('chatroom-home.html', error="Make sure to enter a valid room code!", code=code, name=name)

        room = ''
        if create != False and not code:
            room = generate_room_code(6)
            rooms[room] = {'members': 0, 'messages': []}
            code = room
        elif code not in rooms:
            rooms[code] = {'members': 0, 'messages': []}

        session['room'] = code
        session['name'] = name
        return redirect(url_for('chatroom')) 

    return render_template('chatroom-home.html', title='Chatroom Home')

@app.route('/chatroom')
def chatroom():
    room = session.get('room')
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for('chatroom_home'))
    
    return render_template('chatroom.html', code=room, messages=rooms[room]['messages'])

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return 
    
    content = {
        "name": session.get("name"),
        "message": data["data"]
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on('connect')
def connect(auth):
    room = session.get('room')
    name = session.get('name')

    join_room(room)
    rooms[room]["members"] += 1
    send({'name': name, 'message': 'has entered the room'}, to=room)
    print(f'{name} has entered room {room}')

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
    
    send({"name": name, "message": "has left the room"}, to=room)
    print(f"{name} has left the room {room}")

if __name__ == '__main__':
    socketio.run(app, debug=True, port=8000)