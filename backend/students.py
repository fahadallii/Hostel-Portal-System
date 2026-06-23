"""
Student Management - CRUD operations
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.database import get_db_connection
from mysql.connector import Error


# ─── CREATE ──────────────────────────────────
def add_student(data: dict):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        sql = """
            INSERT INTO students
                (reg_number, full_name, email, phone, cnic, guardian_name,
                 guardian_phone, department, program, semester, gender, dob, address, status)
            VALUES
                (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(sql, (
            data.get("reg_number"), data.get("full_name"),
            data.get("email"),      data.get("phone"),
            data.get("cnic"),       data.get("guardian_name"),
            data.get("guardian_phone"), data.get("department"),
            data.get("program"),    data.get("semester"),
            data.get("gender"),     data.get("dob"),
            data.get("address"),    data.get("status", "Active"),
        ))
        conn.commit()
        student_id = cur.lastrowid
        return True, f"Student added with ID {student_id}"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


# ─── READ ─────────────────────────────────────
def get_all_students(status_filter=None):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        if status_filter and status_filter != "All":
            cur.execute("SELECT * FROM students WHERE status=%s ORDER BY full_name", (status_filter,))
        else:
            cur.execute("SELECT * FROM students ORDER BY full_name")
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_student_by_id(student_id: int):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM students WHERE student_id=%s", (student_id,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()


def search_students(query: str):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        like = f"%{query}%"
        cur.execute("""
            SELECT * FROM students
            WHERE full_name LIKE %s OR reg_number LIKE %s OR email LIKE %s OR department LIKE %s
            ORDER BY full_name
        """, (like, like, like, like))
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_unallocated_students():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT s.* FROM students s
            WHERE s.status='Active'
            AND s.student_id NOT IN (
                SELECT student_id FROM allocations WHERE status='Active'
            )
            ORDER BY s.full_name
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


# ─── UPDATE ───────────────────────────────────
def update_student(student_id: int, data: dict):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        sql = """
            UPDATE students SET
                full_name=%s, email=%s, phone=%s, cnic=%s,
                guardian_name=%s, guardian_phone=%s, department=%s,
                program=%s, semester=%s, gender=%s, dob=%s,
                address=%s, status=%s
            WHERE student_id=%s
        """
        cur.execute(sql, (
            data.get("full_name"),    data.get("email"),
            data.get("phone"),        data.get("cnic"),
            data.get("guardian_name"), data.get("guardian_phone"),
            data.get("department"),   data.get("program"),
            data.get("semester"),     data.get("gender"),
            data.get("dob"),          data.get("address"),
            data.get("status"),       student_id,
        ))
        conn.commit()
        return True, "Student updated successfully"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


# ─── DELETE ───────────────────────────────────
def delete_student(student_id: int):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE student_id=%s", (student_id,))
        conn.commit()
        return True, "Student deleted successfully"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


# ─── STATS ────────────────────────────────────
def get_student_stats():
    conn = get_db_connection()
    if not conn:
        return {}
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT
                COUNT(*) as total,
                SUM(status='Active') as active,
                SUM(status='Inactive') as inactive,
                SUM(gender='Male') as male,
                SUM(gender='Female') as female
            FROM students
        """)
        return cur.fetchone() or {}
    finally:
        cur.close(); conn.close()
