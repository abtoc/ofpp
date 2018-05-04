#!/usr/bin/env python
from flask_script  import Manager
from flask_migrate import Migrate, MigrateCommand
from getpass       import getpass
from flaskr        import app, db
from flaskr.models import User

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

@manager.command
def admin():
    """ Admin password settings """
    p1 = getpass('Enter new admin password: ')
    p2 = getpass('Retype new admin password: ')
    if p1 != p2:
        print('Authentication token manipulation error')
        print('password unchanged')
        return
    user = User.query.filter_by(userid='admin').first()
    if user is None:
        user = User(userid='admin')
    user.set_password(p1)
    db.session.add(user)
    try:
        db.session.commit()
        print('password updated successfully')
    except:
        print('password unchanged')
        db.session.rollback()

@manager.command
def reset(userid):
    """ Reset user password  """
    user = User.query.filter_by(userid=userid).first()
    if user is None:
        print('User not found!')
        return
    user.set_password('password')
    db.session.add(user)
    try:
        db.session.commit()
        print('password reset successfully')
    except:
        print('password unchanged')
        db.session.rollback()


if __name__ == '__main__':
    manager.run()
