import sqlite3

def run_query(sql, db_path="app.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    conn.close()
    return rows