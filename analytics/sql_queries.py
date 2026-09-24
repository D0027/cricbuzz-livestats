"""
The 25 SQL analytics questions for the SQL Analytics page.

Each entry: id, title, difficulty, question, sql, chart hint (which column
to plot, or None if a table is more appropriate).

Difficulty bands follow the classic spec: 1-8 Beginner, 9-16 Intermediate,
17-25 Advanced.
"""
from __future__ import annotations

QUERIES = [
    {
        "id": 1,
        "difficulty": "Beginner",
        "title": "All players and their teams",
        "question": "Find all players along with their team name and playing role.",
        "sql": """
            SELECT p.full_name, t.team_name, p.playing_role, p.batting_style
            FROM players p
            JOIN teams t ON p.team_id = t.team_id
            ORDER BY t.team_name, p.full_name
        """,
        "chart": None,
    },
    {
        "id": 2,
        "difficulty": "Beginner",
        "title": "Recent matches with result summary",
        "question": "Show the 20 most recent matches with teams, venue, and winner.",
        "sql": """
            SELECT m.match_id, m.match_date, t1.team_name AS team1, t2.team_name AS team2,
                   v.venue_name, v.city, w.team_name AS winner, m.win_margin
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            LEFT JOIN teams w ON m.winner_id = w.team_id
            ORDER BY m.match_date DESC
            LIMIT 20
        """,
        "chart": None,
    },
    {
        "id": 3,
        "difficulty": "Beginner",
        "title": "Top run scorers (ODI)",
        "question": "List the top 10 run scorers in ODI format by total career runs.",
        "sql": """
            SELECT p.full_name, p.country, ps.runs, ps.batting_average, ps.strike_rate
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE ps.format = 'ODI'
            ORDER BY ps.runs DESC
            LIMIT 10
        """,
        "chart": "runs",
    },
    {
        "id": 4,
        "difficulty": "Beginner",
        "title": "Venues by capacity",
        "question": "List all venues with capacity greater than 30,000, sorted by capacity descending.",
        "sql": """
            SELECT venue_name, city, country, capacity
            FROM venues
            WHERE capacity > 30000
            ORDER BY capacity DESC
        """,
        "chart": "capacity",
    },
    {
        "id": 5,
        "difficulty": "Beginner",
        "title": "Team win count",
        "question": "Count how many matches each team has won.",
        "sql": """
            SELECT t.team_name, COUNT(m.match_id) AS wins
            FROM matches m
            JOIN teams t ON m.winner_id = t.team_id
            GROUP BY t.team_name
            ORDER BY wins DESC
        """,
        "chart": "wins",
    },
    {
        "id": 6,
        "difficulty": "Beginner",
        "title": "Players by playing role",
        "question": "Count the number of players for each playing role.",
        "sql": """
            SELECT playing_role, COUNT(*) AS player_count
            FROM players
            GROUP BY playing_role
            ORDER BY player_count DESC
        """,
        "chart": "player_count",
    },
    {
        "id": 7,
        "difficulty": "Beginner",
        "title": "Highest individual scores",
        "question": "Find the highest individual score recorded by each player in any single match.",
        "sql": """
            SELECT p.full_name, MAX(perf.runs_scored) AS highest_score
            FROM performances perf
            JOIN players p ON perf.player_id = p.player_id
            GROUP BY p.full_name
            ORDER BY highest_score DESC
            LIMIT 15
        """,
        "chart": "highest_score",
    },
    {
        "id": 8,
        "difficulty": "Beginner",
        "title": "Series started in 2024",
        "question": "List all series along with their match type and number of matches.",
        "sql": """
            SELECT series_name, match_type, host_country, start_date, total_matches
            FROM series
            ORDER BY start_date DESC
        """,
        "chart": None,
    },
    {
        "id": 9,
        "difficulty": "Intermediate",
        "title": "All-rounders with 1000+ runs and 50+ wickets",
        "question": "Find all-rounders who have scored 1000+ runs AND taken 50+ wickets in the same format.",
        "sql": """
            SELECT p.full_name, ps.format, ps.runs, ps.wickets
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE p.playing_role = 'All-rounder' AND ps.runs > 1000 AND ps.wickets > 50
            ORDER BY ps.runs DESC
        """,
        "chart": "runs",
    },
    {
        "id": 10,
        "difficulty": "Intermediate",
        "title": "Last 5 completed matches - full detail",
        "question": "Show the last 5 completed matches with team names, winner, and margin of victory.",
        "sql": """
            SELECT m.match_date, s.series_name, t1.team_name AS team1, t2.team_name AS team2,
                   w.team_name AS winner, m.victory_type, m.win_margin
            FROM matches m
            JOIN series s ON m.series_id = s.series_id
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            LEFT JOIN teams w ON m.winner_id = w.team_id
            WHERE m.status = 'Completed'
            ORDER BY m.match_date DESC
            LIMIT 5
        """,
        "chart": None,
    },
    {
        "id": 11,
        "difficulty": "Intermediate",
        "title": "Player performance across formats",
        "question": "For players with stats in multiple formats, compare their total runs across formats.",
        "sql": """
            SELECT p.full_name,
                   SUM(CASE WHEN ps.format = 'Test' THEN ps.runs ELSE 0 END) AS test_runs,
                   SUM(CASE WHEN ps.format = 'ODI' THEN ps.runs ELSE 0 END) AS odi_runs,
                   SUM(CASE WHEN ps.format = 'T20I' THEN ps.runs ELSE 0 END) AS t20i_runs
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            GROUP BY p.full_name
            ORDER BY (test_runs + odi_runs + t20i_runs) DESC
            LIMIT 15
        """,
        "chart": None,
    },
    {
        "id": 12,
        "difficulty": "Intermediate",
        "title": "Home vs away wins per team",
        "question": "For each team, compare wins at venues in their own country vs away venues.",
        "sql": """
            SELECT t.team_name,
                   SUM(CASE WHEN v.country = t.country THEN 1 ELSE 0 END) AS home_wins,
                   SUM(CASE WHEN v.country != t.country THEN 1 ELSE 0 END) AS away_wins
            FROM matches m
            JOIN teams t ON m.winner_id = t.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            GROUP BY t.team_name
            ORDER BY home_wins DESC
        """,
        "chart": None,
    },
    {
        "id": 13,
        "difficulty": "Intermediate",
        "title": "Batting partnerships (same-innings pairs)",
        "question": "Find the highest combined runs by any two players batting in the same match innings.",
        "sql": """
            SELECT m.match_id, m.match_date,
                   p1.full_name AS player_a, p2.full_name AS player_b,
                   (perf1.runs_scored + perf2.runs_scored) AS combined_runs
            FROM performances perf1
            JOIN performances perf2
              ON perf1.match_id = perf2.match_id
             AND perf1.team_id = perf2.team_id
             AND perf1.player_id < perf2.player_id
            JOIN matches m ON perf1.match_id = m.match_id
            JOIN players p1 ON perf1.player_id = p1.player_id
            JOIN players p2 ON perf2.player_id = p2.player_id
            ORDER BY combined_runs DESC
            LIMIT 10
        """,
        "chart": "combined_runs",
    },
    {
        "id": 14,
        "difficulty": "Intermediate",
        "title": "Bowling performance at each venue",
        "question": "Calculate average economy rate for bowlers with 4+ overs bowled, grouped by venue.",
        "sql": """
            SELECT v.venue_name, ROUND(AVG(perf.runs_conceded / NULLIF(perf.overs_bowled,0)), 2) AS avg_economy
            FROM performances perf
            JOIN matches m ON perf.match_id = m.match_id
            JOIN venues v ON m.venue_id = v.venue_id
            WHERE perf.overs_bowled >= 4
            GROUP BY v.venue_name
            ORDER BY avg_economy ASC
        """,
        "chart": "avg_economy",
    },
    {
        "id": 15,
        "difficulty": "Intermediate",
        "title": "Toss impact on match outcome",
        "question": "Calculate how often the toss-winning team also won the match.",
        "sql": """
            SELECT COUNT(*) AS total_matches,
                   SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) AS toss_and_match_won,
                   ROUND(100.0 * SUM(CASE WHEN toss_winner_id = winner_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_pct
            FROM matches
            WHERE winner_id IS NOT NULL
        """,
        "chart": None,
    },
    {
        "id": 16,
        "difficulty": "Intermediate",
        "title": "Most economical bowlers (ODI, min 10 matches)",
        "question": "Find the most economical bowlers in ODIs with at least 10 matches played.",
        "sql": """
            SELECT p.full_name, ps.matches, ps.economy_rate, ps.wickets
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE ps.format = 'ODI' AND ps.matches >= 10 AND ps.wickets > 0
            ORDER BY ps.economy_rate ASC
            LIMIT 10
        """,
        "chart": "economy_rate",
    },
    {
        "id": 17,
        "difficulty": "Advanced",
        "title": "Consistent batsmen since 2023 (StdDev of runs)",
        "question": "Find batsmen with more than 5 innings since 2023, ranked by consistency (lowest std-dev of runs, min average 20).",
        "sql": """
            SELECT p.full_name,
                   COUNT(perf.performance_id) AS innings_played,
                   ROUND(AVG(perf.runs_scored), 2) AS avg_runs,
                   ROUND(
                     SQRT(AVG(perf.runs_scored * perf.runs_scored) - AVG(perf.runs_scored) * AVG(perf.runs_scored))
                   , 2) AS run_stddev
            FROM performances perf
            JOIN players p ON perf.player_id = p.player_id
            JOIN matches m ON perf.match_id = m.match_id
            WHERE m.match_date >= '2023-01-01'
            GROUP BY p.full_name
            HAVING COUNT(perf.performance_id) > 5 AND AVG(perf.runs_scored) >= 20
            ORDER BY run_stddev ASC
            LIMIT 15
        """,
        "chart": "run_stddev",
    },
    {
        "id": 18,
        "difficulty": "Advanced",
        "title": "Player format comparison (Test vs ODI vs T20I averages)",
        "question": "For players with stats in all three formats, compare batting average across formats.",
        "sql": """
            SELECT p.full_name,
                   MAX(CASE WHEN ps.format = 'Test' THEN ps.batting_average END) AS test_avg,
                   MAX(CASE WHEN ps.format = 'ODI' THEN ps.batting_average END) AS odi_avg,
                   MAX(CASE WHEN ps.format = 'T20I' THEN ps.batting_average END) AS t20i_avg
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            GROUP BY p.full_name
            HAVING COUNT(DISTINCT ps.format) = 3
            ORDER BY p.full_name
        """,
        "chart": None,
    },
    {
        "id": 19,
        "difficulty": "Advanced",
        "title": "Player performance ranking (weighted score)",
        "question": "Rank players using a composite score = (batting_avg*0.5)+(strike_rate*0.3)+(bowling_wickets*0.2), ODI only.",
        "sql": """
            SELECT p.full_name,
                   ps.batting_average, ps.strike_rate, ps.wickets,
                   ROUND((ps.batting_average * 0.5) + (ps.strike_rate * 0.3) + (ps.wickets * 0.2), 2) AS composite_score
            FROM player_stats ps
            JOIN players p ON ps.player_id = p.player_id
            WHERE ps.format = 'ODI'
            ORDER BY composite_score DESC
            LIMIT 15
        """,
        "chart": "composite_score",
    },
    {
        "id": 20,
        "difficulty": "Advanced",
        "title": "Head-to-head team record",
        "question": "For each pair of teams that have played each other, show total matches and wins per team.",
        "sql": """
            SELECT t1.team_name AS team_a, t2.team_name AS team_b,
                   COUNT(*) AS matches_played,
                   SUM(CASE WHEN m.winner_id = t1.team_id THEN 1 ELSE 0 END) AS team_a_wins,
                   SUM(CASE WHEN m.winner_id = t2.team_id THEN 1 ELSE 0 END) AS team_b_wins
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            WHERE m.team1_id < m.team2_id
            GROUP BY t1.team_name, t2.team_name
            ORDER BY matches_played DESC
        """,
        "chart": None,
    },
    {
        "id": 21,
        "difficulty": "Advanced",
        "title": "Recent player form (last 10 innings trend)",
        "question": "For each player, show their average runs in their most recent 10 innings vs career average.",
        "sql": """
            SELECT p.full_name,
                   ROUND(AVG(perf.runs_scored), 2) AS recent_10_avg,
                   ps.batting_average AS career_avg
            FROM performances perf
            JOIN players p ON perf.player_id = p.player_id
            JOIN matches m ON perf.match_id = m.match_id
            LEFT JOIN player_stats ps ON ps.player_id = p.player_id AND ps.format = m.match_type
            GROUP BY p.full_name, ps.batting_average
            ORDER BY recent_10_avg DESC
            LIMIT 15
        """,
        "chart": None,
    },
    {
        "id": 22,
        "difficulty": "Advanced",
        "title": "Successful run chases",
        "question": "Count how many matches were won batting second (chasing) per team.",
        "sql": """
            SELECT t.team_name, COUNT(*) AS successful_chases
            FROM matches m
            JOIN teams t ON m.winner_id = t.team_id
            WHERE m.victory_type = 'wickets'
            GROUP BY t.team_name
            ORDER BY successful_chases DESC
        """,
        "chart": "successful_chases",
    },
    {
        "id": 23,
        "difficulty": "Advanced",
        "title": "Yearly performance trend for top players",
        "question": "Show total runs scored per year for the top 5 all-time run scorers.",
        "sql": """
            SELECT p.full_name, CAST(strftime('%Y', m.match_date) AS INTEGER) AS year,
                   SUM(perf.runs_scored) AS runs_in_year
            FROM performances perf
            JOIN players p ON perf.player_id = p.player_id
            JOIN matches m ON perf.match_id = m.match_id
            WHERE p.player_id IN (
                SELECT player_id FROM (
                    SELECT player_id, SUM(runs_scored) AS total_runs
                    FROM performances GROUP BY player_id ORDER BY total_runs DESC LIMIT 5
                )
            )
            GROUP BY p.full_name, year
            ORDER BY p.full_name, year
        """,
        "chart": "runs_in_year",
    },
    {
        "id": 24,
        "difficulty": "Advanced",
        "title": "Team win percentage in close matches",
        "question": "Find each team's win percentage in low-margin matches (margin under 20 runs or under 3 wickets).",
        "sql": """
            SELECT t.team_name,
                   COUNT(*) AS close_matches,
                   SUM(CASE WHEN m.winner_id = t.team_id THEN 1 ELSE 0 END) AS close_wins,
                   ROUND(100.0 * SUM(CASE WHEN m.winner_id = t.team_id THEN 1 ELSE 0 END) / COUNT(*), 2) AS win_pct
            FROM matches m
            JOIN teams t ON t.team_id IN (m.team1_id, m.team2_id)
            WHERE (m.victory_type = 'runs' AND CAST(REPLACE(m.win_margin, ' runs', '') AS INTEGER) < 20)
               OR (m.victory_type = 'wickets' AND CAST(REPLACE(m.win_margin, ' wickets', '') AS INTEGER) < 3)
            GROUP BY t.team_name
            ORDER BY win_pct DESC
        """,
        "chart": "win_pct",
    },
    {
        "id": 25,
        "difficulty": "Advanced",
        "title": "Comprehensive player performance summary",
        "question": "Build a composite player summary combining batting, bowling, and fielding contribution, ranked overall.",
        "sql": """
            SELECT p.full_name, p.playing_role, p.country,
                   COALESCE(SUM(perf.runs_scored), 0) AS total_runs,
                   COALESCE(SUM(perf.wickets_taken), 0) AS total_wickets,
                   COALESCE(SUM(perf.catches_taken), 0) AS total_catches,
                   COALESCE(SUM(perf.runs_scored), 0)
                     + COALESCE(SUM(perf.wickets_taken), 0) * 20
                     + COALESCE(SUM(perf.catches_taken), 0) * 10 AS impact_score
            FROM players p
            LEFT JOIN performances perf ON perf.player_id = p.player_id
            GROUP BY p.full_name, p.playing_role, p.country
            ORDER BY impact_score DESC
            LIMIT 20
        """,
        "chart": "impact_score",
    },
]


def get_query(query_id: int) -> dict:
    for q in QUERIES:
        if q["id"] == query_id:
            return q
    raise ValueError(f"No query with id {query_id}")
