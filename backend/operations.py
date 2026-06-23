"""
Allocation, Fees, Complaints, Visitors, Notices — CRUD operations
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.database import get_db_connection
from backend.rooms import update_room_occupancy
from mysql.connector import Error


# ══════════════════════════════════════════════
#  ALLOCATIONS
# ══════════════════════════════════════════════

def allocate_room(student_id: int, room_id: int, alloc_date, notes=""):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor(dictionary=True)
        # Check existing active allocation
        cur.execute("""
            SELECT allocation_id FROM allocations
            WHERE student_id=%s AND status='Active'
        """, (student_id,))
        if cur.fetchone():
            return False, "Student already has an active room allocation"

        # Check room capacity
        cur.execute("SELECT capacity, occupied FROM rooms WHERE room_id=%s", (room_id,))
        room = cur.fetchone()
        if not room:
            return False, "Room not found"
        if room["occupied"] >= room["capacity"]:
            return False, "Room is at full capacity"

        # Insert allocation
        cur.execute("""
            INSERT INTO allocations (student_id, room_id, alloc_date, status, notes)
            VALUES (%s,%s,%s,'Active',%s)
        """, (student_id, room_id, alloc_date, notes))
        conn.commit()

        # Update occupancy
        update_room_occupancy(room_id, +1)
        return True, "Room allocated successfully"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def vacate_room(allocation_id: int, vacate_date):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM allocations WHERE allocation_id=%s", (allocation_id,))
        alloc = cur.fetchone()
        if not alloc:
            return False, "Allocation not found"

        cur.execute("""
            UPDATE allocations SET status='Vacated', vacate_date=%s
            WHERE allocation_id=%s
        """, (vacate_date, allocation_id))
        conn.commit()
        update_room_occupancy(alloc["room_id"], -1)
        return True, "Room vacated successfully"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def get_all_allocations():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*,
                   s.full_name, s.reg_number, s.department,
                   r.room_number, r.block, r.room_type, r.monthly_fee
            FROM allocations a
            JOIN students s ON a.student_id = s.student_id
            JOIN rooms    r ON a.room_id    = r.room_id
            ORDER BY a.created_at DESC
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_active_allocations():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT a.*,
                   s.full_name, s.reg_number, s.department, s.phone,
                   r.room_number, r.block, r.room_type, r.monthly_fee
            FROM allocations a
            JOIN students s ON a.student_id = s.student_id
            JOIN rooms    r ON a.room_id    = r.room_id
            WHERE a.status='Active'
            ORDER BY r.room_number
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


# ══════════════════════════════════════════════
#  FEES
# ══════════════════════════════════════════════

def add_fee(data: dict):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        sql = """
            INSERT INTO fees
                (student_id, room_id, amount, fee_type, month_year,
                 due_date, status, payment_method, receipt_no, remarks)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(sql, (
            data.get("student_id"), data.get("room_id"),
            data.get("amount"),     data.get("fee_type"),
            data.get("month_year"), data.get("due_date"),
            data.get("status", "Pending"), data.get("payment_method"),
            data.get("receipt_no"), data.get("remarks"),
        ))
        conn.commit()
        return True, f"Fee record added (ID {cur.lastrowid})"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def mark_fee_paid(fee_id: int, paid_date, payment_method, receipt_no=""):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE fees SET status='Paid', paid_date=%s,
                            payment_method=%s, receipt_no=%s
            WHERE fee_id=%s
        """, (paid_date, payment_method, receipt_no, fee_id))
        conn.commit()
        return True, "Fee marked as paid"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def get_all_fees(status_filter=None):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        if status_filter and status_filter != "All":
            cur.execute("""
                SELECT f.*, s.full_name, s.reg_number, r.room_number
                FROM fees f
                JOIN students s ON f.student_id = s.student_id
                LEFT JOIN rooms r ON f.room_id = r.room_id
                WHERE f.status=%s
                ORDER BY f.created_at DESC
            """, (status_filter,))
        else:
            cur.execute("""
                SELECT f.*, s.full_name, s.reg_number, r.room_number
                FROM fees f
                JOIN students s ON f.student_id = s.student_id
                LEFT JOIN rooms r ON f.room_id = r.room_id
                ORDER BY f.created_at DESC
            """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_student_fees(student_id: int):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT f.*, r.room_number FROM fees f
            LEFT JOIN rooms r ON f.room_id = r.room_id
            WHERE f.student_id=%s ORDER BY f.created_at DESC
        """, (student_id,))
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_fee_stats():
    conn = get_db_connection()
    if not conn:
        return {}
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT
                COUNT(*) as total_records,
                SUM(amount) as total_amount,
                SUM(CASE WHEN status='Paid'    THEN amount ELSE 0 END) as collected,
                SUM(CASE WHEN status='Pending' THEN amount ELSE 0 END) as pending,
                SUM(CASE WHEN status='Overdue' THEN amount ELSE 0 END) as overdue
            FROM fees
        """)
        return cur.fetchone() or {}
    finally:
        cur.close(); conn.close()


def get_monthly_collection():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT month_year, SUM(amount) as total,
                   SUM(CASE WHEN status='Paid' THEN amount ELSE 0 END) as collected
            FROM fees
            WHERE month_year IS NOT NULL
            GROUP BY month_year ORDER BY month_year DESC LIMIT 12
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


# ══════════════════════════════════════════════
#  COMPLAINTS
# ══════════════════════════════════════════════

def add_complaint(data: dict):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        sql = """
            INSERT INTO complaints
                (student_id, room_id, category, description, priority, status)
            VALUES (%s,%s,%s,%s,%s,'Open')
        """
        cur.execute(sql, (
            data.get("student_id"), data.get("room_id"),
            data.get("category"),   data.get("description"),
            data.get("priority"),
        ))
        conn.commit()
        return True, f"Complaint registered (ID {cur.lastrowid})"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def update_complaint_status(complaint_id: int, status: str, assigned_to="", resolution=""):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        resolved_at = "NOW()" if status == "Resolved" else "NULL"
        cur.execute(f"""
            UPDATE complaints SET
                status=%s, assigned_to=%s, resolution=%s,
                resolved_at={resolved_at}
            WHERE complaint_id=%s
        """, (status, assigned_to, resolution, complaint_id))
        conn.commit()
        return True, "Complaint updated"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def get_all_complaints(status_filter=None):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        if status_filter and status_filter != "All":
            cur.execute("""
                SELECT c.*, s.full_name, s.reg_number, r.room_number
                FROM complaints c
                JOIN students s ON c.student_id = s.student_id
                LEFT JOIN rooms r ON c.room_id = r.room_id
                WHERE c.status=%s ORDER BY c.created_at DESC
            """, (status_filter,))
        else:
            cur.execute("""
                SELECT c.*, s.full_name, s.reg_number, r.room_number
                FROM complaints c
                JOIN students s ON c.student_id = s.student_id
                LEFT JOIN rooms r ON c.room_id = r.room_id
                ORDER BY c.created_at DESC
            """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_complaint_stats():
    conn = get_db_connection()
    if not conn:
        return {}
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT
                COUNT(*) as total,
                SUM(status='Open') as open_complaints,
                SUM(status='In Progress') as in_progress,
                SUM(status='Resolved') as resolved,
                SUM(priority='Urgent') as urgent
            FROM complaints
        """)
        return cur.fetchone() or {}
    finally:
        cur.close(); conn.close()


# ══════════════════════════════════════════════
#  VISITORS
# ══════════════════════════════════════════════

def add_visitor(data: dict):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        sql = """
            INSERT INTO visitors
                (student_id, visitor_name, relation, phone, cnic, purpose, check_in)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(sql, (
            data.get("student_id"),   data.get("visitor_name"),
            data.get("relation"),     data.get("phone"),
            data.get("cnic"),         data.get("purpose"),
            data.get("check_in"),
        ))
        conn.commit()
        return True, f"Visitor logged (ID {cur.lastrowid})"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def checkout_visitor(visitor_id: int, check_out):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        cur.execute("UPDATE visitors SET check_out=%s WHERE visitor_id=%s", (check_out, visitor_id))
        conn.commit()
        return True, "Visitor checked out"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def get_all_visitors():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT v.*, s.full_name as student_name, s.reg_number
            FROM visitors v
            JOIN students s ON v.student_id = s.student_id
            ORDER BY v.check_in DESC
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


# ══════════════════════════════════════════════
#  NOTICES
# ══════════════════════════════════════════════

def add_notice(data: dict):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        sql = """
            INSERT INTO notices
                (title, content, category, priority, posted_by, valid_until, status)
            VALUES (%s,%s,%s,%s,%s,%s,'Active')
        """
        cur.execute(sql, (
            data.get("title"),      data.get("content"),
            data.get("category"),   data.get("priority"),
            data.get("posted_by"),  data.get("valid_until"),
        ))
        conn.commit()
        return True, "Notice posted successfully"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def get_active_notices():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT * FROM notices WHERE status='Active'
            ORDER BY
                FIELD(priority,'Urgent','High','Normal','Low'),
                created_at DESC
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_all_notices():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM notices ORDER BY created_at DESC")
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def delete_notice(notice_id: int):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM notices WHERE notice_id=%s", (notice_id,))
        conn.commit()
        return True, "Notice deleted"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


# ══════════════════════════════════════════════
#  DASHBOARD SUMMARY
# ══════════════════════════════════════════════

def get_dashboard_summary():
    conn = get_db_connection()
    if not conn:
        return {}
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT
                (SELECT COUNT(*) FROM students WHERE status='Active')          AS active_students,
                (SELECT COUNT(*) FROM rooms)                                    AS total_rooms,
                (SELECT SUM(capacity) FROM rooms)                              AS total_beds,
                (SELECT SUM(occupied) FROM rooms)                              AS occupied_beds,
                (SELECT COUNT(*) FROM allocations WHERE status='Active')       AS active_allocations,
                (SELECT COUNT(*) FROM fees WHERE status='Pending')             AS pending_fees,
                (SELECT COALESCE(SUM(amount),0) FROM fees WHERE status='Pending') AS pending_amount,
                (SELECT COUNT(*) FROM complaints WHERE status='Open')          AS open_complaints,
                (SELECT COUNT(*) FROM visitors WHERE check_out IS NULL)        AS current_visitors,
                (SELECT COUNT(*) FROM notices WHERE status='Active')           AS active_notices
        """)
        return cur.fetchone() or {}
    finally:
        cur.close(); conn.close()
