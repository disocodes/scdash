import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

def calculate_funding_depletion(df):
    """Calculate expected funding depletion dates for each participant."""
    depletion = []
    for _, row in df.iterrows():
        days = row['total_funding'] / row['daily_expenditure'] if row['daily_expenditure'] > 0 else 365
        depletion.append({
            'participant_id': row['participant_id'],
            'days_until_depletion': min(days, 365)
        })
    return pd.DataFrame(depletion)

def assess_service_risks(df, funding_threshold, service_hours_threshold):
    """Assess service risks for each participant."""
    risks = []
    for _, row in df.iterrows():
        funding_remaining = row['total_funding'] - (row['daily_expenditure'] * 365)
        funding_risk = (funding_remaining / row['total_funding']) * 100
        
        risk_score = (
            (funding_threshold - funding_risk) / funding_threshold +
            (service_hours_threshold - row['service_hours']) / service_hours_threshold
        ) / 2
        
        risk_level = 'High' if risk_score > 0.7 else 'Medium' if risk_score > 0.3 else 'Low'
        
        risks.append({
            'participant_id': row['participant_id'],
            'risk_score': risk_score,
            'risk_level': risk_level
        })
    return pd.DataFrame(risks)

def recommend_coordinator_allocation(df):
    """Generate coordinator allocation recommendations."""
    recommendations = []
    
    # Calculate complexity scores
    df['complexity_score'] = (
        StandardScaler().fit_transform(df[['daily_expenditure']]) +
        StandardScaler().fit_transform(df[['service_hours']])
    ) / 2
    
    # Group participants by complexity
    high_complexity = df[df['complexity_score'] > 0.5]
    low_complexity = df[df['complexity_score'] <= 0.5]
    
    # Generate recommendations
    recommendations = pd.DataFrame({
        'complexity_level': ['High'] * len(high_complexity) + ['Low'] * len(low_complexity),
        'participant_count': [len(high_complexity), len(low_complexity)],
        'recommended_coordinators': [
            max(1, len(high_complexity) // 10),
            max(1, len(low_complexity) // 15)
        ]
    })
    
    return recommendations

def generate_forecasts(df, forecast_days):
    """Generate expenditure forecasts."""
    # Create date range for forecasting
    dates = pd.date_range(
        start=datetime.now(),
        periods=forecast_days,
        freq='D'
    )
    
    # Calculate total daily expenditure
    daily_total = df['daily_expenditure'].sum()
    
    # Create simple trend with some randomness
    trend = np.linspace(0, 0.2, forecast_days)  # Assuming 20% growth over period
    noise = np.random.normal(0, 0.02, forecast_days)
    
    predicted_expenditure = daily_total * (1 + trend + noise)
    
    return pd.DataFrame({
        'date': dates,
        'predicted_expenditure': predicted_expenditure
    })