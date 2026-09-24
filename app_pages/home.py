from __future__ import annotations

import streamlit as st
from sqlalchemy import select, func

from database.connection import get_session
from database.models import Player, Team, Match, Series
from api.cricbuzz_client import get_client
from utils.ui import page_header, kpi_card, empty_state
from utils.config import settings

page_header(
    "Welcome to Cricbuzz LiveStats",
    "Real-Time Cricket Insights & SQL-Based Analytics · your command center for live scores, "
    "player statistics, and deep SQL analytics.",
    breadcrumb="Home",
)

# ---- KPI row ----
with get_session() as s:
    n_players = s.execute(select(func.count(Player.player_id))).scalar_one()
    n_teams = s.execute(select(func.count(Team.team_id))).scalar_one()
    n_matches = s.execute(select(func.count(Match.match_id))).scalar_one()
    n_series = s.execute(select(func.count(Series.series_id))).scalar_one()

c1, c2, c3, c4 = st.columns(4)
c1.markdown(kpi_card("Players Tracked", f"{n_players}"), unsafe_allow_html=True)
c2.markdown(kpi_card("Teams", f"{n_teams}"), unsafe_allow_html=True)
c3.markdown(kpi_card("Matches in DB", f"{n_matches}"), unsafe_allow_html=True)
c4.markdown(kpi_card("Series Tracked", f"{n_series}"), unsafe_allow_html=True)

st.write("")

# ---- Status row: API + DB health ----
st.subheader("System Status")
client = get_client()
s1, s2 = st.columns(2)
with s1:
    if client.is_configured():
        st.success("✅ Cricbuzz API: configured and ready for live data.")
    else:
        st.warning(
            "⚠️ Cricbuzz API key not set — Live Matches page will show setup instructions. "
            "All analytics/CRUD pages work fully offline using the seeded SQL database."
        )
with s2:
    st.success(f"✅ Database: connected ({settings.db_type}), schema ready and seeded.")

st.divider()

# ---- Feature / navigation cards ----
st.subheader("Explore the Platform")
cards = [
    ("🏏", "Live Matches", "Live scores, scorecards, commentary, and match timelines pulled from the Cricbuzz API.", "Live Cricket"),
    ("📊", "Player Statistics", "Top batsmen, bowlers, all-rounders — with filters, search, charts, and CSV export.", "Analytics"),
    ("🧮", "SQL Analytics", "All 25 analytics questions, from beginner joins to advanced window-style aggregates.", "Analytics"),
    ("⚖️", "Comparisons", "Head-to-head player and team comparisons with visual breakdowns.", "Analytics"),
    ("🗄️", "CRUD Operations", "Full create/read/update/delete across players, teams, matches, series, and venues.", "Data Management"),
    ("⚙️", "Settings", "Configure API keys, database connection, and app preferences.", "Info"),
]
cols = st.columns(3)
for i, (icon, title, desc, _section) in enumerate(cards):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="glass-card" style="min-height:150px; margin-bottom:1rem;">
                <div style="font-size:1.6rem;">{icon}</div>
                <div style="font-weight:700; margin:0.3rem 0;">{title}</div>
                <div style="color:rgba(255,255,255,0.6); font-size:0.88rem;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.divider()

# ---- Architecture overview ----
with st.expander("📐 Architecture & Tech Stack Overview"):
    st.markdown(
        """
**Layers**
- **API layer** (`api/`) — retry logic, caching, timeouts, structured errors around the Cricbuzz REST API.
- **Database layer** (`database/`) — SQLAlchemy ORM models, connection/session management, seed data.
- **Analytics layer** (`analytics/`) — the 25 SQL analytics queries with metadata for the UI.
- **CRUD layer** (`crud/`) — reusable create/read/update/delete operations shared by the CRUD page.
- **Presentation layer** (`pages/`) — one Streamlit page per feature, styled via `utils/ui.py`.

**Stack:** Python · Streamlit · SQLAlchemy · SQLite (default) / MySQL / PostgreSQL · Requests · Pandas ·
NumPy · Plotly · Pydantic · python-dotenv · rotating-file logging.
        """
    )

with st.expander("👩‍💻 Developer Information"):
    st.markdown(
        """
- **Project:** Cricbuzz LiveStats — Real-Time Cricket Insights & SQL-Based Analytics
- **GitHub:** [D0027](https://github.com/D0027)
- **Docs:** see `docs/README.md` in the project root for full setup & deployment instructions.
        """
    )
