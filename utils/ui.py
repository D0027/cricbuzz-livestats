"""
Shared UI helpers: CSS injection, KPI cards, headers, footer, empty states.
Keeping all styling in one place gives the whole app a consistent,
premium, Cricbuzz-style look instead of default Streamlit chrome.
"""
from __future__ import annotations

import streamlit as st

# ---- Brand palette (cricket-broadcast inspired: pitch-navy + Cricbuzz red) ----
PRIMARY = "#E1261C"        # Cricbuzz red
PRIMARY_DARK = "#B01810"
ACCENT = "#00D2A0"         # scoreboard green
GOLD = "#F5B301"           # milestones / centuries
SUCCESS = "#00C875"
WARNING = "#F5B301"
DANGER = "#FF4757"
LIVE = "#FF3B3B"
BG_DARK = "#0A0E17"
CARD_BG = "rgba(255,255,255,0.045)"
CARD_BORDER = "rgba(255,255,255,0.09)"


def inject_global_css() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Rajdhani:wght@600;700&display=swap');

        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}

        html, body, [class*="css"] {{
            font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
        }}

        .stApp {{
            background:
                radial-gradient(circle at 15% -10%, rgba(225,38,28,0.14) 0%, transparent 40%),
                radial-gradient(circle at 85% 0%, rgba(0,210,160,0.08) 0%, transparent 35%),
                linear-gradient(180deg, #10131f 0%, #090b12 55%, #07080d 100%);
        }}

        .block-container {{
            padding-top: 1.4rem;
            padding-bottom: 3rem;
            max-width: 1340px;
        }}

        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, #13060a 0%, #0c0e19 45%, #0a0b12 100%);
            border-right: 1px solid rgba(225,38,28,0.15);
        }}
        section[data-testid="stSidebar"] * {{
            font-family: 'Inter', sans-serif;
        }}

        h1, h2, h3, h4 {{
            font-family: 'Inter', -apple-system, sans-serif;
            letter-spacing: -0.02em;
            font-weight: 800;
        }}

        /* ---- Top app header: sticky, brand strip ---- */
        .app-header {{
            display:flex; align-items:center; justify-content:space-between;
            padding: 1rem 1.5rem; margin-bottom: 1.3rem;
            background: linear-gradient(120deg, rgba(225,38,28,0.14), rgba(255,255,255,0.03) 60%);
            border: 1px solid {CARD_BORDER};
            border-left: 4px solid {PRIMARY};
            border-radius: 14px;
            backdrop-filter: blur(14px);
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
        }}

        .breadcrumb {{
            color: rgba(255,255,255,0.45); font-size: 0.78rem; margin-bottom: 0.35rem;
            text-transform: uppercase; letter-spacing: 0.08em; font-weight: 600;
        }}

        /* ---- Glass / score cards ---- */
        .glass-card {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 16px;
            padding: 1.2rem 1.35rem;
            backdrop-filter: blur(12px);
            transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
        }}
        .glass-card:hover {{
            transform: translateY(-3px);
            border-color: rgba(225,38,28,0.45);
            box-shadow: 0 10px 26px rgba(0,0,0,0.35);
        }}

        .match-card {{
            background: linear-gradient(135deg, rgba(255,255,255,0.05), rgba(255,255,255,0.02));
            border: 1px solid {CARD_BORDER};
            border-radius: 16px;
            padding: 1.1rem 1.3rem;
            margin-bottom: 0.9rem;
            position: relative;
            overflow: hidden;
            transition: transform 0.15s ease, border-color 0.15s ease;
        }}
        .match-card:hover {{ transform: translateY(-2px); border-color: rgba(225,38,28,0.4); }}
        .match-card.is-live {{ border-left: 3px solid {LIVE}; }}
        .match-card.is-done {{ border-left: 3px solid {SUCCESS}; }}
        .match-card.is-upcoming {{ border-left: 3px solid {GOLD}; }}

        .team-row {{
            display:flex; justify-content:space-between; align-items:center;
            padding: 0.15rem 0;
        }}
        .team-name {{ font-weight: 700; font-size: 1.02rem; }}
        .team-score {{
            font-family: 'Rajdhani', 'Inter', sans-serif;
            font-weight: 700; font-size: 1.15rem;
            color: {ACCENT};
            letter-spacing: 0.01em;
        }}
        .match-meta {{
            color: rgba(255,255,255,0.5); font-size: 0.82rem; margin-top: 0.55rem;
        }}
        .match-result {{
            color: {GOLD}; font-size: 0.85rem; font-weight: 600; margin-top: 0.35rem;
        }}

        /* ---- KPIs ---- */
        .kpi-value {{
            font-family: 'Rajdhani', 'Inter', sans-serif;
            font-size: 2.1rem; font-weight: 700;
            background: linear-gradient(90deg, {PRIMARY}, {GOLD});
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .kpi-label {{ color: rgba(255,255,255,0.55); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.07em; font-weight: 600;}}

        /* ---- Status pills ---- */
        .pill {{
            display:inline-flex; align-items:center; gap:0.35rem;
            padding: 0.2rem 0.75rem; border-radius: 999px;
            font-size: 0.72rem; font-weight: 700; letter-spacing: 0.03em;
            text-transform: uppercase;
        }}
        .pill-live {{ background: rgba(255,59,59,0.16); color: {LIVE}; }}
        .pill-done {{ background: rgba(0,200,117,0.16); color: {SUCCESS}; }}
        .pill-upcoming {{ background: rgba(245,179,1,0.16); color: {GOLD}; }}

        .live-dot {{
            width: 8px; height: 8px; border-radius: 50%;
            background: {LIVE};
            box-shadow: 0 0 0 0 rgba(255,59,59,0.6);
            animation: livepulse 1.4s infinite;
            display: inline-block;
        }}
        @keyframes livepulse {{
            0%   {{ box-shadow: 0 0 0 0 rgba(255,59,59,0.55); }}
            70%  {{ box-shadow: 0 0 0 7px rgba(255,59,59,0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(255,59,59,0); }}
        }}

        .footer-bar {{
            margin-top: 3rem; padding-top: 1.2rem;
            border-top: 1px solid {CARD_BORDER};
            color: rgba(255,255,255,0.38); font-size: 0.8rem; text-align:center;
        }}

        div[data-testid="stMetric"] {{
            background: {CARD_BG};
            border: 1px solid {CARD_BORDER};
            border-radius: 14px;
            padding: 0.8rem 1rem;
        }}

        div[data-testid="stMetricValue"] {{
            font-family: 'Rajdhani', 'Inter', sans-serif;
            color: {ACCENT};
        }}

        /* ---- Buttons & tabs ---- */
        .stButton>button {{
            border-radius: 10px; border: 1px solid rgba(225,38,28,0.55);
            background: linear-gradient(90deg, {PRIMARY}, {PRIMARY_DARK});
            color: white; font-weight: 700;
            transition: filter 0.15s ease, transform 0.1s ease;
        }}
        .stButton>button:hover {{ filter: brightness(1.12); border-color: {ACCENT}; }}
        .stButton>button:active {{ transform: scale(0.98); }}

        .stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
        .stTabs [data-baseweb="tab"] {{
            border-radius: 10px 10px 0 0;
            font-weight: 600;
        }}
        .stTabs [aria-selected="true"] {{
            color: {PRIMARY} !important;
            border-bottom: 2px solid {PRIMARY} !important;
        }}

        div[data-testid="stExpander"] {{
            border: 1px solid {CARD_BORDER};
            border-radius: 12px;
            background: {CARD_BG};
        }}

        .empty-state {{
            text-align:center; padding: 3rem 1rem; color: rgba(255,255,255,0.45);
        }}

        /* scrollbar polish */
        ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
        ::-webkit-scrollbar-track {{ background: transparent; }}
        ::-webkit-scrollbar-thumb {{ background: rgba(225,38,28,0.35); border-radius: 8px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: rgba(225,38,28,0.55); }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def page_header(title: str, subtitle: str = "", breadcrumb: str = "") -> None:
    if breadcrumb:
        st.markdown(f"<div class='breadcrumb'>{breadcrumb}</div>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="app-header">
            <div>
                <h2 style="margin:0;">{title}</h2>
                <div style="color:rgba(255,255,255,0.55); font-size:0.92rem;">{subtitle}</div>
            </div>
            <div style="font-size:1.7rem;">🏏</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_card(label: str, value: str) -> str:
    return f"""
        <div class="glass-card">
            <div class="kpi-value">{value}</div>
            <div class="kpi-label">{label}</div>
        </div>
    """


def status_pill(status: str) -> str:
    status_l = (status or "").lower()
    cls = "pill-done"
    dot = ""
    if "live" in status_l or "progress" in status_l or "innings break" in status_l or "stumps" in status_l:
        cls = "pill-live"
        dot = "<span class='live-dot'></span>"
    elif "upcoming" in status_l or "scheduled" in status_l or "preview" in status_l:
        cls = "pill-upcoming"
    return f"<span class='pill {cls}'>{dot}{status or 'Unknown'}</span>"


def match_status_class(status: str) -> str:
    status_l = (status or "").lower()
    if "live" in status_l or "progress" in status_l:
        return "is-live"
    if "upcoming" in status_l or "scheduled" in status_l:
        return "is-upcoming"
    return "is-done"


def empty_state(message: str, icon: str = "🏏") -> None:
    st.markdown(
        f"<div class='empty-state'><div style='font-size:2.4rem;'>{icon}</div>{message}</div>",
        unsafe_allow_html=True,
    )


def footer() -> None:
    st.markdown(
        """
        <div class="footer-bar">
            🏏 Cricbuzz LiveStats · Built with Streamlit · Data via Cricbuzz API &amp; SQL Analytics Engine
        </div>
        """,
        unsafe_allow_html=True,
    )
