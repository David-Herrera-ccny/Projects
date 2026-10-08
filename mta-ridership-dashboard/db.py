import sqlite3
from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).parent
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def is_built(conn):
    """True if the database already has the normalized tables."""
    cursor = conn.execute("""
        SELECT COUNT(*)
        FROM sqlite_master
        WHERE name IN ('stations', 'fare_classes', 'ridership_hourly', 'ridership_detail')
    """)
    return cursor.fetchone()[0] == 4


def build_database(conn, csv_path):
    """Create the schema in sql/schema.sql and load the cleaned CSV into it."""
    df = pd.read_csv(
        csv_path,
        dtype={"station_complex_id": str},
        low_memory=False
    )

    # Start clean so an older, single-table database is replaced
    conn.executescript("""
        DROP VIEW IF EXISTS ridership_detail;
        DROP TABLE IF EXISTS ridership_hourly;
        DROP TABLE IF EXISTS fare_classes;
        DROP TABLE IF EXISTS stations;
    """)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

    # One row per station complex
    stations = (
        df[[
            "station_complex_id",
            "station_complex",
            "borough",
            "transit_mode",
            "latitude",
            "longitude"
        ]]
        .drop_duplicates("station_complex_id")
        .sort_values("station_complex_id")
    )

    # One row per fare class, each belonging to a single payment method
    fare_classes = (
        df[["fare_class_category", "payment_method"]]
        .drop_duplicates()
        .sort_values("fare_class_category")
        .reset_index(drop=True)
    )
    fare_classes.insert(0, "fare_class_id", fare_classes.index + 1)

    # Hourly facts, pointing at the two lookup tables by key
    ridership = df.merge(
        fare_classes[["fare_class_id", "fare_class_category"]],
        on="fare_class_category"
    )[[
        "transit_timestamp",
        "station_complex_id",
        "fare_class_id",
        "ridership",
        "transfers"
    ]]

    stations.to_sql("stations", conn, if_exists="append", index=False)
    fare_classes.to_sql("fare_classes", conn, if_exists="append", index=False)
    ridership.to_sql(
        "ridership_hourly",
        conn,
        if_exists="append",
        index=False,
        chunksize=50_000
    )

    conn.commit()


def connect(db_path, **kwargs):
    conn = sqlite3.connect(db_path, **kwargs)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
