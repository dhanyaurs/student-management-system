from database_module import create_connection
from mysql.connector import Error

def enroll_students(student_id,course_id):
    conn=create_connection()
    cursor=conn.cursor()
    try:
        sql=("insert into enrollments(student_id,course_id)"
            "values(%s,%s)")
        values=(student_id,course_id)
        cursor.execute(sql,values)
        conn.commit()
        return "Added Successfully"
    except Error as e:
        if e.errno==1062:
            return "This student is already enrolled in this course"
        else:
            return f"Error:{e}"
    except Exception as e:
        return f"Error:{e}"
    finally:
        cursor.close()
        conn.close()

def view_courses_of_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        sql = """
        SELECT c.course_id, c.course_name
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        WHERE e.student_id = %s
        """
        cursor.execute(sql, (student_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

def view_students_for_course(course_id):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        sql = """
        SELECT s.student_id, s.student_name, s.email, s.phone_number
        FROM enrollments e
        JOIN students s ON e.student_id = s.student_id
        WHERE e.course_id = %s
        """
        cursor.execute(sql, (course_id,))
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


