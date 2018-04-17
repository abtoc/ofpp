from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash
from flask_wtf     import FlaskForm
from wtforms       import StringField
from wtforms.validators import DataRequired
from flaskr        import db
from flaskr.models import Person

bp = Blueprint('persons', __name__, url_prefix="/persons")

class PersonForm(FlaskForm):
    name = StringField('名前', validators=[DataRequired()])

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
        db.session.add(person)
        try:
          db.session.commit()
          flash('Person created correctly.', 'success')
          return redirect(url_for('persons.index'))
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
        db.session.add(person)
        try:
          db.session.commit()
          flash('Entry saved successfully.', 'success')
          return redirect(url_for('persons.index'))
        except:
          db.session.rollback()
          flash('Error update entry!', 'danger')
    return render_template('persons/edit.pug', form=form)

@bp.route('/<id>/destroy')
def destroy(id):
    person = Person.query.filter_by(id=id).first()
    db.session.delete(person)
    try:
        db.session.commit()
        flash('Entry delete successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error delete entry!', 'danger')
    return redirect(url_for('persons.index'))
