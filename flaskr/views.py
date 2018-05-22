from flask         import request, redirect, url_for, render_template, flash
from flaskr        import app,db
from flaskr.models import Person

@app.route('/')
def index():
    persons = Person.query.filter_by(enabled=True).order_by(Person.name.desc()).all()
    return render_template('index.pug', persons=persons)
    #return redirect(url_for('persons.index'))

@app.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"]        = "DENY"
    response.headers["X-XSS-Protection"]       = "1; mode=block"
    response.headers["X-Content-Type-Options"] = "nosniff"
    return response

from flaskr  import views_persons
app.register_blueprint(views_persons.bp)
from flaskr  import views_workrecs
app.register_blueprint(views_workrecs.bp)
from flaskr  import api_idm
app.register_blueprint(api_idm.bp)
from flaskr  import views_pdf
app.register_blueprint(views_pdf.bp)
from flaskr  import views_auth
app.register_blueprint(views_auth.bp)
from flaskr  import views_users
app.register_blueprint(views_users.bp)
from flaskr  import views_options
app.register_blueprint(views_options.bp)
