from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash, abort
from flask_login   import login_required
from flask_wtf     import FlaskForm
from wtforms       import StringField, BooleanField
from wtforms.validators import DataRequired, Regexp
from sqlalchemy    import func
from flaskr        import db
from flaskr.models import Person,WorkRec
from sqlalchemy.exc import IntegrityError

bp = Blueprint('persons', __name__, url_prefix="/persons")

class PersonForm(FlaskForm):
    name = StringField('名前', validators=[
            DataRequired(message='必須入力です')
        ])
    idm    = StringField('IDM')
    enabled = BooleanField('有効化', default='checked')
    staff   = BooleanField('職員')
    number  = StringField('受給者番号',
        validators=[
            Regexp(message='数字10桁で入力してください',regex='^[0-9]{10}$')
        ])
    amount  = StringField('契約支給量',
        validators=[
            DataRequired(message='入力必須です')
        ])

@bp.route('/')
@login_required
def index():
    persons = Person.query.order_by(Person.name.desc()).all()
    return render_template('persons/index.pug', persons=persons)

@bp.route('/create', methods=('GET','POST'))
@login_required
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
@login_required
def edit(id):
    person = Person.query.filter_by(id=id).first()
    if person is None:
      abort(404)
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
@login_required
def destroy(id):
    person = Person.query.filter_by(id=id).first()
    if person is None:
      abort(404)
    q=db.session.\
        query(func.count(WorkRec.yymm)).\
        filter_by(person_id=id).\
        group_by(WorkRec.person_id).first()
    if q is not None:
        flash('このユーザは勤怠データが存在しています', 'danger')
        return redirect(url_for('persons.index'))
    db.session.delete(person)
    try:
        db.session.commit()
        flash('Person delete successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error delete person!', 'danger')
    return redirect(url_for('persons.index'))
