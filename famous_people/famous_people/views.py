#!/usr/bin/env python
from famous_people import app
from flask import session, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import RadioField, SubmitField

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

class Person(db.Model):
    person_id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(200))
    nationality_id = db.Column('nationality_id', db.Integer)
    occupation_id = db.Column('occupation_id', db.Integer)
    estimated_iq_score = db.Column('estimated_iq_score', db.Integer)


class Agg_func(Form):
    func = RadioField('Choose one', choices=[('All','Everyone'),('USA', 'USA Count'),('Sum','The Sum'),('Avg', 'The Average'),('Bounce', 'Second Highest Avg IQ')])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    func = ''
    form = Agg_func()
    if form.validate_on_submit():
        if form.func.data=='All':
            return redirect(url_for('all'))
        elif form.func.data=='USA':
            return redirect(url_for('usa'))
        elif form.func.data=='Sum':
            return redirect(url_for('sum_ger'))
        elif form.func.data=='Avg':
            return redirect(url_for('avg_pol'))
        elif form.func.data=='Bounce':
            return redirect(url_for('bounce'))
    return render_template('index.html', form=form)


@app.route('/all')
def all():
    form = Agg_func()
    return render_template('all.html', form=form, result=Person.query.all())


@app.route('/USA')
def usa():
    form = Agg_func()
    return render_template('usa.html', form=form, result=Person.query.filter(Person.nationality_id == 25).count())


@app.route('/sum')
def sum_ger():
    form = Agg_func()
    iq_list = [r[0] for r in Person.query.filter(Person.nationality_id == 2).with_entities(Person.estimated_iq_score)]
    sum_res = sum(i for i in iq_list) 
    return render_template('sum.html', form=form, result=Person.query.filter(Person.nationality_id == 2).with_entities(Person.estimated_iq_score), sum_res=sum_res)


@app.route('/avg')
def avg_pol():
    form = Agg_func()
    iq_list = [r[0] for r in Person.query.filter(Person.occupation_id == 14).with_entities(Person.estimated_iq_score)]
    avg_res = float(sum(i for i in iq_list)) / len(iq_list)
    return render_template('avg.html', form=form, result=Person.query.filter(Person.occupation_id == 14).with_entities(Person.estimated_iq_score), avg_res=avg_res)


@app.route('/bounce')
def bounce():
    form = Agg_func()
    iq_list = [list(r) for r in Person.query.with_entities(Person.occupation_id, Person.estimated_iq_score)]
    temp_dict = {}
    count_dict = {}
    avg_dict = {}
    for i in iq_list:
        if i[0] in temp_dict and count_dict:
            temp_dict[i[0]] += i[1]
            count_dict[i[0]] += 1
        else:
            temp_dict[i[0]] = i[1]
            count_dict[i[0]] = 1
    for i in iq_list:
        avg_dict[i[0]] = temp_dict[i[0]] / count_dict[i[0]]
#    list_vals = [[v,k] for k, v in dict.items(avg_dict)]
#    print list_vals
    return render_template('bounce.html', form=form, result=avg_dict)

