from flask import Flask, render_template, request, session
from werkzeug.utils import redirect

import hashlib
import datetime

from DB import db, query as q

methods = ['GET', 'POST']
USERNAME = 'username'
EMAIL = 'Email'
PASSWORD = 'Passoword'
POST = 'POST'
USN = 'USN'
NAME = 'Name'
KEY = 'aljflajfoAWHAOGAJ'
SECTION = 'Section'
BRANCH = 'Branch'
CPASSWORD = 'Confirm Password'
DEPARTMENT = 'Department'
COURSE = 'Course'
LINK = 'Link'
DAY = 'Day'
TIME = 'Time'
EXAM = 'Exam'
SEMESTER = 'Semester'
ATTENDANCE = 'Attendance'
SECTION_COURSE = 'Section_Course'
ABSENTEE = 'absentee'


app = Flask(__name__)
app.secret_key = KEY
conn = db.fypDB_Connect()

# HOME PAGE


@app.route('/')
def home():
    """
    returns the base home page, with login options
    """
    return render_template('home.html')


@app.route('/student_signup', methods=methods)
def student_signup():
    """
    returns the student signup page, with option to signup for the courseware
    """
    if request.method == POST:
        usn = request.form[USN]
        password = request.form[PASSWORD]
        name = request.form[NAME]
        email = request.form[EMAIL]
        section = request.form[SECTION]
        branch = request.form[BRANCH]
        c_password = request.form[CPASSWORD]

        # password hash
        dk = hashlib.pbkdf2_hmac('sha256', bytes(
            password, 'utf-8'), b'salt', 100000)

        section_id = db.fetch(conn, q.get_section_id.format(section))
        sectionId = section_id[0][0]

        if password == c_password:
            db.execute(conn, q.add_new_student.format(
                sectionId, usn, name, dk.hex(), email, branch))
            return redirect("/student_login")
        else:
            return redirect("/student_signup")
    else:
        return render_template("student_signup.html")


@app.route('/faculty_signup', methods=methods)
def faculty_signup():
    """
    returns the faculty signup page with option to signup for the college
    """
    if request.method == POST:
        name = request.form[NAME]
        email = request.form[EMAIL]
        department = request.form[DEPARTMENT]
        password = request.form[PASSWORD]
        c_password = request.form[CPASSWORD]
        dk = hashlib.pbkdf2_hmac('sha256', bytes(
            password, 'utf-8'), b'salt', 100000)

        if password == c_password:
            db.execute(conn, q.add_new_teacher.format(
                name, dk.hex(), email, department))
            return redirect("/faculty_login")
        else:
            return redirect("/faculty_signup")
    else:
        return render_template("faculty_signup.html")


@app.route('/student_login', methods=methods)
def student_login():
    """
    returns the login page for students
    """
    if request.method == POST:
        usn = request.form[USN]
        password = request.form[PASSWORD]
        hash_pw = hashlib.pbkdf2_hmac(
            'sha256', bytes(password, 'utf-8'), b'salt', 100000)

        fetch_pw = db.fetch(conn, q.get_student_pw.format(usn))[0][0]
        if fetch_pw == hash_pw.hex():
            print("login sucessful!!")
            session[USERNAME] = usn
            return redirect('/student')
        else:
            return render_template('student_login.html')
    else:
        return render_template('student_login.html')


@app.route('/faculty_login', methods=methods)
def faculty_login():
    """
    returns login page for faculty
    """
    if request.method == POST:
        name = request.form[NAME]
        password = request.form[PASSWORD]
        hash_pw = hashlib.pbkdf2_hmac(
            'sha256', bytes(password, 'utf-8'), b'salt', 100000)
        fetch_pw = db.fetch(conn, q.get_teacher_pw.format(name))[0][0]
        if fetch_pw == hash_pw.hex():
            session[USERNAME] = name
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
    if request.method == POST:
        password = request.form[PASSWORD]
        if password == 'admin':
            return render_template('control.html')
        else:
            return render_template('admin_login.html')
    else:
        return render_template('admin_login.html')


@app.route('/student', methods=methods)
def student():
    """
    Returns the student home page
    """
    if session[USERNAME]:
        now = datetime.datetime.now()
        day = now.strftime('%A')
        classes = db.fetch(conn, q.get_classes.format(
            session[USERNAME], day))
        grades = db.fetch(conn, q.get_grades.format(session[USERNAME]))
        attendance_list = db.fetch(
            conn, q.get_attendance.format(session[USERNAME]))
        attendance_percent = []
        for i in range(len(attendance_list)):
            if attendance_list[i][1] == None:
                percent = 1
            else:
                percent = (
                    (attendance_list[i][2] - attendance_list[i][1]) / attendance_list[i][2])
            attendance_percent.append(percent * 100)

        return render_template('student.html', classes=classes, class_len=len(classes), grades=grades, grade_len=len(grades), 
        list=attendance_list, percent=attendance_percent, list_len=len(attendance_list))
    else:
        return redirect('/student_login')


@app.route('/faculty')
def faculty():
    if session[USERNAME]:
        # getting the day
        now = datetime.datetime.now()
        day = now.strftime("%A")
        classes = db.fetch(conn, q.get_teacher_cls.format(
            session[USERNAME], day))
        return render_template('faculty.html', classes=classes, name=session[USERNAME], class_len=len(classes))
    else:
        return redirect('/faculty_login')


@app.route("/schedule", methods=methods)
def schedule():
    """
    Page for scheduling classes
    """
    # getting `courses` list
    getcourses = db.fetch(conn, q.get_all_courses)
    courses = []
    for i in range(len(getcourses)):
        if getcourses != None:
            courses.append(getcourses[i][0])

    if session[USERNAME]:
        if request.method == POST:
            if session[USERNAME]:
                section = request.form[SECTION]
                n = int(request.form[COURSE])
                course = courses[n]
                link = request.form[LINK]
                day = request.form[DAY]
                time = request.form[TIME]
                section_id = db.fetch(conn, q.get_section_id.format(section))
                teacher_id = db.fetch(
                    conn, q.get_teacher_id.format(session[USERNAME]))
                course_id = db.fetch(conn, q.get_courseId.format(course))

                db.execute(conn, q.add_class.format(
                    section_id[0][0], course_id[0][0], link, day, time, teacher_id[0][0]))

                return redirect('/faculty')
            else:
                return redirect('/faculty_login')
        else:

            return render_template("schedule.html", courses=courses, course_len=len(courses))
    else:
        return redirect('/faculty_login')


@app.route('/grades', methods=methods)
def grades():
    """
    Returns page to select class section and exam to enter grades in
    """
    if session[USERNAME]:
        get_section_subject = db.fetch(conn, q.get_section_from_grades)
        if request.method == POST:
            session[SECTION] = int(request.form['section_course'])
            session[EXAM] = request.form[EXAM]
            return redirect('/grades1')
        else:
            return render_template('grades.html', list=get_section_subject, list_len=len(get_section_subject))
    else:
        return redirect('/faculty_login')



@app.route('/logout')
def logout():
    if session[USERNAME]:
        session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    db.close(conn)
