#!/usr/bin/env python
from flask import Flask #, session, render_template, redirect, url_for
#from flask_bootstrap import Bootstrap
#from flask_sqlalchemy import SQLAlchemy
#from flask.ext.wtf import Form
#from wtforms import RadioField, SubmitField

app = Flask(__name__, instance_relative_config=True)
#app.config.from_object('config')
app.config.from_pyfile('config.py')
#bootstrap = Bootstrap(app)
#db = SQLAlchemy(app)

import famous_people.views
