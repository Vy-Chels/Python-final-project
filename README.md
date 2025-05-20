# COVID-19 Data Analysis Dashboard

## Project Description
An interactive dashboard for analyzing and visualizing COVID-19 data across different countries. The project provides insights into cases, deaths, vaccinations, and hospitalization trends using real-time data from Our World in Data.

## Project Objectives
1. Import and clean COVID-19 global data
2. Analyze time trends (cases, deaths, vaccinations)
3. Compare metrics across countries/regions
4. Visualize trends with interactive charts and maps
5. Create an interactive dashboard for data exploration

## Tools and Libraries Used
- **Data Processing & Analysis**
  - pandas: Data manipulation and analysis
  - numpy: Numerical computations
  - plotly: Interactive visualizations
  - matplotlib & seaborn: Statistical visualizations

- **Dashboard Development**
  - Streamlit: Interactive web application
  - openpyxl & xlrd: Excel file support

## How to Run the Project

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Dashboard**
   ```bash
   streamlit run covid_dashboard.py
   ```

3. **Access the Dashboard**
   - The dashboard will open in your default web browser
   - If it doesn't open automatically, navigate to the URL shown in the terminal (typically http://localhost:8501)

## Key Features
- Interactive country selection
- Customizable date range
- Multiple visualization types:
  - Time series plots
  - Vaccination progress
  - Hospitalization data
  - Global choropleth map
- Data download capability
- Real-time metrics updates

## Insights and Reflections
1. **Data Visualization Impact**
   - Interactive visualizations make complex data more accessible
   - Time series analysis reveals important patterns in pandemic progression
   - Comparative analysis highlights differences in country responses

2. **Technical Learnings**
   - Streamlit provides an efficient way to create interactive dashboards
   - Plotly enables sophisticated interactive visualizations
   - Data caching improves dashboard performance

3. **Future Improvements**
   - Add more advanced statistical analysis
   - Include predictive modeling
   - Enhance mobile responsiveness
   - Add more detailed regional analysis

## Data Source
- Our World in Data COVID-19 dataset
- Updated daily with global COVID-19 statistics