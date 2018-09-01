from flask             import Flask
from flask_login       import LoginManager
from flask_sqlalchemy  import SQLAlchemy
from flask_httpauth    import HTTPBasicAuth
from werkzeug.contrib.cache import SimpleCache
from celery            import Celery
#import locale
#locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)
    class ContextTask(celery.Task):
        abstract = True
        def __call__(self, *args, **kwarg):
            with app.app_context():
                return self.run(*args, **kwarg)
    celery.Task = ContextTask
    return celery

weeka=('月', '火', '水', '木', '金', '土', '日')

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('flaskr.config')
app.config.from_pyfile('config.py', silent=True)
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'auth.login'

auth = HTTPBasicAuth()

db = SQLAlchemy(app)
cache = SimpleCache()

celery = make_celery(app)
celery.conf.update(app.config)

import flaskr.views
import flaskr.models
import flaskr.jobs

