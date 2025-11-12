import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'processed')
RESULTS_DIR = os.path.join(PROJECT_DIR, 'results')
FIGURES_DIR = os.path.join(RESULTS_DIR, 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)

print("Cargando datos...")
df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'integrated_data_1990_2019.csv'))
corr_df = pd.read_csv(os.path.join(RESULTS_DIR, 'climate_mortality_correlations.csv'))

sns.set_style("whitegrid")

print("Creando visualización 1: Top 20 correlaciones")
top_corr = corr_df.nlargest(20, 'Correlation', keep='all')

plt.figure(figsize=(12, 8))
plt.barh(range(len(top_corr)), top_corr['Correlation'].values)
plt.yticks(range(len(top_corr)), 
           [f"{row['Cause'][:30]} vs {row['Climate_Variable']}" 
            for _, row in top_corr.iterrows()], fontsize=8)
plt.xlabel('Correlation Coefficient')
plt.title('Top 20 Strongest Climate-Mortality Correlations')
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, '01_top_correlations.png'), dpi=300, bbox_inches='tight')
plt.close()

print("Creando visualización 2: Temperatura vs Neoplasms")
plt.figure(figsize=(10, 6))
plt.scatter(df['Temperature_C'], df['Neoplasms_Rate_per_100k'], alpha=0.3)
plt.xlabel('Temperature (°C)')
plt.ylabel('Neoplasms Death Rate (per 100k)')
plt.title(f'Temperature vs Cancer Mortality (r={df["Temperature_C"].corr(df["Neoplasms_Rate_per_100k"]):.3f})')
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, '02_temp_vs_neoplasms.png'), dpi=300, bbox_inches='tight')
plt.close()

continent_mapping = {
    'Germany': 'Europe', 'United Kingdom': 'Europe', 'France': 'Europe', 'Italy': 'Europe',
    'Spain': 'Europe', 'Poland': 'Europe', 'Netherlands': 'Europe', 'Belgium': 'Europe',
    'Greece': 'Europe', 'Portugal': 'Europe',
    'China': 'Asia', 'India': 'Asia', 'Japan': 'Asia', 'Indonesia': 'Asia',
    'Pakistan': 'Asia', 'Bangladesh': 'Asia', 'Russia': 'Asia', 'Turkey': 'Asia',
    'Iran': 'Asia', 'Thailand': 'Asia',
    'United States': 'Americas', 'Brazil': 'Americas', 'Mexico': 'Americas', 'Canada': 'Americas',
    'Argentina': 'Americas', 'Colombia': 'Americas', 'Peru': 'Americas', 'Venezuela': 'Americas',
    'Chile': 'Americas', 'Ecuador': 'Americas',
    'Nigeria': 'Africa', 'Ethiopia': 'Africa', 'Egypt': 'Africa', 'South Africa': 'Africa',
    'Tanzania': 'Africa', 'Kenya': 'Africa', 'Algeria': 'Africa', 'Sudan': 'Africa',
    'Uganda': 'Africa',
    'Australia': 'Oceania', 'Papua New Guinea': 'Oceania', 'New Zealand': 'Oceania',
    'Fiji': 'Oceania', 'Solomon Islands': 'Oceania', 'Samoa': 'Oceania',
    'Vanuatu': 'Oceania', 'Kiribati': 'Oceania', 'Tonga': 'Oceania', 'Micronesia': 'Oceania'
}

df['Continent'] = df['Country/Territory'].map(continent_mapping)

temp_by_continent = df.groupby(['Year', 'Continent'])['Temperature_C'].mean().reset_index()

plt.figure(figsize=(12, 6))
for continent in temp_by_continent['Continent'].unique():
    data = temp_by_continent[temp_by_continent['Continent'] == continent]
    plt.plot(data['Year'], data['Temperature_C'], marker='o', label=continent, linewidth=2)

plt.xlabel('Year')
plt.ylabel('Average Temperature (°C)')
plt.title('Temperature Evolution by Continent (1990-2019)')
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, '03_temp_evolution_by_continent.png'), dpi=300, bbox_inches='tight')
plt.close()

print(f"\nVisualizaciones guardadas en: {FIGURES_DIR}")
print("Archivos creados:")
print("  - 01_top_correlations.png")
print("  - 02_temp_vs_neoplasms.png")
print("  - 03_temp_evolution_by_continent.png")