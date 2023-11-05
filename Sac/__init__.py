import os
from flask_socketio import SocketIO
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = "KRISHNA"
socketio = SocketIO(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:kv0309//@localhost/Sac'
##THIS IS A COMMAND FOR SQL to connext with XAMPP
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/fashion_classifier'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'krishnaguptapyrax4@gmail.com'
app.config['MAIL_PASSWORD'] = 'wjgzztvfjbtegtcn'

mail = Mail(app)



from Sac import route

