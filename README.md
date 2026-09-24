<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:14532d,50:16a34a,100:4ade80&height=220&section=header&text=Cricbuzz%20LiveStats&fontSize=56&fontColor=ffffff&animation=fadeIn&fontAlignY=38&desc=Real-Time%20Cricket%20Insights%20%26%20SQL-Based%20Analytics&descAlignY=60&descSize=20" width="100%" />

<a href="https://git.io/typing-svg">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=600&size=22&pause=1000&color=16A34A&center=true&vCenter=true&width=750&lines=Live+cricket+data+at+your+fingertips+%F0%9F%8F%8F;25+hand-built+SQL+analytics+questions+%F0%9F%93%8A;Player+%26+team+head-to-head+comparisons+%E2%9A%94%EF%B8%8F;Runs+fully+offline+out+of+the+box+%E2%9A%A1" alt="Typing SVG" />
</a>

<br/><br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)

![Stars](https://img.shields.io/github/stars/D0027/cricbuzz-livestats?style=social)
![Forks](https://img.shields.io/github/forks/D0027/cricbuzz-livestats?style=social)
![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)
![SQL Queries](https://img.shields.io/badge/SQL%20queries-25-16a34a?style=flat-square)
![Tests](https://img.shields.io/badge/tests-pytest-success?style=flat-square)

**A production-style sports analytics platform: live cricket data, a normalized SQL database, 25 hand-built SQL analytics questions, full CRUD management, and a premium Streamlit dashboard, all runnable locally in two commands.**

[🚀 Quick Start](#-quick-start) · [🐛 Report Bug](https://github.com/D0027/cricbuzz-livestats/issues) · [✨ Request Feature](https://github.com/D0027/cricbuzz-livestats/issues)

</div>

---

## 📑 Table of Contents

- [✨ Features](#-features)
- [📸 Screenshots](#-screenshots)
- [🏗️ Architecture](#️-architecture)
- [🧰 Tech Stack](#-tech-stack)
- [🚀 Quick Start](#-quick-start)
- [⚙️ Configuration](#️-configuration)
- [📁 Project Structure](#-project-structure)
- [🗄️ Database Design](#️-database-design)
- [📊 SQL Analytics](#-sql-analytics)
- [🧪 Testing](#-testing)
- [🌐 Deployment](#-deployment)
- [❓ FAQ](#-faq)
- [👨‍💻 Author](#-author)

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🏏 Live Matches
Live, upcoming, and completed matches, powered by the Cricbuzz API (with retries, caching, and timeouts).

### 📊 25 SQL Analytics Questions
8 Beginner, 8 Intermediate, and 9 Advanced queries. Each has syntax-highlighted SQL, a Run button, execution time, results, an auto chart, and CSV download.

### ⚔️ Head-to-Head Comparisons
Compare players and teams side by side.

</td>
<td width="50%">

### 👤 Player Statistics
Filter by role, explore stats, and see interactive charts.

### 🛠️ Full CRUD Management
Create, read, update, and delete records for 5 entities, with validated forms.

### 📥 Export Anywhere
Download results as **CSV** or **Excel**.

</td>
</tr>
<tr>
<td colspan="2" align="center">

### ⚡ Works Fully Offline
The database is created and **seeded automatically** on first run. Every page works out of the box, and live data switches on when you add a free Cricbuzz API key.

</td>
</tr>
</table>

---

## 📸 Screenshots

<!-- Save your screenshots in the assets/ folder with these names, or edit the paths below -->

<table>
<tr>
<td align="center" width="50%">
<img src="assets/home.png" width="100%" /><br/>
<b>🏠 Home Dashboard</b>
</td>
<td align="center" width="50%">
<img src="assets/live-matches.png" width="100%" /><br/>
<b>🏏 Live Matches</b>
</td>
</tr>
<tr>
<td align="center">
<img src="assets/player-stats.png" width="100%" /><br/>
<b>👤 Player Statistics</b>
</td>
<td align="center">
<img src="assets/sql-analytics.png" width="100%" /><br/>
<b>📊 SQL Analytics</b>
</td>
</tr>
<tr>
<td align="center">
<img src="assets/comparisons.png" width="100%" /><br/>
<b>⚔️ Comparisons</b>
</td>
<td align="center">
<img src="assets/crud.png" width="100%" /><br/>
<b>🛠️ CRUD Management</b>
</td>
</tr>
</table>

---

## 🏗️ Architecture

```mermaid
flowchart LR
    U([👤 User]) --> M[🖥️ Streamlit<br/>main.py]
    M --> P[📄 app_pages]
    P --> A[🌐 API Client]
    P --> Q[📊 SQL Analytics]
    P --> C[🛠️ CRUD]
    A -->|REST| R[(🏏 Cricbuzz API<br/>via RapidAPI)]
    Q --> D[🗄️ SQLAlchemy]
    C --> D
    D --> S[(💾 SQLite / MySQL / PostgreSQL)]
```

---

## 🧰 Tech Stack

| Layer | Technology |
|---|---|
| 🖥️ Frontend | Streamlit (custom dark theme) |
| 🐍 Language | Python |
| 🗄️ ORM | SQLAlchemy |
| 💾 Database | SQLite (default) · MySQL · PostgreSQL |
| 📈 Data & Charts | Pandas · NumPy · Plotly |
| ✅ Validation | Pydantic |
| 🌐 Data Source | Cricbuzz Cricket API (RapidAPI) |
| 🧪 Testing | pytest |

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/D0027/cricbuzz-livestats.git
cd cricbuzz-livestats

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run main.py
```

🌍 Open the URL Streamlit prints (usually **http://localhost:8501**).

> 💡 That's it. The database is created and seeded automatically on first run (SQLite file at `data/cricbuzz.db`).

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and edit as needed:

```bash
cp .env.example .env          # Windows: copy .env.example .env
```

<details open>
<summary><b>🏏 Cricbuzz API (optional, only for the Live Matches page)</b></summary>

1. Sign up at [RapidAPI: Cricbuzz Cricket](https://rapidapi.com/cricbuzz-cricbuzz-default/api/cricbuzz-cricket)
2. Subscribe to the free tier and copy your API key
3. Set it in `.env`:

```env
CRICBUZZ_API_KEY=your_api_key_here
```

Without a key, every other page (Home, Player Statistics, SQL Analytics, Comparisons, CRUD) works normally on the seeded database. Only the live and upcoming tabs show a setup notice.

</details>

<details>
<summary><b>🗄️ Database (SQLite by default, MySQL / PostgreSQL optional)</b></summary>

`DB_TYPE` defaults to `sqlite` (zero setup). To use MySQL:

```env
DB_TYPE=mysql
DB_HOST=localhost
DB_PORT=3306
DB_NAME=cricbuzz_livestats
DB_USER=root
DB_PASSWORD=your_password
```

Run `database/schema_mysql.sql` against your MySQL instance first, or let the app's `init_db()` create the tables via SQLAlchemy (both give the same schema). For PostgreSQL, set `DB_TYPE=postgresql`.

</details>

> ⚠️ Never commit your real `.env` file. Keep secrets out of Git!

---

## 📁 Project Structure

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
│   ├── ui.py                # Shared CSS/theme, KPI cards, headers, footer
│   └── exporters.py         # CSV / Excel export helpers
├── app_pages/
│   ├── home.py              # Landing dashboard
│   ├── live_matches.py      # Live / upcoming / completed matches
│   ├── player_stats.py      # Player statistics with filters + charts
│   ├── sql_analytics.py     # The 25-query analytics page
│   ├── comparisons.py       # Player & team head-to-head comparisons
│   ├── crud.py              # Create/Read/Update/Delete UI
│   ├── settings_page.py     # Configuration reference
│   └── about.py             # About / credits
├── tests/                   # pytest suite (DB, CRUD, all 25 queries, API client)
├── .streamlit/config.toml   # Dark theme configuration
├── .env.example             # Copy to .env and fill in your values
└── requirements.txt
```

---

## 🗄️ Database Design

**8 normalized tables**, with primary/foreign keys, unique constraints, and indexes on the most-queried columns (player role, match date, match/player lookups).

| Table | Purpose |
|---|---|
| 🏟️ `teams` | Cricket teams |
| 📍 `venues` | Grounds and stadiums |
| 🏆 `series` | Tournaments and series |
| 👤 `players` | Player profiles |
| 📈 `player_stats` | Career statistics |
| 🏏 `matches` | Match records |
| 🎯 `innings` | Innings details |
| ⭐ `performances` | Per-match player performances |

See `database/models.py` for the full schema and `database/schema_mysql.sql` for plain SQL with example views.

---

## 📊 SQL Analytics

**25 questions** across three difficulty levels:

| Level | Questions | Focus |
|---|:---:|---|
| 🟢 Beginner | 8 | Filters, sorting, basic aggregation |
| 🟡 Intermediate | 8 | Joins, grouping, subqueries |
| 🔴 Advanced | 9 | Complex analytics and window-style logic |

Every question ships with the **question, raw SQL (highlighted), a Run button, execution time, results table, an auto-generated chart where relevant, and a CSV download**.

---

## 🧪 Testing

```bash
pytest -v
```

Covers schema creation, seed data integrity, all CRUD operations, all 25 SQL queries running without error, and API client behavior when no key is configured.

```bash
# Just the SQL analytics tests
pytest tests/test_sql_queries.py -v
```

---

## 🌐 Deployment

- ☁️ **Streamlit Community Cloud:** push this repo to GitHub, point Streamlit Cloud at `main.py`, and add your `.env` values as **Secrets** (same key names).
- 🐳 **Docker / VM:**
```bash
  pip install -r requirements.txt && streamlit run main.py --server.port 8501 --server.address 0.0.0.0
```
- 🗄️ **MySQL / PostgreSQL in production:** provision the database first and set the `DB_*` env vars. The app creates tables on first boot if they don't exist.

---

## ❓ FAQ

<details>
<summary><b>Live Matches page shows "API key not configured"</b></summary>

Expected until you add `CRICBUZZ_API_KEY` to `.env`. Every other page works without it.

</details>

<details>
<summary><b>I get <code>sqlite3.OperationalError: unable to open database file</code></b></summary>

Make sure the `data/` folder is writable. Some hosting environments mount the working directory read-only, so set `DB_PATH` to a writable location.

</details>

<details>
<summary><b>How do I reset the sample data?</b></summary>

Delete `data/cricbuzz.db` and restart the app. It reseeds automatically.

</details>

<details>
<summary><b>Charts look empty on a query</b></summary>

Not every query has a natural chart (like wide comparison tables). Those intentionally show a table only.

</details>

---

## 🤝 Contributing

Contributions are welcome! Fork the repo, create a branch, and open a Pull Request 🎉

---

## 👨‍💻 Author

<div align="center">

**Deepak Yadav**

[![GitHub](https://img.shields.io/badge/GitHub-D0027-181717?style=for-the-badge&logo=github)](https://github.com/D0027)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-deepakyadav027-0A66C2?style=for-the-badge&logo=linkedin)](https://linkedin.com/in/deepakyadav027)
[![Portfolio](https://img.shields.io/badge/Portfolio-d0027.github.io-16A34A?style=for-the-badge&logo=googlechrome&logoColor=white)](https://d0027.github.io)

Data via the Cricbuzz Cricket API (RapidAPI).

⭐ **If you like this project, drop a star, it really helps!** ⭐

**Built with Python · Streamlit · SQLAlchemy · Pandas · Plotly · Pydantic**

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:4ade80,50:16a34a,100:14532d&height=120&section=footer" width="100%" />

</div>
