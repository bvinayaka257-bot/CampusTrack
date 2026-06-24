from flask import Flask, render_template, request, redirect

from database import (
    init_db,
    add_user,
    check_user,
    add_student,
    get_students,
    delete_student,
    add_subject,
    get_subjects,
    add_marks,
    get_marks,
    get_report,
    get_dashboard_counts,
    search_students,
    get_student_by_id,
    update_student,
    get_top_performer
)

app = Flask(__name__)

init_db()


@app.route("/")
def home():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        add_user(
            request.form["username"],
            request.form["email"],
            request.form["password"]
        )
        return redirect("/")

    return render_template("register.html")


@app.route("/login", methods=["POST"])
def login():
    user = check_user(
        request.form["username"],
        request.form["password"]
    )

    if user:
        total_students, total_subjects, total_marks = get_dashboard_counts()

        return render_template(
            "dashboard.html",
            total_students=total_students,
            total_subjects=total_subjects,
            total_marks=total_marks
        )

    return "User not allowed"


@app.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "POST":
        result = add_student(
            request.form["name"],
            request.form["roll"],
            request.form["department"],
            request.form["semester"]
        )

        if result == False:
            return "Roll Number already exists!"

    keyword = request.args.get("search")

    if keyword:
        data = search_students(keyword)
    else:
        data = get_students()

    return render_template("students.html", students=data)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    if request.method == "POST":
        update_student(
            id,
            request.form["name"],
            request.form["roll"],
            request.form["department"],
            request.form["semester"]
        )
        return redirect("/students")

    student = get_student_by_id(id)

    return render_template("edit_student.html", student=student)


@app.route("/delete/<int:id>")
def delete(id):
    delete_student(id)
    return redirect("/students")


@app.route("/subjects", methods=["GET", "POST"])
def subjects():
    if request.method == "POST":
        add_subject(
            request.form["name"],
            request.form["code"],
            request.form["max_marks"]
        )
        return redirect("/subjects")

    subjects_data = get_subjects()

    return render_template("subjects.html", subjects=subjects_data)


@app.route("/marks", methods=["GET", "POST"])
def marks():
    if request.method == "POST":
        add_marks(
            request.form["student_id"],
            request.form["subject_id"],
            request.form["marks"]
        )
        return redirect("/marks")

    return render_template(
        "marks.html",
        students=get_students(),
        subjects=get_subjects(),
        marks=get_marks()
    )


@app.route("/reports")
def reports():
    return render_template(
        "reports.html",
        students=get_students()
    )


@app.route("/report", methods=["POST"])
def report():
    student_id = request.form["student_id"]

    data = get_report(student_id)

    total = 0

    for d in data:
        total += float(d[1])

    if len(data) > 0:
        average = total / len(data)
    else:
        average = 0

    return render_template(
        "report.html",
        data=data,
        average=average
    )


@app.route("/analytics")
def analytics():
    return render_template(
        "analytics.html",
        marks=get_marks()
    )


@app.route("/topper")
def topper():
    return render_template(
        "topper.html",
        topper=get_top_performer()
    )


if __name__ == "__main__":
    app.run(debug=True)