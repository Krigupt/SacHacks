import subprocess
import tkinter as tk
from flask import Flask, render_template, url_for, flash, redirect,request
from forms import RegistrationForm, LoginForm
import cv2

import os
import util
app = Flask(__name__)

app.config['SECRET_KEY'] = 'krishna'

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



#
# # Database directory
# db_dir = './db'
# if not os.path.exists(db_dir):
#     os.mkdir(db_dir)
#
# # Webcam setup
# cap = cv2.VideoCapture(0)
#
# # Face recognition setup (you need to populate this)
# known_face_encodings = []
# known_face_names = []
#
#
#
# def login(self):
#     unknown_img_path = './.tmp.jpg'
#     cv2.imwrite(unknown_img_path, self.most_recent_capture_arr)
#     output = str(subprocess.check_output(['face_recognition', self.db_dir, unknown_img_path]))
#     name = output.split(',')[1][:-3]
#     print(name)
#     if name in ['unknown_person', 'no_person_found']:
#         util.msg_box('Ups...', 'Unknown user, please register again and try again')
#     else:
#         util.msg_box('Success', 'Welcome back {}'.format(name))
#     os.remove(unknown_img_path)
#
#
# @app.route("/face_login", methods=['GET', 'POST'])
# def face_login():
#     if request.method == 'POST':
#         # Capture a frame from the webcam
#         ret, frame = cap.read()
#
#         # Your face recognition logic goes here
#         login()
#
#     return render_template('login.html')
#
# def register_new_user(self):
#     self.register_new_user_window = tk.Toplevel(self.main_window)
#     self.register_new_user_window.geometry("1200x520+370+120")
#
#     self.accept_button_register_new_user_window = util.get_button(self.register_new_user_window,
#                                                                               text='Accept',
#                                                                               command=self.accept_register_new_user,
#                                                                               color='green')
#     self.accept_button_register_new_user_window.place(x=750, y=300)
#
#     self.try_again_button_register_new_user_window = util.get_button(self.register_new_user_window,
#                                                                                  text='Try again',
#                                                                                  command=self.try_again_register_new_user,
#                                                                                  color='red')
#     self.try_again_button_register_new_user_window.place(x=750, y=400)
#
#     self.capture_label = tk.Label(self.register_new_user_window)
#     self.capture_label.place(x=10, y=0, width=700, height=500)
#
#     self.add_img_to_label(self.capture_label)
#
#     self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
#     self.entry_text_register_new_user.place(x=750, y=150)
#
#     self.text_label_register_new_user = util.get_text_label(self.register_new_user_window,
#                                                                         "please input username")
#     self.text_label_register_new_user.place(x=750, y=70)
#
# @app.route("/face_register", methods=['GET', 'POST'])
# def face_register():
#     if request.method == 'POST':
#         # Capture a frame from the webcam
#         ret, frame = cap.read()
#
#         # Save the captured image with the user's name
#         name = request.form.get('username')
#         if name:
#             img_path = os.path.join(db_dir, '{}.jpg'.format(name))
#             cv2.imwrite(img_path, frame)
#             known_face_names.append(name)
#             # Add face encoding to known_face_encodings (use face_recognition)
#             register_new_user()
#
#     return render_template('register.html')
#
#


if __name__ == '__main__':
    app.run(debug=True)
