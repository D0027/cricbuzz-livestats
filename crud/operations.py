"""
CRUD operations for the five core entities: Players, Teams, Matches,
Series, Venues. Each function opens its own session so it's safe to call
directly from Streamlit callbacks.
"""
from __future__ import annotations

import pandas as pd
from sqlalchemy import select

from database.connection import get_session
from database.models import Player, Team, Match, Series, Venue
from utils.logger import get_logger

logger = get_logger("crud")

MODEL_MAP = {
    "Players": Player,
    "Teams": Team,
    "Matches": Match,
    "Series": Series,
    "Venues": Venue,
}

PK_MAP = {
    "Players": "player_id",
    "Teams": "team_id",
    "Matches": "match_id",
    "Series": "series_id",
    "Venues": "venue_id",
}


def list_records(entity: str, search: str | None = None, search_col: str | None = None) -> pd.DataFrame:
    """Return all rows for an entity as a DataFrame, optionally filtered by a text search."""
    model = MODEL_MAP[entity]
    with get_session() as session:
        query = select(model)
        rows = session.execute(query).scalars().all()
        data = [row_to_dict(r) for r in rows]
    df = pd.DataFrame(data)
    if search and search_col and search_col in df.columns and not df.empty:
        df = df[df[search_col].astype(str).str.contains(search, case=False, na=False)]
    return df


def row_to_dict(obj) -> dict:
    return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}


def get_record(entity: str, record_id: int):
    model = MODEL_MAP[entity]
    pk = PK_MAP[entity]
    with get_session() as session:
        obj = session.get(model, record_id)
        return row_to_dict(obj) if obj else None


def create_record(entity: str, data: dict) -> tuple[bool, str]:
    model = MODEL_MAP[entity]
    try:
        with get_session() as session:
            obj = model(**data)
            session.add(obj)
        logger.info("Created %s: %s", entity, data)
        return True, f"{entity[:-1]} created successfully."
    except Exception as exc:
        logger.exception("Create failed for %s", entity)
        return False, f"Error creating {entity[:-1]}: {exc}"


def update_record(entity: str, record_id: int, data: dict) -> tuple[bool, str]:
    model = MODEL_MAP[entity]
    try:
        with get_session() as session:
            obj = session.get(model, record_id)
            if obj is None:
                return False, f"{entity[:-1]} not found."
            for k, v in data.items():
                setattr(obj, k, v)
        logger.info("Updated %s id=%s: %s", entity, record_id, data)
        return True, f"{entity[:-1]} updated successfully."
    except Exception as exc:
        logger.exception("Update failed for %s id=%s", entity, record_id)
        return False, f"Error updating {entity[:-1]}: {exc}"


def delete_record(entity: str, record_id: int) -> tuple[bool, str]:
    model = MODEL_MAP[entity]
    try:
        with get_session() as session:
            obj = session.get(model, record_id)
            if obj is None:
                return False, f"{entity[:-1]} not found."
            session.delete(obj)
        logger.info("Deleted %s id=%s", entity, record_id)
        return True, f"{entity[:-1]} deleted successfully."
    except Exception as exc:
        logger.exception("Delete failed for %s id=%s", entity, record_id)
        return False, f"Error deleting {entity[:-1]}: {exc}"


def bulk_delete(entity: str, record_ids: list[int]) -> tuple[bool, str]:
    model = MODEL_MAP[entity]
    pk = PK_MAP[entity]
    try:
        with get_session() as session:
            col = getattr(model, pk)
            objs = session.execute(select(model).where(col.in_(record_ids))).scalars().all()
            for obj in objs:
                session.delete(obj)
        return True, f"Deleted {len(record_ids)} record(s)."
    except Exception as exc:
        logger.exception("Bulk delete failed for %s", entity)
        return False, f"Error during bulk delete: {exc}"


def get_foreign_key_options(entity: str) -> dict:
    """Return {label: id} maps needed to populate dropdowns for FK fields."""
    options = {}
    with get_session() as session:
        if entity in ("Players", "Matches"):
            teams = session.execute(select(Team)).scalars().all()
            options["teams"] = {t.team_name: t.team_id for t in teams}
        if entity == "Matches":
            venues = session.execute(select(Venue)).scalars().all()
            options["venues"] = {f"{v.venue_name} ({v.city})": v.venue_id for v in venues}
            series = session.execute(select(Series)).scalars().all()
            options["series"] = {s.series_name: s.series_id for s in series}
            players = session.execute(select(Player)).scalars().all()
            options["players"] = {p.full_name: p.player_id for p in players}
    return options
