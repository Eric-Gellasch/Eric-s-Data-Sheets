from csv_ingestor import load_csv
from schema_manager import save_to_sqlite, get_schema
from query_service import run_query

def main():
    df = load_csv("test.csv")
    print("shape:", df.shape)

    save_to_sqlite(df, "test")
    print(get_schema("test"))

    rows = run_query("SELECT * FROM test LIMIT 5")
    print(rows)

if __name__ == "__main__":
    main()