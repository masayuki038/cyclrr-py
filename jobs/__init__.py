from flask import Flask
from flask.cli import AppGroup

app = Flask(__name__)

def create_app():
    return app

from .batches.send_mail import sendmail_run

job = AppGroup('job')
job.add_command(sendmail_run)