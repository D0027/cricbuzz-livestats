"""
Seeds the database with realistic sample cricket data so every SQL query,
chart, and CRUD screen has something meaningful to show out of the box
(no API key required to explore the analytics side of the app).

Run directly: `python -m database.seed_data`
"""
from __future__ import annotations

import random
from datetime import date, timedelta

from database.connection import get_session, init_db, get_engine
from database.models import Team, Venue, Series, Player, PlayerStats, Match, Innings, Performance
from utils.logger import get_logger

logger = get_logger("seed_data")
random.seed(42)

TEAMS = [
    ("India", "India", "International"),
    ("Australia", "Australia", "International"),
    ("England", "England", "International"),
    ("South Africa", "South Africa", "International"),
    ("New Zealand", "New Zealand", "International"),
    ("Pakistan", "Pakistan", "International"),
    ("Sri Lanka", "Sri Lanka", "International"),
    ("West Indies", "West Indies", "International"),
    ("Mumbai Indians", "India", "Franchise"),
    ("Chennai Super Kings", "India", "Franchise"),
]

VENUES = [
    ("Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
    ("Eden Gardens", "Kolkata", "India", 66000),
    ("Lord's", "London", "England", 30000),
    ("Wankhede Stadium", "Mumbai", "India", 33108),
    ("Newlands", "Cape Town", "South Africa", 25000),
    ("Basin Reserve", "Wellington", "New Zealand", 11600),
    ("Gaddafi Stadium", "Lahore", "Pakistan", 27000),
    ("R Premadasa Stadium", "Colombo", "Sri Lanka", 35000),
]

PLAYER_POOL = {
    "India": [
        ("Rohit Sharma", "Batsman", "Right-hand bat", "-"),
        ("Virat Kohli", "Batsman", "Right-hand bat", "-"),
        ("Jasprit Bumrah", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Ravindra Jadeja", "All-rounder", "Left-hand bat", "Left-arm orthodox"),
        ("KL Rahul", "WK-Batsman", "Right-hand bat", "-"),
        ("Mohammed Shami", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Shubman Gill", "Batsman", "Right-hand bat", "-"),
        ("Hardik Pandya", "All-rounder", "Right-hand bat", "Right-arm medium-fast"),
    ],
    "Australia": [
        ("Pat Cummins", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Steve Smith", "Batsman", "Right-hand bat", "Right-arm leg-break"),
        ("David Warner", "Batsman", "Left-hand bat", "-"),
        ("Mitchell Starc", "Bowler", "Left-hand bat", "Left-arm fast"),
        ("Glenn Maxwell", "All-rounder", "Right-hand bat", "Right-arm off-break"),
        ("Alex Carey", "WK-Batsman", "Left-hand bat", "-"),
    ],
    "England": [
        ("Joe Root", "Batsman", "Right-hand bat", "Right-arm off-break"),
        ("Ben Stokes", "All-rounder", "Left-hand bat", "Right-arm fast-medium"),
        ("Jos Buttler", "WK-Batsman", "Right-hand bat", "-"),
        ("James Anderson", "Bowler", "Left-hand bat", "Right-arm fast-medium"),
        ("Harry Brook", "Batsman", "Right-hand bat", "-"),
    ],
    "South Africa": [
        ("Kagiso Rabada", "Bowler", "Right-hand bat", "Right-arm fast"),
        ("Quinton de Kock", "WK-Batsman", "Left-hand bat", "-"),
        ("Aiden Markram", "Batsman", "Right-hand bat", "Right-arm off-break"),
    ],
    "New Zealand": [
        ("Kane Williamson", "Batsman", "Right-hand bat", "Right-arm off-break"),
        ("Trent Boult", "Bowler", "Right-hand bat", "Left-arm fast-medium"),
        ("Devon Conway", "WK-Batsman", "Left-hand bat", "-"),
    ],
    "Pakistan": [
        ("Babar Azam", "Batsman", "Right-hand bat", "-"),
        ("Shaheen Afridi", "Bowler", "Left-hand bat", "Left-arm fast"),
        ("Mohammad Rizwan", "WK-Batsman", "Right-hand bat", "-"),
    ],
    "Sri Lanka": [
        ("Wanindu Hasaranga", "All-rounder", "Right-hand bat", "Right-arm leg-break"),
        ("Kusal Mendis", "WK-Batsman", "Right-hand bat", "-"),
    ],
    "West Indies": [
        ("Nicholas Pooran", "WK-Batsman", "Left-hand bat", "-"),
        ("Jason Holder", "All-rounder", "Right-hand bat", "Right-arm fast-medium"),
    ],
}

FORMATS = ["Test", "ODI", "T20I"]


def seed() -> None:
    init_db()
    with get_session() as s:
        if s.query(Team).count() > 0:
            logger.info("Database already seeded, skipping.")
            return

        # Teams
        team_objs = {}
        for name, country, ttype in TEAMS:
            t = Team(team_name=name, country=country, team_type=ttype)
            s.add(t)
            team_objs[name] = t
        s.flush()

        # Venues
        venue_objs = []
        for name, city, country, cap in VENUES:
            v = Venue(venue_name=name, city=city, country=country, capacity=cap)
            s.add(v)
            venue_objs.append(v)
        s.flush()

        # Series
        series_objs = []
        for i, (mtype) in enumerate(["Test", "ODI", "T20I", "ODI", "T20I"]):
            sr = Series(
                series_name=f"{random.choice(['Border-Gavaskar','World Championship','Tri-Series','Bilateral Series','Tour Series'])} {2023+i}",
                host_country=random.choice([c for _, c, _ in TEAMS]),
                match_type=mtype,
                start_date=date(2023 + i, 1, 1) + timedelta(days=i * 40),
                end_date=date(2023 + i, 2, 15) + timedelta(days=i * 40),
                total_matches=random.randint(3, 5),
            )
            s.add(sr)
            series_objs.append(sr)
        s.flush()

        # Players
        player_objs = []
        for country, plist in PLAYER_POOL.items():
            for name, role, bat_style, bowl_style in plist:
                p = Player(
                    full_name=name,
                    playing_role=role,
                    batting_style=bat_style,
                    bowling_style=bowl_style,
                    country=country,
                    date_of_birth=date(1988 + random.randint(0, 12), random.randint(1, 12), random.randint(1, 28)),
                    team_id=team_objs[country].team_id,
                    is_active=True,
                )
                s.add(p)
                player_objs.append(p)
        s.flush()

        # Player career stats per format
        for p in player_objs:
            for fmt in FORMATS:
                is_bowler = p.playing_role in ("Bowler", "All-rounder")
                is_batsman = p.playing_role in ("Batsman", "All-rounder", "WK-Batsman")
                matches = random.randint(20, 220)
                innings_batted = int(matches * random.uniform(0.8, 1.0)) if is_batsman else int(matches * 0.3)
                runs = int(innings_batted * random.uniform(15, 55)) if is_batsman else int(innings_batted * random.uniform(5, 15))
                balls_faced = int(runs * random.uniform(1.1, 1.8)) + 1
                stat = PlayerStats(
                    player_id=p.player_id,
                    format=fmt,
                    matches=matches,
                    innings_batted=innings_batted,
                    runs=runs,
                    balls_faced=balls_faced,
                    highest_score=random.randint(45, 254) if is_batsman else random.randint(5, 40),
                    batting_average=round(runs / max(innings_batted * random.uniform(0.75, 0.95), 1), 2),
                    strike_rate=round((runs / max(balls_faced, 1)) * 100, 2),
                    centuries=random.randint(0, 45) if is_batsman and fmt != "T20I" else random.randint(0, 5),
                    half_centuries=random.randint(0, 60),
                    fours=int(runs * random.uniform(0.08, 0.14)),
                    sixes=int(runs * random.uniform(0.01, 0.06)),
                    innings_bowled=int(matches * random.uniform(0.6, 1.0)) if is_bowler else 0,
                    balls_bowled=int(matches * random.uniform(20, 200)) if is_bowler else 0,
                    runs_conceded=int(matches * random.uniform(20, 180)) if is_bowler else 0,
                    wickets=int(matches * random.uniform(0.8, 2.2)) if is_bowler else 0,
                    best_bowling=f"{random.randint(3,7)}/{random.randint(10,60)}" if is_bowler else None,
                    bowling_average=round(random.uniform(18, 34), 2) if is_bowler else 0.0,
                    economy_rate=round(random.uniform(3.2, 6.5), 2) if is_bowler else 0.0,
                    five_wicket_hauls=random.randint(0, 10) if is_bowler else 0,
                    catches=random.randint(5, 120),
                    stumpings=random.randint(0, 40) if p.playing_role == "WK-Batsman" else 0,
                )
                s.add(stat)
        s.flush()

        # Matches + Innings + Performances
        team_names = list(team_objs.keys())
        match_date = date(2023, 1, 1)
        for i in range(60):
            t1_name, t2_name = random.sample(team_names, 2)
            t1, t2 = team_objs[t1_name], team_objs[t2_name]
            venue = random.choice(venue_objs)
            sr = random.choice(series_objs)
            mtype = sr.match_type
            match_date = match_date + timedelta(days=random.randint(2, 9))
            toss_winner = random.choice([t1, t2])
            winner = random.choice([t1, t2, None]) if random.random() > 0.05 else None
            victory_type = random.choice(["runs", "wickets"])
            margin = f"{random.randint(5,150)} runs" if victory_type == "runs" else f"{random.randint(1,9)} wickets"

            eligible_players = [
                p for p in player_objs if p.team_id in (t1.team_id, t2.team_id)
            ]
            pom = random.choice(eligible_players) if eligible_players else None

            m = Match(
                series_id=sr.series_id,
                team1_id=t1.team_id,
                team2_id=t2.team_id,
                venue_id=venue.venue_id,
                match_type=mtype,
                match_date=match_date,
                toss_winner_id=toss_winner.team_id,
                toss_decision=random.choice(["Bat", "Bowl"]),
                winner_id=winner.team_id if winner else None,
                win_margin=margin if winner else None,
                victory_type=victory_type if winner else None,
                player_of_match_id=pom.player_id if pom else None,
                status="Completed",
            )
            s.add(m)
            s.flush()

            for inn_num, batting_team in enumerate([t1, t2], start=1):
                total_runs = random.randint(120, 420) if mtype != "T20I" else random.randint(110, 230)
                total_wkts = random.randint(3, 10)
                overs = round(random.uniform(35, 50), 1) if mtype != "T20I" else round(random.uniform(15, 20), 1)
                inn = Innings(
                    match_id=m.match_id,
                    batting_team_id=batting_team.team_id,
                    innings_number=inn_num,
                    total_runs=total_runs,
                    total_wickets=total_wkts,
                    overs=overs,
                    run_rate=round(total_runs / max(overs, 1), 2),
                )
                s.add(inn)

                squad = [p for p in eligible_players if p.team_id == batting_team.team_id][:6] or eligible_players[:6]
                for p in squad:
                    runs_scored = random.randint(0, 120)
                    balls_faced = runs_scored + random.randint(0, 40)
                    perf = Performance(
                        match_id=m.match_id,
                        player_id=p.player_id,
                        team_id=batting_team.team_id,
                        runs_scored=runs_scored,
                        balls_faced=max(balls_faced, 1),
                        fours=random.randint(0, 10),
                        sixes=random.randint(0, 5),
                        dismissal_type=random.choice(["Bowled", "Caught", "LBW", "Run Out", "Not Out"]),
                        overs_bowled=round(random.uniform(0, 10), 1) if p.playing_role in ("Bowler", "All-rounder") else 0.0,
                        runs_conceded=random.randint(0, 60) if p.playing_role in ("Bowler", "All-rounder") else 0,
                        wickets_taken=random.randint(0, 4) if p.playing_role in ("Bowler", "All-rounder") else 0,
                        maidens=random.randint(0, 2),
                        catches_taken=random.randint(0, 3),
                        stumpings_made=random.randint(0, 1) if p.playing_role == "WK-Batsman" else 0,
                    )
                    s.add(perf)

        logger.info("Seed data inserted: %d teams, %d players, 60 matches.", len(team_objs), len(player_objs))

    logger.info("Database seeding complete.")


if __name__ == "__main__":
    seed()
