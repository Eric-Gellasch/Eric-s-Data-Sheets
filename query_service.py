import sqlite3
from validator import validate_sql

def run_query(sql, db_path="app.db"):
    ok, message = validate_sql(sql, db_path)
    if not ok:
        raise ValueError(message)

    conn = sqlite3.connect(db_path)
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows