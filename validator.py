import re
from schema_manager import list_tables, get_columns

def validate_sql(sql, db_path="app.db"):
    q = sql.strip().rstrip(";")
    q_lower = q.lower()

    if not q_lower.startswith("select"):
        return False, "Only SELECT queries are allowed"

    blocked = ["insert", "update", "delete", "drop", "alter", "create", "pragma", "attach"]
    if any(word in q_lower for word in blocked):
        return False, "Query contains blocked SQL"

    table_match = re.search(r'from\s+"?([a-zA-Z_][a-zA-Z0-9_]*)"?', q, re.IGNORECASE)
    if not table_match:
        return False, "Missing table name"

    table_name = table_match.group(1)
    if table_name not in list_tables(db_path):
        return False, f"Unknown table: {table_name}"

    valid_columns = get_columns(table_name, db_path)

    quoted_cols = re.findall(r'"([a-zA-Z_][a-zA-Z0-9_]*)"', q)
    for col in quoted_cols:
        if col != table_name and col not in valid_columns:
            return False, f"Unknown column: {col}"

    return True, "Valid query"