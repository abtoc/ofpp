from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash
from flask_wtf     import FlaskForm
from wtforms       import StringField, TextAreaField
from wtforms.validators import DataRequired
from flaskr        import db
from flaskr.models import Entry

bp = Blueprint('entres', __name__, url_prefix="/entres")

class EntryForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    text  = TextAreaField('text')

@bp.route('/')
def index():
    entres = Entry.query.all()
    return render_template('entres/index.pug', entres=entres)

@bp.route('/create', methods=['GET','POST'])
def create():
    form = EntryForm()
    if form.validate_on_submit():
        entry = Entry()
        form.populate_obj(entry)
        db.session.add(entry)
        try:
          db.session.commit()
          flash('Entry created correctly.', 'success')
          return redirect(url_for('index'))
        except:
          db.session.rollback()
          flash('Error generating entry!', 'danger')
    return render_template('entres/create.pug', form=form)
