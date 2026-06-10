from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import sqlite3
import os

app = FastAPI(
    title="Student Management API",
    description="Simple CRUD API using FastAPI + SQLite",
    version="1.0"
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "students.db")

# ----------------------------
# Database Setup
# ----------------------------

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                course TEXT NOT NULL
            )
        """)

init_db()


# ----------------------------
# Models
# ----------------------------

class StudentCreate(BaseModel):
    name: str
    age: int
    course: str


class Student(StudentCreate):
    id: int


# ----------------------------
# Home
# ----------------------------

@app.get("/")
def home():
    return {"message": "Student Management API is running"}


# ----------------------------
# Create Student
# ----------------------------

@app.post("/students")
def create_student(student: StudentCreate):

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            """
            INSERT INTO students(name, age, course)
            VALUES (?, ?, ?)
            """,
            (student.name, student.age, student.course)
        )

        return {
            "id": cursor.lastrowid,
            "name": student.name,
            "age": student.age,
            "course": student.course
        }


# ----------------------------
# Get All Students
# ----------------------------

@app.get("/students")
def get_students():

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            "SELECT id, name, age, course FROM students"
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "course": row[3]
            }
            for row in rows
        ]


# ----------------------------
# Get Student By ID
# ----------------------------

@app.get("/students/{student_id}")
def get_student(student_id: int):

    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.execute(
            """
            SELECT id, name, age, course
            FROM students
            WHERE id = ?
            """,
            (student_id,)
        )

        row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "course": row[3]
        }


# ----------------------------
# Update Student
# ----------------------------

@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    student: StudentCreate
):

    with sqlite3.connect(DB_NAME) as conn:

        cursor = conn.execute(
            """
            UPDATE students
            SET name = ?, age = ?, course = ?
            WHERE id = ?
            """,
            (
                student.name,
                student.age,
                student.course,
                student_id
            )
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "message": "Student updated successfully"
        }


# ----------------------------
# Delete Student
# ----------------------------

@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    with sqlite3.connect(DB_NAME) as conn:

        cursor = conn.execute(
            """
            DELETE FROM students
            WHERE id = ?
            """,
            (student_id,)
        )

        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail="Student not found"
            )

        return {
            "message": "Student deleted successfully"
        }


# ----------------------------
# Search By Course
# ----------------------------

@app.get("/students/course/{course}")
def get_students_by_course(course: str):

    with sqlite3.connect(DB_NAME) as conn:

        cursor = conn.execute(
            """
            SELECT id, name, age, course
            FROM students
            WHERE LOWER(course) = LOWER(?)
            """,
            (course,)
        )

        rows = cursor.fetchall()

        return [
            {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "course": row[3]
            }
            for row in rows
        ]