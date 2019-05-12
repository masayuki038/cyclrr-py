from datetime import datetime
from flask_marshmallow.fields import fields
from marshmallow_sqlalchemy import field_for
from sqlalchemy import ForeignKey

from cyclrr import db, ma

class Content(db.Model): 
    __tablename__ = 'contents'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    title = db.Column(db.String(256))
    content = db.Column(db.Text())
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    display = db.Column(db.Boolean, default=True)

    def __init__(self, user_id, title, content, display):
        self.user_id = user_id
        self.title = title
        self.content = content
        now = datetime.now()
        self.created_at = now
        self.updated_at = now
        self.display = display

class ContentSchema(ma.ModelSchema):
    class Meta:
        model = Content

    id = field_for(Content, 'id', dump_only=False)
    user_id = field_for(Content, 'user_id', dump_only=False)
    created_at = fields.DateTime('%Y-%m-%dT%H:%M:%S')
    updated_at = fields.DateTime('%Y-%m-%dT%H:%M:%S')