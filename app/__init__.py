from flask import Flask, request, jsonify
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from flask_mail import Mail
from flask_mysqldb import MySQL
import pymysql, os, json
# local imports
from config import app_config


# db variable initialization
config_name = os.getenv('FLASK_CONFIG')
app = Flask(__name__, instance_relative_config=True)
app.config.from_object(app_config[config_name])
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)
engine = create_engine('mysql://uf_admin:uF_admin2019#@localhost/uFaculties_db')
db_session=(scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine)))
mysql = pymysql.connect("localhost","uf_admin","uF_admin2019#","uFaculties_db")

app.url_map.strict_slashes = False

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

from .api import api as api_blueprint
app.register_blueprint(api_blueprint)

from .user import user as user_blueprint
app.register_blueprint(user_blueprint)


#@app.route('/api/test')
#def get():
#    cur = mysql.cursor()
#
#    query = "select * from departments"
#
#    cur.execute(query)
#    
#    r = [dict((cur.description[i][0], value)
#              for i, value in enumerate(row)) for row in cur.fetchall()]
#
#    return jsonify({'myCollection' : r})
@app.route('/api/test/test')
def Index():
    db1 = pymysql.connect("localhost","uf_admin","uF_admin2019#","uFaculties_db")
    cursor = db1.cursor()

    query = "select * from researchfields"

    cursor.execute(query)
    tuples = cursor.fetchall()
    cur = db1.cursor()

    keys = ["id", "name", "parent_id"]

    answer = [{k: v for k, v in zip(keys, tup)} for tup in tuples]
    
    return jsonify(answer)
