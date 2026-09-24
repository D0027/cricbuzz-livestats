from database.connection import init_db, get_session, run_raw_query
from database.models import Team, Player
from database.seed_data import seed


def test_init_db_creates_tables():
    init_db()
    with get_session() as s:
        assert s.query(Team).count() >= 0


def test_seed_populates_data():
    seed()
    with get_session() as s:
        assert s.query(Team).count() > 0
        assert s.query(Player).count() > 0


def test_raw_query_execution():
    seed()
    columns, rows = run_raw_query("SELECT COUNT(*) as cnt FROM teams")
    assert columns == ["cnt"]
    assert rows[0][0] > 0
