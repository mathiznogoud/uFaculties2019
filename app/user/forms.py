from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, Form
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Role

class UserAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to user
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')