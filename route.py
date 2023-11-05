import subprocess
import tkinter as tk
from flask import Flask, render_template, url_for, flash, redirect,request
from forms import RegistrationForm, LoginForm

import os
#import util

app = Flask(__name__)

app.config['SECRET_KEY'] = 'krishna'

@app.route("/")
def home():
    return render_template('home.html', title='Home')

@app.route("/stress")
def stress():
    return render_template('stress-test.html', title='Stress')

@app.route("/questionaire")
def questionaire():
    return render_template('questionaire.html', title='Questionaire')

@app.route("/dropdown")
def dropdown():
    return render_template('dropdown.html', title='Dropdown')

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

@app.route("/profiles", methods=['GET', 'POST'])
def profiles():
    form = RegistrationForm()
    return render_template('profiles.html', title='Profiles', form=form)





if __name__ == '__main__':
    app.run(debug=True)
