-- Schema for Student Attendance & Records
CREATE TABLE IF NOT EXISTS students (
    student_id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE IF NOT EXISTS records (
    record_id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    attendance REAL,
    hw_avg REAL,
    midterm REAL,
    prev_gpa REAL,
    extracurricular REAL,
    at_risk INTEGER,
    prediction INTEGER,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(student_id) REFERENCES students(student_id)
);
