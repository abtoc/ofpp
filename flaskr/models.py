from flask_login import UserMixin
from datetime    import datetime
from werkzeug    import check_password_hash, generate_password_hash
from flaskr      import db
from uuid        import uuid4
import pymysql
pymysql.install_as_MySQLdb()

def _get_now():
    return datetime.now()

def _gen_uuid():
    return str(uuid4())

class Person(db.Model):
    __tablename__ = 'persons'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id        = db.Column(db.String(36), primary_key=True, default=_gen_uuid)
    name      = db.Column(db.String(64), nullable=False)
    display   = db.Column(db.String(64), nullable=False)
    idm       = db.Column(db.String(16), unique=True)
    enabled   = db.Column(db.Boolean,    nullable=False)
    staff     = db.Column(db.Boolean,    nullable=False)
    number    = db.Column(db.String(10), nullable=False)
    amount    = db.Column(db.String(64), nullable=False)
    create_at = db.Column(db.DateTime,   default =_get_now)
    update_at = db.Column(db.DateTime,   onupdate=_get_now)
    def __repr__(self):
        return '<Person id={id},name={name},idm={idm}>'.format(
            id=self.id, name=self.name, idm=self.idm
        )

class WorkRec(db.Model):
    __tablename__ = 'workrecs'
    __table_args__ = (
        (db.UniqueConstraint('yymm', 'dd', 'person_id', name='idx_yymm_dd_id')),
        {'mysql_engine': 'InnoDB'}
    )
    person_id = db.Column(db.String(36), db.ForeignKey('persons.id'), primary_key=True)
    yymm      = db.Column(db.String(8),  primary_key=True)
    dd        = db.Column(db.Integer,    primary_key=True)
    situation = db.Column(db.String(8))
    work_in   = db.Column(db.String(5))
    work_out  = db.Column(db.String(5))
    value     = db.Column(db.Float)
    break_t   = db.Column(db.Float)
    over_t    = db.Column(db.Float)
    reason    = db.Column(db.String(128))
    create_at = db.Column(db.DateTime,   default =_get_now)
    update_at = db.Column(db.DateTime,   onupdate=_get_now)
    def __repr__(self):
        return '<WorkRec id={id},yymm={yymm},dd={dd},in={work_in},out={work_out},val={val}>'.format(
            id=self.person_id, yymm=self.yymm, dd=self.dd, work_in=self.work_in, work_out=self.work_out, val=self.value
        )

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id        = db.Column(db.String(36),  primary_key=True, default=_gen_uuid)
    userid    = db.Column(db.String(20),  nullable=False, unique=True)
    password  = db.Column(db.String(100), nullable=False)
    create_at = db.Column(db.DateTime,    default =_get_now)
    update_at = db.Column(db.DateTime,    onupdate=_get_now)
    def set_password(self, password):
        if password:
            password = password.strip()
        self.password = generate_password_hash(password)
    def check_password(self, password):
        password = password.strip()
        if not password:
            return False
        return check_password_hash(self.password, password)
    @classmethod
    def auth(cls, userid, password):
        user = cls.query.filter_by(userid=userid).first()
        if user is None:
            return None, False
        return user, user.check_password(password)
    def __repr__(self):
        return '<User: id={id},userid={userid},name={name}>'.format(
            id=self.id, userid=self.userid, name=self.name
        )

class Option(db.Model):
    __tablename__ = 'options'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id        = db.Column(db.String(36), primary_key=True, default=_gen_uuid)
    name      = db.Column(db.String(64), nullable=False, unique=True)
    value     = db.Column(db.String(128),nullable=True)
    create_at = db.Column(db.DateTime,    default =_get_now)
    update_at = db.Column(db.DateTime,    onupdate=_get_now)
    @classmethod
    def get(cls,name,value):
        opt = cls.query.filter_by(name=name).first()
        if opt is None:
            return value
        return opt.value
    @classmethod
    def set(cls,name,value):
        opt = cls.query.filter_by(name=name).first()
        if opt is None:
            opt = Option(name=name)
        opt.value = value
        db.session.add(opt)