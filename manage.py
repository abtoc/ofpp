#!/usr/bin/env python
from flask_script  import Manager
from flask_migrate import Migrate, MigrateCommand
from getpass       import getpass
from flaskr        import app, db
from flaskr.models import User, Person, Option, WorkRec

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

@manager.command
def export():
    persons = Person.query.all()
    for p in persons:
        sql = 'INSERT INTO persons(id, name, display, idm, enabled, staff,create_at,update_at) VALUES ({},{},{},{},{},{},{},{});'.format(
            '"{}"'.format(p.id),
            '"{}"'.format(p.name),
            '"{}"'.format(p.display) if bool(p.display) or (p.name != p.display) else 'NULL',
            '"{}"'.format(p.idm) if bool(p.idm) else 'NULL',
            '1' if p.enabled else '0',
            '1' if p.staff else '0',
            '"{}"'.format(p.create_at) if bool(p.create_at) else 'NULL',
            '"{}"'.format(p.update_at) if bool(p.update_at) else 'NULL'
        )
        print(sql)
        if not p.staff:
            sql = 'INSERT INTO recipients(person_id, number, amount, usestart, create_at) VALUES ({},{},{},{},{});'.format(
                '"{}"'.format(p.id),
                '"{}"'.format(p.number),
                '"{}"'.format(p.amount),
                '"{}"'.format(p.usestart) if bool(p.usestart) else 'NULL',
                '"{}"'.format(p.create_at) if bool(p.create_at) else 'NULL',
            )
            print(sql)
    print('COMMIT;')
    users = User.query.all()
    for u in users:
        if u.userid == 'admin':
            continue
        sql = 'INSERT INTO users(id, enabled, userid, password, create_at, update_at) VALUES({},1,{},{},{},{});'.format(
            '"{}"'.format(u.id),
            '"{}"'.format(u.userid),
            '"{}"'.format(u.password),
            '"{}"'.format(u.create_at) if bool(p.create_at) else 'NULL',
            '"{}"'.format(u.update_at) if bool(p.update_at) else 'NULL'
        )
        print(sql)
    print('COMMIT;')
    options = Option.query.all()
    for o in options:
        sql = 'INSERT INTO options(id, name, value, create_at, update_at) VALUES({},{},{},{},{});'.format(
            '"{}"'.format(o.id),
            '"{}"'.format(o.name),
            '"{}"'.format(o.value),
            '"{}"'.format(o.create_at) if bool(p.create_at) else 'NULL',
            '"{}"'.format(o.update_at) if bool(p.update_at) else 'NULL'
        )
        print(sql)
    print('COMMIT;')

@manager.command
def export2():
    workrecs = WorkRec.query.filter(WorkRec.export == False).all()
    for w in workrecs:
        person = Person.get(w.person_id)
        if not person.staff:
            sql = 'INSERT INTO performlogs(person_id, yymm, dd, enabled, absence, absence_add, work_in, work_out, remarks, create_at, update_at) VALUES({},{},{},{},{},{},{},{},{},{},{});'.format(
                '"{}"'.format(w.person_id),
                '"{}"'.format(w.yymm),
                w.dd,
                1 if w.enabled else 0,
                1 if w.situation == '欠席' else 0,
                0,
                '"{}"'.format(w.work_in) if bool(w.work_in) else 'NULL',
                '"{}"'.format(w.work_out) if bool(w.work_out) else 'NULL',
                '"{}"'.format(w.reason) if bool(w.reason) else 'NULL',
                '"{}"'.format(w.create_at) if bool(w.create_at) else 'NULL',
                '"{}"'.format(w.update_at) if bool(w.update_at) else 'NULL'
            )
            print(sql)
        sql = 'INSERT INTO worklogs(person_id, yymm, dd, work_in, work_out, value, break_t, over_t, absence, create_at, update_at) VALUES({},{},{},{},{},{},{},{},{},{},{});'.format(
                '"{}"'.format(w.person_id),
                '"{}"'.format(w.yymm),
                w.dd,
                '"{}"'.format(w.work_in) if bool(w.work_in) else 'NULL',
                '"{}"'.format(w.work_out) if bool(w.work_out) else 'NULL',
                'NULL',
                'NULL',
                'NULL',
                1 if w.situation == '欠席' else 0,
                '"{}"'.format(w.create_at) if bool(w.create_at) else 'NULL',
                '"{}"'.format(w.update_at) if bool(w.update_at) else 'NULL'
        )
        print(sql)
        w.export = True
        db.session.add(w)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(e)
    print('COMMIT;')
     
if __name__ == '__main__':
    manager.run()
