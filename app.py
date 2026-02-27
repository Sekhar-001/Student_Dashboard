from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",   # default XAMPP password is empty
        database="student_dashboard"
    )

# =========================
# DASHBOARD ROUTE
# =========================
@app.route("/dashboard")
def dashboard():
    sort = request.args.get("sort")
    department = request.args.get("department")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT * FROM student WHERE 1=1"
    params = []

    if department:
        query += " AND department=%s"
        params.append(department)

    if sort == "name":
        query += " ORDER BY name ASC"
    elif sort == "date":
        query += " ORDER BY joining_date DESC"

    cursor.execute(query, params)
    students = cursor.fetchall()

    cursor.execute("""
        SELECT department, COUNT(*) as total
        FROM student
        GROUP BY department
    """)
    counts = cursor.fetchall()

    conn.close()

    return render_template("dashboard.html", students=students, counts=counts)


# =========================
# ADD STUDENT ROUTE
# =========================
@app.route("/add_student", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        name = request.form["name"]
        department = request.form["department"]
        joining_date = request.form["joining_date"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO student (name, department, joining_date) VALUES (%s, %s, %s)",
            (name, department, joining_date)
        )

        conn.commit()
        conn.close()

        return redirect("/dashboard")

    return render_template("add_student.html")


if __name__ == "__main__":
    app.run(debug=True)
