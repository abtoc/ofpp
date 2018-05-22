from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash
from flask_wtf     import FlaskForm
from flask_login   import login_user, logout_user
from wtforms       import StringField, PasswordField
from wtforms.validators import DataRequired
from flaskr        import lm, db
from flaskr.models import User

bp = Blueprint('auth', __name__, url_prefix="/auth")

@lm.user_loader
def load_user(id):
    return User.query.get(id)

class LoginForm(FlaskForm):
    userid   = StringField('ログインID')
    password = PasswordField('パスワード')

@bp.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user, checked = User.auth(form.userid.data, form.password.data)
        if checked:
            login_user(user)
            return redirect(request.args.get("next") or url_for("index"))
        flash('ユーザIDまたはパスワードが違います', 'danger')
        return render_template('auth/login.pug', form=form), 401
    return render_template('auth/login.pug', form=form)

@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
