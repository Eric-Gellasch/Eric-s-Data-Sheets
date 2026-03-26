import pandas as pd

df = pd.read_csv('test.csv')

print(df.head())

table_name = "my_table"

for _, row in df.iterrows():
    columns = ", ".join(row.index)
    values = ", ".join([f"'{str(v)}'" for v in row.values])
    
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
    print(sql)

