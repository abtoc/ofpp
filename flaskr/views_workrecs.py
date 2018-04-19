from datetime      import datetime
from dateutil.relativedelta import relativedelta
from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash
from flask_wtf     import FlaskForm
from wtforms       import StringField,DecimalField
from wtforms.validators import DataRequired, Regexp
from flaskr        import db
from flaskr.models import Person,WorkRec

bp = Blueprint('workrecs', __name__, url_prefix="/workrecs")

class WorkRecCreateForm(FlaskForm):
    work_in  = StringField('開始時刻',
        validators=[
            DataRequired(message='必須入力です'),
            Regexp(message='HH:MMで入力してください',regex='^[0-9]{2}:[0-9]{2}$')
        ])
    reason   = StringField('他')

class WorkRecEditForm(FlaskForm):
    work_in  = StringField('開始時刻', 
        validators=[
            DataRequired(message='必須入力です'),
            Regexp(message='HH:MMで入力してください',regex='^[0-9]{2}:[0-9]{2}$')
        ])
    work_out = StringField('終了時刻',
        validators=[
            DataRequired(message='必須入力です'),
            Regexp(message='HH:MMで入力してください',regex='^[0-9]{2}:[0-9]{2}$')
        ])
    value    = DecimalField('勤務時間', 
        validators=[
            DataRequired(message='必須入力です')
        ])
    reason   = StringField('欠席理由・備考')

@bp.route('/<id>')
@bp.route('/<id>/<yymm>')
def index(id,yymm=None):
    person   = Person.query.filter_by(id=id).first()
    if yymm == None:
        now  = datetime.now()
        yymm = now.strftime('%Y%m')
    else:
        now  = datetime(int(yymm[:4]),int(yymm[4:]),1)
    first    = datetime(now.year, now.month, 1)
    last     = first + relativedelta(months=1)
    items    = []
    foot     = dict(
        sum=0.0,
        count=0,
        avg=0.0
    )
    while first < last:
        item = dict(
            dd=first.day,
            week=first.strftime('%a'),
            work_in=None,
            work_out=None,
            value=None,
            reson=None,
            creation=True
        )
        workrec = WorkRec.query.filter_by(person_id=id, yymm=yymm, dd=first.day).first()
        if workrec != None:
            item['work_in']  = workrec.work_in
            item['work_out'] = workrec.work_out
            item['value']    = workrec.value
            item['reson']    = workrec.reason
            item['creation'] = False
            if workrec.value != None:
                foot['sum']      = foot['sum'] + workrec.value;
                foot['count']    = foot['count'] + 1
        items.append(item)
        first = first + relativedelta(days=1)
    if foot['count'] > 0:
        foot['avg'] = foot['sum'] / foot['count']
    return render_template('workrecs/index.pug', person=person,items=items,yymm=yymm,foot=foot)

@bp.route('/<id>/<yymm>/<dd>/create', methods=('GET','POST'))
def create(id,yymm,dd):
    person   = Person.query.filter_by(id=id).first()
    form     = WorkRecCreateForm()
    if form.validate_on_submit():
        workrec = WorkRec(person_id=id, yymm=yymm, dd=dd)
        form.populate_obj(workrec)
        db.session.add(workrec)
        try:
            db.session.commit()
            flash('WrkRec saved successfully.', 'success')
            return redirect(url_for('workrecs.index',id=id,yymm=yymm))
        except:
            db.session.rollback()
            flash('Error update workrec!', 'danger')
    return render_template('workrecs/edit.pug',person=person,form=form,yymm=yymm)

@bp.route('/<id>/<yymm>/<dd>/edit', methods=('GET','POST'))
def edit(id,yymm,dd):
    person   = Person.query.filter_by(id=id).first()
    workrec  = WorkRec.query.filter_by(person_id=id, yymm=yymm,dd=dd).first()
    form     = WorkRecEditForm(obj=workrec)
    if form.validate_on_submit():
        form.populate_obj(workrec)
        db.session.add(workrec)
        try:
            db.session.commit()
            flash('WrkRec saved successfully.', 'success')
            return redirect(url_for('workrecs.index',id=id,yymm=yymm))
        except:
            db.session.rollback()
            flash('Error update workrec!', 'danger')
    return render_template('workrecs/edit.pug',person=person,form=form,yymm=yymm)

@bp.route('/<id>/<yymm>/<dd>/destroy')
def destroy(id,yymm,dd):
    workrec  = WorkRec.query.filter_by(person_id=id, yymm=yymm, dd=dd).first()
    if workrec != None:
        db.session.delete(workrec)
        try:
            db.session.commit()
            flash('Entry delete successfully.', 'success')
        except:
            db.session.rollback()
            flash('Error delete entry!', 'danger')
    return redirect(url_for('workrecs.index',id=id,yymm=yymm))
