from datetime import datetime

from flask_login import login_required
from flask_restful import Resource
from flask import jsonify
from flask import request
from marshmallow import ValidationError

from cyclrr import db
from cyclrr.models.content import Content, ContentSchema

class ContentResource(Resource):

    @login_required
    def get(self, content_id):
        content = db.session.query(Content).filter_by(id=content_id).first()
        data = ContentSchema(many=False).dump(content).data
        return jsonify(data)

    @login_required
    def put(self, content_id):
        try:
            js = request.get_json()
            unmarshalled = ContentSchema().load(js, session=db.session)
        except ValidationError as err:
            return "ValidationError: " + str(err), 400

        if unmarshalled.errors:
            return "Invalid parameter. errors: " + str(unmarshalled.errors), 400

        content = unmarshalled.data
        db.session.commit()

        return "Updated", 200
    
    @login_required
    def delete(self, content_id):
        db.session.query(Content).filter_by(id=content_id).delete()
        db.session.commit()
        return "Deleted", 200

class ContentListResource(Resource):

    @login_required
    def get(self, user_id):
        contents = db.session.query(Content.id, Content.user_id, Content.title, Content.display).\
          filter_by(user_id=user_id).all()
        data = ContentSchema(many=True).dump(contents).data
        return jsonify(data)

    @login_required
    def post(self):
        try:
            js = request.get_json()
            unmarshalled = ContentSchema().load(js)
        except ValidationError as err:
            return "ValidationError: " + str(err), 400

        if unmarshalled.errors:
            return "Invalid parameter. errors: " + str(unmarshalled.errors), 400

        content = unmarshalled.data
        now = datetime.now()
        content.created_at = now
        content.updated_at = now
        db.session.add(content)
        db.session.commit()
        data = ContentSchema(many=False).dump(content).data
        return jsonify(data)
