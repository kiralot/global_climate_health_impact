import xarray as xr
import pandas as pd
import numpy as np
import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
EXTERNAL_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'external')
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'processed')

print("Cargando datos climáticos de ERA5...")

nc_file1 = os.path.join(EXTERNAL_DATA_DIR, 'data_stream-moda_stepType-avgua.nc')
nc_file2 = os.path.join(EXTERNAL_DATA_DIR, 'data_stream-moda_stepType-avgad.nc')

print(f"Archivo 1: {os.path.basename(nc_file1)} ({os.path.getsize(nc_file1) / (1024*1024):.2f} MB)")
print(f"Archivo 2: {os.path.basename(nc_file2)} ({os.path.getsize(nc_file2) / (1024*1024):.2f} MB)")

ds1 = xr.open_dataset(nc_file1)
ds2 = xr.open_dataset(nc_file2)

ds = xr.merge([ds1, ds2], join='outer', compat='override')

print(f"\nDataset combinado - Variables: {list(ds.data_vars)}")

country_coordinates = {
    'Germany': (51.1657, 10.4515),
    'United Kingdom': (55.3781, -3.4360),
    'France': (46.2276, 2.2137),
    'Italy': (41.8719, 12.5674),
    'Spain': (40.4637, -3.7492),
    'Poland': (51.9194, 19.1451),
    'Netherlands': (52.1326, 5.2913),
    'Belgium': (50.5039, 4.4699),
    'Greece': (39.0742, 21.8243),
    'Portugal': (39.3999, -8.2245),
    'China': (35.8617, 104.1954),
    'India': (20.5937, 78.9629),
    'Japan': (36.2048, 138.2529),
    'Indonesia': (-0.7893, 113.9213),
    'Pakistan': (30.3753, 69.3451),
    'Bangladesh': (23.6850, 90.3563),
    'Russia': (61.5240, 105.3188),
    'Turkey': (38.9637, 35.2433),
    'Iran': (32.4279, 53.6880),
    'Thailand': (15.8700, 100.9925),
    'United States': (37.0902, -95.7129),
    'Brazil': (-14.2350, -51.9253),
    'Mexico': (23.6345, -102.5528),
    'Canada': (56.1304, -106.3468),
    'Argentina': (-38.4161, -63.6167),
    'Colombia': (4.5709, -74.2973),
    'Peru': (-9.1900, -75.0152),
    'Venezuela': (6.4238, -66.5897),
    'Chile': (-35.6751, -71.5430),
    'Ecuador': (-1.8312, -78.1834),
    'Nigeria': (9.0820, 8.6753),
    'Ethiopia': (9.1450, 40.4897),
    'Egypt': (26.8206, 30.8025),
    'South Africa': (-30.5595, 22.9375),
    'Tanzania': (-6.3690, 34.8888),
    'Kenya': (-0.0236, 37.9062),
    'Algeria': (28.0339, 1.6596),
    'Sudan': (12.8628, 30.2176),
    'Uganda': (1.3733, 32.2903),
    'Australia': (-25.2744, 133.7751),
    'Papua New Guinea': (-6.3150, 143.9555),
    'New Zealand': (-40.9006, 174.8860),
    'Fiji': (-17.7134, 178.0650),
    'Solomon Islands': (-9.6457, 160.1562),
    'Samoa': (-13.7590, -172.1046),
    'Vanuatu': (-15.3767, 166.9592),
    'Kiribati': (-3.3704, -168.7340),
    'Tonga': (-21.1790, -175.1982),
    'Micronesia': (7.4256, 150.5508)
}

print("\nExtrayendo datos por país...")
climate_data = []

for country, (lat, lon) in country_coordinates.items():
    print(f"Procesando {country}...")
    
    point_data = ds.sel(latitude=lat, longitude=lon, method='nearest')
    
    df_country = point_data.to_dataframe().reset_index()
    df_country['Country/Territory'] = country
    
    climate_data.append(df_country)

climate_df = pd.concat(climate_data, ignore_index=True)

climate_df['Year'] = pd.to_datetime(climate_df['valid_time']).dt.year
climate_df['Month'] = pd.to_datetime(climate_df['valid_time']).dt.month

climate_annual = climate_df.groupby(['Country/Territory', 'Year']).agg({
    't2m': 'mean',
    'tp': 'sum',
    'sp': 'mean',
    'd2m': 'mean',
    'u10': 'mean',
    'v10': 'mean'
}).reset_index()

climate_annual.columns = ['Country/Territory', 'Year', 'Temperature_K', 'Precipitation_m', 
                          'Surface_Pressure_Pa', 'Dewpoint_K', 'Wind_U', 'Wind_V']

climate_annual['Temperature_C'] = climate_annual['Temperature_K'] - 273.15
climate_annual['Precipitation_mm'] = climate_annual['Precipitation_m'] * 1000
climate_annual['Wind_Speed_ms'] = np.sqrt(climate_annual['Wind_U']**2 + climate_annual['Wind_V']**2)

climate_final = climate_annual[['Country/Territory', 'Year', 'Temperature_C', 
                                 'Precipitation_mm', 'Surface_Pressure_Pa', 
                                 'Dewpoint_K', 'Wind_Speed_ms']]

print(f"\nDatos climáticos procesados:")
print(f"Registros: {len(climate_final)}")
print(f"Países: {climate_final['Country/Territory'].nunique()}")
print(f"Años: {climate_final['Year'].min()} - {climate_final['Year'].max()}")
print(f"\nPrimeras filas:")
print(climate_final.head())

output_file = os.path.join(PROCESSED_DATA_DIR, 'climate_annual_1990_2019.csv')
climate_final.to_csv(output_file, index=False)

print(f"\nArchivo guardado en: {output_file}")

ds1.close()
ds2.close()