import json
from flask_cors import CORS
from flask_login import LoginManager, current_user, login_user, login_required, logout_user
from flask import Flask, request, render_template, redirect, flash, url_for, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 


from models import db, Exercise, User, SignUp, Routines, LogIn #add application models

''' Begin boilerplate code '''

''' Begin Flask Login Functions '''
login_manager = LoginManager()
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

''' End Flask Login Functions '''

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) # uncomment if using flsk jwt
  CORS(app)
  login_manager.init_app(app) # uncomment if using flask login
  db.init_app(app)
  return app

app = create_app() 

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here (if using flask JWT)'''
def authenticate(uname, password):
    #search for the specified user
    user = User.query.filter_by(username=uname).first()
    #if user is found and password matches
    if user and user.check_password(password):
        return user

#Payload is a dictionary which is passed to the function by Flask JWT
def identity(payload):
    return User.query.get(payload['identity'])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

@app.route('/', methods=['GET'])
def index():
  form = LogIn()
  return render_template('login.html', form=form)


@app.route('/signup', methods=['GET'])
def signup():
    form = SignUp() # create form object
    return render_template('signup.html', form=form) # pass form object to template

@app.route('/signup', methods=['POST'])
def signupAction():
    form = SignUp() # create form object
    if form.validate_on_submit():
        data = request.form # get data from form submission
        newuser = User(username=data['username'], email=data['email']) # create user object
        newuser.set_password(data['password']) # set password
        db.session.add(newuser) # save new user
        db.session.commit()
        flash('Account Created!')# send message
        return redirect(url_for('index'))# redirect to login page
    flash('Error invalid input!')
    return redirect(url_for('signup')) 

@app.route('/login', methods=['POST'])
def loginAction():
  form = LogIn()
  if form.validate_on_submit(): # respond to form submission
      data = request.form
      user = User.query.filter_by(username = data['username']).first()
      if user and user.check_password(data['password']): # check credentials
        flash('Logged in successfully.') # send message to next page
        login_user(user) # login the user
        return redirect(url_for('home')) # redirect to main page if login successful
  flash('Invalid credentials')
  return redirect(url_for('index'))

@app.route('/home')
@login_required
def home():
    return render_template('home.html')    

@app.route('/exercises')
@login_required
def exercises():
    exerciseList = Exercise.query.all()
    exerciseList = [row.toDict() for row in exerciseList]
    return render_template('exercises.html', exerciseList=exerciseList, option=2)

@app.route('/exercises/<id>')
@login_required
def get_exercises(id):
    exercise = Exercise.query.get(id)
    exercise = exercise.toDict()
    return render_template('exercises.html', exerciseList=exercise, option=1)

@app.route('/routines')
@login_required
def get_routines():
    routines= []
    routines = Routines.query.all()
    routines = routines.toDict()
    return render_template('routines.html', routinesList=routines, option=2)

@app.route('/myroutines')
@login_required
def get_myroutines():
    routines= []
    routines = Routines.query.get(current_user.id)
    routines = routines.toDict()
    return render_template('routines.html', routinesList=routines, option=1)


@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  flash('Logged Out!')
  return redirect(url_for('index')) 

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
