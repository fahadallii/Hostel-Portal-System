"""
Room Management - CRUD operations
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.database import get_db_connection
from mysql.connector import Error


# ─── CREATE ──────────────────────────────────
def add_room(data: dict):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        sql = """
            INSERT INTO rooms
                (room_number, floor, block, room_type, capacity, monthly_fee, amenities, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        cur.execute(sql, (
            data.get("room_number"), data.get("floor"),
            data.get("block"),       data.get("room_type"),
            data.get("capacity"),    data.get("monthly_fee"),
            data.get("amenities"),   data.get("status", "Available"),
        ))
        conn.commit()
        return True, f"Room {data.get('room_number')} added successfully"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


# ─── READ ─────────────────────────────────────
def get_all_rooms(status_filter=None):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        if status_filter and status_filter != "All":
            cur.execute("""
                SELECT r.*,
                       (r.capacity - r.occupied) AS available_beds
                FROM rooms r WHERE r.status=%s ORDER BY r.block, r.room_number
            """, (status_filter,))
        else:
            cur.execute("""
                SELECT r.*,
                       (r.capacity - r.occupied) AS available_beds
                FROM rooms r ORDER BY r.block, r.room_number
            """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_room_by_id(room_id: int):
    conn = get_db_connection()
    if not conn:
        return None
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM rooms WHERE room_id=%s", (room_id,))
        return cur.fetchone()
    finally:
        cur.close(); conn.close()


def get_available_rooms():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT *, (capacity - occupied) AS available_beds
            FROM rooms
            WHERE status='Available' AND occupied < capacity
            ORDER BY block, room_number
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


def get_room_occupants(room_id: int):
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT s.student_id, s.reg_number, s.full_name, s.email,
                   s.phone, s.department, s.program,
                   a.alloc_date, a.allocation_id
            FROM allocations a
            JOIN students s ON a.student_id = s.student_id
            WHERE a.room_id=%s AND a.status='Active'
        """, (room_id,))
        return cur.fetchall()
    finally:
        cur.close(); conn.close()


# ─── UPDATE ───────────────────────────────────
def update_room(room_id: int, data: dict):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        sql = """
            UPDATE rooms SET
                room_number=%s, floor=%s, block=%s, room_type=%s,
                capacity=%s, monthly_fee=%s, amenities=%s, status=%s
            WHERE room_id=%s
        """
        cur.execute(sql, (
            data.get("room_number"), data.get("floor"),
            data.get("block"),       data.get("room_type"),
            data.get("capacity"),    data.get("monthly_fee"),
            data.get("amenities"),   data.get("status"),
            room_id,
        ))
        conn.commit()
        return True, "Room updated successfully"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


def update_room_occupancy(room_id: int, delta: int):
    """Increment or decrement occupied count by delta (+1 / -1)."""
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        cur.execute("SELECT capacity, occupied FROM rooms WHERE room_id=%s", (room_id,))
        row = cur.fetchone()
        if not row:
            return False, "Room not found"
        capacity, occupied = row
        new_occ = max(0, occupied + delta)
        new_status = "Full" if new_occ >= capacity else "Available"
        cur.execute(
            "UPDATE rooms SET occupied=%s, status=%s WHERE room_id=%s",
            (new_occ, new_status, room_id)
        )
        conn.commit()
        return True, "Occupancy updated"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


# ─── DELETE ───────────────────────────────────
def delete_room(room_id: int):
    conn = get_db_connection()
    if not conn:
        return False, "No database connection"
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM rooms WHERE room_id=%s", (room_id,))
        conn.commit()
        return True, "Room deleted successfully"
    except Error as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close(); conn.close()


# ─── STATS ────────────────────────────────────
def get_room_stats():
    conn = get_db_connection()
    if not conn:
        return {}
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT
                COUNT(*) as total_rooms,
                SUM(capacity) as total_beds,
                SUM(occupied) as occupied_beds,
                SUM(capacity - occupied) as vacant_beds,
                SUM(status='Available') as available_rooms,
                SUM(status='Full') as full_rooms,
                SUM(status='Maintenance') as maintenance_rooms
            FROM rooms
        """)
        return cur.fetchone() or {}
    finally:
        cur.close(); conn.close()


def get_rooms_by_block():
    conn = get_db_connection()
    if not conn:
        return []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT block,
                   COUNT(*) as rooms,
                   SUM(capacity) as total_beds,
                   SUM(occupied) as occupied_beds
            FROM rooms GROUP BY block ORDER BY block
        """)
        return cur.fetchall()
    finally:
        cur.close(); conn.close()
