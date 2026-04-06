from validator import validate_sql

def test_reject_drop():
    ok, _ = validate_sql("DROP TABLE test")
    assert not ok