from flask         import request, redirect, url_for, render_template, flash
from flask_wtf     import FlaskForm
from wtforms       import StringField, TextAreaField
from wtforms.validators import DataRequired
from flaskr        import app,db
from flaskr.models import Entry

class EntryForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    text  = TextAreaField('text')

@app.route('/')
def index():
    return redirect(url_for('entres_index'))

#    flash('Success Hello World.', 'success')
#    flash('Error Hello World!!',  'danger')

@app.route('/entres')
def entres_index():
    entres = Entry.query.all()
    return render_template('index.pug', entres=entres)

@app.route('/entres/create', methods=['GET','POST'])
def entres_create():
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
    return render_template('create.pug', form=form)

@app.route('/menu/<id>')
def menu(id):
    return redirect(url_for('index'))
