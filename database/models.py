"""
ORM models for the Cricbuzz LiveStats database.

Schema (normalized, 3NF-ish for an analytics workload):
    teams        - country/franchise teams
    venues       - stadiums
    series       - tournament/series info
    matches      - individual matches (FK: team1, team2, venue, series)
    players      - player master data (FK: team)
    player_stats - aggregated career stats per player per format
    innings      - per-innings batting/bowling summary per match
    performances - per-player, per-match performance rows (batting+bowling)

Works identically on SQLite, MySQL, and PostgreSQL via SQLAlchemy.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    Text,
    Boolean,
    UniqueConstraint,
    Index,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String(100), nullable=False, unique=True)
    country = Column(String(100), nullable=False)
    team_type = Column(String(30), default="International")  # International / Franchise
    created_at = Column(DateTime, default=datetime.utcnow)

    players = relationship("Player", back_populates="team")


class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True, autoincrement=True)
    venue_name = Column(String(150), nullable=False)
    city = Column(String(100))
    country = Column(String(100))
    capacity = Column(Integer)

    __table_args__ = (UniqueConstraint("venue_name", "city", name="uq_venue_city"),)


class Series(Base):
    __tablename__ = "series"

    series_id = Column(Integer, primary_key=True, autoincrement=True)
    series_name = Column(String(200), nullable=False)
    host_country = Column(String(100))
    match_type = Column(String(20))  # Test / ODI / T20
    start_date = Column(Date)
    end_date = Column(Date)
    total_matches = Column(Integer, default=0)

    matches = relationship("Match", back_populates="series")


class Player(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(150), nullable=False)
    playing_role = Column(String(30))  # Batsman/Bowler/All-rounder/WK-Batsman
    batting_style = Column(String(30))
    bowling_style = Column(String(50))
    country = Column(String(100))
    date_of_birth = Column(Date)
    team_id = Column(Integer, ForeignKey("teams.team_id"))
    is_active = Column(Boolean, default=True)

    team = relationship("Team", back_populates="players")
    stats = relationship("PlayerStats", back_populates="player")
    performances = relationship("Performance", back_populates="player")

    __table_args__ = (Index("ix_players_role", "playing_role"),)


class PlayerStats(Base):
    """Aggregated career statistics per player per format."""

    __tablename__ = "player_stats"

    stat_id = Column(Integer, primary_key=True, autoincrement=True)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    format = Column(String(10), nullable=False)  # Test/ODI/T20I/T20

    matches = Column(Integer, default=0)
    innings_batted = Column(Integer, default=0)
    runs = Column(Integer, default=0)
    balls_faced = Column(Integer, default=0)
    highest_score = Column(Integer, default=0)
    batting_average = Column(Float, default=0.0)
    strike_rate = Column(Float, default=0.0)
    centuries = Column(Integer, default=0)
    half_centuries = Column(Integer, default=0)
    fours = Column(Integer, default=0)
    sixes = Column(Integer, default=0)

    innings_bowled = Column(Integer, default=0)
    balls_bowled = Column(Integer, default=0)
    runs_conceded = Column(Integer, default=0)
    wickets = Column(Integer, default=0)
    best_bowling = Column(String(20))
    bowling_average = Column(Float, default=0.0)
    economy_rate = Column(Float, default=0.0)
    five_wicket_hauls = Column(Integer, default=0)

    catches = Column(Integer, default=0)
    stumpings = Column(Integer, default=0)

    player = relationship("Player", back_populates="stats")

    __table_args__ = (UniqueConstraint("player_id", "format", name="uq_player_format"),)


class Match(Base):
    __tablename__ = "matches"

    match_id = Column(Integer, primary_key=True, autoincrement=True)
    series_id = Column(Integer, ForeignKey("series.series_id"))
    team1_id = Column(Integer, ForeignKey("teams.team_id"))
    team2_id = Column(Integer, ForeignKey("teams.team_id"))
    venue_id = Column(Integer, ForeignKey("venues.venue_id"))
    match_type = Column(String(10))  # Test/ODI/T20I/T20
    match_date = Column(Date)
    toss_winner_id = Column(Integer, ForeignKey("teams.team_id"), nullable=True)
    toss_decision = Column(String(10))
    winner_id = Column(Integer, ForeignKey("teams.team_id"), nullable=True)
    win_margin = Column(String(50))
    victory_type = Column(String(20))  # runs/wickets
    player_of_match_id = Column(Integer, ForeignKey("players.player_id"), nullable=True)
    status = Column(String(30), default="Completed")

    series = relationship("Series", back_populates="matches")
    innings = relationship("Innings", back_populates="match")
    performances = relationship("Performance", back_populates="match")

    __table_args__ = (Index("ix_matches_date", "match_date"),)


class Innings(Base):
    __tablename__ = "innings"

    innings_id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("matches.match_id"), nullable=False)
    batting_team_id = Column(Integer, ForeignKey("teams.team_id"))
    innings_number = Column(Integer)
    total_runs = Column(Integer, default=0)
    total_wickets = Column(Integer, default=0)
    overs = Column(Float, default=0.0)
    run_rate = Column(Float, default=0.0)

    match = relationship("Match", back_populates="innings")


class Performance(Base):
    """One row per player per match: batting + bowling + fielding for that match."""

    __tablename__ = "performances"

    performance_id = Column(Integer, primary_key=True, autoincrement=True)
    match_id = Column(Integer, ForeignKey("matches.match_id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.player_id"), nullable=False)
    team_id = Column(Integer, ForeignKey("teams.team_id"))

    runs_scored = Column(Integer, default=0)
    balls_faced = Column(Integer, default=0)
    fours = Column(Integer, default=0)
    sixes = Column(Integer, default=0)
    dismissal_type = Column(String(30))

    overs_bowled = Column(Float, default=0.0)
    runs_conceded = Column(Integer, default=0)
    wickets_taken = Column(Integer, default=0)
    maidens = Column(Integer, default=0)

    catches_taken = Column(Integer, default=0)
    stumpings_made = Column(Integer, default=0)

    match = relationship("Match", back_populates="performances")
    player = relationship("Player", back_populates="performances")

    __table_args__ = (Index("ix_perf_match_player", "match_id", "player_id"),)
