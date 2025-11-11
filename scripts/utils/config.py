"""
Configuración global del proyecto
"""
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(PROJECT_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')
EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, 'external')
RESULTS_DIR = os.path.join(PROJECT_DIR, 'results')
FIGURES_DIR = os.path.join(RESULTS_DIR, 'figures')
REPORTS_DIR = os.path.join(RESULTS_DIR, 'reports')
MODELS_DIR = os.path.join(PROJECT_DIR, 'models')

CDS_URL = os.getenv('CDS_URL')
CDS_API_KEY = os.getenv('CDS_API_KEY')

YEAR_START = 1990
YEAR_END = 2019

CONTINENTS = {
    'Europe': ['Germany', 'United Kingdom', 'France', 'Italy', 'Spain', 'Poland', 'Netherlands', 'Belgium', 'Greece', 'Portugal'],
    'Asia': ['China', 'India', 'Japan', 'Indonesia', 'Pakistan', 'Bangladesh', 'Russia', 'Turkey', 'Iran', 'Thailand'],
    'Americas': ['United States', 'Brazil', 'Mexico', 'Canada', 'Argentina', 'Colombia', 'Peru', 'Venezuela', 'Chile', 'Ecuador'],
    'Africa': ['Nigeria', 'Ethiopia', 'Egypt', 'Democratic Republic of Congo', 'South Africa', 'Tanzania', 'Kenya', 'Algeria', 'Sudan', 'Uganda'],
    'Oceania': ['Australia', 'Papua New Guinea', 'New Zealand', 'Fiji', 'Solomon Islands', 'Samoa', 'Vanuatu', 'Kiribati', 'Tonga', 'Micronesia']
}

RESPIRATORY_DISEASES = [
    'Lower Respiratory Infections',
    'Chronic Respiratory Diseases',
    'Tuberculosis'
]

POPULATION_RATE = 100000
