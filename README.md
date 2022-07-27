# coursware
## ER Diagram
```mermaid
erDiagram
    Student ||--|{ attendance : gets
    Faculty ||--|{ material : prepares
    Faculty ||--|{ attendance :gives
    Student ||--|{ grades :scores
    Student ||--|{ courses :takes
    Student }|--|| section : Is_in
    Student }|--|{ material :takes

   
    
    Faculty ||--|{ grades :grades
    Faculty ||--|{ section :teaches

    Department ||--|{ Faculty : teaches_in
    Department ||--|{ Student : studies_in
    courses ||--|{ attendance : have
    courses ||--|{ grades :have
    courses }|--|{ material :have
    section ||--|{ courses :has
    classes }|--|{ section :have
    classes }|--|{ courses :have
    Student {
        int_pk student_id
        int_fk section_id
        string USN
        string Name
        string Password
        string Email
        string Branch
    }

    Faculty {
        int_pk teacher_id
        string Name
        string Password
        string Email
        string Department
    }

    attendance {
        int_fk student_id
        int_fk course_id
        int semester
        int missed
        int total
    }
    grades {
        int_fk student_id
        int_fk course_id
        int semester
        int CIE1
        int CIE2
        int CIE3
        int AAT
        int SEE
    }
    section {
        int_pk section_id
        int_fk dept_id
        int semester
        char section
    }
    material {
        int_pk material_id
        int_fk course_id
        int_fk section_id
        varchar location
    }
    Department {
        int_pk department_id
        string department_name
    }
    courses {
        int_pk course_id
        int_fk department_id
        string course_name
        string course_code
    }
    classes {
        int_pk class_id
        int_fk course_id
        string link
        string day
        string time
    }