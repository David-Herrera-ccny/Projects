from pathlib import Path

from db import build_database, connect

BASE_DIR = Path(__file__).parent

CSV_PATH = BASE_DIR / "data" / "mta_ridership_clean.csv"
DB_PATH = BASE_DIR / "data" / "mta_ridership.db"

conn = connect(DB_PATH)

build_database(conn, CSV_PATH)

conn.close()

print("SQLite database created successfully.")
