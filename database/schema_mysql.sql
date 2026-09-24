-- =====================================================================
-- Cricbuzz LiveStats — MySQL-compatible schema reference
-- The app itself creates this schema automatically via SQLAlchemy
-- (see database/models.py) for whichever DB_TYPE you configure.
-- This file is provided for reference / manual MySQL setup and mirrors
-- that schema, plus example views used by the analytics layer.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS cricbuzz_livestats CHARACTER SET utf8mb4;
USE cricbuzz_livestats;

CREATE TABLE teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    team_name VARCHAR(100) NOT NULL UNIQUE,
    country VARCHAR(100) NOT NULL,
    team_type VARCHAR(30) DEFAULT 'International',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE venues (
    venue_id INT AUTO_INCREMENT PRIMARY KEY,
    venue_name VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    capacity INT,
    UNIQUE KEY uq_venue_city (venue_name, city)
);

CREATE TABLE series (
    series_id INT AUTO_INCREMENT PRIMARY KEY,
    series_name VARCHAR(200) NOT NULL,
    host_country VARCHAR(100),
    match_type VARCHAR(20),
    start_date DATE,
    end_date DATE,
    total_matches INT DEFAULT 0
);

CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(150) NOT NULL,
    playing_role VARCHAR(30),
    batting_style VARCHAR(30),
    bowling_style VARCHAR(50),
    country VARCHAR(100),
    date_of_birth DATE,
    team_id INT,
    is_active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    INDEX ix_players_role (playing_role)
);

CREATE TABLE player_stats (
    stat_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    format VARCHAR(10) NOT NULL,
    matches INT DEFAULT 0,
    innings_batted INT DEFAULT 0,
    runs INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    highest_score INT DEFAULT 0,
    batting_average FLOAT DEFAULT 0,
    strike_rate FLOAT DEFAULT 0,
    centuries INT DEFAULT 0,
    half_centuries INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    innings_bowled INT DEFAULT 0,
    balls_bowled INT DEFAULT 0,
    runs_conceded INT DEFAULT 0,
    wickets INT DEFAULT 0,
    best_bowling VARCHAR(20),
    bowling_average FLOAT DEFAULT 0,
    economy_rate FLOAT DEFAULT 0,
    five_wicket_hauls INT DEFAULT 0,
    catches INT DEFAULT 0,
    stumpings INT DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    UNIQUE KEY uq_player_format (player_id, format)
);

CREATE TABLE matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    series_id INT,
    team1_id INT,
    team2_id INT,
    venue_id INT,
    match_type VARCHAR(10),
    match_date DATE,
    toss_winner_id INT,
    toss_decision VARCHAR(10),
    winner_id INT,
    win_margin VARCHAR(50),
    victory_type VARCHAR(20),
    player_of_match_id INT,
    status VARCHAR(30) DEFAULT 'Completed',
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id),
    FOREIGN KEY (winner_id) REFERENCES teams(team_id),
    FOREIGN KEY (player_of_match_id) REFERENCES players(player_id),
    INDEX ix_matches_date (match_date)
);

CREATE TABLE innings (
    innings_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    batting_team_id INT,
    innings_number INT,
    total_runs INT DEFAULT 0,
    total_wickets INT DEFAULT 0,
    overs FLOAT DEFAULT 0,
    run_rate FLOAT DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (batting_team_id) REFERENCES teams(team_id)
);

CREATE TABLE performances (
    performance_id INT AUTO_INCREMENT PRIMARY KEY,
    match_id INT NOT NULL,
    player_id INT NOT NULL,
    team_id INT,
    runs_scored INT DEFAULT 0,
    balls_faced INT DEFAULT 0,
    fours INT DEFAULT 0,
    sixes INT DEFAULT 0,
    dismissal_type VARCHAR(30),
    overs_bowled FLOAT DEFAULT 0,
    runs_conceded INT DEFAULT 0,
    wickets_taken INT DEFAULT 0,
    maidens INT DEFAULT 0,
    catches_taken INT DEFAULT 0,
    stumpings_made INT DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    INDEX ix_perf_match_player (match_id, player_id)
);

-- =====================================================================
-- Example analytical views (used conceptually by analytics/sql_queries.py;
-- the app queries the base tables directly for portability, but these
-- views are handy for ad-hoc exploration in a MySQL client).
-- =====================================================================

CREATE OR REPLACE VIEW vw_team_win_counts AS
SELECT t.team_name, COUNT(m.match_id) AS wins
FROM matches m
JOIN teams t ON m.winner_id = t.team_id
GROUP BY t.team_name;

CREATE OR REPLACE VIEW vw_top_run_scorers AS
SELECT p.full_name, p.country, ps.format, ps.runs, ps.batting_average, ps.strike_rate
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
ORDER BY ps.runs DESC;

CREATE OR REPLACE VIEW vw_top_wicket_takers AS
SELECT p.full_name, p.country, ps.format, ps.wickets, ps.bowling_average, ps.economy_rate
FROM player_stats ps
JOIN players p ON ps.player_id = p.player_id
WHERE ps.wickets > 0
ORDER BY ps.wickets DESC;
