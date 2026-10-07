import streamlit as st
import pandas as pd
import plotly.express as px
import os
from fpdf import FPDF
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables invisibly
load_dotenv()

# Set wide layout (Must be the first Streamlit command)
st.set_page_config(page_title="Weather ETL Dashboard", page_icon="🌤️", layout="wide")

# --- CUSTOM UI CSS STYLING ---
# Injecting CSS to force larger fonts, prioritize tabs, and enlarge metrics
st.markdown("""
    <style>
        /* 1. Make the navigation tabs massive and bold */
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
            font-size: 26px !important;
            font-weight: 800 !important;
            padding: 10px 15px;
        }
        
        /* 2. Increase metric values (Hottest/Coldest temperatures) */
        [data-testid="stMetricValue"] {
            font-size: 3rem !important;
        }
        
        /* 3. Make the filter label slightly larger */
        .stSelectbox label p {
            font-size: 20px !important;
            font-weight: bold !important;
        }
    </style>
""", unsafe_allow_html=True)

# Grab the cloud database password
DB_URL = os.getenv("DB_URL")

def create_pdf_report(dataframe):
    pdf = FPDF()
    pdf.add_page()
    
    pdf.set_font('helvetica', 'B', 16)
    pdf.cell(0, 10, 'Global Weather Summary Report', border=False, align='C')
    pdf.ln(15) 
    
    pdf.set_font('helvetica', 'B', 10)
    pdf.set_fill_color(200, 220, 255)
    
    columns = ['City', 'Country', 'Temp (C)', 'Wind (km/h)', 'Last Updated (MYT)']
    col_widths = [35, 35, 25, 30, 60]
    
    for col, width in zip(columns, col_widths):
        pdf.cell(width, 10, col, border=1, align='C', fill=True)
    pdf.ln()
    
    pdf.set_font('helvetica', '', 10)
    latest_df = dataframe.drop_duplicates(subset=['city'], keep='first')
    
    for _, row in latest_df.iterrows():
        pdf.cell(col_widths[0], 10, str(row['city']), border=1, align='C')
        pdf.cell(col_widths[1], 10, str(row['country']), border=1, align='C')
        pdf.cell(col_widths[2], 10, f"{row['temperature_c']} °C", border=1, align='C')
        pdf.cell(col_widths[3], 10, str(row['wind_speed_kmh']), border=1, align='C')
        pdf.cell(col_widths[4], 10, str(row['etl_processed_at']), border=1, align='C')
        pdf.ln()
        
    return bytes(pdf.output())

@st.cache_data(ttl=600)
def load_data():
    engine = create_engine(DB_URL)
    df = pd.read_sql("SELECT * FROM daily_weather", engine)
    df['etl_processed_at'] = pd.to_datetime(df['etl_processed_at'], utc=True)
    df['etl_processed_at'] = df['etl_processed_at'].dt.tz_convert('Asia/Kuala_Lumpur').dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

try:
    df = load_data()
    if not df.empty:
        # --- HEADER ---
        st.title("🌤️ Live Weather Data Pipeline")
        # Using a subheader to naturally increase the description text size
        st.subheader("Automated end-to-end ETL pipeline extracting real-time weather metrics.")
        st.divider()

        # --- TOP CONTROLS (Moved from Sidebar) ---
        # 3-column layout: Filter takes most of the space, a blank spacer, and the button on the far right
        col_filter, col_spacer, col_button = st.columns([5, 1, 3])
        
        with col_filter:
            city_list = ["Global View"] + list(df['city'].unique())
            selected_city = st.selectbox("🌍 Filter by City:", city_list)
            
        with col_button:
            st.write("") # Invisible padding to push the button down so it aligns with the dropdown box
            st.write("")
            pdf_bytes = create_pdf_report(df)
            st.download_button(
                label="📄 Download PDF Report",
                data=pdf_bytes,
                file_name="Weather_Report.pdf",
                mime="application/pdf",
                use_container_width=True 
            )

        # Apply the filter to the data
        if selected_city != "Global View":
            display_df = df[df['city'] == selected_city]
        else:
            display_df = df

        st.write("") # Extra padding before the tabs
        
        # --- ENLARGED TABBED NAVIGATION ---
        tab1, tab2, tab3 = st.tabs(["🌍 Global Overview", "📈 Trends & Charts", "🗄️ Raw Database"])

        with tab1:
            st.write("### Global Weather Highlights")
            
            hottest_row = df.loc[df['temperature_c'].idxmax()]
            coldest_row = df.loc[df['temperature_c'].idxmin()]
            
            col1, col2, col3 = st.columns(3)
            
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
            
            st.divider() 
            st.write("### Interactive Temperature Map")

            latest_df = display_df.drop_duplicates(subset=['city'], keep='first')

            fig_map = px.scatter_map(
                latest_df,
                lat="latitude",
                lon="longitude",
                hover_name="city",
                hover_data={"latitude": False, "longitude": False, "temperature_c": True, "wind_speed_kmh": True},
                color="temperature_c",
                color_continuous_scale="bluered", 
                zoom=1.2,
                map_style="carto-positron" 
            )

            fig_map.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
            st.plotly_chart(fig_map, use_container_width=True)

        with tab2:
            st.write("### Temperature Trends by City")
            fig_temp = px.line(display_df, x="observation_time", y="temperature_c", color="city", markers=True)
            st.plotly_chart(fig_temp, use_container_width=True)

        with tab3:
            st.write("### Database Records")
            with st.expander("Click to view raw PostgreSQL tables", expanded=True):
                st.dataframe(
                    display_df.sort_values(by="observation_time", ascending=True).reset_index(drop=True),
                    hide_index=True, 
                    use_container_width=True
                )
    else:
        st.warning("The database is currently empty.")
except Exception as e:
    st.error(f"Database connection failed: {e}")