from datetime import datetime
from flask_marshmallow.fields import fields
from flask_login import UserMixin

from cyclrr import db, ma, login_manager

class User(db.Model, UserMixin): 
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(32))
    password = db.Column(db.String(64))
    first_name = db.Column(db.String(32))
    last_name = db.Column(db.String(32))
    mail = db.Column(db.String(256))
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user_name, password, first_name, last_name, mail):
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.mail = mail
        now = datetime.now()
        self.created_at = now
        self.modified_at = now

@login_manager.user_loader
def load_user(id):
    return db.session.query(User).filter_by(id=id).first()

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
    
    created_at = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%dT%H:%M:%S')

