CREATE TABLE "department" (
  "department_id" SERIAL PRIMARY KEY,
  "department_name" varchar(20)
);

CREATE TABLE "student" (
  "student_id" SERIAL PRIMARY KEY,
  "section_id" int,
  "usn" varchar(10),
  "name" varchar(60),
  "password" varchar(64),
  "email" varchar(64),
  "department_id" int
);

CREATE TABLE "faculty" (
  "faculty_id" SERIAL PRIMARY KEY,
  "department_id" int,
  "name" varchar(60),
  "password" varchar(64),
  "email" varchar(64)
);


CREATE TABLE "attendance" (
  "student_id" int,
  "course_id" int,
  "semester" int,
  "missed" int,
  "total" int
);


CREATE TABLE "grades" (
  "student_id" int,
  "course_id" int,
  "semester" int,
  "cie1" int,
  "cie2" int,
  "cie3" int,
  "aat" int,
  "see" int
);

CREATE TABLE "section" (
  "section_id" SERIAL PRIMARY KEY,
  "department_id" int,
  "semester" int,
  "section" varchar(4)
);

CREATE TABLE "material" (
  "material_id" SERIAL PRIMARY KEY,
  "course_id" int,
  "section_id" int,
  "location" varchar(200),
  "title" varchar(20)
);
