from flask import Blueprint

departments = Blueprint('departments', __name__)

from . import views