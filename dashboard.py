import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# 1. Page Configuration
st.set_page_config(page_title="Weather ETL Dashboard", layout="wide")
st.title("🌦️ Global Weather Dashboard")
st.markdown("This dashboard reads directly from the local SQLite database updated daily by the ETL pipeline.")

# 2. Connect to Database & Load Data
DB_FILE = r"C:\Users\firdaus\Documents\Automated-Weather-ETL-Pipeline\weather_data.db"

@st.cache_data # This prevents Streamlit from querying the DB every time you click a button
def load_data():
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql("SELECT * FROM daily_weather", conn)
    conn.close()
    return df

df = load_data()

# 3. Build Visualizations
if not df.empty:
    # Create a multi-line chart comparing temperatures
    st.subheader("Temperature Trends by City")
    fig_temp = px.line(df, x="observation_time", y="temperature_c", color="city", markers=True)
    st.plotly_chart(fig_temp, use_container_width=True)

    # Show the raw database table at the bottom
    st.subheader("Raw Database Records")
    st.dataframe(df.sort_values(by="observation_time", ascending=False))
else:
    st.warning("The database is currently empty. Run your ETL script first!")