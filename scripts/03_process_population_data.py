import pandas as pd
import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'processed')

deaths_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'deaths_selected_countries.csv'))
population_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'population_annual_1990_2019.csv'))

deaths_countries = set(deaths_df['Country/Territory'].unique())
population_countries = set(population_df['Country/Territory'].unique())

common_countries = deaths_countries.intersection(population_countries)

print(f"Países en dataset de mortalidad: {len(deaths_countries)}")
print(f"Países en dataset de población: {len(population_countries)}")
print(f"Países comunes (final): {len(common_countries)}\n")

deaths_df_final = deaths_df[deaths_df['Country/Territory'].isin(common_countries)]
population_df_final = population_df[population_df['Country/Territory'].isin(common_countries)]

print(f"Registros de mortalidad: {len(deaths_df_final)}")
print(f"Registros de población: {len(population_df_final)}\n")

deaths_df_final.to_csv(os.path.join(PROCESSED_DATA_DIR, 'deaths_selected_countries.csv'), index=False)
population_df_final.to_csv(os.path.join(PROCESSED_DATA_DIR, 'population_annual_1990_2019.csv'), index=False)

with open(os.path.join(PROCESSED_DATA_DIR, 'selected_countries.txt'), 'w') as f:
    for country in sorted(common_countries):
        f.write(f"{country}\n")

print("Datasets actualizados con 49 países comunes")
print(f"Archivos actualizados en: {PROCESSED_DATA_DIR}")