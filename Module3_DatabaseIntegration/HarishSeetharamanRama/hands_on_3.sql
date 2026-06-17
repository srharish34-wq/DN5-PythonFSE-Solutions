

USE college_db;


SELECT s.student_id, CONCAT(s.first_name,' ',s.last_name) AS student_name,
       COUNT(e.enrollment_id) AS course_count
FROM students s
JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id
HAVING COUNT(e.enrollment_id) > (
    SELECT AVG(cnt) FROM (
        SELECT COUNT(enrollment_id) AS cnt
        FROM enrollments
        GROUP BY student_id
    ) AS avg_sub
);

SELECT c.course_name, c.course_code
FROM courses c
WHERE NOT EXISTS (
    SELECT 1 FROM enrollments e
    WHERE e.course_id = c.course_id
    AND (e.grade != 'A' OR e.grade IS NULL)
);

SELECT p.prof_name, p.salary, d.dept_name
FROM professors p
JOIN departments d ON p.department_id = d.department_id
WHERE p.salary = (
    SELECT MAX(p2.salary) FROM professors p2
    WHERE p2.department_id = p.department_id
);

SELECT dept_name, avg_salary
FROM (
    SELECT d.dept_name, ROUND(AVG(p.salary), 2) AS avg_salary
    FROM departments d
    JOIN professors p ON d.department_id = p.department_id
    GROUP BY d.department_id, d.dept_name
) AS dept_avg
WHERE avg_salary > 85000;

CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name AS department,
    COUNT(e.enrollment_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS gpa
FROM students s
JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

-- View 2: Course statistics
CREATE OR REPLACE VIEW vw_course_stats AS
SELECT
    c.course_name,
    c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            WHEN 'F' THEN 0
            ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;

SELECT * FROM vw_student_enrollment_summary WHERE gpa > 3.0;


SELECT * FROM vw_course_stats;

DROP VIEW IF EXISTS vw_student_enrollment_summary;
DROP VIEW IF EXISTS vw_course_stats;

CREATE OR REPLACE VIEW vw_student_enrollment_summary AS
SELECT
    s.student_id,
    CONCAT(s.first_name, ' ', s.last_name) AS full_name,
    d.dept_name AS department,
    COUNT(e.enrollment_id) AS courses_enrolled,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4 WHEN 'B' THEN 3
            WHEN 'C' THEN 2 WHEN 'D' THEN 1
            WHEN 'F' THEN 0 ELSE NULL
        END
    ), 2) AS gpa
FROM students s
JOIN departments d ON s.department_id = d.department_id
LEFT JOIN enrollments e ON s.student_id = e.student_id
GROUP BY s.student_id, s.first_name, s.last_name, d.dept_name;

CREATE OR REPLACE VIEW vw_students_2022 AS
SELECT * FROM students WHERE enrollment_year = 2022
WITH CHECK OPTION;

CREATE OR REPLACE VIEW vw_course_stats AS
SELECT
    c.course_name, c.course_code,
    COUNT(e.enrollment_id) AS total_enrollments,
    ROUND(AVG(
        CASE e.grade
            WHEN 'A' THEN 4 WHEN 'B' THEN 3
            WHEN 'C' THEN 2 WHEN 'D' THEN 1
            WHEN 'F' THEN 0 ELSE NULL
        END
    ), 2) AS avg_gpa
FROM courses c
LEFT JOIN enrollments e ON c.course_id = e.course_id
GROUP BY c.course_id, c.course_name, c.course_code;


DELIMITER $$

CREATE PROCEDURE sp_enroll_student(
    IN p_student_id     INT,
    IN p_course_id      INT,
    IN p_enroll_date    DATE
)
BEGIN
    IF EXISTS (
        SELECT 1 FROM enrollments
        WHERE student_id = p_student_id AND course_id = p_course_id
    ) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'ERROR: Student is already enrolled in this course.';
    ELSE
        INSERT INTO enrollments (student_id, course_id, enrollment_date)
        VALUES (p_student_id, p_course_id, p_enroll_date);
        SELECT 'Enrollment successful.' AS result;
    END IF;
END $$

-- Create transfer log table first
CREATE TABLE IF NOT EXISTS department_transfer_log (
    log_id        INT PRIMARY KEY AUTO_INCREMENT,
    student_id    INT,
    from_dept_id  INT,
    to_dept_id    INT,
    transferred_at DATETIME DEFAULT CURRENT_TIMESTAMP
) $$

CREATE PROCEDURE sp_transfer_student(
    IN p_student_id  INT,
    IN p_new_dept_id INT
)
BEGIN
    DECLARE v_old_dept_id INT;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Transfer failed — transaction rolled back.';
    END;

    START TRANSACTION;

        -- Get current department
        SELECT department_id INTO v_old_dept_id
        FROM students WHERE student_id = p_student_id;

        -- Update student department
        UPDATE students
        SET department_id = p_new_dept_id
        WHERE student_id = p_student_id;

        -- Log the transfer
        INSERT INTO department_transfer_log (student_id, from_dept_id, to_dept_id)
        VALUES (p_student_id, v_old_dept_id, p_new_dept_id);

    COMMIT;
    SELECT 'Transfer successful.' AS result;
END $$

DELIMITER ;

-- Test sp_enroll_student
CALL sp_enroll_student(1, 3, CURDATE());   -- should succeed
CALL sp_enroll_student(1, 1, CURDATE());   -- should raise duplicate error

-- Test sp_transfer_student
CALL sp_transfer_student(5, 2);

-- SAVEPOINT example: 2 inserts, fail 2nd, keep 1st
START TRANSACTION;

    INSERT INTO enrollments (student_id, course_id, enrollment_date)
    VALUES (2, 5, CURDATE());

    SAVEPOINT after_first_insert;

COMMIT;
