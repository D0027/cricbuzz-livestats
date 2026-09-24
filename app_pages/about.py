from __future__ import annotations

import streamlit as st

from utils.ui import page_header

page_header("About", "Project background and contact.", breadcrumb="Info / About")

st.markdown(
    """
### Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A production-style sports analytics platform combining live cricket data (Cricbuzz API),
a normalized relational database, 25 hand-crafted SQL analytics questions, and full CRUD
management — all wrapped in a Streamlit dashboard.

**Highlights**
- Live/upcoming/completed match tracking with scorecards
- Player statistics across Test / ODI / T20I with search, filters, and export
- 25 SQL analytics questions spanning beginner → advanced difficulty
- Full CRUD for players, teams, matches, series, and venues
- Works fully offline out of the box via seeded sample data; live data activates once an API key is added

**Built by:** Amisha ([GitHub: D0027](https://github.com/D0027))

**Contact / Feedback:** open an issue on the project's GitHub repository.
    """
)
