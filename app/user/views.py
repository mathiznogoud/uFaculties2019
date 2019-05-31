from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from ..models import User
from . import user
from flask_mysqldb import MySQL
from .. import app
import pymysql

@user.route('/profile/<email>')
@login_required
def Profile(email):
    user = User.query.filter_by(email=email).first()
    return render_template('user/profile.html', user=user)