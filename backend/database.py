"""
Database Connection Manager
Handles MySQL connection, schema creation, and seeding
"""

import mysql.connector
from mysql.connector import Error, pooling
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.db_config import DB_CONFIG


# ─────────────────────────────────────────────
#  CONNECTION HELPERS
# ─────────────────────────────────────────────

def get_connection():
    """Return a raw MySQL connection (no database selected yet)."""
    cfg = {k: v for k, v in DB_CONFIG.items() if k != "database"}
    return mysql.connector.connect(**cfg)


def get_db_connection():
    """Return a connection to the hostel_mgmt_db database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Error as e:
        return None


def test_connection():
    """Test basic MySQL connectivity. Returns (success, message)."""
    try:
        conn = get_connection()
        if conn.is_connected():
            info = conn.get_server_info()
            conn.close()
            return True, f"Connected to MySQL Server version {info}"
    except Error as e:
        return False, str(e)
    return False, "Unknown error"


# ─────────────────────────────────────────────
#  SCHEMA
# ─────────────────────────────────────────────

SCHEMA_SQL = """
-- ── STUDENTS ────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    student_id      INT AUTO_INCREMENT PRIMARY KEY,
    reg_number      VARCHAR(20)  UNIQUE NOT NULL,
    full_name       VARCHAR(100) NOT NULL,
    email           VARCHAR(100) UNIQUE NOT NULL,
    phone           VARCHAR(20),
    cnic            VARCHAR(20),
    guardian_name   VARCHAR(100),
    guardian_phone  VARCHAR(20),
    department      VARCHAR(100),
    program         VARCHAR(50),
    semester        INT,
    gender          ENUM('Male','Female','Other') DEFAULT 'Male',
    dob             DATE,
    address         TEXT,
    photo_path      VARCHAR(255),
    status          ENUM('Active','Inactive','Graduated') DEFAULT 'Active',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ── ROOMS ────────────────────────────────────
CREATE TABLE IF NOT EXISTS rooms (
    room_id         INT AUTO_INCREMENT PRIMARY KEY,
    room_number     VARCHAR(10) UNIQUE NOT NULL,
    floor           INT NOT NULL,
    block           VARCHAR(10),
    room_type       ENUM('Single','Double','Triple','Quad') DEFAULT 'Double',
    capacity        INT NOT NULL DEFAULT 2,
    occupied        INT NOT NULL DEFAULT 0,
    monthly_fee     DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    amenities       TEXT,
    status          ENUM('Available','Full','Maintenance','Reserved') DEFAULT 'Available',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ── ALLOCATIONS ──────────────────────────────
CREATE TABLE IF NOT EXISTS allocations (
    allocation_id   INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    room_id         INT NOT NULL,
    alloc_date      DATE NOT NULL,
    vacate_date     DATE,
    status          ENUM('Active','Vacated','Transferred') DEFAULT 'Active',
    notes           TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id)    REFERENCES rooms(room_id)       ON DELETE CASCADE
);

-- ── FEES ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS fees (
    fee_id          INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    room_id         INT,
    amount          DECIMAL(10,2) NOT NULL,
    fee_type        ENUM('Monthly','Security','Admission','Fine','Other') DEFAULT 'Monthly',
    month_year      VARCHAR(10),
    due_date        DATE,
    paid_date       DATE,
    status          ENUM('Pending','Paid','Overdue','Waived') DEFAULT 'Pending',
    payment_method  ENUM('Cash','Bank Transfer','Online','Cheque') DEFAULT 'Cash',
    receipt_no      VARCHAR(30),
    remarks         TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id)    REFERENCES rooms(room_id)       ON DELETE SET NULL
);

-- ── COMPLAINTS ───────────────────────────────
CREATE TABLE IF NOT EXISTS complaints (
    complaint_id    INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    room_id         INT,
    category        ENUM('Maintenance','Electricity','Plumbing','Cleanliness','Security','Other') DEFAULT 'Other',
    description     TEXT NOT NULL,
    priority        ENUM('Low','Medium','High','Urgent') DEFAULT 'Medium',
    status          ENUM('Open','In Progress','Resolved','Closed') DEFAULT 'Open',
    assigned_to     VARCHAR(100),
    resolution      TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resolved_at     TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (room_id)    REFERENCES rooms(room_id)       ON DELETE SET NULL
);

-- ── VISITORS ─────────────────────────────────
CREATE TABLE IF NOT EXISTS visitors (
    visitor_id      INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    visitor_name    VARCHAR(100) NOT NULL,
    relation        VARCHAR(50),
    phone           VARCHAR(20),
    cnic            VARCHAR(20),
    purpose         TEXT,
    check_in        DATETIME NOT NULL,
    check_out       DATETIME,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE
);

-- ── NOTICES ──────────────────────────────────
CREATE TABLE IF NOT EXISTS notices (
    notice_id       INT AUTO_INCREMENT PRIMARY KEY,
    title           VARCHAR(200) NOT NULL,
    content         TEXT NOT NULL,
    category        ENUM('General','Fee','Maintenance','Security','Event','Emergency') DEFAULT 'General',
    priority        ENUM('Low','Normal','High','Urgent') DEFAULT 'Normal',
    posted_by       VARCHAR(100) DEFAULT 'Admin',
    valid_until     DATE,
    status          ENUM('Active','Expired','Draft') DEFAULT 'Active',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ── USERS (Admin / Staff) ────────────────────
CREATE TABLE IF NOT EXISTS users (
    user_id         INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    full_name       VARCHAR(100),
    role            ENUM('Admin','Warden','Staff') DEFAULT 'Staff',
    email           VARCHAR(100),
    status          ENUM('Active','Inactive') DEFAULT 'Active',
    last_login      TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

SEED_SQL = """
-- Default admin user (password: admin123)
INSERT IGNORE INTO users (username, password_hash, full_name, role, email)
VALUES ('admin', 'admin123', 'System Administrator', 'Admin', 'admin@university.edu');

-- Sample rooms
INSERT IGNORE INTO rooms (room_number, floor, block, room_type, capacity, monthly_fee, amenities, status) VALUES
('A-101', 1, 'A', 'Single',  1, 8000,  'AC, WiFi, Attached Bath',       'Available'),
('A-102', 1, 'A', 'Double',  2, 6000,  'AC, WiFi, Attached Bath',       'Available'),
('A-103', 1, 'A', 'Double',  2, 6000,  'Fan, WiFi',                     'Available'),
('A-201', 2, 'A', 'Triple',  3, 5000,  'AC, WiFi, Common Bath',         'Available'),
('A-202', 2, 'A', 'Quad',    4, 4000,  'Fan, WiFi, Common Bath',        'Available'),
('B-101', 1, 'B', 'Single',  1, 9000,  'AC, WiFi, Attached Bath, TV',   'Available'),
('B-102', 1, 'B', 'Double',  2, 7000,  'AC, WiFi, Attached Bath',       'Available'),
('B-103', 1, 'B', 'Double',  2, 7000,  'AC, WiFi',                      'Available'),
('B-201', 2, 'B', 'Triple',  3, 5500,  'AC, WiFi, Common Bath',         'Available'),
('B-202', 2, 'B', 'Quad',    4, 4500,  'AC, WiFi, Common Bath',         'Available'),
('C-101', 1, 'C', 'Single',  1, 7500,  'Fan, WiFi, Attached Bath',      'Maintenance'),
('C-102', 1, 'C', 'Double',  2, 5500,  'Fan, WiFi',                     'Available');

-- Sample students
INSERT IGNORE INTO students (reg_number, full_name, email, phone, department, program, semester, gender, status) VALUES
('2021-CS-01', 'Ahmed Hassan',    'ahmed@uni.edu',   '0300-1111111', 'Computer Science', 'BS CS',   5, 'Male',   'Active'),
('2021-CS-02', 'Sara Khan',       'sara@uni.edu',    '0300-2222222', 'Computer Science', 'BS CS',   5, 'Female', 'Active'),
('2022-EE-01', 'Bilal Ahmed',     'bilal@uni.edu',   '0300-3333333', 'Electrical Eng',   'BE EE',   3, 'Male',   'Active'),
('2022-ME-01', 'Fatima Malik',    'fatima@uni.edu',  '0300-4444444', 'Mech Engineering', 'BE ME',   3, 'Female', 'Active'),
('2020-MBA-01','Usman Tariq',     'usman@uni.edu',   '0300-5555555', 'Business Admin',   'MBA',     7, 'Male',   'Active');

-- Sample notices
INSERT IGNORE INTO notices (title, content, category, priority, posted_by) VALUES
('Welcome New Students', 'Welcome to the hostel! Please collect your room keys from the warden office between 9 AM - 5 PM.', 'General', 'Normal', 'Admin'),
('Fee Submission Deadline', 'Monthly hostel fee for June 2025 must be submitted by June 10. Late fee of PKR 500 will be charged.', 'Fee', 'High', 'Admin'),
('Electricity Maintenance', 'Block A electricity will be off on Sunday 8 AM - 12 PM for maintenance work.', 'Maintenance', 'High', 'Admin');
"""


def initialize_database():
    """Create DB, tables, and seed initial data. Returns (success, message)."""
    try:
        # 1. Create database if not exists
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        cursor.execute(f"USE {DB_CONFIG['database']}")

        # 2. Create tables
        for statement in SCHEMA_SQL.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)

        # 3. Seed data
        for statement in SEED_SQL.strip().split(";"):
            stmt = statement.strip()
            if stmt:
                try:
                    cursor.execute(stmt)
                except Error:
                    pass  # ignore duplicate seed rows

        conn.commit()
        cursor.close()
        conn.close()
        return True, "Database initialized successfully!"

    except Error as e:
        return False, f"Database error: {e}"
