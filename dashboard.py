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
    
    # 1. Ensure Pandas knows the database time is UTC
    df['etl_processed_at'] = pd.to_datetime(df['etl_processed_at'], utc=True)
    
    # 2. Convert to Malaysia Time and format it cleanly (removes the +08:00 text)
    df['etl_processed_at'] = df['etl_processed_at'].dt.tz_convert('Asia/Kuala_Lumpur').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    return df

try:
    df = load_data()
    if not df.empty:
        st.subheader("Global Weather Highlights")
        
        # Find the rows with the highest and lowest temperatures
        hottest_row = df.loc[df['temperature_c'].idxmax()]
        coldest_row = df.loc[df['temperature_c'].idxmin()]
        
        # Create 3 columns for the metric cards
        col1, col2, col3 = st.columns(3)
        
        # Note: We use 'delta' to cleverly display the city name underneath the temperature!
        col1.metric(label="🔥 Hottest City", 
                    value=f"{hottest_row['temperature_c']} °C", 
                    delta=f"{hottest_row['city']}, {hottest_row['country']}", 
                    delta_color="off")
        
        col2.metric(label="❄️ Coldest City", 
                    value=f"{coldest_row['temperature_c']} °C", 
                    delta=f"{coldest_row['city']}, {coldest_row['country']}", 
                    delta_color="off")
        
        col3.metric(label="📊 Total Data Points", 
                    value=len(df),
                    delta="Rows in Database",
                    delta_color="off")
        
        st.divider() # Adds a clean horizontal line below the KPIs    
        st.subheader("Temperature Trends by City")
        fig_temp = px.line(df, x="observation_time", y="temperature_c", color="city", markers=True)
        st.plotly_chart(fig_temp, use_container_width=True)

        st.subheader("Raw Database Records")
        st.dataframe(df.sort_values(by="observation_time", ascending=True).reset_index(drop=True))
    else:
        st.warning("The database is currently empty.")
except Exception as e:
    st.error(f"Database connection failed. Did you set the DB_URL secret?")