
USE college_db;


-- departments table (no FK, so create first)
CREATE TABLE departments (
    department_id INT PRIMARY KEY AUTO_INCREMENT,
    dept_name     VARCHAR(100) NOT NULL,
    head_of_dept  VARCHAR(100),
    budget        DECIMAL(12, 2)
);

-- students table
CREATE TABLE students (
    student_id      INT PRIMARY KEY AUTO_INCREMENT,
    first_name      VARCHAR(50)  NOT NULL,
    last_name       VARCHAR(50)  NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth   DATE,
    department_id   INT,
    enrollment_year INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- courses table
CREATE TABLE courses (
    course_id   INT PRIMARY KEY AUTO_INCREMENT,
    course_name VARCHAR(150) NOT NULL,
    course_code VARCHAR(20)  UNIQUE,
    credits     INT,
    department_id INT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

-- enrollments table (references students and courses)
CREATE TABLE enrollments (
    enrollment_id   INT PRIMARY KEY AUTO_INCREMENT,
    student_id      INT,
    course_id       INT,
    enrollment_date DATE,
    grade           CHAR(2),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id)  REFERENCES courses(course_id)
);

-- professors table
CREATE TABLE professors (
    professor_id INT PRIMARY KEY AUTO_INCREMENT,
    prof_name    VARCHAR(100) NOT NULL,
    email        VARCHAR(100) UNIQUE,
    department_id INT,
    salary       DECIMAL(10, 2),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);


-- Add phone_number column to students
ALTER TABLE students ADD COLUMN phone_number VARCHAR(15);

-- Add max_seats to courses with default
ALTER TABLE courses ADD COLUMN max_seats INT DEFAULT 60;

-- Add grade CHECK constraint to enrollments
ALTER TABLE enrollments
    ADD CONSTRAINT chk_grade
    CHECK (grade IN ('A','B','C','D','F') OR grade IS NULL);

ALTER TABLE students DROP COLUMN phone_number;
