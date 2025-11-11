import zipfile
import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
EXTERNAL_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'external')

zip_file = os.path.join(EXTERNAL_DATA_DIR, 'era5_climate_data_1990_2019.nc')
extract_dir = EXTERNAL_DATA_DIR

print(f"Descomprimiendo archivo: {zip_file}")
print(f"Tamaño del archivo: {os.path.getsize(zip_file) / (1024*1024):.2f} MB\n")

with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    file_list = zip_ref.namelist()
    print(f"Archivos en el ZIP:")
    for file in file_list:
        print(f"  - {file}")
    
    print(f"\nExtrayendo archivos a: {extract_dir}")
    zip_ref.extractall(extract_dir)

print("\nExtracción completada.")
print(f"Archivos extraídos en: {extract_dir}")

extracted_files = [f for f in os.listdir(extract_dir) if f.endswith(('.nc', '.grib'))]
print(f"\nArchivos NetCDF/GRIB encontrados:")
for file in extracted_files:
    file_path = os.path.join(extract_dir, file)
    print(f"  - {file} ({os.path.getsize(file_path) / (1024*1024):.2f} MB)")