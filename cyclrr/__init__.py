import os
import sys
import logging

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from flask_restful import Resource, Api
from flask_login import LoginManager

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()

def setup(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    db.init_app(app)
    Migrate(app, db)
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)

    from cyclrr.resources.user import UserResource, UserListResource
    from cyclrr.resources.user_token import UserTokenResource
    from cyclrr.resources.content import ContentResource, ContentListResource
    
    api = Api(app)
    api.add_resource(UserResource, '/users/<int:user_id>')
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserTokenResource, '/user/token')
    api.add_resource(ContentResource, '/content/<int:content_id>')
    api.add_resource(ContentListResource, '/contents', '/contents/<int:user_id>')

    login_manager.init_app(app)
    app.secret_key = 'DWcrTq&r!dNr+vdHy~sTA($_~n|aYSCMr/ndKFdW'
    
    return app