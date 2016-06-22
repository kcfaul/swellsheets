#!/usr/bin/env python2.7

import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from core import create_app
from core.models import db, User

env = os.environ.get('APP_SETTINGS', 'dev')
app = create_app('config.{}Config'.format(env.capitalize()))

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User)

if __name__ == '__main__':
    manager.run()
