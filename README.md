Flask Template
====

## pip

```
pip install -r requirements.txt
```


## Database Migration
### Initialize

```
python manage.py db init
```

### Migration
```
python manage.py db migrate
python manage.py db upgrade
```

## Flask-SQLAlchemy
### CREATE
```python
from flaskr import db

try:
    entry = Entry(hoge1=value1,hoge2=value2)
    db.session.add(entry)
    db.session.commit()
except:
    db.session.rollback()
```

### READ ALL
```python
from flaskr import db

entres = Entry.query.all()
```
### READ&UPDATE
```python
from flaskr import db

try:
    entry = Entry.query.filter_by(id=id).first()
    db.session.add(entry)
    db.session.commit()
except:
    db.session.rollback()
```

### READ&DELETE
```python
from flaskr import db

try:
    entry = Entry.query.filter_by(id=id).first()
    db.session.delete(entry)
    db.session.commit()
except:
    db.session.rollback()
```

## Start Application

```
python manage.py runserver
```

https://ofpp01.herokuapp.com/
