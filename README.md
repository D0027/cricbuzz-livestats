# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

A production-style sports analytics platform: live cricket data, a normalized SQL database,
25 hand-built SQL analytics questions, full CRUD management, and a premium Streamlit dashboard —
all runnable locally in two commands.

The app works **fully offline out of the box** (seeded sample data covers every page). Live match
data activates automatically once you add a free Cricbuzz API key.

---

## 1. Quick Start

```bash
pip install -r requirements.txt
streamlit run main.py
```

That's it — the database is created and seeded automatically on first run (SQLite file at
`data/cricbuzz.db`). Open the URL Streamlit prints (usually http://localhost:8501).

---

## 2. Project Structure

```
cricbuzz_livestats/
├── main.py                  # Entry point: page config, sidebar nav, routing
├── api/
│   └── cricbuzz_client.py   # Cricbuzz REST API wrapper (retries, caching, timeouts)
├── database/
│   ├── models.py            # SQLAlchemy ORM models (8 tables, FKs, indexes)
│   ├── connection.py        # Engine/session management, raw query runner
│   ├── seed_data.py         # Realistic sample data generator
│   └── schema_mysql.sql     # Reference DDL + views for manual MySQL setup
├── models/
│   └── schemas.py           # Pydantic validation schemas for CRUD forms
├── analytics/
│   └── sql_queries.py       # All 25 SQL analytics questions + metadata
├── crud/
│   └── operations.py        # Generic CRUD functions for all 5 entities
├── utils/
│   ├── config.py            # Typed settings loaded from .env
│   ├── logger.py            # Rotating file + console logging
│   ├── ui.py                 # Shared CSS/theme, KPI cards, headers, footer
│   └── exporters.py         # CSV / Excel export helpers
├── pages/
│   ├── home.py               # Landing dashboard
│   ├── live_matches.py       # Live / upcoming / completed matches
│   ├── player_stats.py       # Player statistics with filters + charts
│   ├── sql_analytics.py      # The 25-query analytics page
│   ├── comparisons.py        # Player & team head-to-head comparisons
│   ├── crud.py                # Create/Read/Update/Delete UI
│   ├── settings_page.py      # Configuration reference
│   └── about.py               # About / credits
├── tests/                    # pytest suite (DB, CRUD, all 25 queries, API client)
├── logs/                     # Rotating app.log (created at runtime)
├── data/                     # SQLite database file (created at runtime)
├── .streamlit/config.toml    # Dark theme configuration
├── .env.example               # Copy to .env and fill in your values
└── requirements.txt
```

---

## 3. Configuration

Copy `.env.example` to `.env` and edit as needed:

```bash
cp .env.example .env
```

### Cricbuzz API (optional — only needed for the Live Matches page)
1. Sign up at [RapidAPI – Cricbuzz Cricket](https://rapidapi.com/cricbuzz-cricbuzz-default/api/cricbuzz-cricket).
2. Subscribe to the free tier and copy your API key.
3. Set `CRICBUZZ_API_KEY` in `.env`.

Without a key, every other page (Home, Player Statistics, SQL Analytics, Comparisons, CRUD)
works normally against the seeded database — only the live/upcoming tabs on the Live Matches
page will show a setup notice instead of live data.

### Database
`DB_TYPE` defaults to `sqlite` (zero setup). To use MySQL or PostgreSQL instead:

```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=cricbuzz_livestats
DB_USER=root
DB_PASSWORD=yourpassword
```

Run `database/schema_mysql.sql` against your MySQL instance first (or just let the app's
`init_db()` create the tables automatically via SQLAlchemy — both produce the same schema).
For PostgreSQL, set `DB_TYPE=postgresql`; the same SQLAlchemy models apply.

---

## 4. Database Design

8 normalized tables: `teams`, `venues`, `series`, `players`, `player_stats`, `matches`,
`innings`, `performances` — with primary/foreign keys, unique constraints, and indexes on the
columns queried most often (player role, match date, match/player lookups). See
`database/models.py` for the full schema and `database/schema_mysql.sql` for a plain-SQL
version with example views.

---

## 5. SQL Analytics Page

All 25 questions (8 Beginner, 8 Intermediate, 9 Advanced) live in `analytics/sql_queries.py`.
Each one ships with: the question, the raw SQL (syntax-highlighted), a Run button, execution
time, a results table, an auto-generated chart where relevant, and a CSV download. Run
`pytest tests/test_sql_queries.py -v` to confirm all 25 execute cleanly against the seeded data.

---

## 6. Testing

```bash
pytest -v
```

Covers: schema creation, seed data integrity, all CRUD operations, all 25 SQL queries executing
without error, and API client behavior when no key is configured.

---

## 7. Deployment

- **Streamlit Community Cloud**: push this repo to GitHub, point Streamlit Cloud at `main.py`,
  and add your `.env` values as Secrets (same key names).
- **Docker / VM**: `pip install -r requirements.txt && streamlit run main.py --server.port 8501 --server.address 0.0.0.0`.
- For MySQL/PostgreSQL in production, provision the database first and set the `DB_*` env vars —
  the app will create tables on first boot if they don't exist.

---

## 8. Troubleshooting / FAQ

**Q: Live Matches page shows "API key not configured."**
A: Expected until you add `CRICBUZZ_API_KEY` to `.env`. Every other page works without it.

**Q: I get a `sqlite3.OperationalError: unable to open database file`.**
A: Make sure the `data/` folder is writable; the app creates it automatically but some hosting
environments mount the working directory read-only — set `DB_PATH` to a writable location.

**Q: How do I reset the sample data?**
A: Delete `data/cricbuzz.db` and restart the app — it will reseed automatically.

**Q: Charts look empty on a query.**
A: Not every query has a natural chart (e.g. wide comparison tables) — those intentionally show
a table only.

---

## 9. Credits

Built by deepak ([GitHub: D0027](https://github.com/D0027)). Data via the Cricbuzz Cricket API
(RapidAPI). Tech stack: Python, Streamlit, SQLAlchemy, Pandas, NumPy, Plotly, Pydantic.
