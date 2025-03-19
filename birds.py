import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import folium_static

# Load data
@st.cache_data
def load_data():
    forest_df = pd.read_csv(r"C:\Users\AJITH HARISH\Downloads\Bird_Monitoring_Data_FOREST.csv")
    grassland_df = pd.read_csv(r"C:\Users\AJITH HARISH\Downloads\Bird_Monitoring_Data_GRASSLAND.csv")
    return forest_df, grassland_df

# Load datasets
forest_df, grassland_df = load_data()

# Convert Date column to datetime
forest_df['Date'] = pd.to_datetime(forest_df['Date'])
grassland_df['Date'] = pd.to_datetime(grassland_df['Date'])

# Streamlit App Layout
st.title("🦅 Bird Species Observation Analysis")
st.sidebar.header("Filters")

data_choice = st.sidebar.radio("Select Habitat Type:", ["Forest", "Grassland"])
if data_choice == "Forest":
    df = forest_df
else:
    df = grassland_df

# Temporal Analysis
st.subheader("Bird Observations Over Time")
time_chart = px.line(df, x='Date', y='Initial_Three_Min_Cnt', title="Temporal Analysis", markers=True)
st.plotly_chart(time_chart)

# Species Analysis
st.subheader("Species Analysis")
top_species = df['Common_Name'].value_counts().head(10)
st.bar_chart(top_species)

# Environmental Conditions
st.subheader("Temperature vs. Observations")
temp_chart = px.scatter(df, x='Temperature', y='Initial_Three_Min_Cnt', color='Common_Name', title="Environmental Conditions")
st.plotly_chart(temp_chart)

# Distance Analysis
st.subheader("Observation Distance Distribution")
distance_hist = px.histogram(df, x='Distance', nbins=20, title="Distance Analysis")
st.plotly_chart(distance_hist)

# Spatial Analysis
st.subheader("Spatial Analysis")
# Print column names to check correct ones
st.write("Dataset columns:", df.columns)

# Check for correct latitude and longitude column names
possible_lat_cols = ['Latitude', 'Lat', 'Latitude_DD', 'GPS_Latitude']
possible_lon_cols = ['Longitude', 'Lon', 'Longitude_DD', 'GPS_Longitude']

latitude_col = next((col for col in possible_lat_cols if col in df.columns), None)
longitude_col = next((col for col in possible_lon_cols if col in df.columns), None)

if latitude_col and longitude_col:
    map_center = [df[latitude_col].mean(), df[longitude_col].mean()]
    map_ = folium.Map(location=map_center, zoom_start=6)
    for _, row in df.iterrows():
        folium.Marker([row[latitude_col], row[longitude_col]], popup=row['Common_Name']).add_to(map_)
    folium_static(map_)
else:
    st.warning("Latitude/Longitude columns not found in dataset.")


# Observer Trends
st.subheader("Observer Trends")
top_observers = df['Observer'].value_counts().head(10)
st.bar_chart(top_observers)

# Conservation Insights
st.subheader("Conservation Insights")
# Check for correct conservation column
possible_conservation_cols = ['Conservation_Status', 'PIF_Watchlist_Status', 'Regional_Stewardship_Status']

conservation_col = next((col for col in possible_conservation_cols if col in df.columns), None)

if conservation_col:
    conservation_species = df[df[conservation_col].notnull()]['Common_Name'].value_counts().head(10)
    st.subheader("Species of Conservation Concern")
    st.bar_chart(conservation_species)
else:
    st.warning("No conservation status column found in dataset.")


st.success("Dashboard ready! Explore the data interactively.")
