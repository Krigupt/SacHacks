import subprocess
import tkinter as tk
from flask import Flask, render_template, url_for, flash, redirect,request
from forms import RegistrationForm, LoginForm
import random
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np

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

@app.route("/questionaire", methods=['POST', 'GET'])
def questionaire():
    if request.method == 'POST':
        name = request.form.get('name')
        gender = request.form.get('gender')
        occupation = request.form.get('occupation')

        qtags = ['Q' + str(x) for x in range(1, 26)]

        results = [name, gender, occupation]

        for tag in qtags:
            results.append(request.form.get(tag))
        
        print(results)
        
        df = pd.read_csv('data-final.csv', sep='\t') 
        questions = pd.DataFrame(df, columns=['EXT1', 'EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT6', 'EXT7', 'EXT8', 'EXT9',
       'EXT10', 'EST1', 'EST2', 'EST3', 'EST4', 'EST5', 'EST6', 'EST7', 'EST8',
       'EST9', 'EST10', 'AGR1', 'AGR2', 'AGR3', 'AGR4', 'AGR5'])
        
        for i in questions.columns:
            questions[i].fillna(questions[i].mean(), inplace=True)

        temp = []
        for i in results[3:]:
            if not i:
                temp.append(2.5)
            else:
                temp.append(i)
            
        print(temp)

        nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(questions)

        input_data = pd.DataFrame([temp], columns=['EXT1', 'EXT2', 'EXT3', 'EXT4', 'EXT5', 'EXT6', 'EXT7', 'EXT8', 'EXT9',
       'EXT10', 'EST1', 'EST2', 'EST3', 'EST4', 'EST5', 'EST6', 'EST7', 'EST8',
       'EST9', 'EST10', 'AGR1', 'AGR2', 'AGR3', 'AGR4', 'AGR5'])

        distance, indices = nbrs.kneighbors(input_data)

        print([x for x in indices[0]])

        return redirect(url_for('profiles',))
    
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
    print(request.method)
    form = RegistrationForm()
    return render_template('profiles.html', title='Profiles', form=form)





if __name__ == '__main__':
    app.run(debug=True, port=8000)