from flask.cli import AppGroup
from .send_mail import sendmail_run

job = AppGroup('job')
job.add_command(sendmail_run)
