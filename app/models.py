from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash

from . import login_manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(255),unique = True,nullable = False)
    email  = db.Column(db.String(255),unique = True,nullable = False)
    secure_password = db.Column(db.String(255),nullable = False)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pitch = db.relationship('Pitch', backref='user', lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.secure_password = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.secure_password,password)


    def __repr__(self):
        return f'User {self.username}'






class Pitch(db.Model):
    __tablename__ = 'pitches'

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255),nullable = False)
    pitch = db.Column(db.Text(), nullable = False)
    category = db.Column(db.String(255), index = True,nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # time = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self):
        return f'User {self.name}' 

