from flask         import request, redirect, url_for, render_template, flash
from flaskr        import app,db

@app.route('/')
def index():
    return redirect(url_for('persons.index'))

from flaskr  import views_persons
app.register_blueprint(views_persons.bp)
from flaskr  import views_workrecs
app.register_blueprint(views_workrecs.bp)
from flaskr  import api_idm
app.register_blueprint(api_idm.bp)
