from flask import Flask, render_template, request, session
from werkzeug.utils import redirect

import hashlib
import datetime

app = Flask(__name__)
app.secret_key = 'aljflajfoAWHAOGAJ'

# HOME PAGE
@app.route('/')
def hello():
    return "hello world"

if __name__ == '__main__':
    app.run()