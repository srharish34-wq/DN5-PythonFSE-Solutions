

import mysql.connector
import time

# ── Change these to match your MySQL credentials ──
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="cognizant123",
    database="college_db"
)

def fetch_with_n1_problem():
    cursor = conn.cursor(dictionary=True)
    query_count = 0

    start = time.time()

    # Query 1: get all enrollments
    cursor.execute("SELECT * FROM enrollments")
    enrollments = cursor.fetchall()
    query_count += 1

    results = []
    for enrollment in enrollments:
        # Query N: one extra query per enrollment row
        cursor.execute(
            "SELECT first_name, last_name FROM students WHERE student_id = %s",
            (enrollment["student_id"],)
        )
        student = cursor.fetchone()
        query_count += 1
        results.append({
            "enrollment_id": enrollment["enrollment_id"],
            "student_name": f"{student['first_name']} {student['last_name']}",
            "course_id": enrollment["course_id"],
            "grade": enrollment["grade"]
        })

    elapsed = time.time() - start
    print(f"\n[N+1 VERSION] Queries executed: {query_count}")
    print(f"Time taken: {elapsed:.4f} seconds")
    print(f"In a real app with 10,000 enrollments: {1 + 10000} queries!")
    cursor.close()
    return results

def fetch_with_join():
    cursor = conn.cursor(dictionary=True)
    query_count = 0

    start = time.time()

    # Single JOIN query — gets everything in ONE round-trip
    cursor.execute("""
        SELECT
            e.enrollment_id,
            CONCAT(s.first_name, ' ', s.last_name) AS student_name,
            e.course_id,
            e.grade
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
    """)
    results = cursor.fetchall()
    query_count += 1

    elapsed = time.time() - start
    print(f"\n[JOIN VERSION] Queries executed: {query_count}")
    print(f"Time taken: {elapsed:.4f} seconds")
    cursor.close()
    return results


if __name__ == "__main__":
    print("=" * 50)
    print("Comparing N+1 vs JOIN approach")
    print("=" * 50)

    n1_results   = fetch_with_n1_problem()
    join_results = fetch_with_join()

    # Verify both return identical data
    print(f"\nN+1 result count  : {len(n1_results)}")
    print(f"JOIN result count : {len(join_results)}")
    print("Both return same data ✅" if len(n1_results) == len(join_results) else "Data mismatch ❌")

    conn.close()

