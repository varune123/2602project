from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Email
from wtforms.fields.html5 import EmailField
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()
import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    routines = db.relationship('Routines', backref='user', lazy=True)

    def toDict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password
        }


    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Exercise(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100))
    difficulty= db.Column(db.String(20))
    description= db.Column(db.String(5000))
    equipment_needed= db.Column(db.String(20))
    equipment= db.Column(db.String(100))
    primary_muscle= db.Column(db.String(100))
    secondary_muscle= db.Column(db.String(100))
    routines = db.relationship('Routines', backref='exercise', lazy=True)

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
            'description': self.description,
            'equipment_needed': self.equipment_needed,
            'equipment': self.equipment,
            'primary_muscle': self.primary_muscle,
            'secondary_muscle': self.secondary_muscle,
            'routines': self.routines
        }

class Routines(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100), unique=True ,nullable=False) #name of routine
    exerciseId= db.Column(db.Integer, db.ForeignKey('exercise.id'), nullable=False) #exercises saved in routine
    userId= db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) #keep track of user that created routine

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'exerciseId': self.exerciseId,
            'userId': self.userId
        }

class SignUp(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    email = EmailField('email', validators=[Email(), InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm  = PasswordField('Repeat Password')
    submit = SubmitField('Sign Up', render_kw={'class': 'btn waves-effect waves-light white-text'})

class LogIn(FlaskForm):
    username = StringField('username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])
    submit = SubmitField('Login', render_kw={'class': 'btn waves-effect waves-light white-text'})