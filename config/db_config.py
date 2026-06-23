"""
Database Configuration for Hostel Management System
University Project - Full Stack Python + MySQL
"""

DB_CONFIG = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "root123",
    "database": "hostel_mgmt_db",
    "autocommit": False,
    "charset": "utf8mb4",
    "use_unicode": True,
    "connection_timeout": 10,
}

APP_CONFIG = {
    "app_name": "University Hostel Portal System",
    "university": "SSUHP",          # ← change this
    "admin_username": "admin",
    "admin_password": "admin123",
    "version": "1.0.0",
    "currency": "PKR",
    "currency_symbol": "₨",
}
