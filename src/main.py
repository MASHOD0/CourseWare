from flask import Flask, render_template, request, session
from werkzeug.utils import redirect

import hashlib
import datetime

app = Flask(__name__)
app.secret_key = 'aljflajfoAWHAOGAJ'

# HOME PAGE
@app.route('/')
def home():
    """
    returns the base home page, with login options
    """
    return render_template('home.html')

@app.route('/student_signup')
def student_signup():
    """
    returns the student signup page, with option to signup for the courseware
    """
    # TODO

def faculty_signup():
    """
    returns the faculty signup page with option to signup for the college
    """
    # TODO

def student_login():
    """
    returns the login page for students
    """
    # TODO

def faculty_login():
    """
    returns login page for faculty
    """
    # TODO

def admin_login():
    """
    returns the admin login page
    """
    # TODO

if __name__ == '__main__':
    app.run()