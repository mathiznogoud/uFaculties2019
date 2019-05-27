from flask import Flask, request, jsonify
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
import pymysql
# local imports
from config import app_config

# db variable initialization
config_name = os.getenv('FLASK_CONFIG')
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')

db = SQLAlchemy(app)

login_manager = LoginManager()
db.init_app(app)

login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"
migrate = Migrate(app, db)

Bootstrap(app)
mail = Mail(app)
from app import models

from .home import home as home_blueprint
app.register_blueprint(home_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .admin import admin as admin_blueprint
app.register_blueprint(admin_blueprint)

db1 = pymysql.connect("localhost","uf_admin","uF_admin2019#","uFaculties_db")

cursor = db1.cursor()

query = "select * from researchfields"

cursor.execute(query)
result = {}
result = cursor.fetchall()



@app.route('/', methods=['GET'])
def home():
    return 'test'


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/resources/books/all', methods=['GET'])
def api_all():
    

    return jsonify(result)