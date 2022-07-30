from flask import Flask, render_template, request, session
from werkzeug.utils import redirect

import hashlib
import datetime

from DB import db, query as q

KEY = 'aljflajfoAWHAOGAJ'


app = Flask(__name__)
app.secret_key = KEY

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
    if request.method == "POST":
        usn = request.form['USN']
        password = request.form['Password']
        name = request.form['Name']
        email = request.form['Email']
        section = request.form['Section']
        branch = request.form['Branch']
        c_password = request.form['Confirm Password']

        # password hash
        dk = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), b'salt', 100000)
       
        section_id = db.fetch(conn, q.get_section_id.format(section))
        sectionId = section_id[0][0]

        if password == c_password:
            db.execute(conn,q.add_new_student.format(sectionId, usn, name, dk.hex(), email, branch))
            return redirect("/student_login")
        else:
            return redirect("/student_signup")
    else:
        return render_template("student_signup.html")

@app.route('/faculty_signup', methods=['GET', 'POST'])
def faculty_signup():
    """
    returns the faculty signup page with option to signup for the college
    """
    if request.method == "POST":
        name = request.form['Name']
        email = request.form['Email']
        department = request.form['Department']
        password = request.form['Password']
        c_password = request.form['Confirm Password']
        dk = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), b'salt', 100000)

        if password == c_password:
            db.execute(conn, q.add_new_teacher.format(
                name, dk.hex(), email, department))
            return redirect("/faculty_login")
        else:
            return redirect("/faculty_signup")
    else:
        return render_template("faculty_signup.html")


@app.route('/student_login', methods=['GET', 'POST'])
def student_login():
    """
    returns the login page for students
    """
    if request.method == 'POST':
        usn = request.form['USN']
        password = request.form['Password']
        hash_pw = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), b'salt', 100000)

        fetch_pw = db.fetch(conn, q.get_student_pw.format(usn))[0][0]
        if fetch_pw == hash_pw.hex():
            print("login sucessful!!")
            session['username'] = usn
            return redirect('/student')
        else:
            return render_template('student_login.html')
    else:
        return render_template('student_login.html')

@app.route('/faculty_login', methods=['GET', 'POST'])
def faculty_login():
    """
    returns login page for faculty
    """
    if request.method == 'POST':
        name = request.form['Name']
        password = request.form['Password']
        hash_pw = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), b'salt', 100000)
        fetch_pw = db.fetch(conn, q.get_teacher_pw.format(name))[0][0]
        if fetch_pw == hash_pw.hex():
            print('login successfull!!!')
            return redirect('/faculty')
        else:
            return render_template('faculty_login.html')
    else:
        return render_template('faculty_login.html')
        
@app.route('/admin_login')
def admin_login():
    """
    returns the admin login page
    """
    if request.method == 'POST':
        password = request.form['Password']
        if password == 'admin':
            return render_template('control.html')
        else:
            return render_template('admin_login.html')
    else:
        return render_template('admin_login.html')

@app.route('/logout')
def logout():
    if session['username']:
        session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug = True)
    db.close(conn)