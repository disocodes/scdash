import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from utils import (
    calculate_funding_depletion,
    assess_service_risks,
    recommend_coordinator_allocation,
    generate_forecasts
)

st.set_page_config(
    page_title="Support Coordination Portfolio Dashboard",
    page_icon="📊",
    layout="wide"
)

# Session state initialization
if 'data' not in st.session_state:
    st.session_state.data = None

def load_data(file):
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        required_columns = ['participant_id', 'total_funding', 'daily_expenditure', 'service_hours']
        if not all(col in df.columns for col in required_columns):
            st.error("Missing required columns. Please ensure your file contains: participant_id, total_funding, daily_expenditure, service_hours")
            return None
        return df
    except Exception as e:
        st.error(f"Error loading file: {str(e)}")
        return None

# Sidebar
st.sidebar.title("Dashboard Controls")
uploaded_file = st.sidebar.file_uploader("Upload Participant Data (CSV/Excel)", type=['csv', 'xlsx'])

if uploaded_file:
    data = load_data(uploaded_file)
    if data is not None:
        st.session_state.data = data

# KPI Configuration
st.sidebar.subheader("KPI Thresholds")
funding_threshold = st.sidebar.slider("Funding Alert Threshold (%)", 0, 100, 20)
service_hours_threshold = st.sidebar.slider("Service Hours Alert (%)", 0, 100, 15)

# Main Dashboard
st.title("Support Coordination Portfolio Dashboard")

if st.session_state.data is not None:
    df = st.session_state.data
    
    # Dashboard Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Funding Overview")
        fig_funding = px.pie(
            df,
            values='total_funding',
            names='participant_id',
            title='Total Funding Distribution'
        )
        st.plotly_chart(fig_funding, use_container_width=True)
        
        # Funding Depletion Forecast
        depletion_dates = calculate_funding_depletion(df)
        fig_depletion = px.bar(
            depletion_dates,
            x='participant_id',
            y='days_until_depletion',
            title='Days Until Funding Depletion'
        )
        st.plotly_chart(fig_depletion, use_container_width=True)
    
    with col2:
        st.subheader("Service Hours Analysis")
        fig_hours = px.scatter(
            df,
            x='daily_expenditure',
            y='service_hours',
            title='Service Hours vs. Daily Expenditure',
            trendline="ols"
        )
        st.plotly_chart(fig_hours, use_container_width=True)
        
        # Risk Assessment
        risks = assess_service_risks(df, funding_threshold, service_hours_threshold)
        fig_risk = px.scatter(
            risks,
            x='risk_score',
            y='participant_id',
            color='risk_level',
            title='Participant Risk Assessment'
        )
        st.plotly_chart(fig_risk, use_container_width=True)
    
    # Forecasting Section
    st.subheader("Performance Forecasting")
    forecast_days = st.slider("Forecast Days", 30, 365, 90)
    forecasts = generate_forecasts(df, forecast_days)
    
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(
        x=forecasts['date'],
        y=forecasts['predicted_expenditure'],
        name='Predicted Expenditure'
    ))
    fig_forecast.update_layout(title='Expenditure Forecast')
    st.plotly_chart(fig_forecast, use_container_width=True)
    
    # Coordinator Allocation
    st.subheader("Coordinator Allocation Recommendations")
    recommendations = recommend_coordinator_allocation(df)
    st.dataframe(recommendations)
    
    # Download Section
    st.subheader("Generate Report")
    if st.button("Generate Report"):
        report_data = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'total_participants': len(df),
            'total_funding': df['total_funding'].sum(),
            'average_service_hours': df['service_hours'].mean(),
            'high_risk_participants': len(risks[risks['risk_level'] == 'High']),
            'recommendations': recommendations.to_dict()
        }
        st.download_button(
            "Download Report",
            data=pd.DataFrame([report_data]).to_csv(),
            file_name=f"support_coordination_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
else:
    st.info("Please upload participant data to view the dashboard")