from __future__ import annotations

import time as _time

import streamlit as st

from api.cricbuzz_client import get_client, CricbuzzAPIError
from api.cricketdata_client import get_cricketdata_client, CricketDataAPIError
from utils.ui import page_header, status_pill, empty_state, match_status_class
from utils.logger import get_logger

logger = get_logger("live_matches")

page_header(
    "Live Matches",
    "Live scores, upcoming fixtures, and completed matches.",
    breadcrumb="Live Cricket / Matches",
)

client = get_client()
cd_client = get_cricketdata_client()

CACHE_KEY = "live_matches_last_result"
CACHE_TIME_KEY = "live_matches_last_fetch_time"
# 5 minutes: cricket scores realistically only change every 1-4 min (roughly
# once per over), so a 5-min refresh window still feels "live" to a user
# while stretching a 100/day free quota to cover a full T20 (~3.5 hrs) or
# even a full ODI (~7-8 hrs) of continuous match-day tracking.
CACHE_TTL_SECONDS = 300

top = st.columns([1, 1, 6])
with top[0]:
    refresh = st.button("🔄 Refresh", use_container_width=True)
with top[1]:
    auto_refresh = st.toggle("Auto-refresh (5 min)", value=False)

if refresh:
    st.cache_data.clear()
    st.session_state.pop(CACHE_KEY, None)
    st.session_state.pop(CACHE_TIME_KEY, None)

if auto_refresh:
    st.caption("Auto-refresh is on — this page will re-run every 5 minutes.")
    st.markdown("<meta http-equiv='refresh' content='300'>", unsafe_allow_html=True)


def render_cricketdata_matches(data: dict) -> None:
    """Render CricketData.org's flat `data: [...]` match list."""
    matches = data.get("data", [])
    if not matches:
        empty_state("No matches found right now.")
        return
    for m in matches:
        teams = m.get("teams", [])
        t1 = teams[0] if len(teams) > 0 else "Team 1"
        t2 = teams[1] if len(teams) > 1 else "Team 2"
        status = m.get("status", "Status unavailable")
        venue = m.get("venue", "")
        match_name = m.get("name", f"{t1} vs {t2}")
        match_id = m.get("id")

        score_lines = ""
        for s in m.get("score", []) or []:
            score_lines += (
                f"<div class='team-row'>"
                f"<span class='team-name'>{s.get('inning', '')}</span>"
                f"<span class='team-score'>{s.get('r', '-')}/{s.get('w', '-')} "
                f"<span style='color:rgba(255,255,255,0.5); font-size:0.8rem;'>({s.get('o', '-')} ov)</span></span>"
                f"</div>"
            )

        st.markdown(
            f"""
            <div class="match-card {match_status_class(status)}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="team-name">{match_name}</div>
                    {status_pill(status)}
                </div>
                {score_lines}
                <div class="match-meta">📍 {venue}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if match_id:
            with st.expander(f"Scorecard & details — {match_id}"):
                try:
                    card = cd_client.get_match_scorecard(match_id)
                    scorecard = card.get("data", {}).get("scorecard", [])
                    if not scorecard:
                        st.info("No detailed scorecard available for this match yet.")
                        with st.expander("🔧 Raw API response"):
                            st.json(card)
                    else:
                        for inn in scorecard:
                            st.markdown(f"**{inn.get('inning', '')}**")
                            for bat in inn.get("batting", []):
                                st.caption(
                                    f"{bat.get('batsman', {}).get('name', '')}: "
                                    f"{bat.get('r', 0)} ({bat.get('b', 0)})"
                                )
                except CricketDataAPIError as exc:
                    st.warning(f"Couldn't load scorecard: {exc}")


def render_api_matches(payload: dict, show_scorecard: bool) -> None:
    """Render Cricbuzz's typeMatches -> seriesMatches -> matchInfo tree."""
    type_matches = payload.get("typeMatches", [])
    if not type_matches:
        empty_state("No matches found for this category right now.")
        return
    for tm in type_matches:
        st.markdown(f"#### {tm.get('matchType', '')}")
        for series_block in tm.get("seriesMatches", []):
            wrapper = series_block.get("seriesAdWrapper", {})
            series_name = wrapper.get("seriesName", "")
            matches = wrapper.get("matches", [])
            if not matches:
                continue
            if series_name:
                st.markdown(f"**{series_name}**")
            for m in matches:
                info = m.get("matchInfo", {})
                t1 = info.get("team1", {}).get("teamName", "Team 1")
                t2 = info.get("team2", {}).get("teamName", "Team 2")
                status = info.get("status", "Status unavailable")
                venue = info.get("venueInfo", {})
                venue_str = f"{venue.get('ground', '')}, {venue.get('city', '')}"
                match_id = info.get("matchId")

                st.markdown(
                    f"""
                    <div class="match-card {match_status_class(status)}">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div class="team-name">{t1} vs {t2}</div>
                            {status_pill(status)}
                        </div>
                        <div class="match-meta">📍 {venue_str}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if match_id and show_scorecard:
                    with st.expander(f"Scorecard & details — Match {match_id}"):
                        try:
                            card = client.get_match_scorecard(match_id)
                            innings_list = card.get("scorecard") or card.get("scoreCard") or []
                            if not innings_list:
                                st.info("No innings data available yet.")
                            else:
                                for inn in innings_list:
                                    st.json(inn)
                        except CricbuzzAPIError as exc:
                            st.warning(f"Couldn't load scorecard: {exc}")


def load_matches_with_fallback():
    """Try Cricbuzz first; on any failure (quota, rate-limit, network),
    fall back to CricketData.org so the page never crashes or shows a
    dead error screen."""
    if client.is_configured():
        try:
            with st.spinner("Fetching from Cricbuzz..."):
                data = client.get_live_matches()
            return "cricbuzz", data
        except Exception as exc:
            logger.warning("Cricbuzz failed (%s), falling back to CricketData.org", exc)
            st.warning(f"⚠️ Cricbuzz API unavailable right now ({exc}). Falling back to CricketData.org...")

    if cd_client.is_configured():
        try:
            with st.spinner("Fetching from CricketData.org..."):
                data = cd_client.get_current_matches()
            return "cricketdata", data
        except Exception as exc:
            st.error(f"CricketData.org also failed: {exc}")
            return None, None

    st.info(
        "🔑 No API configured. Add `CRICBUZZ_API_KEY` and/or `CRICKETDATA_API_KEY` to `.env`."
    )
    return None, None


def get_matches_cached():
    now = _time.time()
    last_time = st.session_state.get(CACHE_TIME_KEY, 0)
    if now - last_time < CACHE_TTL_SECONDS and CACHE_KEY in st.session_state:
        remaining = int(CACHE_TTL_SECONDS - (now - last_time))
        st.caption(f"📦 Showing cached data — next refresh available in ~{remaining // 60}m {remaining % 60}s "
                   f"(protects your free API quota).")
        return st.session_state[CACHE_KEY]
    result = load_matches_with_fallback()
    st.session_state[CACHE_KEY] = result
    st.session_state[CACHE_TIME_KEY] = now
    return result


with st.tabs(["🔴 Live / Current Matches"])[0]:
    source, data = get_matches_cached()
    if source == "cricbuzz":
        render_api_matches(data, show_scorecard=True)
    elif source == "cricketdata":
        st.caption("📡 Showing data from CricketData.org (fallback source)")
        render_cricketdata_matches(data)