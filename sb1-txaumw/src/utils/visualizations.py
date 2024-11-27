"""Utility functions for creating visualizations."""
import plotly.express as px
import plotly.graph_objects as go

def create_funding_chart(df):
    """Create funding distribution pie chart."""
    return px.pie(
        df,
        values='total_funding',
        names='participant_id',
        title='Total Funding Distribution'
    )

def create_depletion_chart(depletion_dates):
    """Create funding depletion bar chart."""
    return px.bar(
        depletion_dates,
        x='participant_id',
        y='days_until_depletion',
        title='Days Until Funding Depletion'
    )

def create_hours_chart(df):
    """Create service hours scatter plot."""
    return px.scatter(
        df,
        x='daily_expenditure',
        y='service_hours',
        title='Service Hours vs. Daily Expenditure',
        trendline="ols"
    )

def create_risk_chart(risks):
    """Create risk assessment scatter plot."""
    return px.scatter(
        risks,
        x='risk_score',
        y='participant_id',
        color='risk_level',
        title='Participant Risk Assessment'
    )

def create_forecast_chart(forecasts):
    """Create expenditure forecast line chart."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=forecasts['date'],
        y=forecasts['predicted_expenditure'],
        name='Predicted Expenditure'
    ))
    fig.update_layout(title='Expenditure Forecast')
    return fig