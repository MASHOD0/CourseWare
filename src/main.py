from flask import Flask, render_template, request, session
from werkzeug.utils import redirect
import PyPDF2
import os
import time

import hashlib
import datetime

from DB import db, query as q

methods = ['GET', 'POST']
USERNAME = 'username'
EMAIL = 'Email'
PASSWORD = 'Password'
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
UPLOAD_FOLDER = 'uploads'
FILE = 'file'
FACULTY_PATH = '/faculty'
FACULTY_LOGIN_PATH = '/faculty_login'
COURSE_CODE = 'Course Code'

app = Flask(__name__)
app.secret_key = KEY
app.config['SESSION_TYPE'] = 'filesystem'
CONTROL_PAGE = "control.html"
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
    departments = db.fetch(conn, q.get_all_depts)
    sections = db.fetch(conn, q.get_all_sections)
    if request.method == POST:
        usn = request.form[USN]
        password = request.form[PASSWORD]
        name = request.form[NAME]
        email = request.form[EMAIL]
        sectionId = request.form[SECTION]
        branch = request.form[BRANCH]
        c_password = request.form[CPASSWORD]

        # password hash
        dk = hashlib.pbkdf2_hmac('sha256', bytes(
            password, 'utf-8'), b'salt', 100000)


        if password == c_password and len(password) > 8:
            db.execute(conn, q.add_new_student.format(
                sectionId, usn, name, dk.hex(), email, int(branch)))
            return redirect("/student_login")
        else:
            return redirect("/student_signup")
    else:
        return render_template("student_signup.html", departments=departments, sections=sections)


@app.route('/faculty_signup', methods=methods)
def faculty_signup():
    """
    returns the faculty signup page with option to signup for the college
    """
    departments = db.fetch(conn, q.get_all_depts)
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
                department, name, dk.hex(), email))
            return redirect("/faculty_login")
        else:
            return redirect("/faculty_signup")
    else:
        return render_template("faculty_signup.html", departments=departments)


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

        fetch_pw = db.fetch(conn, q.get_student_pw.format(usn))
        pw = fetch_pw[0][0]
        if pw == hash_pw.hex():
            print("login sucessful!!")
            session[USERNAME] = usn
            return redirect('/student')
        else:
            return render_template('student_login.html')
    else:
        return render_template('student_login.html')


@app.route(FACULTY_LOGIN_PATH, methods=methods)
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
            return redirect(FACULTY_PATH)

        else:
            return render_template('faculty_login.html')
    else:
        return render_template('faculty_login.html')


@app.route('/admin_login', methods=methods)
def admin_login():
    """
    returns the admin login page
    """
    if request.method == POST:
        password = request.form[PASSWORD]
        if password == 'admin':
            return render_template(CONTROL_PAGE)
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
            day, session[USERNAME]))
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


@app.route(FACULTY_PATH)
def faculty():
    if session[USERNAME]:
        # getting the day
        now = datetime.datetime.now()
        day = now.strftime("%A")
        classes = db.fetch(conn, q.get_teacher_cls.format(
            session[USERNAME], day))
        return render_template('faculty.html', classes=classes, name=session[USERNAME], class_len=len(classes))
    else:
        return redirect(FACULTY_LOGIN_PATH)


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

                return redirect(FACULTY_PATH)
            else:
                return redirect(FACULTY_LOGIN_PATH)
        else:

            return render_template("schedule.html", courses=courses, course_len=len(courses))
    else:
        return redirect(FACULTY_LOGIN_PATH)


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
        return redirect(FACULTY_LOGIN_PATH)


@app.route('/grades1', methods=methods)
def grades1():
    """
    Returns page to enter the grades of a particular class and subject
    """
    if session[USERNAME]:
        section = session[SECTION]
        exam = session[EXAM]
        get_section_subject = db.fetch(conn, q.get_section_from_grades)
        get_usn = db.fetch(conn, q.get_section_usn.format[section][0])
        print(get_usn)
        if request.method == POST:
            for i in range(len(get_usn)):
                marks = int(request.form[str(i)])
                db.execute(conn, q.update_grades.format(
                    exam, marks, get_usn[i][0]))

            return redirect('/grades')
        else:
            return render_template("grades1.html", usn=get_usn, usn_len=len(get_usn))
    else:
        return redirect(FACULTY_LOGIN_PATH)


@app.route('/update', methods=methods)
def update():
    if session[USERNAME]:
        # getting the list of courses
        courses_and_ids = db.fetch(conn, q.get_courses)
        courses = []
        course_id = []

        for i in range(len(courses_and_ids)):
            courses.append(courses_and_ids[i][1])
        for i in range(len(courses_and_ids)):
            course_id.append(courses_and_ids[i][0])

        # getting the list of sections
        sections_and_ids = db.fetch(conn, q.get_sections)
        section_id = []
        sections = []

        for i in range(len(sections_and_ids)):
            section_id.append(sections_and_ids[i][0])
        for i in range(len(sections_and_ids)):
            sections.append(sections_and_ids[i][1])

        if request.method == POST:
            section_id = int(request.form[SECTION])
            course_id = int(request.form[COURSE])
            semester = int(request.form[SEMESTER])
            student_id = db.fetch(conn, q.get_section.format(section_id))

            for i in range(len(student_id)):
                db.execute(conn, q.add_student_to_grades.format(
                    student_id[i][0], course_id, semester, section_id))
                print("student added to grades")

            for i in range(len(student_id)):
                db.execute(conn, q.add_student_to_attendance.format(
                    student_id[i][0], course_id, section_id))
                print("student added to attendance")

            return redirect('/faculty')
        else:
            return render_template("update.html", section_id=section_id, sections=sections,
                                   sect_len=len(sections), course_id=course_id, course=courses, course_len=len(courses))
    else:
        return redirect(FACULTY_LOGIN_PATH)


@app.route('/attendance', methods=methods)
def attendance():
    """
    Returns a page to select class and subject to give attendance to
    """
    if session[USERNAME]:
        get_section_subject = db.fetch(conn, q.get_section_from_attendance)
        if request.method == POST:
            session[ATTENDANCE] = int(request.form[SECTION_COURSE])
            return redirect('/attendance1')
        else:
            return render_template("attendance.html", list=get_section_subject, list_len=len(get_section_subject))
    else:
        return redirect(FACULTY_LOGIN_PATH)



@app.route('/attendance1', methods=methods)
def attendance1():
    if session[USERNAME]:
        section = session[ATTENDANCE]
        get_section_subject = db.fetch(conn, q.get_section_from_attendance)
        get_usn = db.fetch(conn, q.get_section_name.format(
            get_section_subject[section][0], get_section_subject[section][1]))
        print(get_usn)
        if request.method == POST:
            absentee = request.form.getlist(ABSENTEE)
            absentee = [int(i) for i in absentee]

            print(absentee)
            for i in range(len(get_usn)):
                db.execute(conn, q.add_total.format(
                    total, get_usn[i][0], get_section_subject[section][1], get_section_subject[section][0]))
            for i in range(len(absentee)):
                missed = db.fetch(conn, q.get_missed.format(
                    get_usn[absentee[i]][0], get_section_subject[section][1], get_section_subject[section][0]))
                missed_int = missed[0][0]
                if missed_int == None:
                    missed_int = 1
                else:
                    missed_int += 1
                db.execute(conn, q.add_missed.format(
                    missed_int, get_usn[absentee[i]][0], get_section_subject[section][1], get_section_subject[section][0]))

            return redirect('/grades')
        else:
           return render_template("attendance1.html", usn_list=get_usn, usn_len=len(get_usn))
    else:
        return redirect(FACULTY_LOGIN_PATH)

# @app.route('/add_material', methods=methods)
# def add_material():
#     """
#     Returns a page where the user inputs a pdf file which gets watermarked using `watermark()`
#     and gets stored at a local folder
#     """
#     if session[USERNAME]:
#         if request.method == POST:
#             file = request.files[FILE]
#             file.save(os.path.join(app.config[UPLOAD_FOLDER], file.filename))
#             watermark(os.path.join(app.config[UPLOAD_FOLDER], file.filename))
#             db.execute(conn, q.add_material.format(session[USERNAME], file.filename))
#             return redirect('/faculty')
#         else:
#             return render_template("add_material.html")
#     else:
#         return redirect(FACULTY_LOGIN_PATH)




@app.route("/create_sections", methods=methods)
def sections():
    departments = db.fetch(conn, q.get_all_depts)
    if request.method == POST:
        department = request.form[DEPARTMENT]
        name = request.form[SECTION]
        sem = int(request.form[SEMESTER])
        db.execute(conn, q.add_sections.format(department, sem, name))
        return render_template(CONTROL_PAGE)
    else:
        return render_template("create_sections.html", departments=departments)


@app.route("/create_courses", methods=methods)
def courses():
    departments = db.fetch(conn, q.get_all_depts)
    if request.method == POST:
        course = request.form[COURSE]
        course_code = request.form[COURSE_CODE]
        department = request.form[DEPARTMENT]
        db.execute(conn, q.add_courses.format(department, course, course_code))
        return render_template(CONTROL_PAGE)
    else:
        return render_template("create_courses.html", departments=departments)

@app.route("/create_departments", methods=methods)
def departments():
    if request.method == POST:
        department = request.form[DEPARTMENT]
        db.execute(conn, q.add_departments.format(department))
        return render_template(CONTROL_PAGE)
    else:
        return render_template("create_department.html")

@app.route('/logout')
def logout():
    if session[USERNAME]:
        session.clear()
    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    db.close(conn)
