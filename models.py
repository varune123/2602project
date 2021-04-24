from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

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

    def toDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty,
            'description': self.description,
            'equipment_needed': self.equipment_needed,
            'equipment': self.equipment,
            'primary_muscle': self.primary_muscle,
            'secondary_muscle': self.secondary_muscle
        }