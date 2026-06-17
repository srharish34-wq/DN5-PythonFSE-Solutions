

USE college_db;

EXPLAIN
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses  c ON c.course_id  = e.course_id
WHERE s.enrollment_year = 2022;


-- B-Tree index on enrollment_year
CREATE INDEX idx_students_enrollment_year ON students(enrollment_year);

-- Composite UNIQUE index on enrollments — also prevents duplicate enrollments
CREATE UNIQUE INDEX idx_enroll_student_course ON enrollments(student_id, course_id);

-- Index on course_code for fast lookups
CREATE INDEX idx_courses_code ON courses(course_code);

-- Index on professors.department_id for JOIN performance
CREATE INDEX idx_prof_dept ON professors(department_id);

-- Re-run EXPLAIN after indexes
EXPLAIN
SELECT s.first_name, s.last_name, c.course_name
FROM enrollments e
JOIN students s ON s.student_id = e.student_id
JOIN courses  c ON c.course_id  = e.course_id
WHERE s.enrollment_year = 2022;

CREATE INDEX idx_enroll_grade_null ON enrollments(grade);

-- Show all indexes on tables
SHOW INDEX FROM students;
SHOW INDEX FROM enrollments;

