from flask         import Blueprint
from flask         import request, redirect, url_for, render_template, flash
from flask_login   import login_required, current_user
from flask_wtf     import FlaskForm
from wtforms       import StringField, PasswordField
from wtforms.validators import DataRequired, EqualTo
from flaskr        import db
from flaskr.validators import Unique
from flaskr.models import User

bp = Blueprint('users', __name__, url_prefix="/users")

class UsersNewForm(FlaskForm):
    userid = StringField('ユーザID', validators=[
            Unique(User, User.userid, message='同一ユーザIDが指定されています'),
            DataRequired(message='必須入力です')
        ])
    password = PasswordField('パスワード', validators=[
            DataRequired(message='必須入力です'),
            EqualTo('confirm', message='パスワードが一致しません')
        ])
    confirm = PasswordField('パスワード再入力')

class UsersPasswdForm(FlaskForm):
    password = PasswordField('パスワード', validators=[
            DataRequired(message='必須入力です'),
            EqualTo('confirm', message='パスワードが一致しません')
        ])
    confirm = PasswordField('パスワード再入力')

@bp.route('/')
@login_required
def index():
    users = User.query.all()
    return render_template('users/index.pug', users=users)

@bp.route('/create', methods=('GET','POST'))
@login_required
def create():
    form = UsersNewForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.set_password(form.password.data)
        db.session.add(user)
        try:
          db.session.commit()
          flash('User created correctly.', 'success')
          return redirect(url_for('users.index'))
        except:
          db.session.rollback()
          flash('Error generating user!', 'danger')
    return render_template('users/create.pug', form=form)


@bp.route('/passwd', methods=('GET','POST'))
@login_required
def passwd():
    form = UsersPasswdForm()
    if form.validate_on_submit():
        user = current_user
        user.set_password(form.password.data)
        db.session.add(user)
        try:
          db.session.commit()
          flash('User change password successfully.', 'success')
          return redirect(url_for('users.index'))
        except:
          db.session.rollback()
          flash('Error change password user!', 'danger')
    return render_template('users/edit.pug', form=form)


@bp.route('/<id>/destroy')
@login_required
def destroy(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    try:
        db.session.commit()
        flash('User delete successfully.', 'success')
    except:
        db.session.rollback()
        flash('Error delete user!', 'danger')
    return redirect(url_for('users.index'))
