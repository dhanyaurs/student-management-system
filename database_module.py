import mysql.connector
from mysql.connector import Error

connection=None
def create_connection():
    try:
        connection=mysql.connector.connect(
            host="localhost",
            user="root",
            password="dhanya",
            database="student_management_system"
        )
        #print("Connection to MySQL DB successful")
    except Error as e:
        print(f"Error:{e}")
    return connection

if __name__ == "__main__":
    conn = create_connection()
