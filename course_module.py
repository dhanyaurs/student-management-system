from database_module import create_connection

def add_course(course_id, course_name):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO courses(course_id, course_name) VALUES (%s, %s)"
        values = (course_id, course_name)
        cursor.execute(sql, values)
        return "Course Added Successfully"
    except Exception as e:
        # Check for PyMySQL Duplicate Entry Error (Error code 1062)
        if hasattr(e, 'args') and len(e.args) > 0 and e.args[0] == 1062:
            return "Course ID already exists"
        else:
            return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def view_courses():
    conn = create_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM courses")
        rows = cursor.fetchall()
        return rows if rows else []
    except Exception as e:
        return []
    finally:
        cursor.close()
        conn.close()

def update_course(course_id, new_name):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        sql = "UPDATE courses SET course_name=%s WHERE course_id=%s"
        cursor.execute(sql, (new_name, course_id))

        if cursor.rowcount == 0:
            return "Course not found"
        return "Course updated successfully"
    except Exception as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def delete_course(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM courses WHERE course_id=%s", (course_id,))
        if cursor.rowcount == 0:
            return "Course Not Found"
        else:
            return "Deleted Successfully"
    except Exception as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()
