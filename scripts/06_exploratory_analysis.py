import pandas as pd
import numpy as np
import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'processed')
RESULTS_DIR = os.path.join(PROJECT_DIR, 'results')
os.makedirs(RESULTS_DIR, exist_ok=True)

print("Cargando dataset integrado...")
df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'integrated_data_1990_2019.csv'))

print(f"Dataset: {len(df)} registros, {len(df.columns)} columnas\n")

climate_vars = ['Temperature_C', 'Precipitation_mm', 'Surface_Pressure_Pa', 'Dewpoint_K', 'Wind_Speed_ms']
rate_cols = [col for col in df.columns if col.endswith('_Rate_per_100k')]

print(f"Variables climáticas: {len(climate_vars)}")
print(f"Causas de muerte (tasas): {len(rate_cols)}\n")


correlations = []

for rate_col in rate_cols:
    cause = rate_col.replace('_Rate_per_100k', '')
    
    for climate_var in climate_vars:
        corr = df[rate_col].corr(df[climate_var])
        correlations.append({
            'Cause': cause,
            'Climate_Variable': climate_var,
            'Correlation': corr
        })

corr_df = pd.DataFrame(correlations)
corr_df = corr_df.sort_values('Correlation', ascending=False, key=abs)

output_file = os.path.join(RESULTS_DIR, 'climate_mortality_correlations.csv')
corr_df.to_csv(output_file, index=False)

print(f"Correlaciones guardadas en: {output_file}\n")

print("Top 10 correlaciones más fuertes (positivas):")
print(corr_df.head(10))

print("\nTop 10 correlaciones más fuertes (negativas):")
print(corr_df.tail(10))

print("\nEstadísticas descriptivas del dataset:")
print(df[climate_vars + ['Population']].describe())