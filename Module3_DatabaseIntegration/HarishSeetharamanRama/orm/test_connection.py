import mysql.connector

print("Trying to connect...")

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        port=3306,
        user="root",
        password="cognizant123",
        database="college_db"
    )
    print("✅ CONNECTED SUCCESSFULLY!")
    cursor = conn.cursor()
    cursor.execute("SELECT VERSION();")
    print(cursor.fetchone())
    conn.close()
except Exception as e:
    print("❌ FAILED:")
    print(e)