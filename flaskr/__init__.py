from flask             import Flask
from flask_login       import LoginManager
from flask_sqlalchemy  import SQLAlchemy
from flask_apscheduler import APScheduler
#import locale
#locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

weeka=('月', '火', '水', '木', '金', '土', '日')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('flaskr.config')
app.config.from_pyfile('config.py', silent=True)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'

db = SQLAlchemy(app)

scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

import flaskr.views
import flaskr.models
import flaskr.jobs

