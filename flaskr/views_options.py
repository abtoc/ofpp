from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash, abort
from flask_login   import login_required
from flask_wtf     import FlaskForm
from wtforms       import StringField, BooleanField
from wtforms.validators import DataRequired, Regexp
from sqlalchemy    import func
from flaskr        import db
from flaskr.models import Option

bp = Blueprint('options', __name__, url_prefix="/options")

class OptionForm(FlaskForm):
    office_number  = StringField('事業所番号',
        validators=[
            Regexp(message='数字10桁で入力してください',regex='^[0-9]{10}$')
        ])
    office_name = StringField('事業者及びその事業所', validators=[
            DataRequired(message='必須入力です')
        ])

@bp.route('/', methods=('GET','POST'))
@login_required
def index():
    form = OptionForm()
    if form.validate_on_submit():
        Option.set('office_number', form.office_number.data)
        Option.set('office_name',   form.office_name.data)
        try:
            db.session.commit()
            flash('Option saved successfully.', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            flash('Error update option!', 'danger')
    else:
        form.office_number.data = Option.get('office_number','')
        form.office_name.data   = Option.get('office_name', '')
    return render_template('options/edit.pug', form=form)

