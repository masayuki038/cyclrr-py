from datetime import datetime
from sqlalchemy import ForeignKey
from cyclrr import db

class Counter(db.Model): 
    __tablename__ = 'counter'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    count = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, user_id, count):
        self.user_id = user_id
        self.count = count
        now = datetime.now()
        self.created_at = now
        self.updated_at = now
