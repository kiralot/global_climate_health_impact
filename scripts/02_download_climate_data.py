import os
import sys
import cdsapi
import subprocess
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
EXTERNAL_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'external')

os.makedirs(EXTERNAL_DATA_DIR, exist_ok=True)

cdsapirc_path = os.path.join(os.path.expanduser("~"), ".cdsapirc")
if os.path.exists(cdsapirc_path):
    print(f"Archivo .cdsapirc encontrado en: {cdsapirc_path}")
else:
    print(f"ERROR: Archivo .cdsapirc NO encontrado en: {cdsapirc_path}")
    sys.exit(1)

try:
    c = cdsapi.Client()
    print("Cliente CDS inicializado correctamente")
except Exception as e:
    print(f"ERROR al inicializar cliente CDS: {e}")
    sys.exit(1)

output_file = os.path.join(EXTERNAL_DATA_DIR, 'era5_climate_data_1990_2019.nc')

try:
    c.retrieve(
        'reanalysis-era5-single-levels-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': [
                '2m_temperature',
                'total_precipitation',
                'surface_pressure',
                '2m_dewpoint_temperature',
                '10m_u_component_of_wind',
                '10m_v_component_of_wind'
            ],
            'year': [str(year) for year in range(1990, 2020)],
            'month': [f'{month:02d}' for month in range(1, 13)],
            'time': '00:00',
            'format': 'netcdf'
        },
        output_file
    )
    print(f"\nDatos climáticos descargados en: {output_file}")
except Exception as e:
    print(f"\nERROR durante la descarga: {e}")
    sys.exit(1)