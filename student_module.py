from database_module import create_connection
import mysql.connector 
from mysql.connector import Error

def add_student(student_id,student_name,date_of_birth,gender,email,phone_number):
    conn=create_connection()
    cursor=conn.cursor()

    try:
        sql=("insert into students(student_id,student_name,date_of_birth,gender,email,phone_number)"
            "values(%s,%s,%s,%s,%s,%s)")
        values=(student_id,student_name,date_of_birth,gender,email,phone_number)
        cursor.execute(sql,values)
        conn.commit()
        return "Added Successfully"
    except Error as e:
        if e.errno==1062:
            return "Student ID or Email already exists"
        else:
            return f"Error:{e}"
    finally:
        cursor.close()
        conn.close()

def view_students():
    conn=create_connection()
    cursor=conn.cursor()

    try:
        cursor.execute("select * from students")
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
        conn.commit()
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


def search_student(student_id):
    conn=create_connection()
    cursor=conn.cursor()
    #student_id=int(input("Enter Student ID:"))
    try:
        sql=("select * from students where student_id=%s")
        cursor.execute(sql,(student_id,))
        rows=cursor.fetchone()
        return rows
        #if cursor.rowcount==0:
            #print("Student Not Found")
        #else:
            #for r in rows:
                #print(f"ID:{r[0]} Name:{r[1]}  Date of Birth:{r[2]}  Gender:{r[3]} Email:{r[4]} Phone Number:{r[5]}")
    except Error as e:
        #print(f"Error:{e}")
        return None
    finally:
        cursor.close()
        conn.close()

#if __name__ == "__main__":
    #add_student(5,"Dhanya","2003-30-06","Female","dhanya12@gmail.com","8431591466")
    #update_student_details()
    #delete_student()
    #view_students()
    #search_student()