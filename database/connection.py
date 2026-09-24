"""
Database engine and session management.

Single place that creates the SQLAlchemy engine (SQLite by default, but
MySQL/PostgreSQL work by changing DB_TYPE in .env) and hands out sessions.
"""
from __future__ import annotations

from contextlib import contextmanager

import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from database.models import Base
from utils.config import settings
from utils.logger import get_logger

logger = get_logger("database")


@st.cache_resource(show_spinner=False)
def get_engine():
    """Create (and cache) the SQLAlchemy engine for the app's lifetime."""
    connect_args = {"check_same_thread": False} if settings.db_type == "sqlite" else {}
    engine = create_engine(settings.sqlalchemy_url, connect_args=connect_args, pool_pre_ping=True)
    logger.info("Database engine created for db_type=%s", settings.db_type)
    return engine


def init_db() -> None:
    """Create all tables if they don't already exist."""
    engine = get_engine()
    Base.metadata.create_all(engine)
    logger.info("Database schema ensured (create_all).")


def get_session_factory():
    engine = get_engine()
    # expire_on_commit=False: our `get_session()` context manager commits
    # *before* closing the session, and several pages read ORM attributes
    # (e.g. match.win_margin, team.team_name) after the `with` block has
    # exited. With the SQLAlchemy default (expire_on_commit=True), those
    # attributes are marked stale on commit and any later access tries to
    # lazy-load from a session that's already closed, raising
    # DetachedInstanceError. Turning commit-expiry off keeps already-loaded
    # attributes readable after the session closes.
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


@contextmanager
def get_session():
    """Context-managed DB session: `with get_session() as session: ...`"""
    SessionLocal = get_session_factory()
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        logger.exception("Database session error, rolled back.")
        raise
    finally:
        session.close()


def run_raw_query(sql: str, params: dict | None = None):
    """Execute a raw parameterized SQL query and return (columns, rows)."""
    engine = get_engine()
    with engine.connect() as conn:
        result = conn.execute(text(sql), params or {})
        columns = list(result.keys())
        rows = result.fetchall()
    return columns, rows
