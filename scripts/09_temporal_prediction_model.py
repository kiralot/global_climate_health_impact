"""
Temporal Prediction Model using Prophet
Creates forecasts for mortality rates (2020-2030) based on climate trends
"""

import pandas as pd
import numpy as np
from prophet import Prophet
import warnings
warnings.filterwarnings('ignore')
import os
import sys

# Add parent directory to path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

from scripts.utils.config import PROCESSED_DATA_DIR, RESULTS_DIR

def prepare_prophet_data(df, country, mortality_cause, climate_vars):
    """
    Prepare data for Prophet model
    
    Args:
        df: Integrated dataset
        country: Country name
        mortality_cause: Mortality cause column name
        climate_vars: List of climate variables to use as regressors
    
    Returns:
        DataFrame formatted for Prophet (ds, y, and regressors)
    """
    country_data = df[df['Country/Territory'] == country].copy()
    country_data = country_data.sort_values('Year')
    
    # Create Prophet dataframe
    prophet_df = pd.DataFrame({
        'ds': pd.to_datetime(country_data['Year'], format='%Y'),
        'y': country_data[mortality_cause]
    })
    
    # Add climate variables as regressors
    for var in climate_vars:
        prophet_df[var] = country_data[var].values
    
    return prophet_df

def train_prophet_model(train_df, climate_vars):
    """
    Train Prophet model with climate variables as regressors
    
    Args:
        train_df: Training data formatted for Prophet
        climate_vars: List of climate variables
    
    Returns:
        Trained Prophet model
    """
    model = Prophet(
        yearly_seasonality=False,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,
        seasonality_prior_scale=10
    )
    
    # Add climate variables as regressors
    for var in climate_vars:
        model.add_regressor(var)
    
    model.fit(train_df)
    return model

def create_future_climate_scenarios(train_df, climate_vars, periods=11):
    """
    Create future climate scenarios for prediction
    Uses linear trend extrapolation
    
    Args:
        train_df: Historical data
        climate_vars: Climate variables
        periods: Number of years to forecast
    
    Returns:
        DataFrame with future dates and climate projections
    """
    future = pd.DataFrame({
        'ds': pd.date_range(start='2020', periods=periods, freq='YS')
    })
    
    # Project climate variables using linear trend
    for var in climate_vars:
        # Fit linear trend to historical data
        x = np.arange(len(train_df))
        y = train_df[var].values
        coeffs = np.polyfit(x, y, 1)
        
        # Extrapolate
        future_x = np.arange(len(train_df), len(train_df) + periods)
        future[var] = np.polyval(coeffs, future_x)
    
    return future

def generate_predictions_for_country(df, country, top_causes, climate_vars):
    """
    Generate predictions for a specific country
    
    Args:
        df: Integrated dataset
        country: Country name
        top_causes: List of top mortality causes to predict
        climate_vars: Climate variables
    
    Returns:
        Dictionary with predictions for each cause
    """
    predictions = {}
    
    for cause in top_causes:
        try:
            # Prepare data
            train_df = prepare_prophet_data(df, country, cause, climate_vars)
            
            # Train model
            model = train_prophet_model(train_df, climate_vars)
            
            # Create future scenarios
            future = create_future_climate_scenarios(train_df, climate_vars, periods=11)
            
            # Make predictions
            forecast = model.predict(future)
            
            predictions[cause] = {
                'forecast': forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
                'model': model
            }
            
        except Exception as e:
            print(f"Error predicting {cause} for {country}: {str(e)}")
            continue
    
    return predictions

def main():
    print("=" * 80)
    print("TEMPORAL PREDICTION MODEL - MORTALITY FORECASTING")
    print("=" * 80)
    print()
    
    # Load integrated data
    print("Loading integrated data...")
    df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'integrated_data_1990_2019.csv'))
    print(f"Loaded {len(df)} records")
    print()
    
    # Define climate variables and top mortality causes
    climate_vars = ['Temperature_C', 'Precipitation_mm', 'Surface_Pressure_Pa', 
                   'Dewpoint_K', 'Wind_Speed_ms']
    
    # Get top 5 mortality causes by total deaths
    rate_cols = [col for col in df.columns if col.endswith('_Rate_per_100k')]
    top_causes = []
    for col in rate_cols:
        original_col = col.replace('_Rate_per_100k', '')
        if original_col in df.columns:
            top_causes.append((original_col, df[original_col].sum()))
    
    top_causes = sorted(top_causes, key=lambda x: x[1], reverse=True)[:10]
    top_cause_names = [cause[0] for cause in top_causes]
    
    print("Top 10 mortality causes selected for prediction:")
    for i, (cause, total) in enumerate(top_causes, 1):
        print(f"{i}. {cause}: {total:,.0f} total deaths")
    print()
    
    # Select representative countries (different continents)
    selected_countries = [
        'United States', 'Germany', 'China', 'Brazil', 
        'India', 'Nigeria', 'Australia', 'Japan'
    ]
    
    print(f"Generating predictions for {len(selected_countries)} countries...")
    print()
    
    all_predictions = {}
    
    for country in selected_countries:
        print(f"Processing {country}...")
        predictions = generate_predictions_for_country(
            df, country, top_cause_names, climate_vars
        )
        all_predictions[country] = predictions
        print(f"  Generated {len(predictions)} predictions")
    
    print()
    
    # Save predictions
    predictions_file = os.path.join(RESULTS_DIR, 'temporal_predictions.csv')
    
    all_forecasts = []
    for country, country_preds in all_predictions.items():
        for cause, pred_data in country_preds.items():
            forecast_df = pred_data['forecast'].copy()
            forecast_df['Country'] = country
            forecast_df['Cause'] = cause
            forecast_df['Year'] = forecast_df['ds'].dt.year
            all_forecasts.append(forecast_df)
    
    if all_forecasts:
        final_df = pd.concat(all_forecasts, ignore_index=True)
        final_df = final_df[['Country', 'Cause', 'Year', 'yhat', 'yhat_lower', 'yhat_upper']]
        final_df.columns = ['Country', 'Cause', 'Year', 'Predicted_Rate', 
                           'Lower_Bound', 'Upper_Bound']
        final_df.to_csv(predictions_file, index=False)
        print(f" Predictions saved to {predictions_file}")
        print(f"  Total predictions: {len(final_df)}")
    
    print("=" * 80)
    print("PREDICTION COMPLETE")
    print("=" * 80)
    print("Summary:")
    print(f"- Countries analyzed: {len(selected_countries)}")
    print(f"- Mortality causes: {len(top_cause_names)}")
    print(f"- Forecast period: 2020-2030 (11 years)")
    print(f"- Climate regressors: {', '.join(climate_vars)}")

if __name__ == '__main__':
    main()
