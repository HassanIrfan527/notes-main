from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hello, webdesign-notes-flask-html-css-js-password'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Users.db'

db = SQLAlchemy(app)
# db.init_app(app)

bcrypt = Bcrypt(app)
# bcrypt.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)


from Website import routes
from Website import models

@login_manager.user_loader
def load_user(id):
    return models.Users.query.get(int(id))