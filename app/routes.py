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
    if form.validate_on_submit():
        print(form.data)
        searcher = Searcher.Searcher()
        result = searcher.search(form.data['query'])
        form = SearchForm()
        return render_template('template.html',results=result, form = form)
    return  render_template('template.html',results=[], form = SearchForm())
#
