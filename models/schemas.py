"""Pydantic schemas for validating data before it hits the database."""
from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class TeamSchema(BaseModel):
    team_name: str = Field(min_length=2, max_length=100)
    country: str = Field(min_length=2, max_length=100)
    team_type: str = "International"


class VenueSchema(BaseModel):
    venue_name: str = Field(min_length=2, max_length=150)
    city: Optional[str] = None
    country: Optional[str] = None
    capacity: Optional[int] = Field(default=None, ge=0)


class SeriesSchema(BaseModel):
    series_name: str = Field(min_length=2, max_length=200)
    host_country: Optional[str] = None
    match_type: str = "ODI"
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    total_matches: int = Field(default=1, ge=1)


class PlayerSchema(BaseModel):
    full_name: str = Field(min_length=2, max_length=150)
    playing_role: str = "Batsman"
    batting_style: Optional[str] = None
    bowling_style: Optional[str] = None
    country: str
    date_of_birth: Optional[date] = None
    team_id: Optional[int] = None
    is_active: bool = True


class MatchSchema(BaseModel):
    series_id: Optional[int] = None
    team1_id: int
    team2_id: int
    venue_id: Optional[int] = None
    match_type: str = "ODI"
    match_date: Optional[date] = None
    toss_decision: Optional[str] = None
    status: str = "Scheduled"
