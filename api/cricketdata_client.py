"""
Free cricket data source (CricketData.org, formerly CricAPI) — used as the
primary/fallback live-data provider when the Cricbuzz RapidAPI quota (200/mo)
runs out. Free tier: 100 requests/day, no credit card required.
Signup: https://cricketdata.org/signup.aspx
"""
from __future__ import annotations

from typing import Any

import requests
import streamlit as st

from utils.config import settings
from utils.logger import get_logger

logger = get_logger("cricketdata_api")


class CricketDataAPIError(Exception):
    """Raised for any unrecoverable CricketData.org API failure."""


class CricketDataClient:
    BASE_URL = "https://api.cricapi.com/v1"

    def is_configured(self) -> bool:
        return settings.cricketdata_configured

    def _request(self, endpoint: str, params: dict | None = None) -> dict[str, Any]:
        if not self.is_configured():
            raise CricketDataAPIError(
                "CricketData.org API key not configured (set CRICKETDATA_API_KEY in .env)."
            )
        params = dict(params or {})
        params["apikey"] = settings.cricketdata_api_key
        url = f"{self.BASE_URL}/{endpoint}"
        try:
            resp = requests.get(url, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
        except requests.exceptions.RequestException as exc:
            logger.error("CricketData request failed for %s: %s", endpoint, exc)
            raise CricketDataAPIError(str(exc)) from exc

        # CricketData.org returns HTTP 200 even on quota/auth errors, with
        # status field carrying the real result — check it explicitly.
        status = str(data.get("status", "")).lower()
        if status not in ("success", ""):
            reason = data.get("reason") or data.get("message") or "Unknown API error"
            logger.warning("CricketData API returned status=%s reason=%s", status, reason)
            raise CricketDataAPIError(f"CricketData.org: {reason}")
        return data

    @st.cache_data(ttl=60, show_spinner=False)
    def get_current_matches(_self) -> dict[str, Any]:
        """All matches currently live/recent/upcoming in one feed."""
        return _self._request("currentMatches", params={"offset": 0})

    @st.cache_data(ttl=300, show_spinner=False)
    def get_all_matches(_self) -> dict[str, Any]:
        return _self._request("matches", params={"offset": 0})

    @st.cache_data(ttl=30, show_spinner=False)
    def get_match_scorecard(_self, match_id: str) -> dict[str, Any]:
        return _self._request("match_scorecard", params={"id": match_id})

    @st.cache_data(ttl=3600, show_spinner=False)
    def search_player(_self, name: str) -> dict[str, Any]:
        return _self._request("players", params={"offset": 0, "search": name})


@st.cache_resource(show_spinner=False)
def get_cricketdata_client() -> CricketDataClient:
    return CricketDataClient()