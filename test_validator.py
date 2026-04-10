import sqlite3
from validator import validate_sql

TEST_DB = "test_app.db"

def setup_test_db():
    conn = sqlite3.connect(TEST_DB)
    conn.execute('DROP TABLE IF EXISTS "test"')
    conn.execute('CREATE TABLE "test" ("name" TEXT, "email" TEXT)')
    conn.execute('INSERT INTO "test" ("name", "email") VALUES (?, ?)', ("Alice", "alice@example.com"))
    conn.commit()
    conn.close()

def test_valid_select():
    setup_test_db()
    ok, message = validate_sql('SELECT "name" FROM "test"', db_path=TEST_DB)
    assert ok is True
    assert message == "Valid query"

def test_blocks_non_select():
    setup_test_db()
    ok, message = validate_sql('DROP TABLE "test"', db_path=TEST_DB)
    assert ok is False
    assert message == "Only SELECT queries are allowed"

def test_unknown_table():
    setup_test_db()
    ok, message = validate_sql('SELECT "name" FROM "missing_table"', db_path=TEST_DB)
    assert ok is False
    assert "Unknown table" in message

def test_unknown_column():
    setup_test_db()
    ok, message = validate_sql('SELECT "age" FROM "test"', db_path=TEST_DB)
    assert ok is False
    assert "Unknown column" in message