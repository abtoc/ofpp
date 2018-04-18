from datetime import datetime
from flaskr import db
import pymysql
pymysql.install_as_MySQLdb()

def _get_now():
  return datetime.now()

class Person(db.Model):
    __tablename__ = 'persons'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    id        = db.Column(db.Integer, primary_key=True)
    name      = db.Column(db.String(64), nullable=False)
    idm       = db.Column(db.String(16), unique=True)
    staff     = db.Column(db.Boolean, nullable=False)
    create_at = db.Column(db.DateTime, default =_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)
    def __repr__(self):
        return '<Person id={id} name={name} idm={idm}>'.format(
            id=self.id, name=self.name, idm=self.idm
        )

class WorkRec(db.Model):
    __tablename__ = 'workrecs'
    __table_args__ = {'mysql_engine': 'InnoDB'}
    person_id = db.Column(db.Integer, primary_key=True)
    yymm      = db.Column(db.String(8), primary_key=True)
    dd        = db.Column(db.Integer, primary_key=True)
    work_in   = db.Column(db.String(5))
    work_out  = db.Column(db.String(5))
    value     = db.Column(db.Float)
    reason    = db.Column(db.String(128))
    create_at = db.Column(db.DateTime, default =_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)
    def __repr__(self):
        return '<WorkRec id={id} yymm={yymm} dd={dd} in={work_in} out={work_out} val={val}>'.format(
            id=self.person_id, yymm=self.yymm, dd=self.dd, work_in=self.work_in, work_out=self.work_out, val=self.value
        )
