from __future__ import annotations

import time

import pandas as pd
import plotly.express as px
import streamlit as st

from analytics.sql_queries import QUERIES
from database.connection import run_raw_query
from utils.exporters import to_csv_bytes
from utils.ui import page_header, empty_state
from utils.logger import get_logger

logger = get_logger("sql_analytics")

page_header(
    "SQL Analytics",
    "All 25 analytics questions — beginner to advanced — each with live SQL execution, "
    "visualization, and CSV export.",
    breadcrumb="Analytics / SQL Analytics",
)

diff_filter = st.multiselect(
    "Filter by difficulty", ["Beginner", "Intermediate", "Advanced"], default=[]
)
search = st.text_input("🔍 Search questions")

visible = QUERIES
if diff_filter:
    visible = [q for q in visible if q["difficulty"] in diff_filter]
if search:
    visible = [q for q in visible if search.lower() in q["title"].lower() or search.lower() in q["question"].lower()]

st.caption(f"Showing {len(visible)} of {len(QUERIES)} queries.")

for q in visible:
    diff_color = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}[q["difficulty"]]
    with st.expander(f"**Q{q['id']}.** {diff_color} {q['title']}  —  _{q['difficulty']}_"):
        st.markdown(f"**Question:** {q['question']}")
        st.code(q["sql"].strip(), language="sql")

        run = st.button("▶️ Run Query", key=f"run_{q['id']}")
        state_key = f"result_{q['id']}"

        if run:
            try:
                start = time.perf_counter()
                columns, rows = run_raw_query(q["sql"])
                elapsed_ms = (time.perf_counter() - start) * 1000
                df = pd.DataFrame(rows, columns=columns)
                st.session_state[state_key] = (df, elapsed_ms, None)
            except Exception as exc:
                logger.exception("Query %s failed", q["id"])
                st.session_state[state_key] = (None, None, str(exc))

        if state_key in st.session_state:
            df, elapsed_ms, error = st.session_state[state_key]
            if error:
                st.error(f"Query failed: {error}")
            elif df is not None:
                st.success(f"Executed in {elapsed_ms:.1f} ms · {len(df)} row(s) returned")
                if df.empty:
                    empty_state("Query ran successfully but returned no rows.")
                else:
                    st.dataframe(df, use_container_width=True, hide_index=True)

                    chart_col = q.get("chart")
                    if chart_col and chart_col in df.columns:
                        label_col = df.columns[0]
                        fig = px.bar(
                            df.head(20), x=label_col, y=chart_col,
                            color=chart_col, color_continuous_scale="Purples",
                            title=f"{chart_col.replace('_', ' ').title()} by {label_col}",
                        )
                        fig.update_layout(xaxis_tickangle=-35)
                        st.plotly_chart(fig, use_container_width=True)

                    st.download_button(
                        "⬇️ Download CSV",
                        data=to_csv_bytes(df),
                        file_name=f"query_{q['id']}_result.csv",
                        mime="text/csv",
                        key=f"dl_{q['id']}",
                    )
