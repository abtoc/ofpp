from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash, abort
from flask_login   import login_required
from flask_wtf     import FlaskForm
from wtforms       import StringField, BooleanField, DateField, HiddenField
from wtforms.validators import DataRequired, Required, Regexp, Optional, ValidationError
from sqlalchemy    import func
from flaskr        import db
from flaskr.models import Person,WorkRec
from flaskr.validators import RequiredNotIf, RegexpNotIf
from sqlalchemy.exc import IntegrityError

bp = Blueprint('persons', __name__, url_prefix="/persons")

class UniqueIDM(object):
    def __init__(self, message='This element already exists.'):
        self.message = message
    def __call__(self, form, field):
        if len(field.data) == 0:
            return
        id = form._fields.get('id')
        if id is None:
            raise Exception('no field named "id" in form')
        check = Person.query.filter(Person.idm == field.data, Person.id != id.data).first()
        if check:
            raise ValidationError(self.message)

class PersonForm(FlaskForm):
    id   = HiddenField('id')
    name = StringField('名前', validators=[
            DataRequired(message='必須入力です')
        ])
    display = StringField('表示名', validators=[
            DataRequired(message='必須入力です')
        ])
    idm    = StringField('IDM',
        validators=[
            UniqueIDM(message='同一IDMが指定されています')
        ])
    enabled = BooleanField('有効化', default='checked')
    staff   = BooleanField('職員')
    number  = StringField('受給者番号',
        validators=[
            RegexpNotIf('staff', message='数字10桁で入力してください',regex='^[0-9]{10}$')
        ])
    amount  = StringField('契約支給量',
        validators=[
            RequiredNotIf('staff', message='入力必須です')
        ])
    usestart = DateField('利用開始日(YYYY-MM-DDで入力してください)',
        validators=[
            Optional()
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
        person.populate_form(form)
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
        person.populate_form(form)
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
