from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, Form
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Department, Role

class DepartmentForm(FlaskForm):
    """
    Form for admin to add or edit a department
    """
    name = StringField('Name', validators=[DataRequired()])
    code = StringField('Code', validators=[DataRequired()])
    address = StringField('Address',validators=[DataRequired()])
    depType = StringField('DepartmentType',validators=[DataRequired()])
    phone = StringField('Phone',validators=[DataRequired()])
    website = StringField('Website',validators=[DataRequired()])
    submit = SubmitField('Submit')

class RoleForm(FlaskForm):
    """
    Form for admin to add or edit a role
    """
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UserAssignForm(FlaskForm):
    """
    Form for admin to assign departments and roles to user
    """
    department = QuerySelectField(query_factory=lambda: Department.query.all(),
                                  get_label="name")
    role = QuerySelectField(query_factory=lambda: Role.query.all(),
                            get_label="name")
    submit = SubmitField('Submit')

class DepartmentSearchFilter(FlaskForm):
    depType = SelectField('Department Type',choices=[('Bộ môn','Bộ môn')])
    submit = SubmitField('Submit')

class UserEditForm(FlaskForm):
    first_name = StringField('First name',validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    vnu_email = StringField('Email',validators=[DataRequired()])
    degree = SelectField('Degree: ',choices=[('ThS','ThS'),('TS','TS'),('PGS.TS','PGS.TS'),('GS.TS','GS,TS'),('CN','CN')])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    """
    """
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired()])
    vnu_email = StringField('VNU Email',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    first_name = StringField('First name',validators=[DataRequired()])
    last_name = StringField('Last name',validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    degree = SelectField('Degree',choices=[('ThS','ThS'),('TS','TS'),('PGS.TS','PGS.TS'),('GS.TS','GS,TS'),('CN','CN')])
    submit = SubmitField('Submit')