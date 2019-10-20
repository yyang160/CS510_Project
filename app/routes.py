from app import app
from flask import Response, send_file, request,render_template,redirect,flash
import json
import Searcher
import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    query = StringField('Your query')
    submit = SubmitField('Search it')

@app.route('/', methods =['GET', 'POST'])
def index():
    form = SearchForm()
    print(form.data)
    print(form.validate_on_submit())
    if form.validate_on_submit():
        flash('Login requested for user  remember_me=')
        return redirect('/search/{}'.format((form.query.data)))
    return  render_template('template.html',results=[], form = SearchForm())

@app.route("/search/<query>", methods=['GET', 'POST'])
def search(query):
    searcher = Searcher.Searcher()
    print(query)
    result = searcher.search(query)
    form = SearchForm()
    form.query.default = query
    return render_template('template.html',results=result, form = form)
