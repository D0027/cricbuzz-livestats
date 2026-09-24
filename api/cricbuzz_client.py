"""
Professional wrapper around the Cricbuzz Cricket API (via RapidAPI).

Handles: retries with backoff, timeouts, response caching (via Streamlit's
cache_data), structured logging, and graceful error handling so the UI
never crashes on a bad/missing API key or network hiccup.

If no API key is configured, `is_configured()` returns False and callers
should fall back to database-driven content instead of live data.
"""
from __future__ import annotations

import time
from typing import Any

import requests
import streamlit as st

from utils.config import settings
from utils.logger import get_logger

logger = get_logger("cricbuzz_api")


class CricbuzzAPIError(Exception):
    """Raised for any unrecoverable API failure."""


class CricbuzzClient:
    def __init__(self) -> None:
        self.base_url = settings.cricbuzz_base_url.rstrip("/")
        self.headers = {
            "X-RapidAPI-Key": settings.cricbuzz_api_key,
            "X-RapidAPI-Host": settings.cricbuzz_api_host,
        }

    def is_configured(self) -> bool:
        return settings.api_configured

    def _request(self, path: str, params: dict | None = None) -> dict[str, Any]:
        if not self.is_configured():
            raise CricbuzzAPIError("Cricbuzz API key is not configured (set CRICBUZZ_API_KEY in .env).")

        url = f"{self.base_url}{path}"
        last_exc: Exception | None = None

        for attempt in range(1, settings.request_max_retries + 1):
            try:
                resp = requests.get(
                    url, headers=self.headers, params=params, timeout=settings.request_timeout
                )
                if resp.status_code == 429:
                    # Don't burn more of an already-exhausted quota by retrying —
                    # fail fast with a clear message instead. Retrying on 429 just
                    # counts as more requests against a limit that's already hit.
                    logger.warning("Rate limited by Cricbuzz API (HTTP 429) on %s", url)
                    raise CricbuzzAPIError(
                        "Rate limit hit (HTTP 429) — your RapidAPI plan's request quota "
                        "(per-second or monthly) is used up right now. This page's data is "
                        "cached for a bit once it succeeds, so wait ~30-60s before retrying, "
                        "or check usage/upgrade your plan on the RapidAPI dashboard."
                    )
                if resp.status_code == 403:
                    raise CricbuzzAPIError(
                        "Access forbidden (HTTP 403) — your RapidAPI key may not be subscribed "
                        "to this API, or the subscription has expired. Check the RapidAPI dashboard."
                    )
                resp.raise_for_status()
                return resp.json()
            except CricbuzzAPIError:
                raise
            except requests.exceptions.RequestException as exc:
                last_exc = exc
                logger.warning("API request attempt %d/%d failed: %s", attempt, settings.request_max_retries, exc)
                time.sleep(min(2 ** attempt, 8))

        logger.error("API request permanently failed for %s: %s", url, last_exc)
        raise CricbuzzAPIError(str(last_exc) if last_exc else "Unknown error — no response received from the API.")

    # ---- Public endpoints ----

    @st.cache_data(ttl=60, show_spinner=False)
    def get_live_matches(_self) -> dict[str, Any]:
        return _self._request("/matches/v1/live")

    @st.cache_data(ttl=300, show_spinner=False)
    def get_recent_matches(_self) -> dict[str, Any]:
        return _self._request("/matches/v1/recent")

    @st.cache_data(ttl=300, show_spinner=False)
    def get_upcoming_matches(_self) -> dict[str, Any]:
        return _self._request("/matches/v1/upcoming")

    @st.cache_data(ttl=30, show_spinner=False)
    def get_match_scorecard(_self, match_id: int) -> dict[str, Any]:
        return _self._request(f"/mcenter/v1/{match_id}/scard")

    @st.cache_data(ttl=30, show_spinner=False)
    def get_match_commentary(_self, match_id: int) -> dict[str, Any]:
        return _self._request(f"/mcenter/v1/{match_id}/comm")

    @st.cache_data(ttl=3600, show_spinner=False)
    def search_player(_self, name: str) -> dict[str, Any]:
        return _self._request("/stats/v1/player/search", params={"plrN": name})

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_player_info(_self, player_id: int) -> dict[str, Any]:
        return _self._request(f"/stats/v1/player/{player_id}")

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_player_batting_stats(_self, player_id: int) -> dict[str, Any]:
        return _self._request(f"/stats/v1/player/{player_id}/batting")

    @st.cache_data(ttl=3600, show_spinner=False)
    def get_player_bowling_stats(_self, player_id: int) -> dict[str, Any]:
        return _self._request(f"/stats/v1/player/{player_id}/bowling")

    @st.cache_data(ttl=600, show_spinner=False)
    def get_icc_rankings(_self, category: str = "batsmen", format_type: str = "test") -> dict[str, Any]:
        return _self._request(
            "/stats/v1/rankings/" + category, params={"formatType": format_type}
        )


@st.cache_resource(show_spinner=False)
def get_client() -> CricbuzzClient:
    return CricbuzzClient()