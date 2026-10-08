import os
import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

from db import build_database, connect, is_built

st.set_page_config(
    page_title="NYC Subway Ridership Analytics Dashboard",
    layout="wide"
)

BASE_DIR = Path(__file__).parent

DB_PATH = BASE_DIR / "data" / "mta_ridership.db"
CSV_PATH = BASE_DIR / "data" / "mta_ridership_sample.csv"

DB_PATH.parent.mkdir(exist_ok=True)

# -----------------------
# SQLite Connection
# -----------------------
@st.cache_resource
def get_connection():
    conn = connect(
        DB_PATH,
        check_same_thread=False
    )

    # Build the normalized tables from the sample CSV on first launch
    if not is_built(conn):
        build_database(conn, CSV_PATH)

    return conn

conn = get_connection()

def run_query(query, params=()):
    try:
        return pd.read_sql_query(query, conn, params=params)
    except Exception as e:
        st.error(f"Query failed: {e}")
        return pd.DataFrame()

st.title("NYC Subway Ridership Analytics Dashboard")
st.write("Analysis of MTA subway ridership using Python, SQL, SQLite, and Streamlit.")

row_count_df = run_query("SELECT COUNT(*) AS n FROM ridership_hourly")
if not row_count_df.empty:
    st.caption(f"Based on {row_count_df['n'].iloc[0]:,} hourly ridership records.")

# -----------------------
# Sidebar Filters
# -----------------------
boroughs_df = run_query("""
SELECT DISTINCT borough
FROM stations
ORDER BY borough
""")

payment_df_raw = run_query("""
SELECT DISTINCT payment_method
FROM fare_classes
ORDER BY payment_method
""")

date_range_df = run_query("""
SELECT
    MIN(date(transit_timestamp)) AS min_date,
    MAX(date(transit_timestamp)) AS max_date
FROM ridership_hourly
""")

selected_borough = st.sidebar.selectbox(
    "Select Borough",
    ["All"] + boroughs_df["borough"].dropna().tolist()
)

# Station list follows the borough selection
if selected_borough != "All":
    stations_df = run_query("""
    SELECT station_complex
    FROM stations
    WHERE borough = ?
    ORDER BY station_complex
    """, (selected_borough,))
else:
    stations_df = run_query("""
    SELECT station_complex
    FROM stations
    ORDER BY station_complex
    """)

selected_station = st.sidebar.selectbox(
    "Select Station",
    ["All"] + stations_df["station_complex"].dropna().tolist()
)

selected_payment = st.sidebar.selectbox(
    "Select Payment Method",
    ["All"] + payment_df_raw["payment_method"].dropna().tolist()
)

min_date = pd.to_datetime(date_range_df["min_date"].iloc[0]).date()
max_date = pd.to_datetime(date_range_df["max_date"].iloc[0]).date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# -----------------------
# WHERE Clause
# -----------------------
where_clauses = []
params = []

if selected_borough != "All":
    where_clauses.append("borough = ?")
    params.append(selected_borough)

if selected_station != "All":
    where_clauses.append("station_complex = ?")
    params.append(selected_station)

if selected_payment != "All":
    where_clauses.append("payment_method = ?")
    params.append(selected_payment)

# date_input returns a single date until both ends of the range are picked
if len(selected_dates) == 2:
    where_clauses.append("date BETWEEN ? AND ?")
    params.append(selected_dates[0].isoformat())
    params.append(selected_dates[1].isoformat())

where_sql = ""
if where_clauses:
    where_sql = "WHERE " + " AND ".join(where_clauses)

# -----------------------
# KPI Queries
# -----------------------
total_df = run_query(f"""
SELECT SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
""", params)

busiest_df = run_query(f"""
SELECT 
    station_complex, 
    SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
GROUP BY station_complex
ORDER BY total_ridership DESC
LIMIT 1
""", params)

peak_hour_df = run_query(f"""
SELECT 
    hour, 
    SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
GROUP BY hour
ORDER BY total_ridership DESC
LIMIT 1
""", params)

weekend_df = run_query(f"""
SELECT
    CASE 
        WHEN is_weekend = 1 THEN 'Weekend' 
        ELSE 'Weekday' 
    END AS day_type,
    SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
GROUP BY day_type
""", params)

omny_df = run_query(f"""
SELECT 
    payment_method, 
    SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
GROUP BY payment_method
""", params)

# -----------------------
# KPI Value Extraction
# -----------------------
total_ridership = 0
if not total_df.empty and pd.notna(total_df["total_ridership"].iloc[0]):
    total_ridership = total_df["total_ridership"].iloc[0]

station_name = "N/A"
if not busiest_df.empty:
    station_name = busiest_df["station_complex"].iloc[0]
    if len(station_name) > 35:
        station_name = station_name[:35] + "..."

peak_hour_val = "N/A"
if not peak_hour_df.empty:
    peak_hour_val = f"{int(peak_hour_df['hour'].iloc[0])}:00"

weekday_ratio = "N/A"
if not weekend_df.empty:
    weekday_row = weekend_df[weekend_df["day_type"] == "Weekday"]
    weekend_row = weekend_df[weekend_df["day_type"] == "Weekend"]

    if not weekday_row.empty and not weekend_row.empty:
        weekday_value = weekday_row["total_ridership"].values[0]
        weekend_value = weekend_row["total_ridership"].values[0]

        if weekend_value > 0:
            weekday_ratio = f"{round(weekday_value / weekend_value, 1)}x Higher"

omny_percentage = "N/A"
if not omny_df.empty:
    omny_row = omny_df[omny_df["payment_method"] == "omny"]
    total_payment = omny_df["total_ridership"].sum()

    if not omny_row.empty and total_payment > 0:
        omny_value = omny_row["total_ridership"].values[0]
        omny_percentage = f"{round((omny_value / total_payment) * 100, 1)}%"

# -----------------------
# KPI Cards
# -----------------------
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Ridership", f"{total_ridership:,.0f}")
col2.metric("Busiest Station", station_name)
col3.metric("Peak Hour", peak_hour_val)
col4.metric("Weekday Demand", weekday_ratio)
col5.metric("OMNY Adoption", omny_percentage)

# -----------------------
# Top 10 Stations
# -----------------------
top_stations = run_query(f"""
SELECT 
    station_complex, 
    SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
GROUP BY station_complex
ORDER BY total_ridership DESC
LIMIT 10
""", params)

if not top_stations.empty:
    fig_top = px.bar(
        top_stations,
        x="total_ridership",
        y="station_complex",
        orientation="h",
        title="Top 10 Busiest Stations",
        labels={
            "total_ridership": "Total Ridership",
            "station_complex": "Station Complex"
        }
    )

    fig_top.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_top, width="stretch")

    st.caption(
        f"{top_stations['station_complex'].iloc[0]} is the highest-ridership station complex "
        "for the current selection."
    )
else:
    st.warning("No data available for Top 10 Stations.")

# -----------------------
# Ridership by Hour
# -----------------------
hourly = run_query(f"""
SELECT 
    hour, 
    SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
GROUP BY hour
ORDER BY hour
""", params)

if not hourly.empty:
    fig_hour = px.line(
        hourly,
        x="hour",
        y="total_ridership",
        markers=True,
        title="Ridership by Hour of Day",
        labels={
            "hour": "Hour of Day",
            "total_ridership": "Total Ridership"
        }
    )

    st.plotly_chart(fig_hour, width="stretch")

    st.caption(
        "Ridership patterns highlight peak commuting periods and show how demand changes throughout the day."
    )
else:
    st.warning("No data available for hourly ridership.")

# -----------------------
# Borough Comparison
# -----------------------
borough_df = run_query(f"""
SELECT 
    borough, 
    SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
GROUP BY borough
ORDER BY total_ridership DESC
""", params)

if not borough_df.empty:
    fig_borough = px.bar(
        borough_df,
        x="borough",
        y="total_ridership",
        title="Ridership by Borough",
        labels={
            "borough": "Borough",
            "total_ridership": "Total Ridership"
        }
    )

    st.plotly_chart(fig_borough, width="stretch")

    st.caption(
        "Borough-level ridership shows how subway usage is distributed across New York City."
    )
else:
    st.warning("No data available for borough comparison.")

# -----------------------
# Payment Method
# -----------------------
payment_df = run_query(f"""
SELECT 
    payment_method, 
    SUM(ridership) AS total_ridership
FROM ridership_detail
{where_sql}
GROUP BY payment_method
ORDER BY total_ridership DESC
""", params)

if not payment_df.empty:
    fig_payment = px.pie(
        payment_df,
        names="payment_method",
        values="total_ridership",
        title="Ridership by Payment Method"
    )

    st.plotly_chart(fig_payment, width="stretch")

    st.caption(
        "OMNY accounts for the overwhelming majority of fare payment usage in this dataset."
    )
else:
    st.warning("No data available for payment method breakdown.")