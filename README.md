# 🏠 Hostel Management System
**University Project | Full Stack: Python + Streamlit + MySQL**

---

## 📋 Project Overview

A complete **Hostel Management System** built for university administration. This system manages:
- 👨‍🎓 **Students** — registration, profiles, academic info
- 🏠 **Rooms** — room inventory, types, capacities, fees
- 🔑 **Allocations** — assign/vacate rooms with live occupancy tracking
- 💰 **Fees** — monthly & other fee tracking, payment recording
- 📢 **Complaints** — maintenance requests & issue tracking
- 👥 **Visitors** — visitor log with check-in/check-out
- 📌 **Notices** — notice board for hostel announcements
- 📊 **Dashboard** — real-time KPIs & charts

---

## 🛠️ Tech Stack

| Layer     | Technology              |
|-----------|-------------------------|
| Frontend  | Streamlit               |
| Backend   | Python 3.10+            |
| Database  | MySQL 8.x               |
| Charts    | Plotly                  |
| Data      | Pandas                  |

---

## 🚀 Setup Instructions

### 1. Prerequisites
```bash
# Install Python 3.10+
python --version

# Install MySQL 8.x and ensure it's running
mysql --version
```

### 2. Clone / Extract Project
```bash
cd hostel_management
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
Edit `config/db_config.py`:
```python
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",          # your MySQL username
    "password": "yourpassword",  # your MySQL password
    "database": "hostel_mgmt_db",
}
```

### 5. Run the Application
```bash
streamlit run app.py
```

Open **http://localhost:8501** in your browser.

### 6. First-Time Setup
1. On the login page, expand **"Database Setup"**
2. Click **"Initialize Database"** — this creates all tables and seeds sample data
3. Login with: **admin / admin123**

---

## 📁 Project Structure

```
hostel_management/
├── app.py                    # Main Streamlit application (frontend + routing)
├── requirements.txt
├── README.md
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration
├── config/
│   ├── __init__.py
│   └── db_config.py          # Database & app configuration
└── backend/
    ├── __init__.py
    ├── database.py           # DB connection, schema creation, seeding
    ├── students.py           # Student CRUD operations
    ├── rooms.py              # Room CRUD operations
    └── operations.py         # Allocations, Fees, Complaints, Visitors, Notices
```

---

## 🗄️ Database Schema (7 Tables)

| Table         | Description                          |
|---------------|--------------------------------------|
| `students`    | Student profiles and academic info   |
| `rooms`       | Room inventory and details           |
| `allocations` | Room-student assignments             |
| `fees`        | Fee records and payment tracking     |
| `complaints`  | Complaints and maintenance requests  |
| `visitors`    | Visitor log with check-in/out        |
| `notices`     | Notice board announcements           |
| `users`       | Admin/staff user accounts            |

---

## 🔑 Default Login

| Username | Password |
|----------|----------|
| admin    | admin123 |

---

## 🖥️ Features

### Dashboard
- Live KPI cards: students, rooms, beds, fees, complaints, visitors
- Room occupancy bar chart by block
- Monthly fee collection chart
- Active notices preview

### Student Management
- Full CRUD (Create, Read, Update, Delete)
- Search by name, reg number, email, department
- Gender, department, semester tracking
- Guardian contact information

### Room Management
- Room inventory with block/floor organization
- Real-time occupancy tracking
- View current room occupants
- Bed availability per room

### Room Allocation
- Allocate rooms to unallocated students only
- Automatic capacity checks
- Vacate rooms with date tracking
- Full allocation history

### Fee Management
- Monthly, Security, Admission, Fine fee types
- Mark fees as paid with receipt number
- Payment method tracking (Cash, Bank Transfer, Online)
- Fee summary: collected vs pending vs overdue

### Complaints
- Categories: Maintenance, Electricity, Plumbing, etc.
- Priority levels: Low, Medium, High, Urgent
- Assign complaints to staff
- Track resolution with notes

### Visitor Management
- Log visitors with CNIC and relation to student
- Check-in / Check-out timestamps
- Current visitors tracking

### Notice Board
- Post notices with priority and category
- Color-coded by urgency
- Valid-until date support

---

## 📊 Sample Data

The database is seeded with:
- **12 rooms** across Blocks A, B, C
- **5 students** across different departments
- **3 notices** as examples
- **1 admin user**

---

## 🔒 Security Notes
- Passwords should be hashed with bcrypt in production
- Use environment variables for DB credentials in production
- Add proper user roles and session management for deployment

---

*Developed as a university project demonstrating full-stack Python development with MySQL database integration.*
