from flask_restful import Resource
from flask import request, jsonify
from flask_login import login_user, logout_user
from marshmallow import Schema, ValidationError, fields, pprint
from sqlalchemy import and_

from cyclrr import db, ma
from cyclrr.models.user import User

class UserTokenResource(Resource):

    def post(self):
        try:
            js = request.get_json()
            unmarshalled = UserTokenSchema().load(js)
        except ValidationError as err:
            return "Failed to login: " + str(err), 401
    
        if unmarshalled.errors:
            return "Failed to login", 401
        
        login_name = unmarshalled.data['user_name']
        login_password = unmarshalled.data['password']
        u = db.session.query(User).filter(User.user_name == login_name, User.password == login_password).first()
        if u is not None:
            login_user(u)
            return "Logined", 200
        else:
            return "Failed to login", 401

    def delete(self):
        logout_user()
        
class UserTokenSchema(Schema):
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)
