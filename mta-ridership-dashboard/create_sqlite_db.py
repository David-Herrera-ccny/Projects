import pandas as pd
import sqlite3

df = pd.read_csv("data/mta_ridership_clean.csv")

conn = sqlite3.connect("data/mta_ridership.db")

df.to_sql(
    "ridership_hourly",
    conn,
    if_exists="replace",
    index=False
)

conn.close()

print("SQLite database created successfully.")