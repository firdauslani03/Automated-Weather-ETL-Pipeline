import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv

# Load environment variables invisibly
load_dotenv()

st.set_page_config(page_title="Weather ETL Dashboard", layout="wide")
st.title("🌦️ Global Weather Dashboard")
st.markdown("This dashboard reads directly from a Neon Cloud PostgreSQL database updated daily by a GitHub Actions ETL pipeline.")

# Grab the cloud database password
DB_URL = os.getenv("DB_URL")

@st.cache_data(ttl=600)
def load_data():
    engine = create_engine(DB_URL)
    df = pd.read_sql("SELECT * FROM daily_weather", engine)
    return df

try:
    df = load_data()
    if not df.empty:
        st.subheader("Temperature Trends by City")
        fig_temp = px.line(df, x="observation_time", y="temperature_c", color="city", markers=True)
        st.plotly_chart(fig_temp, use_container_width=True)

        st.subheader("Raw Database Records")
        st.dataframe(df.sort_values(by="observation_time", ascending=True).reset_index(drop=True))
    else:
        st.warning("The database is currently empty.")
except Exception as e:
    st.error(f"Database connection failed. Did you set the DB_URL secret?")