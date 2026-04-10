import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def question_to_sql(question, table_name, schema):
    schema_text = ", ".join([f'{row[1]} ({row[2]})' for row in schema if row[1] != "id"])

    prompt = f"""
Convert the user's question into exactly one SQLite SELECT query.

Rules:
- Use only table "{table_name}"
- Use only this schema: {schema_text}
- Return SQL only
- Use double quotes around table and column names
- Use LIMIT 100 for non-aggregate queries
- For "how many" questions, use COUNT(*)
- For text matching, use LOWER("column") LIKE '%value%'
- For unique values, use DISTINCT
- Do not use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, PRAGMA, or ATTACH
- Do not invent columns
- Do not use joins

Examples:
SELECT COUNT(*) FROM "{table_name}" WHERE LOWER("name") LIKE '%a%'
SELECT DISTINCT "color" FROM "{table_name}" WHERE LOWER("color") LIKE '%red%'
SELECT * FROM "{table_name}" WHERE LOWER("city") LIKE '%york%' LIMIT 100

User question: {question}
"""
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    return response.output_text.strip()