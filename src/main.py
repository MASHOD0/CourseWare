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

@app.route('/student_signup', methods=['GET', 'POST'])
def student_signup():
    """
    returns the student signup page, with option to signup for the courseware
    """
    # TODO

@app.route('/faculty_signup', methods=['GET', 'POST'])
def faculty_signup():
    """
    returns the faculty signup page with option to signup for the college
    """
    # TODO

@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    """
    returns the login page for students
    """
    # TODO

@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    """
    returns login page for faculty
    """
    # TODO

@app.route('admin_login', methods=['GET', 'POST'])
def admin_login():
    """
    returns the admin login page
    """
    # TODO



if __name__ == '__main__':
    app.run()