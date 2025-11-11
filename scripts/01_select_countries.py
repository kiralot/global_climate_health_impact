import pandas as pd
import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
RAW_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'raw')
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'processed')

os.makedirs(PROCESSED_DATA_DIR, exist_ok=True)

deaths_df = pd.read_csv(os.path.join(RAW_DATA_DIR, 'cause_of_deaths.csv'))

print(f"Rango de años en el dataset: {deaths_df['Year'].min()} - {deaths_df['Year'].max()}")
print(f"Total registros originales: {len(deaths_df)}\n")

deaths_df_filtered = deaths_df[(deaths_df['Year'] >= 1990) & (deaths_df['Year'] <= 2019)]

print(f"Registros después de filtrar (1990-2019): {len(deaths_df_filtered)}\n")

continents = {
    'Europe': ['Germany', 'United Kingdom', 'France', 'Italy', 'Spain', 'Poland', 'Netherlands', 'Belgium', 'Greece', 'Portugal'],
    'Asia': ['China', 'India', 'Japan', 'Indonesia', 'Pakistan', 'Bangladesh', 'Russia', 'Turkey', 'Iran', 'Thailand'],
    'Americas': ['United States', 'Brazil', 'Mexico', 'Canada', 'Argentina', 'Colombia', 'Peru', 'Venezuela', 'Chile', 'Ecuador'],
    'Africa': ['Nigeria', 'Ethiopia', 'Egypt', 'Democratic Republic of Congo', 'South Africa', 'Tanzania', 'Kenya', 'Algeria', 'Sudan', 'Uganda'],
    'Oceania': ['Australia', 'Papua New Guinea', 'New Zealand', 'Fiji', 'Solomon Islands', 'Samoa', 'Vanuatu', 'Kiribati', 'Tonga', 'Micronesia']
}

selected_countries = []
for continent, countries in continents.items():
    for country in countries:
        if country in deaths_df_filtered['Country/Territory'].values:
            selected_countries.append(country)

print(f"Total de países seleccionados: {len(selected_countries)}\n")

for continent, countries in continents.items():
    available = [c for c in countries if c in deaths_df_filtered['Country/Territory'].values]
    print(f"{continent}: {len(available)} países")
    for country in available:
        print(f"  - {country}")
    print()

deaths_df_final = deaths_df_filtered[deaths_df_filtered['Country/Territory'].isin(selected_countries)]

print(f"Registros finales: {len(deaths_df_final)}")
print(f"Países: {len(deaths_df_final['Country/Territory'].unique())}")
print(f"Años: {deaths_df_final['Year'].min()} - {deaths_df_final['Year'].max()}")

output_path = os.path.join(PROCESSED_DATA_DIR, 'deaths_selected_countries.csv')
deaths_df_final.to_csv(output_path, index=False)
print(f"\nDataset filtrado guardado en: {output_path}")

countries_list_path = os.path.join(PROCESSED_DATA_DIR, 'selected_countries.txt')
with open(countries_list_path, 'w', encoding='utf-8') as f:
    for country in sorted(selected_countries):
        f.write(f"{country}\n")
print(f"Lista de países guardada en: {countries_list_path}")
