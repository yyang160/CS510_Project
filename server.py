import os
import json
from flask import Flask, Response, send_file, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/submit/", methods=['GET', 'POST'])
def save_result():
    if not os.path.exists(os.path.join(os.getcwd(), 'relevance_judgement')):
        os.makedirs(os.path.join(os.getcwd(), 'relevance_judgement'))
    os.chdir(os.path.join(os.getcwd(), 'relevance_judgement'))
    json_data = request.get_data(as_text=True)
    with open('data.txt', 'w') as outfile:
        json.dump(json_data, outfile)