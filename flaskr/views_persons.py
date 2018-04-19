from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash
from flask_wtf     import FlaskForm
from wtforms       import StringField, BooleanField
from wtforms.validators import DataRequired
from flaskr        import db
from flaskr.models import Person
from sqlalchemy.exc import IntegrityError

bp = Blueprint('persons', __name__, url_prefix="/persons")

class PersonForm(FlaskForm):
    name = StringField('名前', validators=[
            DataRequired(message='必須入力です')
        ])
    idm = StringField('IDM')
    staff = BooleanField('職員')

@bp.route('/')
def index():
    persons = Person.query.all()
    return render_template('persons/index.pug', persons=persons)

@bp.route('/create', methods=('GET','POST'))
def create():
    form = PersonForm()
    if form.validate_on_submit():
        person = Person()
        form.populate_obj(person)
        if person.idm == '':
            person.idm = None
        db.session.add(person)
        try:
          db.session.commit()
          flash('Person created correctly.', 'success')
          return redirect(url_for('persons.index'))
        except IntegrityError:
          db.session.rollback()
          flash('同一IDMが指定された可能性が有ります', 'danger')
        except:
          db.session.rollback()
          flash('Error generating person!', 'danger')
    return render_template('persons/create.pug', form=form)

@bp.route('/<id>/edit', methods=('GET','POST'))
def edit(id):
    person = Person.query.filter_by(id=id).first()
    form = PersonForm(obj=person)
    if form.validate_on_submit():
        form.populate_obj(person)
        if person.idm == '':
            person.idm = None
        db.session.add(person)
        try:
          db.session.commit()
          flash('Person saved successfully.', 'success')
          return redirect(url_for('persons.index'))
        except IntegrityError:
          db.session.rollback()
          flash('同一IDMが指定された可能性が有ります', 'danger')
        except:
          db.session.rollback()
          flash('Error update person!', 'danger')
    return render_template('persons/edit.pug', form=form)

@bp.route('/<id>/destroy')
def destroy(id):
    person = Person.query.filter_by(id=id).first()
    db.session.delete(person)
    try:
        db.session.commit()
        flash('Person delete successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error delete person!', 'danger')
    return redirect(url_for('persons.index'))
