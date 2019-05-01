import sys
import logging

from cyclrr import setup
from jobs import job, create_app

app = create_app()
app = setup(app)

app.cli.add_command(job)