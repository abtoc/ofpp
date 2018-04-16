from flask         import request, redirect, url_for, render_template, flash
from flaskr        import app,db

@app.route('/')
def index():
    return redirect(url_for('entres.index'))

from flaskr  import views_entres
app.register_blueprint(views_entres.bp)
