from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import locale
locale.setlocale(locale.LC_TIME, 'ja_JP.UTF-8')

app = Flask(__name__)
app.config.from_object('flaskr.config')
app.jinja_env.add_extension('pypugjs.ext.jinja.PyPugJSExtension')

db = SQLAlchemy(app)

import flaskr.views
import flaskr.models
