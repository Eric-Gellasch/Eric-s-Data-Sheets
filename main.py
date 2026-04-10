from csv_ingestor import load_csv
from schema_manager import drop_table, create_table_from_df, insert_df, get_schema
from llm_adapter import question_to_sql
from query_service import run_query

def main():
    table_name = "test"

    df = load_csv("test.csv")

    drop_table(table_name)
    create_table_from_df(df, table_name)
    insert_df(df, table_name)

    schema = get_schema(table_name)
    print("schema:", [(row[1], row[2]) for row in schema])

    while True:
        question = input("Ask a question or type 'exit': ").strip()
        if question.lower() == "exit":
            break

        try:
            sql = question_to_sql(question, table_name, schema)
            print("SQL:", sql)
            rows = run_query(sql)

            if not rows:
                print("No results.")
            else:
                for row in rows:
                    print(row)
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()