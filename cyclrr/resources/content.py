from datetime import datetime

from flask_login import login_required, current_user
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
        if content is None:
            return "Content Not Found", 404
        
        if content.user_id != int(current_user.get_id()):
            return "Permission Denied", 403

        data = ContentSchema(many=False).dump(content).data
        return jsonify(data)

    @login_required
    def put(self, content_id):
        try:
            js = request.get_json()
            unmarshalled = ContentSchema().load(js, session=db.session)
            
            if unmarshalled.errors:
                db.session.rollback()
                return "Invalid parameter. errors: " + str(unmarshalled.errors), 400
            
            if unmarshalled.data.user_id != int(current_user.get_id()):
                db.session.rollback()
                return "Permission Denied", 403

            db.session.commit()
        except ValidationError as err:
            return "ValidationError: " + str(err), 400
        except Exception as err:
            db.session.rollback()
            return "Error: " + str(err), 500


        return "Updated", 200
    
    @login_required
    def delete(self, content_id):
        try:
            content = db.session.query(Content).filter_by(id=content_id)
            if content.first().user_id != int(current_user.get_id()):
                db.session.rollback()
                return "Permission Denied", 403

            content.delete()
            db.session.commit()
            return "Deleted", 200
        except Exception as err:
            db.session.rollback()
            return "Error: " + str(err), 500

class ContentListResource(Resource):

    @login_required
    def get(self):
        contents = db.session.query(Content.id, 
                                    Content.user_id, 
                                    Content.title, 
                                    Content.display).\
          filter_by(user_id=current_user.get_id()).all()
        data = ContentSchema(many=True).dump(contents).data
        return jsonify(data)

    @login_required
    def post(self):
        try:
            js = request.get_json()
            unmarshalled = ContentSchema().load(js)
            
            if unmarshalled.errors:
                db.session.rollback()
                return "Invalid parameter. errors: " + str(unmarshalled.errors), 400

            content = unmarshalled.data
            if content.user_id != int(current_user.get_id()):
                db.session.rollback()
                return "Permission Denied", 403

            now = datetime.now()
            content.created_at = now
            content.updated_at = now
            db.session.add(content)
            db.session.commit()

            data = ContentSchema(many=False).dump(content).data
            return jsonify(data)
        except ValidationError as err:
            db.session.rollback()
            return "ValidationError: " + str(err), 400
        except Exception as err:
            db.session.rollback()
            return "Error: " + str(err), 500
