import pandas as pd
import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'processed')

deaths_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'deaths_selected_countries.csv'))
population_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'population_annual_1990_2019.csv'))
climate_df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'climate_annual_1990_2019.csv'))

print(f"Mortalidad: {len(deaths_df)} registros")
print(f"Población: {len(population_df)} registros")
print(f"Clima: {len(climate_df)} registros\n")


merged_df = deaths_df.merge(population_df, on=['Country/Territory', 'Year'], how='inner')
merged_df = merged_df.merge(climate_df, on=['Country/Territory', 'Year'], how='inner')

print(f"Registros después de integración: {len(merged_df)}\n")

death_causes = [col for col in deaths_df.columns if col not in ['Country/Territory', 'Year', 'Code']]

print("Calculando tasas de mortalidad por 100,000 habitantes...")

for cause in death_causes:
    if cause in merged_df.columns:
        rate_col = f'{cause}_Rate_per_100k'
        merged_df[rate_col] = (merged_df[cause] / merged_df['Population']) * 100000

print(f"\nDataset final:")
print(f"Registros: {len(merged_df)}")
print(f"Países: {merged_df['Country/Territory'].nunique()}")
print(f"Años: {merged_df['Year'].min()} - {merged_df['Year'].max()}")
print(f"Columnas totales: {len(merged_df.columns)}")

output_file = os.path.join(PROCESSED_DATA_DIR, 'integrated_data_1990_2019.csv')
merged_df.to_csv(output_file, index=False)

print(f"\nArchivo guardado en: {output_file}")

print(f"\nEjemplo - Alemania 2019:")
sample = merged_df[(merged_df['Country/Territory'] == 'Germany') & (merged_df['Year'] == 2019)]
print(f"Temperatura: {sample['Temperature_C'].values[0]:.2f}°C")
print(f"Población: {sample['Population'].values[0]:,}")
print(f"Columnas disponibles: {len(sample.columns)}")