import sqlite3

def save_to_sqlite(df, table_name, db_path="app.db"):
    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()


def get_schema(table_name, db_path="app.db"):
    conn = sqlite3.connect(db_path)
    rows = conn.execute(f'PRAGMA table_info("{table_name}")').fetchall()
    conn.close()
    return rows