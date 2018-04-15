from datetime import datetime
from flaskr import db

def _get_now():
  return datetime.now()

class Entry(db.Model):
    __tablename__ = 'entres'
    id        = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default =_get_now)
    update_at = db.Column(db.DateTime, onupdate=_get_now)
    def __repr__(self):
        return '<Entry id={id}>'.format(
            id=self.id
        )

