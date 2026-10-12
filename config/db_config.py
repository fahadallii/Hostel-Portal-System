"""
Database Configuration for Hostel Management System
University Project - Full Stack Python + MySQL
"""

import streamlit as st

def get_db_config():
    try:
        return {
            "host":               st.secrets["mysql"]["host"],
            "port":               int(st.secrets["mysql"]["port"]),
            "user":               st.secrets["mysql"]["user"],
            "password":           st.secrets["mysql"]["password"],
            "database":           st.secrets["mysql"]["database"],
            "autocommit":         False,
            "charset":            "utf8mb4",
            "use_unicode":        True,
            "connection_timeout": 10,
            "ssl_disabled":       False,
        }
    except:
        return {
            "host":               "localhost",
            "port":               3306,
            "user":               "root",
            "password":           "root123",
            "database":           "hostel_mgmt_db",
            "autocommit":         False,
            "charset":            "utf8mb4",
            "use_unicode":        True,
            "connection_timeout": 10,
            "ssl_disabled":       False,
        }

DB_CONFIG = get_db_config()

APP_CONFIG = {
    "app_name":        "University Hostel Management System",
    "university":      "SSUHP",
    "admin_username":  "admin",
    "admin_password":  "admin123",
    "version":         "1.0.0",
    "currency":        "PKR",
    "currency_symbol": "₨",
}
