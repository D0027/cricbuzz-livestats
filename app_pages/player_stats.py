from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import select

from database.connection import get_session
from database.models import Player, PlayerStats, Team
from utils.ui import page_header, empty_state
from utils.exporters import to_csv_bytes

page_header(
    "Player Statistics",
    "Batting, bowling, and fielding stats with filters, search, and interactive charts.",
    breadcrumb="Analytics / Player Statistics",
)


@st.cache_data(ttl=120, show_spinner=False)
def load_stats() -> pd.DataFrame:
    with get_session() as session:
        rows = session.execute(
            select(
                Player.full_name, Player.country, Player.playing_role, Player.batting_style,
                PlayerStats.format, PlayerStats.matches, PlayerStats.runs, PlayerStats.batting_average,
                PlayerStats.strike_rate, PlayerStats.centuries, PlayerStats.half_centuries,
                PlayerStats.wickets, PlayerStats.bowling_average, PlayerStats.economy_rate,
                PlayerStats.best_bowling, PlayerStats.catches, PlayerStats.stumpings,
            ).join(PlayerStats, PlayerStats.player_id == Player.player_id)
        ).all()
    cols = [
        "Player", "Country", "Role", "Batting Style", "Format", "Matches", "Runs", "Batting Avg",
        "Strike Rate", "100s", "50s", "Wickets", "Bowling Avg", "Economy", "Best Bowling",
        "Catches", "Stumpings",
    ]
    return pd.DataFrame(rows, columns=cols)


df = load_stats()

# ---- Filters ----
f1, f2, f3, f4 = st.columns(4)
with f1:
    countries = sorted(df["Country"].unique())
    country_filter = st.multiselect("Country", countries)
with f2:
    roles = sorted(df["Role"].unique())
    role_filter = st.multiselect("Role", roles)
with f3:
    formats = sorted(df["Format"].unique())
    format_filter = st.multiselect("Format", formats, default=[])
with f4:
    search = st.text_input("🔍 Search player name")

filtered = df.copy()
if country_filter:
    filtered = filtered[filtered["Country"].isin(country_filter)]
if role_filter:
    filtered = filtered[filtered["Role"].isin(role_filter)]
if format_filter:
    filtered = filtered[filtered["Format"].isin(format_filter)]
if search:
    filtered = filtered[filtered["Player"].str.contains(search, case=False, na=False)]

tab_bat, tab_bowl, tab_all, tab_wk = st.tabs(
    ["🏏 Top Batsmen", "🎯 Top Bowlers", "🌟 All-rounders", "🧤 Wicket-keepers"]
)

with tab_bat:
    bat_df = filtered.sort_values("Runs", ascending=False).head(15)
    if bat_df.empty:
        empty_state("No batsmen match the current filters.")
    else:
        fig = px.bar(
            bat_df, x="Player", y="Runs", color="Batting Avg", color_continuous_scale="Purples",
            title="Top run scorers"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(
            bat_df[["Player", "Country", "Format", "Matches", "Runs", "Batting Avg", "Strike Rate", "100s", "50s"]],
            use_container_width=True, hide_index=True,
        )

with tab_bowl:
    bowl_df = filtered[filtered["Wickets"] > 0].sort_values("Wickets", ascending=False).head(15)
    if bowl_df.empty:
        empty_state("No bowlers match the current filters.")
    else:
        fig = px.bar(
            bowl_df, x="Player", y="Wickets", color="Economy", color_continuous_scale="Teal",
            title="Top wicket takers"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(
            bowl_df[["Player", "Country", "Format", "Matches", "Wickets", "Bowling Avg", "Economy", "Best Bowling"]],
            use_container_width=True, hide_index=True,
        )

with tab_all:
    ar_df = filtered[(filtered["Role"] == "All-rounder") & (filtered["Runs"] > 0) & (filtered["Wickets"] > 0)]
    if ar_df.empty:
        empty_state("No all-rounders match the current filters.")
    else:
        fig = px.scatter(
            ar_df, x="Runs", y="Wickets", size="Matches", color="Country", hover_name="Player",
            title="All-rounder impact: runs vs wickets"
        )
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(ar_df, use_container_width=True, hide_index=True)

with tab_wk:
    wk_df = filtered[filtered["Role"] == "WK-Batsman"].sort_values("Stumpings", ascending=False)
    if wk_df.empty:
        empty_state("No wicket-keepers match the current filters.")
    else:
        fig = px.bar(wk_df.head(10), x="Player", y="Stumpings", color="Catches", title="Wicket-keeper dismissals")
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(wk_df[["Player", "Country", "Format", "Catches", "Stumpings", "Runs"]], use_container_width=True, hide_index=True)

st.divider()
st.download_button(
    "⬇️ Export filtered data as CSV", data=to_csv_bytes(filtered), file_name="player_stats.csv", mime="text/csv"
)
