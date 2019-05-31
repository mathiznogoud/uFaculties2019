from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from sqlalchemy.schema import UniqueConstraint

subs = db.Table('subs',
        db.Column('user_id',db.Integer, db.ForeignKey('users.id')),
        db.Column('research_id', db.Integer, db.ForeignKey('researchfields.id'))
        )

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    user_code = db.Column(db.String(100), unique=True,index=True)
    email = db.Column(db.String(100), unique=True, index=True)
    vnu_email = db.Column(db.String(100), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, index=True)
    first_name = db.Column(sqlalchemy.types.NVARCHAR(60), index=True)
    last_name = db.Column(sqlalchemy.types.NVARCHAR(60), index=True)
    phone = db.Column(db.String(100),index=True)
    password_hash = db.Column(db.String(128))
    email_confirmed = db.Column(db.Boolean, default=False)
    email_confirmed_on = db.Column(db.DateTime, default=None)
    is_admin = db.Column(db.Boolean, default=False)
    degree = db.Column(db.String(20),default=None)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    research = db.relationship('ResearchField', secondary=subs, backref=db.backref('research_interest',lazy='dynamic'))

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<email {}'.format(self.email)
        


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Department(db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(60), unique=True)
    name = db.Column(sqlalchemy.types.NVARCHAR(100), unique=True)
    depType = db.Column(sqlalchemy.types.NVARCHAR(100), default=None)
    address = db.Column(db.String(60), default=None)
    phone = db.Column(db.String(60), default=None)
    website = db.Column(db.String(100), default=None)
    user = db.relationship('User', backref='department',
                                lazy='dynamic')
    
    def __repr__(self):
        return '<Department: {}>'.format(self.name)

class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(sqlalchemy.types.NVARCHAR(100), unique=True)
    users = db.relationship('User', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)

class ResearchField(db.Model):

    __tablename__ = "researchfields"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey("researchfields.id") , nullable=True)


    def __repr__(self):
        return '<ResearchField: {}>'.format(self.name)


