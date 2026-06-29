import database_module

def setup_cloud_tables():
    print("⏳ Connecting to Aiven Cloud Database to create tables...")
    try:
        # Borrow a connection from our new secure pool
        conn = database_module.create_connection()
        cursor = conn.cursor()
        
        # 1. Create Students Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT PRIMARY KEY,
            student_name VARCHAR(100) NOT NULL,
            date_of_birth DATE,
            gender VARCHAR(10),
            email VARCHAR(100),
            phone_number VARCHAR(15)
        );
        """)
        print("✅ Students table verified/created.")

        # 2. Create Courses Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            course_id INT PRIMARY KEY,
            course_name VARCHAR(100) NOT NULL
        );
        """)
        print("✅ Courses table verified/created.")

        # 3. Create Enrollments Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT,
            course_id INT,
            FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
            FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE
        );
        """)
        print("✅ Enrollments table verified/created.")
        
        cursor.close()
        conn.close()
        print("🎉 All database tables successfully built in the cloud!")
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")

if __name__ == "__main__":
    setup_cloud_tables()
