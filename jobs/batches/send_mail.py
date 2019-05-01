import click
from datetime import datetime
from flask.cli import with_appcontext
from sqlalchemy import and_

from cyclrr import db
from cyclrr.models.user import User
from cyclrr.models.content import Content
from cyclrr.models.counter import Counter
from jobs import app

@click.command('sendmail', help="Send next content by mail")
@with_appcontext
def sendmail_run():
    users = db.session.query(User).all()
    for user in users:
        counter = db.session.query(Counter).filter_by(user_id=user.id).first()
        if counter is None:
            counter = Counter(user.id, 0)
            db.session.add(counter)

        contents = db.session.query(Content).\
            filter(and_(Content.user_id==user.id, Content.display==True)).\
            order_by(Content.id).\
            all()
        app.logger.info('title: ' + contents[counter.count].title)
        app.logger.info('content: ' + contents[counter.count].content)
        app.logger.info('counter.count: ' + str(counter.count))
        app.logger.info('len(contents): ' + str(len(contents)))
        
        if counter.count < len(contents) - 1:
            counter.count += 1
        else:
            counter.count = 0
        counter.updated_at = datetime.now()

        db.session.commit()
