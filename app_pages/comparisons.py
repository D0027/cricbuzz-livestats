from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from sqlalchemy import select

from database.connection import get_session
from database.models import Player, PlayerStats, Team, Match
from utils.ui import page_header, empty_state

page_header(
    "Player & Team Comparison",
    "Compare two players head-to-head, or two teams' overall records.",
    breadcrumb="Analytics / Comparisons",
)


@st.cache_data(ttl=120, show_spinner=False)
def load_player_stats() -> pd.DataFrame:
    with get_session() as session:
        rows = session.execute(
            select(
                Player.full_name, PlayerStats.format, PlayerStats.matches, PlayerStats.runs,
                PlayerStats.batting_average, PlayerStats.strike_rate, PlayerStats.wickets,
                PlayerStats.bowling_average, PlayerStats.economy_rate, PlayerStats.catches,
            ).join(PlayerStats, PlayerStats.player_id == Player.player_id)
        ).all()
    return pd.DataFrame(
        rows,
        columns=["Player", "Format", "Matches", "Runs", "Batting Avg", "Strike Rate",
                 "Wickets", "Bowling Avg", "Economy", "Catches"],
    )


tab_players, tab_teams = st.tabs(["🧑‍🤝‍🧑 Player Comparison", "🏳️ Team Comparison"])

with tab_players:
    df = load_player_stats()
    fmt = st.selectbox("Format", sorted(df["Format"].unique()))
    fdf = df[df["Format"] == fmt]
    names = sorted(fdf["Player"].unique())

    c1, c2 = st.columns(2)
    p1 = c1.selectbox("Player A", names, index=0 if names else None, key="p1")
    p2 = c2.selectbox("Player B", names, index=1 if len(names) > 1 else 0, key="p2")

    if p1 and p2 and p1 != p2:
        row1 = fdf[fdf["Player"] == p1].iloc[0]
        row2 = fdf[fdf["Player"] == p2].iloc[0]

        metrics = ["Runs", "Batting Avg", "Strike Rate", "Wickets", "Catches"]
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(r=[row1[m] for m in metrics], theta=metrics, fill="toself", name=p1))
        fig.add_trace(go.Scatterpolar(r=[row2[m] for m in metrics], theta=metrics, fill="toself", name=p2))
        fig.update_layout(polar=dict(radialaxis=dict(visible=True)), title=f"{p1} vs {p2} ({fmt})")
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            pd.DataFrame([row1, row2]).set_index("Player"), use_container_width=True
        )
    elif p1 == p2:
        st.info("Pick two different players to compare.")

with tab_teams:
    with get_session() as session:
        teams = session.execute(select(Team)).scalars().all()
    team_names = sorted(t.team_name for t in teams)
    c1, c2 = st.columns(2)
    t1_name = c1.selectbox("Team A", team_names, key="t1")
    t2_name = c2.selectbox("Team B", team_names, index=1 if len(team_names) > 1 else 0, key="t2")

    if t1_name and t2_name and t1_name != t2_name:
        with get_session() as session:
            t1_id = session.execute(select(Team.team_id).where(Team.team_name == t1_name)).scalar_one()
            t2_id = session.execute(select(Team.team_id).where(Team.team_name == t2_name)).scalar_one()

            t1_wins = session.execute(
                select(Match).where(Match.winner_id == t1_id)
            ).scalars().all()
            t2_wins = session.execute(
                select(Match).where(Match.winner_id == t2_id)
            ).scalars().all()
            h2h = session.execute(
                select(Match).where(
                    ((Match.team1_id == t1_id) & (Match.team2_id == t2_id))
                    | ((Match.team1_id == t2_id) & (Match.team2_id == t1_id))
                )
            ).scalars().all()

        m1, m2, m3 = st.columns(3)
        m1.metric(f"{t1_name} — Total Wins", len(t1_wins))
        m2.metric(f"{t2_name} — Total Wins", len(t2_wins))
        m3.metric("Head-to-Head Matches", len(h2h))

        h2h_t1_wins = sum(1 for m in h2h if m.winner_id == t1_id)
        h2h_t2_wins = sum(1 for m in h2h if m.winner_id == t2_id)
        fig = go.Figure(data=[
            go.Bar(name=t1_name, x=["Head-to-Head Wins"], y=[h2h_t1_wins]),
            go.Bar(name=t2_name, x=["Head-to-Head Wins"], y=[h2h_t2_wins]),
        ])
        fig.update_layout(barmode="group", title=f"{t1_name} vs {t2_name} — Head-to-Head")
        st.plotly_chart(fig, use_container_width=True)
    elif t1_name == t2_name:
        st.info("Pick two different teams to compare.")
