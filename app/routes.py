from app import app
from flask import Response, send_file, request,render_template,redirect,flash
import json
from FinalProject import Searcher
import os

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class SearchForm(FlaskForm):
    query = StringField('Your query')
    submit = SubmitField('Search IT!')

@app.route('/', methods =['GET', 'POST'])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        print(form.data)
        searcher = Searcher.Searcher()
        result = searcher.search(form.data['query'])
        form = SearchForm()
        return render_template('index.html',results=result, form = form)
    return  render_template('index.html',results=[], form = SearchForm())
