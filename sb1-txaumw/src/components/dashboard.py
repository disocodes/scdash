"""Main dashboard component containing the core dashboard layout and structure."""
import streamlit as st
from datetime import datetime
from ..utils.data_loader import load_data
from ..utils.visualizations import (
    create_funding_chart,
    create_depletion_chart,
    create_hours_chart,
    create_risk_chart,
    create_forecast_chart
)
from ..utils.analysis import (
    calculate_funding_depletion,
    assess_service_risks,
    recommend_coordinator_allocation,
    generate_forecasts
)

def render_dashboard():
    st.set_page_config(
        page_title="Support Coordination Portfolio Dashboard",
        page_icon="📊",
        layout="wide"
    )

    # Sidebar controls
    st.sidebar.title("Dashboard Controls")
    uploaded_file = st.sidebar.file_uploader("Upload Participant Data (CSV/Excel)", type=['csv', 'xlsx'])
    
    # KPI Configuration
    st.sidebar.subheader("KPI Thresholds")
    funding_threshold = st.sidebar.slider("Funding Alert Threshold (%)", 0, 100, 20)
    service_hours_threshold = st.sidebar.slider("Service Hours Alert (%)", 0, 100, 15)

    # Main Dashboard
    st.title("Support Coordination Portfolio Dashboard")

    if uploaded_file:
        df = load_data(uploaded_file)
        if df is not None:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Funding Overview")
                fig_funding = create_funding_chart(df)
                st.plotly_chart(fig_funding, use_container_width=True)
                
                depletion_dates = calculate_funding_depletion(df)
                fig_depletion = create_depletion_chart(depletion_dates)
                st.plotly_chart(fig_depletion, use_container_width=True)
            
            with col2:
                st.subheader("Service Hours Analysis")
                fig_hours = create_hours_chart(df)
                st.plotly_chart(fig_hours, use_container_width=True)
                
                risks = assess_service_risks(df, funding_threshold, service_hours_threshold)
                fig_risk = create_risk_chart(risks)
                st.plotly_chart(fig_risk, use_container_width=True)
            
            render_forecasting_section(df)
            render_recommendations_section(df, risks)
    else:
        st.info("Please upload participant data to view the dashboard")