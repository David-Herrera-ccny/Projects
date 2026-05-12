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

## Key Insights

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
├── create_sqlite_db.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── mta_ridership_clean.csv
│   └── mta_ridership.db
│
└── sql/
    └── schema.sql