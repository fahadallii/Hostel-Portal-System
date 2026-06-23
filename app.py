import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime
import sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config.db_config import APP_CONFIG
from backend.database import test_connection, initialize_database
from backend.students import (
    add_student, get_all_students, get_student_by_id,
    update_student, delete_student, search_students,
    get_unallocated_students, get_student_stats,
)
from backend.rooms import (
    add_room, get_all_rooms, get_room_by_id,
    update_room, delete_room, get_available_rooms,
    get_room_occupants, get_room_stats, get_rooms_by_block,
)
from backend.operations import (
    allocate_room, vacate_room, get_all_allocations, get_active_allocations,
    add_fee, mark_fee_paid, get_all_fees, get_student_fees, get_fee_stats, get_monthly_collection,
    add_complaint, update_complaint_status, get_all_complaints, get_complaint_stats,
    add_visitor, checkout_visitor, get_all_visitors,
    add_notice, get_active_notices, get_all_notices, delete_notice,
    get_dashboard_summary,
)

st.set_page_config(
    page_title="SSUHP - SIR SYED UNIVERSITY HOSTEL PORTAL SYSTEM",
    page_icon="H",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={},
)

FUTURISTIC_CSS = """
<style>
/* Hide sidebar toggle button completely */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
.st-emotion-cache-1dp5vir { display: none !important; }
.st-emotion-cache-1egp75v { display: none !important; }
[data-testid="stToolbar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
[data-testid="stSidebarCollapseButton"] { display: none !important; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
section[data-testid="stSidebarCollapsedControl"] { display: none !important; }
div[data-testid="stSidebarCollapsedControl"] { display: none !important; }
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=Share+Tech+Mono&family=Exo+2:wght@200;300;400;600;700&display=swap');

:root {
    --green-primary:   #00ff88;
    --green-dark:      #00c96a;
    --green-deeper:    #00874a;
    --green-glow:      rgba(0,255,136,0.15);
    --green-glow-str:  rgba(0,255,136,0.35);
    --bg-main:         #f0f7f4;
    --bg-card:         #ffffff;
    --bg-sidebar:      #060f0a;
    --text-primary:    #0a1a0f;
    --text-secondary:  #2d5a3d;
    --text-muted:      #6b8f76;
    --border:          rgba(0,255,136,0.2);
    --border-strong:   rgba(0,255,136,0.5);
    --shadow:          0 4px 24px rgba(0,180,80,0.08);
    --shadow-hover:    0 8px 40px rgba(0,255,136,0.18);
}

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {
    background: #060f0a !important;
    border: 1px solid rgba(0,255,136,0.3) !important;
    border-radius: 4px !important;
    color: #00ff88 !important;
    width: 32px !important;
    height: 32px !important;
}

[data-testid="stSidebarCollapseButton"] svg,
[data-testid="stSidebarCollapsedControl"] svg {
    fill: #00ff88 !important;
    stroke: #00ff88 !important;
}

[data-testid="stSidebarCollapseButton"]:hover,
[data-testid="stSidebarCollapsedControl"]:hover {
    background: rgba(0,255,136,0.1) !important;
    border-color: #00ff88 !important;
}

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Exo 2', sans-serif;
    background-color: var(--bg-main) !important;
}

/* ── GRID BACKGROUND ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image:
        linear-gradient(rgba(0,255,136,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,136,0.04) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-strong) !important;
    box-shadow: 4px 0 30px rgba(0,255,136,0.08) !important;
}
[data-testid="stSidebar"] * {
    color: #c8fce2 !important;
    font-family: 'Exo 2', sans-serif !important;
}
[data-testid="stSidebarCollapsedControl"] { display: none !important; }
[data-testid="stSidebar"] hr {
    border-color: rgba(0,255,136,0.15) !important;
    margin: 12px 0 !important;
}

/* sidebar nav buttons */
[data-testid="stSidebar"] .stButton button {
    background: transparent !important;
    border: 1px solid rgba(0,255,136,0.15) !important;
    color: #a0d4b4 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.88rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    padding: 10px 16px !important;
    border-radius: 4px !important;
    transition: all 0.2s ease !important;
    text-align: left !important;
    width: 100% !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(0,255,136,0.08) !important;
    border-color: var(--green-primary) !important;
    color: var(--green-primary) !important;
    box-shadow: 0 0 16px rgba(0,255,136,0.15) !important;
}

/* ── MAIN CONTENT ── */
.main .block-container {
    padding: 2rem 2.5rem !important;
    max-width: 1400px !important;
}

/* ── SECTION HEADER ── */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--text-primary);
    border-left: 3px solid var(--green-primary);
    padding: 10px 20px;
    background: linear-gradient(90deg, rgba(0,255,136,0.06), transparent);
    margin-bottom: 24px;
    position: relative;
}
.section-header::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, var(--green-primary), transparent);
    opacity: 0.3;
}

/* ── METRIC CARDS ── */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 6px;
    padding: 22px 18px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
    box-shadow: var(--shadow);
}
.metric-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--green-primary), transparent);
}
.metric-card:hover {
    border-color: var(--border-strong);
    box-shadow: var(--shadow-hover);
    transform: translateY(-2px);
}
.metric-card .mc-value {
    font-family: 'Share Tech Mono', monospace;
    font-size: 2.4rem;
    color: var(--green-deeper);
    line-height: 1;
    margin-bottom: 6px;
}
.metric-card .mc-label {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-muted);
}
.metric-card .mc-icon {
    font-size: 1.4rem;
    margin-bottom: 8px;
    opacity: 0.6;
}

/* ── NOTICE CARDS ── */
.notice-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--green-primary);
    border-radius: 0 6px 6px 0;
    padding: 16px 20px;
    margin-bottom: 10px;
    transition: all 0.2s ease;
}
.notice-card:hover {
    border-left-color: var(--green-dark);
    box-shadow: var(--shadow-hover);
}
.notice-card.urgent { border-left-color: #ff4444; }
.notice-card.high   { border-left-color: #ffaa00; }
.notice-card .nc-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    color: var(--text-primary);
    margin-bottom: 4px;
}
.notice-card .nc-body {
    font-size: 0.87rem;
    color: var(--text-secondary);
    line-height: 1.5;
}
.notice-card .nc-meta {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: var(--text-muted);
    margin-top: 8px;
}

/* ── BADGES ── */
.badge {
    display: inline-block;
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 2px 10px;
    border-radius: 2px;
    margin-left: 6px;
}
.badge-success  { background: rgba(0,255,136,0.12); color: #00874a; border: 1px solid rgba(0,200,100,0.3); }
.badge-warning  { background: rgba(255,170,0,0.1);  color: #a06800; border: 1px solid rgba(255,170,0,0.3); }
.badge-danger   { background: rgba(255,68,68,0.1);  color: #c00;    border: 1px solid rgba(255,68,68,0.3); }
.badge-info     { background: rgba(0,150,255,0.08); color: #0060b0; border: 1px solid rgba(0,150,255,0.2); }
.badge-neutral  { background: rgba(0,0,0,0.04);     color: #555;    border: 1px solid rgba(0,0,0,0.1); }

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
    padding: 10px 20px !important;
    border-bottom: 2px solid transparent !important;
    background: transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--green-deeper) !important;
    border-bottom-color: var(--green-primary) !important;
}

/* ── INPUTS ── */
.stTextInput input, .stTextArea textarea, .stSelectbox select,
.stNumberInput input, .stDateInput input {
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 0.9rem !important;
    background: white !important;
    color: var(--text-primary) !important;
    transition: border-color 0.2s ease !important;
}
/* Fix black dropdowns and selectboxes */
.stSelectbox > div > div,
.stSelectbox > div > div > div,
[data-baseweb="select"] > div,
[data-baseweb="select"] div,
[data-baseweb="popover"] div,
.stNumberInput > div > div {
    background-color: white !important;
    color: #0a1a0f !important;
}
[data-baseweb="select"] span,
[data-baseweb="select"] div div {
    color: #0a1a0f !important;
    background: white !important;
}
[data-baseweb="popover"] {
    background: white !important;
}
[data-baseweb="menu"] {
    background: white !important;
}
[data-baseweb="menu"] li {
    background: white !important;
    color: #0a1a0f !important;
}
[data-baseweb="menu"] li:hover {
    background: rgba(0,255,136,0.08) !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--green-primary) !important;
    box-shadow: 0 0 0 3px rgba(0,255,136,0.1) !important;
}


/* ── BUTTONS ── */
.stButton button[kind="primary"] {
    background: var(--green-deeper) !important;
    color: white !important;
    border: none !important;
    border-radius: 4px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 10px 24px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 2px 12px rgba(0,135,74,0.25) !important;
}
.stButton button[kind="primary"]:hover {
    background: var(--green-dark) !important;
    box-shadow: 0 4px 20px rgba(0,200,106,0.4) !important;
    transform: translateY(-1px) !important;
}
.stButton button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--border-strong) !important;
    color: var(--green-deeper) !important;
    border-radius: 4px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
.stButton button[kind="secondary"]:hover {
    background: var(--green-glow) !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    overflow: hidden !important;
}
[data-testid="stDataFrame"] th {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    background: #f4faf6 !important;
    color: var(--text-secondary) !important;
}

/* ── ALERTS ── */
.stSuccess, .stError, .stInfo, .stWarning {
    border-radius: 4px !important;
    font-family: 'Exo 2', sans-serif !important;
    font-size: 0.88rem !important;
}

/* ── DIVIDER ── */
hr {
    border-color: var(--border) !important;
}

/* ── METRICS (native) ── */
[data-testid="metric-container"] {
    background: white !important;
    border: 1px solid var(--border) !important;
    border-radius: 6px !important;
    padding: 16px !important;
}
[data-testid="metric-container"] label {
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    color: var(--text-muted) !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-family: 'Share Tech Mono', monospace !important;
    color: var(--green-deeper) !important;
}

/* ── LOGIN PAGE ── */
.login-wrapper {
    background: white;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 48px 40px;
    box-shadow: var(--shadow-hover);
    position: relative;
    overflow: hidden;
}
.login-wrapper::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--green-primary), var(--green-deeper), var(--green-primary));
}
.login-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--text-primary);
    margin: 0;
}
.login-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.08em;
    margin-top: 4px;
    margin-bottom: 32px;
}
.sys-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    color: var(--green-deeper);
    text-transform: uppercase;
    margin-bottom: 20px;
    border: 1px solid var(--border);
    padding: 6px 14px;
    display: inline-block;
    border-radius: 2px;
    background: rgba(0,255,136,0.04);
}

/* ── SIDEBAR BRAND ── */
.sidebar-brand {
    padding: 20px 4px 16px;
    border-bottom: 1px solid rgba(0,255,136,0.12);
    margin-bottom: 16px;
}
.sidebar-brand .brand-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--green-primary) !important;
}
.sidebar-brand .brand-sub {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: rgba(0,255,136,0.4) !important;
    letter-spacing: 0.08em;
    margin-top: 2px;
}
.sidebar-user {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.72rem;
    color: rgba(200,252,226,0.6) !important;
    letter-spacing: 0.06em;
    padding: 8px 4px;
    margin-bottom: 8px;
}
button[title="keyboard_double_arrow_left"],
button[title="keyboard_double_arrow_right"],
[data-testid="collapsedControl"],
[data-testid="baseButton-headerNoPadding"] {
    display: none !important;
}
section[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
}

.sidebar-section {
    font-family: 'Rajdhani', sans-serif;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: rgba(0,255,136,0.35) !important;
    padding: 12px 4px 4px;
}
</style>
"""

st.markdown(FUTURISTIC_CSS, unsafe_allow_html=True)

# ── SESSION STATE ──────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "db_ready" not in st.session_state:
    st.session_state.db_ready = False
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"


# ── HELPERS ───────────────────────────────────────────────
def ok(msg):  st.success(msg)
def err(msg): st.error(msg)
def inf(msg): st.info(msg)

def metric_card(value, label):
    st.markdown(f"""
    <div class="metric-card">
        <div class="mc-value">{value}</div>
        <div class="mc-label">{label}</div>
    </div>""", unsafe_allow_html=True)

def section(title):
    st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)

def badge(text, kind="neutral"):
    return f'<span class="badge badge-{kind}">{text}</span>'


# ════════════════════════════════════════════════════════════
#  LOGIN
# ════════════════════════════════════════════════════════════
def login_page():
    st.markdown("<br>", unsafe_allow_html=True)
    _, col, _ = st.columns([1, 1.4, 1])
    with col:
        st.markdown("""
        <div class="login-wrapper">
            <div class="sys-label">SYSTEM ACCESS PORTAL</div>
            <div class="login-title">Hostel Management</div>
            <div class="login-sub">SSUHP &nbsp;|&nbsp; ADMINISTRATION SYSTEM</div>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("Database Initialization", expanded=not st.session_state.db_ready):
            st.markdown('<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.78rem;color:#2d5a3d;">Configure credentials in config/db_config.py before initializing.</p>', unsafe_allow_html=True)
            conn_ok, conn_msg = test_connection()
            if conn_ok:
                st.success(conn_msg)
                st.session_state.db_ready = True
            else:
                st.error(conn_msg)
            if st.button("Initialize Database", type="primary", use_container_width=True):
                with st.spinner("Initializing database..."):
                    success, msg = initialize_database()
                if success:
                    st.session_state.db_ready = True
                    ok(msg)
                else:
                    err(msg)

        st.markdown("<br>", unsafe_allow_html=True)
        username = st.text_input("Username", placeholder="Enter username")
        password = st.text_input("Password", type="password", placeholder="Enter password")
        st.markdown("<br>", unsafe_allow_html=True)

        if st.button("Access System", type="primary", use_container_width=True):
            if username == APP_CONFIG["admin_username"] and password == APP_CONFIG["admin_password"]:
                if not st.session_state.db_ready:
                    err("Initialize the database first.")
                else:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
            else:
                err("Invalid credentials.")

        st.markdown("""
        <p style="font-family:'Share Tech Mono',monospace;font-size:0.68rem;
           color:#6b8f76;text-align:center;margin-top:20px;">
            Welcome to Sir Syed University Hostel Portal
        </p>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════
def sidebar():
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-brand">
            <div class="brand-title">SSUHP</div>
            <div class="brand-sub">HOSTEL PORTAL SYSTEM</div>
        </div>
        <div class="sidebar-user">
            USER &nbsp;/&nbsp; {st.session_state.get('username','admin').upper()}
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="sidebar-section">Navigation</div>', unsafe_allow_html=True)

        pages = [
            ("Dashboard",    "DASHBOARD"),
            ("Students",     "STUDENTS"),
            ("Rooms",        "ROOMS"),
            ("Allocations",  "ALLOCATIONS"),
            ("Fees",         "FEES"),
            ("Complaints",   "COMPLAINTS"),
            ("Visitors",     "VISITORS"),
            ("Notices",      "NOTICES"),
        ]
        for key, label in pages:
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key

        st.divider()
        st.markdown('<div class="sidebar-section">System</div>', unsafe_allow_html=True)
        if st.button("LOGOUT", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()

    return st.session_state.get("page", "Dashboard")


# ════════════════════════════════════════════════════════════
#  DASHBOARD
# ════════════════════════════════════════════════════════════
def page_dashboard():
    section("Dashboard / System Overview")

    summary = get_dashboard_summary()
    if not summary:
        err("Could not load dashboard data.")
        return

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1: metric_card(summary.get("active_students", 0),  "Active Students")
    with c2: metric_card(summary.get("total_rooms", 0),      "Total Rooms")
    with c3: metric_card(summary.get("occupied_beds", 0),    "Occupied Beds")
    with c4: metric_card(summary.get("pending_fees", 0),     "Pending Fees")
    with c5: metric_card(summary.get("open_complaints", 0),  "Open Complaints")
    with c6: metric_card(summary.get("current_visitors", 0), "Visitors Inside")

    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<p style="font-family:\'Rajdhani\',sans-serif;font-size:0.78rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#6b8f76;margin-bottom:12px;">Room Occupancy by Block</p>', unsafe_allow_html=True)
        blocks = get_rooms_by_block()
        if blocks:
            df_b = pd.DataFrame(blocks)
            fig = go.Figure(data=[
                go.Bar(name='Occupied', x=df_b['block'], y=df_b['occupied_beds'],
                       marker_color='#00874a', marker_line_width=0),
                go.Bar(name='Vacant',   x=df_b['block'],
                       y=df_b['total_beds'].astype(int) - df_b['occupied_beds'].astype(int),
                       marker_color='rgba(0,200,100,0.15)', marker_line_color='rgba(0,200,100,0.4)',
                       marker_line_width=1),
            ])
            fig.update_layout(
                barmode='stack', height=280,
                margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor='white', plot_bgcolor='white',
                font=dict(family='Exo 2, sans-serif', size=11, color='#2d5a3d'),
                legend=dict(orientation='h', y=1.12, font=dict(size=10)),
                xaxis=dict(gridcolor='rgba(0,0,0,0.04)'),
                yaxis=dict(gridcolor='rgba(0,0,0,0.04)'),
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown('<p style="font-family:\'Rajdhani\',sans-serif;font-size:0.78rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#6b8f76;margin-bottom:12px;">Monthly Fee Collection</p>', unsafe_allow_html=True)
        monthly = get_monthly_collection()
        if monthly:
            df_m = pd.DataFrame(monthly)
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df_m['month_year'], y=df_m['total'],
                name='Total', marker_color='rgba(0,180,80,0.15)',
                marker_line_color='rgba(0,180,80,0.4)', marker_line_width=1,
            ))
            fig2.add_trace(go.Bar(
                x=df_m['month_year'], y=df_m['collected'],
                name='Collected', marker_color='#00874a', marker_line_width=0,
            ))
            fig2.update_layout(
                barmode='overlay', height=280,
                margin=dict(l=0,r=0,t=10,b=0),
                paper_bgcolor='white', plot_bgcolor='white',
                font=dict(family='Exo 2, sans-serif', size=11, color='#2d5a3d'),
                legend=dict(orientation='h', y=1.12, font=dict(size=10)),
                xaxis=dict(gridcolor='rgba(0,0,0,0.04)'),
                yaxis=dict(gridcolor='rgba(0,0,0,0.04)'),
            )
            st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<p style="font-family:\'Rajdhani\',sans-serif;font-size:0.78rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#6b8f76;margin-bottom:12px;">Active Notices</p>', unsafe_allow_html=True)
    notices = get_active_notices()
    if notices:
        for n in notices[:4]:
            p = n.get('priority','Normal')
            cls = "urgent" if p=="Urgent" else ("high" if p=="High" else "")
            st.markdown(f"""
            <div class="notice-card {cls}">
                <div class="nc-title">{n['title']} {badge(n['category'],'info')} {badge(p, 'danger' if p=='Urgent' else 'warning' if p=='High' else 'neutral')}</div>
                <div class="nc-body">{n['content'][:140]}{'...' if len(n['content'])>140 else ''}</div>
                <div class="nc-meta">POSTED BY {n['posted_by'].upper()} &nbsp;/&nbsp; {str(n['created_at'])[:10]}</div>
            </div>""", unsafe_allow_html=True)
    else:
        inf("No active notices.")


# ════════════════════════════════════════════════════════════
#  STUDENTS
# ════════════════════════════════════════════════════════════
def page_students():
    section("Student Management")
    tab_list, tab_add, tab_edit = st.tabs(["All Students", "Add Student", "Edit / Delete"])

    with tab_list:
        c1, c2 = st.columns([3, 1])
        with c1:
            q = st.text_input("Search", placeholder="Name, registration number, email, department...")
        with c2:
            sf = st.selectbox("Status", ["All","Active","Inactive","Graduated"])
        students = search_students(q) if q else get_all_students(sf)
        st.markdown(f'<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.75rem;color:#6b8f76;">{len(students)} RECORDS FOUND</p>', unsafe_allow_html=True)
        if students:
            df = pd.DataFrame(students)
            cols = [c for c in ['student_id','reg_number','full_name','email','phone','department','program','semester','gender','status'] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)
        stats = get_student_stats()
        if stats:
            s1,s2,s3,s4 = st.columns(4)
            s1.metric("Total",  stats.get("total",0))
            s2.metric("Active", stats.get("active",0))
            s3.metric("Male",   stats.get("male",0))
            s4.metric("Female", stats.get("female",0))

    with tab_add:
        with st.form("add_student_form"):
            st.markdown('<p style="font-family:\'Rajdhani\',sans-serif;font-weight:600;letter-spacing:0.06em;color:#2d5a3d;text-transform:uppercase;font-size:0.82rem;">Personal Information</p>', unsafe_allow_html=True)
            r1c1, r1c2, r1c3 = st.columns(3)
            reg_no    = r1c1.text_input("Registration Number", placeholder="2024-CS-01")
            full_name = r1c2.text_input("Full Name")
            gender    = r1c3.selectbox("Gender", ["Male","Female","Other"])
            r2c1, r2c2, r2c3 = st.columns(3)
            email = r2c1.text_input("Email")
            phone = r2c2.text_input("Phone")
            cnic  = r2c3.text_input("CNIC")
            dob   = st.date_input("Date of Birth", value=date(2000,1,1), min_value=date(1980,1,1), max_value=date(2010,12,31))
            st.markdown('<p style="font-family:\'Rajdhani\',sans-serif;font-weight:600;letter-spacing:0.06em;color:#2d5a3d;text-transform:uppercase;font-size:0.82rem;margin-top:12px;">Academic Information</p>', unsafe_allow_html=True)
            a1, a2, a3 = st.columns(3)
            dept    = a1.text_input("Department")
            program = a2.selectbox("Program", ["BS CS","BS SE","BE EE","BE ME","MBA","MCS","PhD","Other"])
            sem     = a3.number_input("Semester", 1, 10, 1)
            st.markdown('<p style="font-family:\'Rajdhani\',sans-serif;font-weight:600;letter-spacing:0.06em;color:#2d5a3d;text-transform:uppercase;font-size:0.82rem;margin-top:12px;">Guardian Information</p>', unsafe_allow_html=True)
            g1, g2 = st.columns(2)
            g_name  = g1.text_input("Guardian Name")
            g_phone = g2.text_input("Guardian Phone")
            address = st.text_area("Address")
            if st.form_submit_button("Add Student", type="primary", use_container_width=True):
                if not reg_no or not full_name or not email:
                    err("Registration number, full name, and email are required.")
                else:
                    res, msg = add_student({"reg_number":reg_no,"full_name":full_name,"email":email,"phone":phone,"cnic":cnic,"dob":str(dob),"gender":gender,"department":dept,"program":program,"semester":sem,"guardian_name":g_name,"guardian_phone":g_phone,"address":address})
                    ok(msg) if res else err(msg)

    with tab_edit:
        students_all = get_all_students()
        if not students_all:
            inf("No students in system.")
            return
        options = {f"{s['reg_number']} — {s['full_name']}": s['student_id'] for s in students_all}
        choice = st.selectbox("Select Student", list(options.keys()))
        sid = options[choice]
        s = get_student_by_id(sid)
        if not s: return
        with st.form("edit_student_form"):
            ec1, ec2, ec3 = st.columns(3)
            e_name   = ec1.text_input("Full Name",   s.get("full_name",""))
            e_email  = ec2.text_input("Email",        s.get("email",""))
            e_phone  = ec3.text_input("Phone",        s.get("phone","") or "")
            ed1, ed2, ed3 = st.columns(3)
            e_dept   = ed1.text_input("Department",   s.get("department","") or "")
            e_prog   = ed2.text_input("Program",      s.get("program","") or "")
            e_sem    = ed3.number_input("Semester",   1, 10, int(s.get("semester") or 1))
            e_status = st.selectbox("Status", ["Active","Inactive","Graduated"], index=["Active","Inactive","Graduated"].index(s.get("status","Active")))
            e_addr   = st.text_area("Address", s.get("address","") or "")
            if st.form_submit_button("Update Student", type="primary"):
                res, msg = update_student(sid, {"full_name":e_name,"email":e_email,"phone":e_phone,"cnic":s.get("cnic"),"guardian_name":s.get("guardian_name"),"guardian_phone":s.get("guardian_phone"),"department":e_dept,"program":e_prog,"semester":e_sem,"gender":s.get("gender"),"dob":str(s.get("dob","")) if s.get("dob") else None,"address":e_addr,"status":e_status})
                ok(msg) if res else err(msg)
        with st.expander("Delete Student"):
            st.warning("This will permanently delete the student and all associated records.")
            if st.button("Delete Student", type="secondary"):
                res, msg = delete_student(sid)
                ok(msg) if res else err(msg)
                if res: st.rerun()

# ════════════════════════════════════════════════════════════
#  ROOMS
# ════════════════════════════════════════════════════════════
def page_rooms():
    section("Room Management")
    tab_list, tab_add, tab_edit = st.tabs(["All Rooms", "Add Room", "Edit / Delete"])

    with tab_list:
        sf = st.selectbox("Filter by Status", ["All","Available","Full","Maintenance","Reserved"])
        rooms = get_all_rooms(sf)
        st.markdown(f'<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.75rem;color:#6b8f76;">{len(rooms)} ROOMS FOUND</p>', unsafe_allow_html=True)
        if rooms:
            df = pd.DataFrame(rooms)
            cols = [c for c in ['room_id','room_number','block','floor','room_type','capacity','occupied','available_beds','monthly_fee','status'] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)
        stats = get_room_stats()
        if stats:
            m1,m2,m3,m4,m5 = st.columns(5)
            m1.metric("Total Rooms",  stats.get("total_rooms",0))
            m2.metric("Total Beds",   stats.get("total_beds",0))
            m3.metric("Occupied",     stats.get("occupied_beds",0))
            m4.metric("Vacant",       stats.get("vacant_beds",0))
            m5.metric("Maintenance",  stats.get("maintenance_rooms",0))
        if stats and stats.get("total_beds",0):
            occ = int(stats.get("occupied_beds") or 0)
            vac = int(stats.get("total_beds") or 0) - occ
            fig = go.Figure(data=[go.Pie(
                values=[occ, vac], labels=["Occupied","Vacant"],
                marker=dict(colors=["#00874a","rgba(0,200,100,0.15)"],
                            line=dict(color=["#00874a","rgba(0,200,100,0.4)"], width=[0,1])),
                hole=0.6, textfont=dict(family="Exo 2, sans-serif"),
            )])
            fig.update_layout(height=260, margin=dict(l=0,r=0,t=10,b=0),
                              paper_bgcolor='white',
                              legend=dict(font=dict(family="Exo 2, sans-serif", size=11)))
            st.plotly_chart(fig, use_container_width=True)

    with tab_add:
        with st.form("add_room_form"):
            fc1, fc2, fc3 = st.columns(3)
            room_no  = fc1.text_input("Room Number", placeholder="A-101")
            block    = fc2.text_input("Block",        placeholder="A")
            floor    = fc3.number_input("Floor", 0, 20, 1)
            fc4, fc5, fc6 = st.columns(3)
            room_type = fc4.selectbox("Room Type", ["Single","Double","Triple","Quad"])
            capacity  = fc5.number_input("Capacity", 1, 10, 2)
            fee       = fc6.number_input("Monthly Fee (PKR)", 0, 100000, 5000, step=500)
            amenities = st.text_input("Amenities", placeholder="AC, WiFi, Attached Bath")
            r_status  = st.selectbox("Status", ["Available","Maintenance","Reserved"])
            if st.form_submit_button("Add Room", type="primary", use_container_width=True):
                if not room_no or not block:
                    err("Room number and block are required.")
                else:
                    res, msg = add_room({"room_number":room_no,"floor":floor,"block":block,"room_type":room_type,"capacity":capacity,"monthly_fee":fee,"amenities":amenities,"status":r_status})
                    ok(msg) if res else err(msg)

    with tab_edit:
        all_rooms = get_all_rooms()
        if not all_rooms:
            inf("No rooms in system.")
            return
        opts = {f"Room {r['room_number']} (Block {r['block']})": r['room_id'] for r in all_rooms}
        sel = st.selectbox("Select Room", list(opts.keys()))
        rid = opts[sel]
        room = get_room_by_id(rid)
        if not room: return
        occupants = get_room_occupants(rid)
        if occupants:
            st.markdown(f'<p style="font-family:\'Rajdhani\',sans-serif;font-size:0.8rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;color:#2d5a3d;">Current Occupants ({len(occupants)})</p>', unsafe_allow_html=True)
            st.dataframe(pd.DataFrame(occupants)[['reg_number','full_name','department','phone','alloc_date']], use_container_width=True, hide_index=True)
        with st.form("edit_room_form"):
            ec1,ec2,ec3 = st.columns(3)
            e_rno  = ec1.text_input("Room Number", room.get("room_number",""))
            e_blk  = ec2.text_input("Block",       room.get("block",""))
            e_flr  = ec3.number_input("Floor", 0, 20, int(room.get("floor") or 1))
            ed1,ed2,ed3 = st.columns(3)
            types  = ["Single","Double","Triple","Quad"]
            e_type = ed1.selectbox("Room Type", types, index=types.index(room.get("room_type","Double")))
            e_cap  = ed2.number_input("Capacity", 1, 10, int(room.get("capacity") or 2))
            e_fee  = ed3.number_input("Fee (PKR)", 0, 100000, int(room.get("monthly_fee") or 5000), step=500)
            e_amen = st.text_input("Amenities", room.get("amenities","") or "")
            statuses = ["Available","Full","Maintenance","Reserved"]
            e_stat = st.selectbox("Status", statuses, index=statuses.index(room.get("status","Available")))
            if st.form_submit_button("Update Room", type="primary"):
                res, msg = update_room(rid, {"room_number":e_rno,"floor":e_flr,"block":e_blk,"room_type":e_type,"capacity":e_cap,"monthly_fee":e_fee,"amenities":e_amen,"status":e_stat})
                ok(msg) if res else err(msg)
        with st.expander("Delete Room"):
            st.warning("Only delete empty rooms with no active allocations.")
            if st.button("Delete Room", type="secondary"):
                res, msg = delete_room(rid)
                ok(msg) if res else err(msg)
                if res: st.rerun()


# ════════════════════════════════════════════════════════════
#  ALLOCATIONS
# ════════════════════════════════════════════════════════════
def page_allocations():
    section("Room Allocations")
    tab_active, tab_all, tab_alloc, tab_vacate = st.tabs(["Active","All History","Allocate Room","Vacate Room"])

    with tab_active:
        data = get_active_allocations()
        st.markdown(f'<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.75rem;color:#6b8f76;">{len(data)} ACTIVE ALLOCATIONS</p>', unsafe_allow_html=True)
        if data:
            df = pd.DataFrame(data)
            cols = [c for c in ['allocation_id','reg_number','full_name','department','room_number','block','room_type','monthly_fee','alloc_date'] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)
        else: inf("No active allocations.")

    with tab_all:
        data = get_all_allocations()
        if data:
            df = pd.DataFrame(data)
            cols = [c for c in ['allocation_id','reg_number','full_name','room_number','block','alloc_date','vacate_date','status'] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)
        else: inf("No allocation records.")

    with tab_alloc:
        students = get_unallocated_students()
        rooms    = get_available_rooms()
        if not students: inf("All active students are already allocated, or no students exist."); return
        if not rooms:    inf("No available rooms."); return
        s_opts = {f"{s['reg_number']} — {s['full_name']}": s['student_id'] for s in students}
        r_opts = {f"Room {r['room_number']} (Block {r['block']}, {r['room_type']}) — PKR {r['monthly_fee']}/mo — {r['available_beds']} bed(s) free": r['room_id'] for r in rooms}
        with st.form("alloc_form"):
            sel_s   = st.selectbox("Select Student", list(s_opts.keys()))
            sel_r   = st.selectbox("Select Room",    list(r_opts.keys()))
            a_date  = st.date_input("Allocation Date", value=date.today())
            a_notes = st.text_area("Notes")
            if st.form_submit_button("Allocate Room", type="primary", use_container_width=True):
                res, msg = allocate_room(s_opts[sel_s], r_opts[sel_r], str(a_date), a_notes)
                ok(msg) if res else err(msg)
                if res: st.rerun()

    with tab_vacate:
        active_allocs = get_active_allocations()
        if not active_allocs: inf("No active allocations to vacate."); return
        opts = {f"{a['reg_number']} — {a['full_name']} | Room {a['room_number']}": a['allocation_id'] for a in active_allocs}
        choice = st.selectbox("Select Allocation", list(opts.keys()))
        with st.form("vacate_form"):
            v_date = st.date_input("Vacate Date", value=date.today())
            if st.form_submit_button("Vacate Room", type="secondary", use_container_width=True):
                res, msg = vacate_room(opts[choice], str(v_date))
                ok(msg) if res else err(msg)
                if res: st.rerun()


# ════════════════════════════════════════════════════════════
#  FEES
# ════════════════════════════════════════════════════════════
def page_fees():
    section("Fee Management")
    tab_list, tab_add, tab_pay = st.tabs(["Fee Records","Add Fee","Mark as Paid"])

    with tab_list:
        sf = st.selectbox("Filter by Status", ["All","Pending","Paid","Overdue","Waived"])
        fees = get_all_fees(sf)
        st.markdown(f'<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.75rem;color:#6b8f76;">{len(fees)} RECORDS</p>', unsafe_allow_html=True)
        if fees:
            df = pd.DataFrame(fees)
            cols = [c for c in ['fee_id','reg_number','full_name','room_number','fee_type','month_year','amount','due_date','paid_date','status','payment_method'] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)
        stats = get_fee_stats()
        if stats:
            fc1,fc2,fc3,fc4 = st.columns(4)
            fc1.metric("Total Amount", f"PKR {float(stats.get('total_amount') or 0):,.0f}")
            fc2.metric("Collected",    f"PKR {float(stats.get('collected') or 0):,.0f}")
            fc3.metric("Pending",      f"PKR {float(stats.get('pending') or 0):,.0f}")
            fc4.metric("Overdue",      f"PKR {float(stats.get('overdue') or 0):,.0f}")

    with tab_add:
        students = get_all_students("Active")
        rooms    = get_all_rooms()
        if not students: inf("No active students."); return
        s_opts = {f"{s['reg_number']} — {s['full_name']}": s['student_id'] for s in students}
        r_opts = {f"Room {r['room_number']} (Block {r['block']})": r['room_id'] for r in rooms}
        r_opts["None"] = None
        with st.form("add_fee_form"):
            fc1,fc2 = st.columns(2)
            sel_s = fc1.selectbox("Student", list(s_opts.keys()))
            sel_r = fc2.selectbox("Room (optional)", list(r_opts.keys()))
            fa1,fa2,fa3 = st.columns(3)
            f_type  = fa1.selectbox("Fee Type", ["Monthly","Security","Admission","Fine","Other"])
            f_month = fa2.text_input("Month/Year", placeholder="Jun-2025")
            f_amt   = fa3.number_input("Amount (PKR)", 0, 500000, 5000, step=500)
            fb1,fb2 = st.columns(2)
            f_due   = fb1.date_input("Due Date", value=date.today())
            f_stat  = fb2.selectbox("Status", ["Pending","Paid","Overdue"])
            f_rem   = st.text_area("Remarks")
            if st.form_submit_button("Add Fee Record", type="primary", use_container_width=True):
                res, msg = add_fee({"student_id":s_opts[sel_s],"room_id":r_opts[sel_r],"amount":f_amt,"fee_type":f_type,"month_year":f_month,"due_date":str(f_due),"status":f_stat,"remarks":f_rem})
                ok(msg) if res else err(msg)

    with tab_pay:
        pending = get_all_fees("Pending")
        if not pending: inf("No pending fees."); return
        opts = {f"#{f['fee_id']} | {f['reg_number']} — {f['full_name']} | PKR {f['amount']} ({f.get('month_year','')})": f['fee_id'] for f in pending}
        choice = st.selectbox("Select Fee Record", list(opts.keys()))
        with st.form("pay_fee_form"):
            pc1,pc2,pc3 = st.columns(3)
            p_date   = pc1.date_input("Payment Date", value=date.today())
            p_method = pc2.selectbox("Method", ["Cash","Bank Transfer","Online","Cheque"])
            p_rec    = pc3.text_input("Receipt No.")
            if st.form_submit_button("Mark as Paid", type="primary", use_container_width=True):
                res, msg = mark_fee_paid(opts[choice], str(p_date), p_method, p_rec)
                ok(msg) if res else err(msg)
                if res: st.rerun()


# ════════════════════════════════════════════════════════════
#  COMPLAINTS
# ════════════════════════════════════════════════════════════
def page_complaints():
    section("Complaints Management")
    tab_list, tab_add, tab_update = st.tabs(["All Complaints","New Complaint","Update Status"])

    with tab_list:
        sf = st.selectbox("Filter", ["All","Open","In Progress","Resolved","Closed"])
        complaints = get_all_complaints(sf)
        st.markdown(f'<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.75rem;color:#6b8f76;">{len(complaints)} RECORDS</p>', unsafe_allow_html=True)
        if complaints:
            df = pd.DataFrame(complaints)
            cols = [c for c in ['complaint_id','reg_number','full_name','room_number','category','priority','description','status','assigned_to','created_at'] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)
        stats = get_complaint_stats()
        if stats:
            cs1,cs2,cs3,cs4 = st.columns(4)
            cs1.metric("Open",        stats.get("open_complaints",0))
            cs2.metric("In Progress", stats.get("in_progress",0))
            cs3.metric("Resolved",    stats.get("resolved",0))
            cs4.metric("Urgent",      stats.get("urgent",0))

    with tab_add:
        students = get_all_students("Active")
        if not students: inf("No active students."); return
        s_opts = {f"{s['reg_number']} — {s['full_name']}": s['student_id'] for s in students}
        rooms  = get_all_rooms()
        r_opts = {f"Room {r['room_number']} (Block {r['block']})": r['room_id'] for r in rooms}
        r_opts["No specific room"] = None
        with st.form("add_complaint_form"):
            ca1,ca2 = st.columns(2)
            sel_s = ca1.selectbox("Student", list(s_opts.keys()))
            sel_r = ca2.selectbox("Room (optional)", list(r_opts.keys()))
            cb1,cb2 = st.columns(2)
            cat  = cb1.selectbox("Category", ["Maintenance","Electricity","Plumbing","Cleanliness","Security","Other"])
            pri  = cb2.selectbox("Priority", ["Low","Medium","High","Urgent"])
            desc = st.text_area("Description", placeholder="Describe the issue in detail...")
            if st.form_submit_button("Submit Complaint", type="primary", use_container_width=True):
                if not desc.strip(): err("Please provide a description.")
                else:
                    res, msg = add_complaint({"student_id":s_opts[sel_s],"room_id":r_opts[sel_r],"category":cat,"description":desc,"priority":pri})
                    ok(msg) if res else err(msg)

    with tab_update:
        all_c = get_all_complaints("Open") + get_all_complaints("In Progress")
        if not all_c: inf("No open complaints to update."); return
        opts = {f"#{c['complaint_id']} | {c['full_name']} | {c['category']} | {c['priority']}": c['complaint_id'] for c in all_c}
        choice = st.selectbox("Select Complaint", list(opts.keys()))
        with st.form("update_complaint_form"):
            uc1,uc2 = st.columns(2)
            new_status = uc1.selectbox("New Status", ["Open","In Progress","Resolved","Closed"])
            assigned   = uc2.text_input("Assigned To")
            resolution = st.text_area("Resolution Notes")
            if st.form_submit_button("Update Complaint", type="primary", use_container_width=True):
                res, msg = update_complaint_status(opts[choice], new_status, assigned, resolution)
                ok(msg) if res else err(msg)
                if res: st.rerun()


# ════════════════════════════════════════════════════════════
#  VISITORS
# ════════════════════════════════════════════════════════════
def page_visitors():
    section("Visitor Management")
    tab_list, tab_add, tab_checkout = st.tabs(["Visitor Log","Check In","Check Out"])

    with tab_list:
        visitors = get_all_visitors()
        st.markdown(f'<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.75rem;color:#6b8f76;">{len(visitors)} VISITOR RECORDS</p>', unsafe_allow_html=True)
        if visitors:
            df = pd.DataFrame(visitors)
            cols = [c for c in ['visitor_id','student_name','reg_number','visitor_name','relation','phone','purpose','check_in','check_out'] if c in df.columns]
            st.dataframe(df[cols], use_container_width=True, hide_index=True)
        else: inf("No visitor records.")

    with tab_add:
        students = get_all_students("Active")
        if not students: inf("No active students."); return
        s_opts = {f"{s['reg_number']} — {s['full_name']}": s['student_id'] for s in students}
        with st.form("add_visitor_form"):
            va1,va2 = st.columns(2)
            sel_s    = va1.selectbox("Student Being Visited", list(s_opts.keys()))
            vname    = va2.text_input("Visitor Name")
            vb1,vb2,vb3 = st.columns(3)
            relation = vb1.text_input("Relation", placeholder="Parent / Sibling / Friend")
            vphone   = vb2.text_input("Phone")
            vcnic    = vb3.text_input("CNIC")
            purpose  = st.text_area("Purpose of Visit")
            checkin  = st.text_input("Check-in Time", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if st.form_submit_button("Check In Visitor", type="primary", use_container_width=True):
                if not vname: err("Visitor name is required.")
                else:
                    res, msg = add_visitor({"student_id":s_opts[sel_s],"visitor_name":vname,"relation":relation,"phone":vphone,"cnic":vcnic,"purpose":purpose,"check_in":checkin})
                    ok(msg) if res else err(msg)

    with tab_checkout:
        visitors = get_all_visitors()
        active_v = [v for v in visitors if not v.get("check_out")]
        if not active_v: inf("No visitors currently inside."); return
        opts = {f"#{v['visitor_id']} | {v['visitor_name']} visiting {v['student_name']} | In: {v['check_in']}": v['visitor_id'] for v in active_v}
        choice = st.selectbox("Select Visitor", list(opts.keys()))
        checkout_time = st.text_input("Check-out Time", value=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if st.button("Check Out", type="primary"):
            res, msg = checkout_visitor(opts[choice], checkout_time)
            ok(msg) if res else err(msg)
            if res: st.rerun()


# ════════════════════════════════════════════════════════════
#  NOTICES
# ════════════════════════════════════════════════════════════
def page_notices():
    section("Notice Board")
    tab_board, tab_add, tab_manage = st.tabs(["Notice Board","Post Notice","Manage"])

    with tab_board:
        notices = get_active_notices()
        if notices:
            for n in notices:
                p   = n.get("priority","Normal")
                cls = "urgent" if p=="Urgent" else ("high" if p=="High" else "")
                st.markdown(f"""
                <div class="notice-card {cls}">
                    <div class="nc-title">
                        {n['title']}
                        {badge(n['category'],'info')}
                        {badge(p, 'danger' if p=='Urgent' else 'warning' if p=='High' else 'neutral')}
                    </div>
                    <div class="nc-body">{n['content']}</div>
                    <div class="nc-meta">POSTED BY {n['posted_by'].upper()} &nbsp;/&nbsp; {str(n['created_at'])[:10]}</div>
                </div>""", unsafe_allow_html=True)
        else:
            inf("No active notices.")

    with tab_add:
        with st.form("add_notice_form"):
            n_title = st.text_input("Notice Title")
            nc1,nc2,nc3 = st.columns(3)
            n_cat   = nc1.selectbox("Category", ["General","Fee","Maintenance","Security","Event","Emergency"])
            n_pri   = nc2.selectbox("Priority",  ["Low","Normal","High","Urgent"])
            n_by    = nc3.text_input("Posted By", value="Admin")
            n_valid = st.date_input("Valid Until", value=date.today())
            n_content = st.text_area("Content", height=150)
            if st.form_submit_button("Post Notice", type="primary", use_container_width=True):
                if not n_title or not n_content: err("Title and content are required.")
                else:
                    res, msg = add_notice({"title":n_title,"content":n_content,"category":n_cat,"priority":n_pri,"posted_by":n_by,"valid_until":str(n_valid)})
                    ok(msg) if res else err(msg)

    with tab_manage:
        all_notices = get_all_notices()
        if not all_notices: inf("No notices."); return
        df = pd.DataFrame(all_notices)
        cols = [c for c in ['notice_id','title','category','priority','posted_by','status','created_at'] if c in df.columns]
        st.dataframe(df[cols], use_container_width=True, hide_index=True)
        opts = {f"#{n['notice_id']} | {n['title']}": n['notice_id'] for n in all_notices}
        choice = st.selectbox("Select Notice to Delete", list(opts.keys()))
        if st.button("Delete Notice", type="secondary"):
            res, msg = delete_notice(opts[choice])
            ok(msg) if res else err(msg)
            if res: st.rerun()


# ════════════════════════════════════════════════════════════
#  MAIN ROUTER
# ════════════════════════════════════════════════════════════
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    page = sidebar()

    dispatch = {
        "Dashboard":   page_dashboard,
        "Students":    page_students,
        "Rooms":       page_rooms,
        "Allocations": page_allocations,
        "Fees":        page_fees,
        "Complaints":  page_complaints,
        "Visitors":    page_visitors,
        "Notices":     page_notices,
    }
    dispatch.get(page, page_dashboard)()

    st.divider()
    st.markdown(
        f'<p style="font-family:\'Share Tech Mono\',monospace;font-size:0.68rem;'
        f'color:#6b8f76;text-align:center;letter-spacing:0.08em;">'
        f'HPS &nbsp;/&nbsp; {APP_CONFIG["university"].upper()} &nbsp;/&nbsp; '
        f'v{APP_CONFIG["version"]}</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()

    