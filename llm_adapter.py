import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def question_to_sql(question, table_name, columns):
    prompt = f"""
Convert the user's question into one SQLite SELECT query.

Rules:
- Use only table "{table_name}"
- Use only these columns: {", ".join(columns)}
  SELECT * FROM "{table_name}" LIMIT 5
  SELECT "Column" FROM "{table_name}"
  SELECT * FROM "{table_name}" WHERE "Column" = 'value'
  SELECT * FROM "{table_name}" WHERE "Column" LIKE '%value%'

User question: {question}
"""
    response = client.responses.create(
        model="gpt-5.4-mini",
        input=prompt
    )
    return response.output_text.strip()