"""Utility functions for loading and validating data."""
import pandas as pd
import streamlit as st

def load_data(file):
    """Load and validate data from uploaded file."""
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