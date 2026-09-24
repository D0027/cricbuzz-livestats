from __future__ import annotations

import streamlit as st

from utils.config import settings, BASE_DIR
from utils.ui import page_header

page_header("Settings", "Configuration reference for this deployment.", breadcrumb="Info / Settings")

st.subheader("🔑 API Configuration")
st.write(f"**Configured:** {'✅ Yes' if settings.api_configured else '❌ No'}")
st.write(f"**Base URL:** `{settings.cricbuzz_base_url}`")
st.info(
    "To enable live data, create a `.env` file (copy from `.env.example`) in the project root "
    "and set `CRICBUZZ_API_KEY` to a RapidAPI key for the Cricbuzz Cricket API. Restart the app after editing."
)

st.subheader("🗄️ Database Configuration")
st.write(f"**Type:** `{settings.db_type}`")
if settings.db_type == "sqlite":
    st.write(f"**File:** `{BASE_DIR / settings.db_path}`")
else:
    st.write(f"**Host:** `{settings.db_host}:{settings.db_port}` · **Database:** `{settings.db_name}`")
st.caption("Change DB_TYPE in `.env` to `mysql` or `postgresql` to point at a different database engine.")

st.subheader("📜 Logging")
st.write(f"**Level:** `{settings.log_level}` · **Log file:** `logs/app.log` (rotating, 5 backups)")

st.subheader("⚡ Performance")
st.write(f"**Cache TTL:** {settings.cache_ttl_seconds}s · **Request timeout:** {settings.request_timeout}s "
         f"· **Max retries:** {settings.request_max_retries}")

st.divider()
if st.button("🧹 Clear app cache"):
    st.cache_data.clear()
    st.success("Cache cleared.")
