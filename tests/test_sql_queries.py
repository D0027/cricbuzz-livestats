import pytest

from database.connection import init_db, run_raw_query
from database.seed_data import seed
from analytics.sql_queries import QUERIES

init_db()
seed()


def test_all_25_queries_present():
    assert len(QUERIES) == 25
    ids = sorted(q["id"] for q in QUERIES)
    assert ids == list(range(1, 26))


@pytest.mark.parametrize("q", QUERIES, ids=[f"Q{q['id']}" for q in QUERIES])
def test_query_executes_without_error(q):
    columns, rows = run_raw_query(q["sql"])
    assert isinstance(columns, list)
