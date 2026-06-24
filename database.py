import sqlite3


def connect():

    return sqlite3.connect("campus_track.db")



def init_db():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT

    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS students(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT UNIQUE,
        department TEXT,
        semester INTEGER

    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS subjects(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        code TEXT,
        max_marks INTEGER

    )
    """)



    cur.execute("""
    CREATE TABLE IF NOT EXISTS marks(

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        subject_id INTEGER,
        marks REAL

    )
    """)



    conn.commit()

    conn.close()





# ---------------- USERS ----------------


def add_user(username,email,password):

    conn = connect()

    cur = conn.cursor()


    cur.execute(
        """
        INSERT INTO users(username,email,password)
        VALUES(?,?,?)
        """,
        (username,email,password)
    )


    conn.commit()

    conn.close()





def check_user(username,password):

    conn = connect()

    cur = conn.cursor()


    cur.execute(
        """
        SELECT *
        FROM users
        WHERE username=? AND password=?
        """,
        (username,password)
    )


    user = cur.fetchone()


    conn.close()


    return user







# ---------------- STUDENTS ----------------


def add_student(name,roll,department,semester):

    conn = connect()

    cur = conn.cursor()


    cur.execute(
        "SELECT * FROM students WHERE roll=?",
        (roll,)
    )


    if cur.fetchone():

        conn.close()

        return False



    cur.execute(
        """
        INSERT INTO students(name,roll,department,semester)
        VALUES(?,?,?,?)
        """,
        (name,roll,department,semester)
    )


    conn.commit()

    conn.close()


    return True






def get_students():

    conn = connect()

    cur = conn.cursor()


    cur.execute(
        "SELECT * FROM students"
    )


    data = cur.fetchall()


    conn.close()


    return data





def delete_student(id):

    conn = connect()

    cur = conn.cursor()


    cur.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )


    conn.commit()

    conn.close()







# ---------------- SUBJECTS ----------------


def add_subject(name,code,max_marks):

    conn = connect()

    cur = conn.cursor()


    cur.execute(
        """
        INSERT INTO subjects(name,code,max_marks)
        VALUES(?,?,?)
        """,
        (name,code,max_marks)
    )


    conn.commit()

    conn.close()






def get_subjects():

    conn = connect()

    cur = conn.cursor()


    cur.execute(
        "SELECT * FROM subjects"
    )


    data = cur.fetchall()


    conn.close()


    return data







# ---------------- MARKS ----------------


def add_marks(student_id,subject_id,marks):

    conn = connect()

    cur = conn.cursor()


    cur.execute(
        """
        INSERT INTO marks(student_id,subject_id,marks)
        VALUES(?,?,?)
        """,
        (student_id,subject_id,marks)
    )


    conn.commit()

    conn.close()





def get_marks():

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT

    students.name,
    subjects.name,
    marks.marks


    FROM marks


    JOIN students

    ON marks.student_id = students.id


    JOIN subjects

    ON marks.subject_id = subjects.id

    """)


    data = cur.fetchall()


    conn.close()


    return data





def get_report(student_id):

    conn = connect()

    cur = conn.cursor()


    cur.execute("""
    SELECT

    subjects.name,
    marks.marks


    FROM marks


    JOIN subjects

    ON marks.subject_id = subjects.id


    WHERE marks.student_id=?

    """,(student_id,))


    data = cur.fetchall()


    conn.close()


    return data
def get_dashboard_counts():

    conn = connect()

    cur = conn.cursor()


    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]


    cur.execute("SELECT COUNT(*) FROM subjects")
    total_subjects = cur.fetchone()[0]


    cur.execute("SELECT COUNT(*) FROM marks")
    total_marks = cur.fetchone()[0]


    conn.close()


    return total_students, total_subjects, total_marks
def get_dashboard_counts():

    conn = connect()

    cur = conn.cursor()


    cur.execute("SELECT COUNT(*) FROM students")
    total_students = cur.fetchone()[0]


    cur.execute("SELECT COUNT(*) FROM subjects")
    total_subjects = cur.fetchone()[0]


    cur.execute("SELECT COUNT(*) FROM marks")
    total_marks = cur.fetchone()[0]


    conn.close()


    return total_students, total_subjects, total_marks
def search_students(keyword):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT * FROM students
    WHERE name LIKE ? OR roll LIKE ? OR department LIKE ?
    """,
    ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%')
    )

    data = cur.fetchall()

    conn.close()

    return data
def get_student_by_id(id):

    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT * FROM students WHERE id=?", (id,))

    student = cur.fetchone()

    conn.close()

    return student


def update_student(id,name,roll,department,semester):

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    UPDATE students
    SET name=?, roll=?, department=?, semester=?
    WHERE id=?
    """,
    (name,roll,department,semester,id)
    )

    conn.commit()
    conn.close()

def get_top_performer():

    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    SELECT students.name, AVG(marks.marks) as average_marks
    FROM marks
    JOIN students ON marks.student_id = students.id
    GROUP BY students.id
    ORDER BY average_marks DESC
    LIMIT 1
    """)

    data = cur.fetchone()

    conn.close()

    return data