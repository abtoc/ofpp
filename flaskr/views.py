from flask import request, redirect, url_for, render_template, flash
from flaskr import app,db
#from flask import Entry

@app.route('/')
def index():
    flash('Success Hello World.', 'success')
    flash('Error Hello World!!',  'danger')
    return render_template('index.pug',message="Hello World!!!!")

@app.route('/menu/<id>')
def menu(id):
    return redirect(url_for('index'))
