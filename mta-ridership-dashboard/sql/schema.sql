-- NYC Subway Ridership Analytics Dashboard
-- Normalized SQLite schema for data/mta_ridership.db
--
-- The raw MTA file repeats each station's name, borough, and coordinates on
-- every row, and repeats the payment method for every fare class. Here each
-- of those facts is stored once:
--
--   stations          one row per station complex
--   fare_classes      one row per fare class, with its payment method
--   ridership_hourly  one row per station, hour, and fare class
--
-- Calendar fields (date, hour, day of week, weekend flag) are not stored;
-- the ridership_detail view derives them from transit_timestamp.

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS stations (
    station_complex_id  TEXT PRIMARY KEY,
    station_complex     TEXT NOT NULL UNIQUE,   -- name with its lines
    borough             TEXT NOT NULL,
    transit_mode        TEXT NOT NULL,          -- subway, tram, staten_island_railway
    latitude            REAL,
    longitude           REAL
);

CREATE TABLE IF NOT EXISTS fare_classes (
    fare_class_id        INTEGER PRIMARY KEY,
    fare_class_category  TEXT NOT NULL UNIQUE,  -- e.g. 'OMNY - Full Fare'
    payment_method       TEXT NOT NULL          -- 'omny' or 'metrocard'
);

CREATE TABLE IF NOT EXISTS ridership_hourly (
    transit_timestamp   TEXT    NOT NULL,       -- 'YYYY-MM-DD HH:MM:SS', start of the hour
    station_complex_id  TEXT    NOT NULL REFERENCES stations (station_complex_id),
    fare_class_id       INTEGER NOT NULL REFERENCES fare_classes (fare_class_id),
    ridership           REAL,                   -- entries in that hour
    transfers           REAL,
    PRIMARY KEY (transit_timestamp, station_complex_id, fare_class_id)
);

CREATE INDEX IF NOT EXISTS idx_ridership_station
    ON ridership_hourly (station_complex_id);

CREATE INDEX IF NOT EXISTS idx_ridership_fare_class
    ON ridership_hourly (fare_class_id);

-- Flat, query-friendly view used by the dashboard.
CREATE VIEW IF NOT EXISTS ridership_detail AS
SELECT
    r.transit_timestamp,
    date(r.transit_timestamp)                             AS date,
    CAST(strftime('%H', r.transit_timestamp) AS INTEGER)  AS hour,
    CASE strftime('%w', r.transit_timestamp)
        WHEN '0' THEN 'Sunday'
        WHEN '1' THEN 'Monday'
        WHEN '2' THEN 'Tuesday'
        WHEN '3' THEN 'Wednesday'
        WHEN '4' THEN 'Thursday'
        WHEN '5' THEN 'Friday'
        ELSE 'Saturday'
    END                                                   AS day_of_week,
    strftime('%w', r.transit_timestamp) IN ('0', '6')     AS is_weekend,
    s.station_complex_id,
    s.station_complex,
    s.borough,
    s.transit_mode,
    s.latitude,
    s.longitude,
    f.payment_method,
    f.fare_class_category,
    r.ridership,
    r.transfers
FROM ridership_hourly AS r
JOIN stations     AS s ON s.station_complex_id = r.station_complex_id
JOIN fare_classes AS f ON f.fare_class_id = r.fare_class_id;
