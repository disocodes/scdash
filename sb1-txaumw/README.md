# Support Coordination Portfolio Dashboard

A comprehensive dashboard for managing support coordination portfolios, built with Streamlit.

## Features

- Participant funding analysis
- KPI performance tracking
- Funding exhaustion projection
- Service reduction risk assessment
- Staffing recommendation tool
- Interactive data visualization
- Predictive analytics
- Downloadable reports

## Requirements

- Python 3.8+
- Required packages listed in `requirements.txt`

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Upload your participant data file (CSV or Excel) containing:
   - participant_id
   - total_funding
   - daily_expenditure
   - service_hours

3. Use the interactive controls to:
   - Set KPI thresholds
   - Generate forecasts
   - View visualizations
   - Download reports

## Data Format

Your input file should be a CSV or Excel file with the following columns:

- participant_id: Unique identifier for each participant
- total_funding: Total funding allocated
- daily_expenditure: Daily spending rate
- service_hours: Number of service hours