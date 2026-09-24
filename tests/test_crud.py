from database.connection import init_db
from database.seed_data import seed
from crud.operations import create_record, update_record, delete_record, list_records

init_db()
seed()


def test_create_and_delete_team():
    ok, msg = create_record("Teams", {"team_name": "Test XI", "country": "Testland", "team_type": "International"})
    assert ok, msg

    df = list_records("Teams")
    row = df[df["team_name"] == "Test XI"].iloc[0]
    team_id = int(row["team_id"])

    ok, msg = update_record("Teams", team_id, {"country": "Testlandia"})
    assert ok, msg

    ok, msg = delete_record("Teams", team_id)
    assert ok, msg


def test_delete_nonexistent_record_fails_gracefully():
    ok, msg = delete_record("Teams", 999999)
    assert not ok
