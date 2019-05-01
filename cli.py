from flask import Flask
from cyclrr import create_app
from jobs import job

app = Flask(__name__, static_url_path='', template_folder='static')

app = create_app(app)
app.cli.add_command(job)