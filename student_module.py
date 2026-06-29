from database_module import create_connection

def add_student(student_id, student_name, date_of_birth, gender, email, phone_number):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        sql = ("INSERT INTO students(student_id, student_name, date_of_birth, gender, email, phone_number) "
               "VALUES (%s, %s, %s, %s, %s, %s)")
        values = (student_id, student_name, date_of_birth, gender, email, phone_number)
        cursor.execute(sql, values)
        return "Added Successfully"
    except Exception as e:
        # Check for PyMySQL Duplicate Entry Error (Error code 1062)
        if hasattr(e, 'args') and len(e.args) > 0 and e.args[0] == 1062:
            return "Student ID or Email already exists"
        else:
            return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def view_students():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
        return rows if rows else []
    except Exception as e:
        return []
    finally:
        cursor.close()
        conn.close()

def update_student_details(student_id, new_email, new_phone):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT email, phone_number FROM students WHERE student_id=%s", (student_id,))
        student = cursor.fetchone()
        if student is None:
            return "Student not found"

        cursor.execute(
            "UPDATE students SET email=%s, phone_number=%s WHERE student_id=%s",
            (new_email, new_phone, student_id)
        )
        return "Updated Successfully"
    except Exception as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def delete_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
        if cursor.rowcount == 0:
            return "Student Not Found"
        else:
            return "Deleted Successfully"
    except Exception as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def search_student(student_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM students WHERE student_id=%s"
        cursor.execute(sql, (student_id,))
        row = cursor.fetchone()
        return row
    except Exception as e:
        return None
    finally:
        cursor.close()
        conn.close()
