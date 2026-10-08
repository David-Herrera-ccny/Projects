# NYC Subway Ridership Analytics Dashboard

An interactive dashboard built using Python, SQL, SQLite, Streamlit, and Plotly to analyze over 1.2 million MTA subway ridership records across New York City.

This project explores commuter behavior, busiest station complexes, peak travel hours, borough-level ridership distribution, weekday demand patterns, and OMNY fare adoption trends using official MTA open data.

---

## Project Overview

This dashboard was designed to answer key transit analytics questions such as:

- Which subway stations are the busiest?
- What are the peak commuting hours?
- How does ridership vary by borough?
- How much higher is weekday ridership compared to weekends?
- How dominant is OMNY compared to MetroCard usage?

The goal was to combine data engineering, SQL querying, and interactive dashboard development into a portfolio-ready analytics project.

---

## Tech Stack

- Python
- SQL
- SQLite
- Streamlit
- Plotly
- Pandas

---

## Data Source

Official MTA Open Data:

MTA Subway Hourly Ridership Dataset

The dataset includes:

- station complex
- borough
- payment method
- fare class category
- ridership
- transfers
- transit timestamp
- latitude / longitude

Over 1.2 million records were cleaned, transformed, and loaded into SQLite for analysis.

---

## Database Design

The raw MTA file is one wide table: every row repeats the station's name, borough, and coordinates, and repeats the payment method for each fare class. The database stores each of those facts once, in three tables defined in `sql/schema.sql`:

| Table | One row per | Columns |
|-------|-------------|---------|
| `stations` | station complex (428) | id, name, borough, transit mode, latitude, longitude |
| `fare_classes` | fare class | id, fare class category, payment method |
| `ridership_hourly` | station, hour, and fare class | timestamp, station id, fare class id, ridership, transfers |

`ridership_hourly` references the other two by foreign key, and its primary key is the combination of timestamp, station, and fare class.

Calendar fields (date, hour, day of week, weekend flag) are not stored. A view, `ridership_detail`, joins the three tables and derives those fields from the timestamp, so the dashboard's queries stay simple.

`db.py` creates the schema and loads the cleaned CSV into it. Both `create_sqlite_db.py` and the dashboard use it.

---

## Dashboard Filters

The sidebar filters every chart and KPI by:

- borough
- station (the list follows the selected borough)
- payment method
- date range

Filter values are passed to SQLite as query parameters.

---

## Key Insights

These figures come from the full dataset (about 1.26 million rows, April 1-22, 2026). The deployed dashboard runs on a 25,000-row sample, so its numbers differ slightly.

### Top Station

Times Sq–42 St / Port Authority Bus Terminal is the busiest station complex in the dataset, reflecting its importance as a major commuter and transfer hub.

### Peak Commuting Hour

Peak ridership occurs around 7:00 AM, highlighting traditional morning commuter demand.

### Weekday Demand

Weekday ridership is approximately 3.8x higher than weekend ridership.

### OMNY Adoption

OMNY accounts for roughly 98% of fare payment usage in the dataset, showing strong adoption compared to MetroCard.

### Borough Comparison

Manhattan has the highest ridership volume, followed by Brooklyn and Queens.

---

## Project Structure

```text
mta-ridership-dashboard/
│
├── app.py
├── db.py
├── create_sqlite_db.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   └── mta_ridership_sample.csv
│
└── sql/
    └── schema.sql
```

### Data in this repository

The full cleaned dataset (`data/mta_ridership_clean.csv`, about 1.26 million rows) is too large for GitHub, so the repository includes a 25,000-row sample, `data/mta_ridership_sample.csv`. The deployed dashboard builds its SQLite database from that sample on first launch.

To run against the full dataset, place the cleaned CSV at `data/mta_ridership_clean.csv` and run `python create_sqlite_db.py`, which writes `data/mta_ridership.db`.