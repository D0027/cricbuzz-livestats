"""
Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics
Entry point: `streamlit run main.py`
"""
from __future__ import annotations

import streamlit as st

from database.connection import init_db
from database.seed_data import seed
from utils.ui import inject_global_css, footer
from utils.logger import get_logger

logger = get_logger("main")

st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_global_css()

# Ensure DB exists + seeded on first run
init_db()
try:
    seed()
except Exception:
    logger.exception("Seeding skipped/failed (likely already seeded).")

# ---- Sidebar branding + nav ----
with st.sidebar:
    st.markdown(
        """
        <style>
        .sidebar-brand {
            display:flex; align-items:center; gap:0.7rem;
            padding: 0.4rem 0 1rem 0;
        }
        .sidebar-brand .logo-badge {
            width:42px; height:42px; border-radius:11px;
            background: linear-gradient(135deg, #E1261C, #B01810);
            display:flex; align-items:center; justify-content:center;
            font-size:1.4rem; box-shadow: 0 4px 14px rgba(225,38,28,0.35);
        }
        .sidebar-brand .brand-title {
            font-weight:800; font-size:1.15rem; line-height:1.1; margin:0;
        }
        .sidebar-brand .brand-sub {
            color: rgba(255,255,255,0.45); font-size:0.72rem;
            text-transform:uppercase; letter-spacing:0.06em; font-weight:600;
        }
        .sidebar-tagline {
            color: rgba(255,255,255,0.55); font-size: 0.82rem;
            padding: 0.5rem 0.75rem; margin-bottom: 0.9rem;
            background: rgba(255,255,255,0.035);
            border: 1px solid rgba(255,255,255,0.07);
            border-left: 3px solid #00D2A0;
            border-radius: 8px;
        }
        </style>
        <div class="sidebar-brand">
            <div class="logo-badge">🏏</div>
            <div>
                <p class="brand-title">Cricbuzz LiveStats</p>
                <div class="brand-sub">Analytics Platform</div>
            </div>
        </div>
        <div class="sidebar-tagline">
            📡 Real-Time Cricket Insights &amp; SQL-Based Analytics — live scores, deep stats, and a full 25-query analytics engine in one place.
        </div>
        """,
        unsafe_allow_html=True,
    )

pages = {
    "Overview": [
        st.Page("app_pages/home.py", title="Home", icon="🏠", default=True),
    ],
    "Live Cricket": [
        st.Page("app_pages/live_matches.py", title="Live Matches", icon="🏏"),
    ],
    "Analytics": [
        st.Page("app_pages/player_stats.py", title="Player Statistics", icon="📊"),
        st.Page("app_pages/sql_analytics.py", title="SQL Analytics (25 Queries)", icon="🧮"),
        st.Page("app_pages/comparisons.py", title="Player & Team Comparison", icon="⚖️"),
    ],
    "Data Management": [
        st.Page("app_pages/crud.py", title="CRUD Operations", icon="🗄️"),
    ],
    "Info": [
        st.Page("app_pages/settings_page.py", title="Settings", icon="⚙️"),
        st.Page("app_pages/about.py", title="About", icon="ℹ️"),
    ],
}

nav = st.navigation(pages)

with st.sidebar:
    st.divider()
    st.caption("Built with Streamlit · SQLAlchemy · Cricbuzz & CricketData.org APIs")

nav.run()

footer()