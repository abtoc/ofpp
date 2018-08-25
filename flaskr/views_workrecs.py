from datetime      import datetime
from dateutil.relativedelta import relativedelta
from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash, abort
from flask_login   import login_required
from flask_wtf     import FlaskForm
from wtforms       import StringField,DecimalField
from wtforms.validators import DataRequired, Regexp
from flaskr        import db, weeka, cache
from flaskr.models import Person,WorkRec

bp = Blueprint('workrecs', __name__, url_prefix="/workrecs")

class WorkRecEditForm(FlaskForm):
    situation = StringField('状況')
    work_in  = StringField('開始時刻', 
        validators=[
            Regexp(message='HH:MMで入力してください',regex='^(([0-9]{2}:[0-9]{2})?)?$')
        ])
    work_out = StringField('終了時刻',
        validators=[
            Regexp(message='HH:MMで入力してください',regex='^(([0-9]{2}:[0-9]{2})?)?$')
        ])
    break_t  = StringField('休憩時間',
        validators=[
            Regexp(message='数字で入力してください',regex='^([0-9]+(\.[0-9])?)?$')
        ])
    value    = StringField('勤務時間',
        validators=[
            Regexp(message='数字で入力してください',regex='^([0-9]+(\.[0-9])?)?$')
        ])
    over_t   = StringField('残業時間',
        validators=[
            Regexp(message='数字で入力してください',regex='^([0-9]+(\.[0-9])?)?$')
        ])
    reason   = StringField('欠席理由・備考')

class WorkRecAbsenceForm(FlaskForm):
    situation = StringField('状況')
    break_t  = StringField('休憩時間',
        validators=[
            Regexp(message='数字で入力してください',regex='^([0-9]+(\.[0-9])?)?$')
        ])
    value    = StringField('勤務時間',
        validators=[
            Regexp(message='数字で入力してください',regex='^([0-9]+(\.[0-9])?)?$')
        ])
    over_t   = StringField('残業時間',
        validators=[
            Regexp(message='数字で入力してください',regex='^([0-9]+(\.[0-9])?)?$')
        ])
    reason   = StringField('欠席理由・備考')


def _check_yymmdd(yymm, dd=1):
    if len(yymm) != 6:
        return False
    try:
        yy = int(yymm[:4])
        mm = int(yymm[4:])
        dd = int(dd)
        datetime(yy,mm,dd)
        return True
    except ValueError:
        return False

@bp.route('/<id>')
@bp.route('/<id>/<yymm>')
def index(id,yymm=None):
    if (yymm is not None) and (not _check_yymmdd(yymm)):
        abort(400)
    person   = Person.query.filter_by(id=id).first()
    if person is None:
        abort(404)
    if yymm is None:
        now  = datetime.now()
        yymm = now.strftime('%Y%m')
    else:
        now  = datetime(int(yymm[:4]),int(yymm[4:]),1)
    first    = datetime(now.year, now.month, 1)
    last     = first + relativedelta(months=1)
    prev     = first - relativedelta(months=1)
    items    = []
    head     = dict(
        prev=prev.strftime('%Y%m'), 
        next=last.strftime('%Y%m'),
        idm=person.idm == cache.get('idm')
    )
    foot     = dict(
        sum=0.0,
        count=0,
        avg=0.0
    )
    while first < last:
        item = dict(
            dd=first.day,
            week=weeka[first.weekday()],
            situation=None,
            work_in=None,
            work_out=None,
            value=None,
            reson=None,
            creation=True
        )
        workrec = WorkRec.query.filter_by(person_id=id, yymm=yymm, dd=first.day).first()
        if workrec != None:
            item['situation'] = workrec.situation
            item['work_in']  = workrec.work_in
            item['work_out'] = workrec.work_out
            item['value']    = workrec.value
            item['reson']    = workrec.reason
            item['creation'] = False
            if (workrec.value != None) and (workrec.value != 0.0):
                foot['sum']      = foot['sum'] + workrec.value;
                foot['count']    = foot['count'] + 1
        items.append(item)
        first = first + relativedelta(days=1)
    if foot['count'] > 0:
        foot['avg'] = round(foot['sum'] / foot['count'], 1)
    else:
        foot['avg'] = 0.0
    return render_template('workrecs/index.pug', person=person,items=items,yymm=yymm,head=head,foot=foot)

@bp.route('/<id>/<yymm>/<dd>/create', methods=('GET','POST'))
@login_required
def create(id,yymm,dd):
    if (not _check_yymmdd(yymm,dd=dd)):
        abort(400)
    person   = Person.query.filter_by(id=id).first()
    if person is None:
        abort(404)
    idm      = cache.get('idm')
    if idm != person.idm:
        form = WorkRecAbsenceForm()
    else:
        form = WorkRecEditForm()
    if form.validate_on_submit():
        workrec = WorkRec(person_id=id, yymm=yymm, dd=dd)
        form.populate_obj(workrec)
        if (workrec.situation is not None) and (len(workrec.situation) == 0):
            workrec.situation = None
        if (workrec.work_in is not None) and (len(workrec.work_in) == 0):
            workrec.work_in = None
        if (workrec.work_out is not None) and (len(workrec.work_out) == 0):
            workrec.work_out = None
        if (workrec.value is not None) and (len(workrec.value) == 0):
            workrec.value = None
        if (workrec.break_t is not None) and (len(workrec.break_t) == 0):
            workrec.break_t = None
        if (workrec.over_t is not None) and (len(workrec.over_t) == 0):
            workrec.over_t = None
        if (workrec.reason is not None) and (len(workrec.reason) == 0):
            workrec.reason = None
        db.session.add(workrec)
        try:
            db.session.commit()
            flash('WorkRec saved successfully.', 'success')
            return redirect(url_for('workrecs.index',id=id,yymm=yymm))
        except:
            db.session.rollback()
            flash('Error update workrec!', 'danger')
    return render_template('workrecs/edit.pug',person=person,form=form,yymm=yymm)

@bp.route('/<id>/<yymm>/<dd>/edit', methods=('GET','POST'))
@login_required
def edit(id,yymm,dd):
    person   = Person.query.filter_by(id=id).first()
    if person is None:
        abort(404)
    workrec  = WorkRec.query.filter_by(person_id=id, yymm=yymm,dd=dd).first()
    if workrec is None:
        abort(404)
    idm      = cache.get('idm')
    if idm != person.idm:
        form = WorkRecAbsenceForm(obj=workrec)
    else:
        form = WorkRecEditForm(obj=workrec)
    if form.validate_on_submit():
        form.populate_obj(workrec)
        if len(workrec.situation) == 0:
            workrec.situation = None
        if len(workrec.work_in) == 0:
            workrec.work_in = None
        if len(workrec.work_out) == 0:
            workrec.work_out = None
        if len(workrec.value) == 0:
            workrec.value = None
        if len(workrec.break_t) == 0:
            workrec.break_t = None
        if len(workrec.over_t) == 0:
            workrec.over_t = None
        if len(workrec.reason) == 0:
            workrec.reason = None
        db.session.add(workrec)
        try:
            db.session.commit()
            flash('WorkRec saved successfully.', 'success')
            return redirect(url_for('workrecs.index',id=id,yymm=yymm))
        except:
            db.session.rollback()
            flash('Error update workrec!', 'danger')
    return render_template('workrecs/edit.pug',person=person,form=form,yymm=yymm)

@bp.route('/<id>/<yymm>/<dd>/destroy')
@login_required
def destroy(id,yymm,dd):
    person   = Person.query.filter_by(id=id).first()
    if person is None:
        abort(404)
    idm      = cache.get('idm')
    workrec  = WorkRec.query.filter_by(person_id=id, yymm=yymm, dd=dd).first()
    if (idm != person.idm) and ((workrec is not None) and (workrec.work_in is not None)):
        flash('利用者のICカードをタッチしてください', 'danger')
    if (workrec is not None) and ((idm == person.idm) or (workrec.work_in is None)):
        db.session.delete(workrec)
        try:
            db.session.commit()
            flash('Entry delete successfully.', 'success')
        except:
            db.session.rollback()
            flash('Error delete entry!', 'danger')
    return redirect(url_for('workrecs.index',id=id,yymm=yymm))
