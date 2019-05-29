#!flask/bin/python

from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from scenarios import *
from rules import *
from table import *

if(__name__ == "__main__"):
    app.run(host='0.0.0.0', port=5000)
