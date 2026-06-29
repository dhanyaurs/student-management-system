from database_module import create_connection
import mysql.connector 
from mysql.connector import Error

def add_course(course_id,course_name):
    conn=create_connection()
    cursor=conn.cursor()

    try:
        sql=("insert into courses(course_id,course_name)"
            "values(%s,%s)")
        values=(course_id,course_name)
        cursor.execute(sql,values)
        conn.commit()
        return "Course Added Successfully"
    except Error as e:
        if e.errno==1062:
            return "Course ID already exists"
        else:
            return f"Error:{e}"
    finally:
        cursor.close()
        conn.close()

def view_courses():
    conn=create_connection()
    cursor=conn.cursor()

    try:
        cursor.execute("select * from courses")
        rows=cursor.fetchall()
        return rows
        #if cursor.rowcount==0:
            #print("Empty Table:There are no students")
        #for r in rows:
            #print(f"ID:{r[0]},Name:{r[1]},DOB:{r[2]},Gender:{r[3]},Email:{r[4]},Phone Number:{r[5]}")
    except Exception as e:
        #return f":Error:{e}"
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
        conn.commit()

        if cursor.rowcount == 0:
            return "Course not found"
        return "Course updated successfully"

    except Error as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()

def delete_course(course_id):
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM courses WHERE course_id=%s", (course_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return "Student Not Found"
        else:
            return "Deleted Successfully"
    except Exception as e:
        return f"Error: {e}"
    finally:
        cursor.close()
        conn.close()