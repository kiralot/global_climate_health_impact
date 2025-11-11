import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
EXTERNAL_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'external')

nc_file = os.path.join(EXTERNAL_DATA_DIR, 'era5_climate_data_1990_2019.nc')

print(f"Verificando archivo: {nc_file}")
print(f"Existe: {os.path.exists(nc_file)}")

if os.path.exists(nc_file):
    file_size = os.path.getsize(nc_file)
    print(f"Tamaño: {file_size / (1024*1024):.2f} MB")
    
    with open(nc_file, 'rb') as f:
        first_bytes = f.read(100)
        print(f"Primeros bytes: {first_bytes[:50]}")