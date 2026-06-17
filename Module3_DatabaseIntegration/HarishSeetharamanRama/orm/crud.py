

from sqlalchemy.orm import sessionmaker, joinedload
from models import engine, Department, Student, Course, Enrollment, Professor
from datetime import date

Session = sessionmaker(bind=engine)


def seed_data():
    with Session() as session:
        # 3 Departments
        cs   = Department(dept_name="Computer Science", hod_name="Dr. Ramesh Kumar", budget=850000)
        ec   = Department(dept_name="Electronics",      hod_name="Dr. Priya Nair",   budget=620000)
        mech = Department(dept_name="Mechanical",       hod_name="Dr. Suresh Iyer",  budget=540000)
        session.add_all([cs, ec, mech])
        session.flush()  # get IDs without committing

        # 5 Students
        students = [
            Student(first_name="Arjun",  last_name="Mehta",  email="arjun.mehta@college.edu",
                    department_id=cs.department_id,   enrollment_year=2022),
            Student(first_name="Priya",  last_name="Suresh", email="priya.suresh@college.edu",
                    department_id=cs.department_id,   enrollment_year=2022),
            Student(first_name="Rohan",  last_name="Verma",  email="rohan.verma@college.edu",
                    department_id=ec.department_id,   enrollment_year=2021),
            Student(first_name="Sneha",  last_name="Patel",  email="sneha.patel@college.edu",
                    department_id=mech.department_id, enrollment_year=2023),
            Student(first_name="Vikram", last_name="Das",    email="vikram.das@college.edu",
                    department_id=cs.department_id,   enrollment_year=2022),
        ]
        session.add_all(students)
        session.flush()

        # 3 Courses
        courses = [
            Course(course_name="Data Structures & Algorithms", course_code="CS101",
                   credits=4, department_id=cs.department_id),
            Course(course_name="Database Management Systems",  course_code="CS102",
                   credits=3, department_id=cs.department_id),
            Course(course_name="Circuit Theory",               course_code="EC101",
                   credits=3, department_id=ec.department_id),
        ]
        session.add_all(courses)
        session.flush()

        # 4 Enrollments
        enrollments = [
            Enrollment(student_id=students[0].student_id, course_id=courses[0].course_id,
                       enrollment_date=date(2022, 7, 1), grade="A"),
            Enrollment(student_id=students[0].student_id, course_id=courses[1].course_id,
                       enrollment_date=date(2022, 7, 1), grade="B"),
            Enrollment(student_id=students[1].student_id, course_id=courses[0].course_id,
                       enrollment_date=date(2022, 7, 1), grade="B"),
            Enrollment(student_id=students[2].student_id, course_id=courses[2].course_id,
                       enrollment_date=date(2021, 7, 1), grade="A"),
        ]
        session.add_all(enrollments)
        session.commit()
        print("✅ Seed data inserted")



def get_cs_students():
    with Session() as session:
        students = (
            session.query(Student)
            .join(Department)
            .filter(Department.dept_name == "Computer Science")
            .all()
        )
        print("\n── CS Students ──")
        for s in students:
            print(f"  {s.first_name} {s.last_name} | {s.email}")
        return students


def get_enrollments_n1():
    print("\n── Enrollments (N+1 BAD version) ──")
    with Session() as session:
        enrollments = session.query(Enrollment).all()
        for e in enrollments:
            # Each access to e.student and e.course fires a separate SQL query!
            print(f"  {e.student.first_name} {e.student.last_name} → {e.course.course_name} | {e.grade}")

def get_enrollments_joinedload():
    print("\n── Enrollments (joinedload GOOD version) ──")
    with Session() as session:
        enrollments = (
            session.query(Enrollment)
            .options(
                joinedload(Enrollment.student),
                joinedload(Enrollment.course)
            )
            .all()
        )
        for e in enrollments:
            print(f"  {e.student.first_name} {e.student.last_name} → {e.course.course_name} | {e.grade}")

def update_student_email(email: str, new_year: int):
    with Session() as session:
        student = session.query(Student).filter_by(email=email).first()
        if student:
            student.enrollment_year = new_year
            session.commit()
            print(f"✅ Updated enrollment_year for {student.first_name} to {new_year}")
        else:
            print("❌ Student not found")



def delete_enrollment(enrollment_id: int):
    with Session() as session:
        enrollment = session.get(Enrollment, enrollment_id)
        if enrollment:
            session.delete(enrollment)
            session.commit()
            print(f"✅ Deleted enrollment ID {enrollment_id}")
        else:
            print("❌ Enrollment not found")


if __name__ == "__main__":
    seed_data()
    get_cs_students()

    print("\n[COMPARE N+1 vs joinedload — watch the SQL log above]")
    get_enrollments_n1()         # Many SQL queries
    get_enrollments_joinedload() # Single SQL query

    update_student_email("arjun.mehta@college.edu", 2023)
    delete_enrollment(4)
