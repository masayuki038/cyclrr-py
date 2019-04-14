from flask_restful import Resource, reqparse
from flask import jsonify
from flask import request
from marshmallow import ValidationError

from cyclrr import db
from cyclrr.models.user import User, UserSchema

class UserResource(Resource):

    def get(self, user_id):
        user = db.session.query(User).filter_by(id=user_id).first()
        data = UserSchema(many=False).dump(user).data
        return jsonify(data)


class UserListResource(Resource):

    def post(self):
        #args = self.reqparser.parse_args()
        #user = User(user_name = args.user_name, password = args.password, first_name = args.first_name, last_name = args.last_name, mail = args.mail)
        try:
            js = request.get_json()
            unmarshalled = UserSchema().load(js)
        except ValidationError as err:
            return "ValidationError: " + str(err), 400

        if unmarshalled.errors:
            return "Invalid parameter. errors: " + str(unmarshalled.errors), 400

        user = unmarshalled.data
        db.session.add(user)
        db.session.commit()
        data = UserSchema(many=False).dump(user).data
        return jsonify(data)
