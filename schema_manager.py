import sqlite3

def infer_type(series):
    s = series.dropna()

    if s.empty:
        return "TEXT"

    try:
        s.astype(int)
        return "INTEGER"
    except:
        pass

    try:
        s.astype(float)
        return "REAL"
    except:
        return "TEXT"

def drop_table(table_name, db_path="app.db"):
    conn = sqlite3.connect(db_path)
    conn.execute(f'DROP TABLE IF EXISTS "{table_name}"')
    conn.commit()
    conn.close()

def create_table_from_df(df, table_name, db_path="app.db"):
    conn = sqlite3.connect(db_path)
    cols = [f'"{col}" {infer_type(df[col])}' for col in df.columns]
    sql = f'CREATE TABLE IF NOT EXISTS "{table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {", ".join(cols)})'
    conn.execute(sql)
    conn.commit()
    conn.close()

def insert_df(df, table_name, db_path="app.db"):
    conn = sqlite3.connect(db_path)
    col_names = ", ".join([f'"{c}"' for c in df.columns])
    placeholders = ", ".join(["?" for _ in df.columns])
    sql = f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})'
    for row in df.itertuples(index=False, name=None):
        conn.execute(sql, row)
    conn.commit()
    conn.close()

def get_schema(table_name, db_path="app.db"):
    conn = sqlite3.connect(db_path)
    rows = conn.execute(f'PRAGMA table_info("{table_name}")').fetchall()
    conn.close()
    return rows

def list_tables(db_path="app.db"):
    conn = sqlite3.connect(db_path)
    rows = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    conn.close()
    return [row[0] for row in rows]

def get_columns(table_name, db_path="app.db"):
    return [row[1] for row in get_schema(table_name, db_path)]