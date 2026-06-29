from student_module import add_student,view_students,search_student,update_student_details,delete_student
from course_module import add_course,view_courses,update_course,delete_course
from enrollment_module import enroll_students
from report_module import student_enrollment_report
from database_module import create_connection
from enrollment_module import view_courses_of_student,view_students_for_course
from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = "your_secret_key"

ADMIN_USERNAME = "Admin"
ADMIN_PASSWORD = "admin123"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")

        if password == ADMIN_PASSWORD:
            session["username"] = ADMIN_USERNAME
            return redirect(url_for("home"))
        else:
            flash("Incorrect password!")

    return render_template("login.html", admin_name=ADMIN_USERNAME)


@app.route("/")
def home():
    if "username" not in session:
        return redirect(url_for("login"))
    return render_template("home.html", admin_name=session["username"])


@app.route("/add_student",methods=["GET","POST"])
def add_studentt():
    stu_details=""
    if request.method == "POST":
        student_id = int(request.form.get("student_id"))
        student_name = request.form.get("student_name")
        date_of_birth = request.form.get("date_of_birth")
        gender = request.form.get("gender")
        email = request.form.get("email")
        phone_number = request.form.get("phone_number")
        stu_details= add_student(student_id,student_name,date_of_birth,gender,email,phone_number)  
    return render_template("add_student.html",stu_details=stu_details)

@app.route("/add_course",methods=["GET","POST"])
def add_coursee():
    course_details=""
    if request.method == "POST":
        course_id = int(request.form.get("course_id"))
        course_name = request.form.get("course_name")
        course_details= add_course(course_id,course_name) 
    return render_template("add_course.html",course_details=course_details)


@app.route("/view_student",methods=["GET","POST"])
def view_studentt():
    students=view_students()
    message=""
    if request.method=="POST":
        student_id=request.form.get("student_id")
        if student_id:
            student=search_student(student_id)
            if student:
                students=[student]
            else:
                students=[]
                message="Not Found"

    return render_template("view_student.html",students=students,message=message)

@app.route("/update-student/<int:student_id>", methods=["GET", "POST"])
def update_student_route(student_id):
    if request.method == "POST":
        new_email = request.form.get("email")
        new_phone = request.form.get("phone_number")
        update_student_details(student_id, new_email, new_phone)  # your DB function
        return redirect(url_for("view_studentt"))
    
    student = search_student(student_id)  # get current details
    return render_template("edit_student.html", student=student)

@app.route("/delete-student/<int:student_id>", methods=["POST"])
def delete_student_route(student_id):
    message = delete_student(student_id)  # your DB function
    return redirect(url_for("view_studentt"))



@app.route("/view_courses")
def view_coursess():
    courses=view_courses()
    return render_template("view_courses.html",courses=courses)

def get_all_students():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT student_id, student_name FROM students")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_all_courses():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT course_id, course_name FROM courses")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

@app.route("/update-course/<course_id>", methods=["GET", "POST"])
def update_course_route(course_id):
    if request.method == "POST":
        new_name = request.form.get("course_name")
        message = update_course(course_id, new_name)
        return render_template("update_course.html", message=message)

    return render_template("update_course.html")

@app.route("/delete-course/<int:course_id>", methods=["POST"])
def delete_course_route(course_id):
    message = delete_course(course_id)  # your DB function
    return redirect(url_for("view_coursess"))


@app.route("/enroll")
def enroll():
    return render_template("enroll.html")


@app.route("/enroll_student", methods=["GET", "POST"])
def enroll_stu():
    message = None

    students = get_all_students()   # returns list of students
    courses = get_all_courses()     # returns list of courses

    if request.method == "POST":
        student_id = request.form.get("student_id")
        course_id = request.form.get("course_id")

        message = enroll_students(student_id, course_id)

    return render_template(
        "enroll_students.html",
        students=students,
        courses=courses,
        message=message
    )


@app.route("/report")
def report():
    data = student_enrollment_report()
    return render_template("report.html", report=data)

@app.route("/student-courses", methods=["GET", "POST"])
def student_courses():
    courses = None
    if request.method == "POST":
        student_id = request.form.get("student_id")
        courses = view_courses_of_student(student_id)

    return render_template("student_courses.html", courses=courses)

@app.route("/course-students", methods=["GET", "POST"])
def course_students():
    students = None

    if request.method == "POST":
        course_id = request.form.get("course_id")
        students = view_students_for_course(course_id)

    return render_template("course_students.html", students=students)

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
