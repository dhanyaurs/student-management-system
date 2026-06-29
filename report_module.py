from database_module import create_connection
from mysql.connector import Error

def student_enrollment_report():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        sql = """
        SELECT 
            s.student_id,
            s.student_name,
            c.course_id,
            c.course_name
        FROM students s
        JOIN enrollments e ON s.student_id = e.student_id
        JOIN courses c ON e.course_id = c.course_id
        """
        cursor.execute(sql)
        return cursor.fetchall()

    except Error as e:
        return []

    finally:
        cursor.close()
        conn.close()
