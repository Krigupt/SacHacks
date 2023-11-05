import flask
from flask import render_template, url_for, flash, redirect,request,abort, session
import os
from Sac.forms import RegistrationForm, LoginForm,UpdateAccountForm,PostForm
from Sac.models import User,Post
from flask_login import login_user,current_user,logout_user,login_required
from PIL import Image
from Sac import app,db,bcrypt,mail, socketio
import secrets
import io
from flask_socketio import join_room, leave_room, send, SocketIO
import random
from string import ascii_uppercase



@login_required
@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html',posts=posts)


@login_required
@app.route("/about")
def about():
    return render_template("about.html")



@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)




@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)





def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@login_required
@app.route("/account", methods=['GET', 'POST'])
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated', 'success')
        return redirect(url_for('account'))

    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename=current_user.image_file)



    return render_template("account.html", title='Account', image_file=image_file, form=form)




@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('Create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

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