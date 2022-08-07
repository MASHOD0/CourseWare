# 1-- gets section_id from sections
get_all_depts = "SELECT department_id, department_name FROM department"
get_section_id = """
                SELECT section_id
                FROM section
                WHERE section = '{}';
                """
get_all_sections = """
                    SELECT section.section_id, section.section, department.department_name
                    FROM section
                    JOIN department ON section.department_id = department.department_id;
                """
# 2-- gets password from student
get_student_pw = """SELECT distinct password
                FROM student
                WHERE usn = '{}' 
                LIMIT  1;
                """

# 3-- gets password from teachers
get_teacher_pw = """
                SELECT distinct password
                FROM faculty
                WHERE name = '{}' 
                LIMIT  1;
                """

# 4-- adds new user in students table
add_new_student = """
                INSERT INTO student(student_id, section_id, usn, name, password, email, department_id)
                VALUES (DEFAULT, {}, '{}', '{}', '{}', '{}', {});
                """

# 5-- adds new user in teachers table
add_new_teacher = """
                INSERT INTO faculty (faculty_id, department_id, name, password, email) 
                VALUES (DEFAULT, {}, '{}', '{}', '{}');
                """

# 6-- gets classes for a given usn and day
get_classes = """
                SELECT classes.class_id, classes.course_id, classes.link, classes.time, faculty.name, courses.course_name, courses.course_code
                    FROM classes
                    JOIN faculty ON classes.faculty_id = faculty.faculty_id
                    JOIN courses ON classes.course_id = courses.course_id
                    WHERE day = '{}'
                    AND classes.section_id = (select section_id from student where usn = '{}' limit 1);
                """

# 7-- gets classes for a given faculty name and day
get_teacher_cls = """
                SELECT sections.section, courses.course_code, link, "time"
                FROM classes
                INNER JOIN courses ON classes.course_id = courses.course_id
				INNER JOIN teachers ON classes.teacher_id = teachers.teacher_id 
				LEFT JOIN sections ON classes.section_id = sections.section_id
				where teachers.name = '{}'
				AND "day" = '{}';
                """

# 8-- creates a new class
add_class = """
            INSERT INTO classes(
	        section_id, course_id, link, day, "time", class_id, teacher_id)
	        VALUES ({}, {}, '{}','{}', '{}:00', default, {});
            """

# 9-- gets course_id given a course code
get_courseId = """
            SELECT course_id 
	        FROM public.courses
	        WHERE course_code = '{}'
            LIMIT 1;
            """

# 10-- gets teacher_id given a teacher name
get_teacher_id = """
                SELECT teacher_id FROM  teachers WHERE name = '{}' limit 1;
                """

# 11-- gets the list of all the courses
get_all_courses = """
                    SELECT course_code
                    FROM courses;
                """

# 12-- gets list of students from grades
get_student_list = """SELECT grades.student_id, semester, course_id, student."USN" 
                        FROM grades
                        INNER JOIN student ON  grades.student_id = student.student_id;
                    """

# 13-- updating grades given a exam, marks and student id
update_grades = """UPDATE public.grades
                    SET "{}"={}
                    WHERE student_id = {};
                """

# 14-- getting all the students(student_id) from a section
get_section = """SELECT student_id FROM student WHERE section_id = {};"""

# 15-- adds students to grades table
add_student_to_grades = """INSERT INTO grades(student_id, course_id, semester, section_id) VALUES ({}, {}, {}, {})"""

# 16-- create new courses
add_courses = """INSERT INTO courses(course_id, department, course_code) VALUES (DEFAULT, '{}', '{}');"""

# 17-- create new sections
add_sections = """INSERT INTO sections(section_id, semester, section) VALUES (DEFAULT, {}, '{}');"""

# 18-- gets section_id and section from sections
get_sections = """
                SELECT section_id, section
                FROM sections
                """

# 19-- gets course_id and course code
get_courses = """SELECT course_id, course_code FROM courses;"""

# 20-- gets section from student id
get_section = """SELECT student_id FROM student WHERE section_id = {};"""

# 21-- adding students to attendance table
add_student_to_attendance = """INSERT INTO "Attendance"(student_id, course_id, section_id) VALUES ({}, {}, {});"""

# 22-- gets a section from grades
get_section_from_grades = """SELECT DISTINCT grades.section_id, grades.course_id, courses.course_code, sections.section
                            FROM grades
                            INNER JOIN courses ON grades.course_id = courses.course_id
                            INNER JOIN sections on grades.section_id = sections.section_id;
                         """

# 23-- gets studentid and usn from students given a section_id
get_section_usn = """SELECT student_id, "USN" FROM student WHERE section_id = {};"""

# 24
get_section_from_attendance = """SELECT DISTINCT "Attendance".section_id, "Attendance".course_id,courses.course_code , sections.section 
                            FROM "Attendance"
                            INNER JOIN courses ON "Attendance".course_id = courses.course_id
                            INNER JOIN sections on "Attendance".section_id = sections.section_id;
                            """

# 25
get_section_name = """select "Attendance".student_id, "USN", "Name", missed, total from "Attendance" 
                    INNER JOIN "student" ON "Attendance".student_id = student.student_id
                    WHERE "Attendance".section_id = {}
                    AND "Attendance".course_id = {};
                    """

# 26
add_total = """UPDATE public."Attendance"
                SET total= {}
                WHERE student_id = {}
                AND course_id = {}
                AND section_id = {};
            """

# 27
add_missed = """UPDATE public."Attendance"
                SET missed= {}
                WHERE student_id = {}
                AND course_id = {}
                AND section_id = {};
            """

# 28
get_missed = """SELECT missed
                FROM public."Attendance"
                WHERE student_id = {}
                AND course_id = {}
                AND section_id = {};
            """

# 29
get_grades = """
            SELECT courses.course_name, courses.course_code, grades.semester, grades.cie1, grades.cie2, grades.cie3, grades.aat, grades.see
            FROM grades
            JOIN courses
            ON grades.course_id = courses.course_id
            WHERE grades.student_id = (select student_id from student where usn = '{}' limit 1);    
            """

# 30
get_attendance = """
                    SELECT  courses.course_name, attendance.missed, attendance.total
                    FROM attendance
                    JOIN courses
                    ON attendance.course_id = courses.course_id;
                    WHERE attendance.student_id = (select student_id from student where usn = '{}' limit 1);
                """
