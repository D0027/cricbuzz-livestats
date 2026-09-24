from __future__ import annotations

import streamlit as st

from crud.operations import (
    list_records, get_record, create_record, update_record, delete_record,
    bulk_delete, get_foreign_key_options, MODEL_MAP, PK_MAP,
)
from utils.ui import page_header, empty_state

page_header(
    "CRUD Operations",
    "Create, read, update, and delete players, teams, matches, series, and venues.",
    breadcrumb="Data Management / CRUD",
)

entity = st.selectbox("Select entity", list(MODEL_MAP.keys()))
pk = PK_MAP[entity]

tab_read, tab_create, tab_update, tab_delete = st.tabs(
    ["📋 Browse", "➕ Create", "✏️ Update", "🗑️ Delete"]
)

# ---------------- READ ----------------
with tab_read:
    c1, c2 = st.columns([3, 1])
    with c1:
        search = st.text_input("🔍 Search", key=f"search_{entity}")
    df = list_records(entity)
    search_col = "full_name" if "full_name" in df.columns else (df.columns[1] if len(df.columns) > 1 else None)
    if search and search_col:
        df = df[df[search_col].astype(str).str.contains(search, case=False, na=False)]

    if df.empty:
        empty_state(f"No {entity.lower()} found.")
    else:
        page_size = 15
        total_pages = max((len(df) - 1) // page_size + 1, 1)
        page_num = st.number_input("Page", min_value=1, max_value=total_pages, value=1, key=f"page_{entity}")
        start = (page_num - 1) * page_size
        st.dataframe(df.iloc[start:start + page_size], use_container_width=True, hide_index=True)
        st.caption(f"Page {page_num} of {total_pages} · {len(df)} total records")

        with st.expander("Bulk delete"):
            ids = st.multiselect(f"Select {pk}s to delete", df[pk].tolist())
            if st.button("🗑️ Delete selected", type="primary", disabled=not ids):
                st.session_state["confirm_bulk_delete"] = ids
            if st.session_state.get("confirm_bulk_delete"):
                st.warning(f"Confirm deletion of {len(st.session_state['confirm_bulk_delete'])} record(s)?")
                cc1, cc2 = st.columns(2)
                if cc1.button("✅ Confirm delete"):
                    ok, msg = bulk_delete(entity, st.session_state["confirm_bulk_delete"])
                    st.session_state["confirm_bulk_delete"] = None
                    (st.success if ok else st.error)(msg)
                    st.rerun()
                if cc2.button("❌ Cancel"):
                    st.session_state["confirm_bulk_delete"] = None
                    st.rerun()

# ---------------- CREATE ----------------
with tab_create:
    st.markdown(f"#### Add a new {entity[:-1]}")
    fk = get_foreign_key_options(entity)

    with st.form(f"create_form_{entity}"):
        data = {}
        if entity == "Teams":
            data["team_name"] = st.text_input("Team name *")
            data["country"] = st.text_input("Country *")
            data["team_type"] = st.selectbox("Team type", ["International", "Franchise"])
        elif entity == "Venues":
            data["venue_name"] = st.text_input("Venue name *")
            data["city"] = st.text_input("City")
            data["country"] = st.text_input("Country")
            data["capacity"] = st.number_input("Capacity", min_value=0, value=20000)
        elif entity == "Series":
            data["series_name"] = st.text_input("Series name *")
            data["host_country"] = st.text_input("Host country")
            data["match_type"] = st.selectbox("Match type", ["Test", "ODI", "T20I"])
            data["start_date"] = st.date_input("Start date")
            data["end_date"] = st.date_input("End date")
            data["total_matches"] = st.number_input("Total matches", min_value=1, value=3)
        elif entity == "Players":
            data["full_name"] = st.text_input("Full name *")
            data["playing_role"] = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder", "WK-Batsman"])
            data["batting_style"] = st.selectbox("Batting style", ["Right-hand bat", "Left-hand bat"])
            data["bowling_style"] = st.text_input("Bowling style", value="-")
            data["country"] = st.text_input("Country *")
            data["date_of_birth"] = st.date_input("Date of birth")
            team_label = st.selectbox("Team", list(fk.get("teams", {}).keys()) or ["No teams yet"])
            data["team_id"] = fk.get("teams", {}).get(team_label)
            data["is_active"] = st.checkbox("Active", value=True)
        elif entity == "Matches":
            team_names = list(fk.get("teams", {}).keys())
            t1 = st.selectbox("Team 1", team_names, key="c_t1")
            t2 = st.selectbox("Team 2", team_names, key="c_t2")
            data["team1_id"] = fk["teams"].get(t1)
            data["team2_id"] = fk["teams"].get(t2)
            venue_label = st.selectbox("Venue", list(fk.get("venues", {}).keys()))
            data["venue_id"] = fk.get("venues", {}).get(venue_label)
            series_label = st.selectbox("Series", list(fk.get("series", {}).keys()))
            data["series_id"] = fk.get("series", {}).get(series_label)
            data["match_type"] = st.selectbox("Match type", ["Test", "ODI", "T20I"])
            data["match_date"] = st.date_input("Match date")
            data["toss_decision"] = st.selectbox("Toss decision", ["Bat", "Bowl"])
            data["status"] = st.selectbox("Status", ["Scheduled", "Live", "Completed"])

        submitted = st.form_submit_button("Create", type="primary")
        if submitted:
            required_ok = all(v not in (None, "") for k, v in data.items() if k in (
                "team_name", "full_name", "venue_name", "series_name", "country"
            ))
            if not required_ok:
                st.error("Please fill all required (*) fields.")
            else:
                ok, msg = create_record(entity, data)
                (st.success if ok else st.error)(msg)

# ---------------- UPDATE ----------------
with tab_update:
    df = list_records(entity)
    if df.empty:
        empty_state(f"No {entity.lower()} to update yet.")
    else:
        record_id = st.selectbox(f"Select {entity[:-1]} ({pk})", df[pk].tolist(), key=f"upd_select_{entity}")
        record = get_record(entity, record_id)
        if record:
            with st.form(f"update_form_{entity}"):
                new_data = {}
                for field, value in record.items():
                    if field == pk:
                        continue
                    if isinstance(value, bool):
                        new_data[field] = st.checkbox(field, value=value)
                    elif isinstance(value, (int, float)) and field.endswith("_id"):
                        new_data[field] = st.number_input(field, value=int(value) if value else 0)
                    elif isinstance(value, (int, float)):
                        new_data[field] = st.number_input(field, value=float(value) if value else 0.0)
                    else:
                        new_data[field] = st.text_input(field, value=str(value) if value is not None else "")
                if st.form_submit_button("Update", type="primary"):
                    ok, msg = update_record(entity, record_id, new_data)
                    (st.success if ok else st.error)(msg)

# ---------------- DELETE ----------------
with tab_delete:
    df = list_records(entity)
    if df.empty:
        empty_state(f"No {entity.lower()} to delete.")
    else:
        record_id = st.selectbox(f"Select {entity[:-1]} ({pk}) to delete", df[pk].tolist(), key=f"del_select_{entity}")
        st.dataframe(df[df[pk] == record_id], use_container_width=True, hide_index=True)
        if st.button("🗑️ Delete this record", type="primary"):
            st.session_state["confirm_single_delete"] = record_id
        if st.session_state.get("confirm_single_delete") == record_id:
            st.warning("Are you sure? This cannot be undone.")
            cc1, cc2 = st.columns(2)
            if cc1.button("✅ Yes, delete"):
                ok, msg = delete_record(entity, record_id)
                st.session_state["confirm_single_delete"] = None
                (st.success if ok else st.error)(msg)
                st.rerun()
            if cc2.button("❌ Cancel"):
                st.session_state["confirm_single_delete"] = None
                st.rerun()
