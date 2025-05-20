import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="COVID-19 Dashboard",
    page_icon="🦠",
    layout="wide"
)

# Title and description
st.title("COVID-19 Data Analysis Dashboard")
st.markdown("""
This dashboard provides an interactive analysis of COVID-19 data, including cases, deaths, and vaccinations.
Select your preferred countries and date range to explore the data.
""")

# Load data
@st.cache_data
def load_data():
    url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    df = pd.read_csv(url)
    df['date'] = pd.to_datetime(df['date'])
    return df

# Load the data
df = load_data()

# Sidebar for controls
st.sidebar.header("Dashboard Controls")

# Country selection
available_countries = sorted(df['location'].unique())
selected_countries = st.sidebar.multiselect(
    "Select Countries",
    available_countries,
    default=['United States', 'India', 'Kenya']
)

# Date range selection
min_date = df['date'].min()
max_date = df['date'].max()
start_date = st.sidebar.date_input(
    "Start Date",
    min_date,
    min_value=min_date,
    max_value=max_date
)
end_date = st.sidebar.date_input(
    "End Date",
    max_date,
    min_value=min_date,
    max_value=max_date
)

# Filter data based on selections
mask = (df['location'].isin(selected_countries)) & \
       (df['date'] >= pd.to_datetime(start_date)) & \
       (df['date'] <= pd.to_datetime(end_date))
filtered_df = df[mask].copy()

# Main content
if not selected_countries:
    st.warning("Please select at least one country to view the analysis.")
else:
    # Create three columns for metrics
    col1, col2, col3 = st.columns(3)
    
    # Calculate latest metrics
    latest_data = filtered_df[filtered_df['date'] == filtered_df['date'].max()]
    
    with col1:
        st.metric(
            "Total Cases",
            f"{latest_data['total_cases'].sum():,.0f}",
            f"{latest_data['new_cases'].sum():,.0f} new"
        )
    
    with col2:
        st.metric(
            "Total Deaths",
            f"{latest_data['total_deaths'].sum():,.0f}",
            f"{latest_data['new_deaths'].sum():,.0f} new"
        )
    
    with col3:
        st.metric(
            "Total Vaccinations",
            f"{latest_data['total_vaccinations'].sum():,.0f}",
            f"{latest_data['new_vaccinations'].sum():,.0f} new"
        )

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["Cases & Deaths", "Vaccinations", "Hospitalization", "Global Map"])

    with tab1:
        st.subheader("COVID-19 Cases and Deaths Over Time")
        
        # Cases over time
        fig_cases = px.line(
            filtered_df,
            x='date',
            y='total_cases',
            color='location',
            title='Total Cases Over Time',
            labels={'total_cases': 'Total Cases', 'date': 'Date'}
        )
        st.plotly_chart(fig_cases, use_container_width=True)
        
        # Deaths over time
        fig_deaths = px.line(
            filtered_df,
            x='date',
            y='total_deaths',
            color='location',
            title='Total Deaths Over Time',
            labels={'total_deaths': 'Total Deaths', 'date': 'Date'}
        )
        st.plotly_chart(fig_deaths, use_container_width=True)

    with tab2:
        st.subheader("Vaccination Progress")
        
        # Vaccination rate
        filtered_df['vaccination_rate'] = (filtered_df['total_vaccinations'] / 
                                         (filtered_df['population'] * 2)) * 100
        
        fig_vacc = px.line(
            filtered_df,
            x='date',
            y='vaccination_rate',
            color='location',
            title='Vaccination Rate Over Time',
            labels={'vaccination_rate': 'Vaccination Rate (%)', 'date': 'Date'}
        )
        st.plotly_chart(fig_vacc, use_container_width=True)

    with tab3:
        st.subheader("Hospitalization Data")
        
        # Check if hospitalization data is available
        hosp_columns = [col for col in filtered_df.columns if 'hosp' in col.lower() or 'icu' in col.lower()]
        
        if hosp_columns:
            for col in hosp_columns:
                fig_hosp = px.line(
                    filtered_df,
                    x='date',
                    y=col,
                    color='location',
                    title=f'{col.replace("_", " ").title()} Over Time',
                    labels={col: col.replace('_', ' ').title(), 'date': 'Date'}
                )
                st.plotly_chart(fig_hosp, use_container_width=True)
        else:
            st.info("Hospitalization data is not available for the selected countries and time period.")

    with tab4:
        st.subheader("Global COVID-19 Map")
        
        # Prepare data for the map
        latest_global = df[df['date'] == df['date'].max()].copy()
        latest_global['cases_per_million'] = (latest_global['total_cases'] / 
                                            latest_global['population']) * 1000000
        
        # Create choropleth map
        fig_map = px.choropleth(
            latest_global,
            locations='iso_code',
            color='cases_per_million',
            hover_name='location',
            color_continuous_scale='Reds',
            title='COVID-19 Cases per Million People',
            labels={'cases_per_million': 'Cases per Million'}
        )
        
        fig_map.update_layout(
            geo=dict(showframe=False, showcoastlines=True),
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        st.plotly_chart(fig_map, use_container_width=True)

    # Add download button for the filtered data
    st.sidebar.markdown("---")
    st.sidebar.subheader("Download Data")
    csv = filtered_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="covid_data.csv",
        mime="text/csv"
    )

    # Add data source and last updated information
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    ### Data Source
    Data from Our World in Data COVID-19 dataset
    
    ### Last Updated
    """ + str(max_date.strftime("%Y-%m-%d"))) 