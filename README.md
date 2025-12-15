# Impacto del Cambio Climático en la Calidad del Aire y la Salud

Análisis de cómo las variaciones climáticas y las políticas medioambientales han afectado la calidad del aire y la salud pública en distintos países durante 1990-2019.

## Estructura del Proyecto

```
global-weather-analysis/
├── data/
│   ├── raw/                      # Datos originales sin procesar
│   ├── processed/                # Datos procesados y limpios
│   │   ├── deaths_selected_countries.csv
│   │   ├── population_annual_1990_2019.csv
│   │   ├── climate_annual_1990_2019.csv
│   │   └── integrated_data_1990_2019.csv
│   └── external/                 # Datos climáticos de Copernicus
├── scripts/                      # Scripts de procesamiento
│   ├── 01_select_countries.py   # Selección de 49 países (10 por continente)
│   ├── 02_download_climate_data.py  # Descarga datos ERA5
│   ├── 03_process_population_data.py  # Procesa datos de población
│   ├── 04_process_climate_data.py    # Extrae variables climáticas
│   ├── 05_integrate_datasets.py      # Integra y calcula tasas
│   ├── 06_exploratory_analysis.py    # Análisis de correlaciones
│   ├── 07_create_visualizations.py   # Genera gráficos
│   └── 08_predictive_modeling.py     # Modelo Random Forest
├── dashboard/                    # Dashboard interactivo
│   └── app.py                    # Aplicación Streamlit
├── models/                       # Modelos ML entrenados
│   └── rf_neoplasms_model.pkl
├── results/                      # Resultados y visualizaciones
│   ├── climate_mortality_correlations.csv
│   ├── model_predictions.csv
│   └── figures/
│       ├── 01_top_correlations.png
│       ├── 02_temp_vs_neoplasms.png
│       └── 03_temp_evolution_by_continent.png
├── .gitignore
├── requirements.txt
└── README.md
```

## Objetivos

1. Analizar la evolución temporal de variables climáticas (1990-2019)
2. Correlacionar niveles climáticos con tasas de mortalidad
3. Explorar efectos sobre la salud pública por causa de muerte
4. Predecir tasas de mortalidad mediante modelos de Machine Learning
5. Crear un dashboard interactivo para comparar países y continentes

## Datos

### Fuentes de Datos

- **Mortalidad por causas**: Our World in Data (1990-2019, 204 países)
- **Población**: World Bank Annual Population Data
- **Variables climáticas**: ERA5 Reanalysis (Copernicus Climate Data Store)

### Países Seleccionados

**49 países distribuidos por continente:**

- **Europa (10)**: Alemania, Reino Unido, Francia, Italia, España, Polonia, Países Bajos, Bélgica, Grecia, Portugal
- **Asia (10)**: China, India, Japón, Indonesia, Pakistán, Bangladesh, Rusia, Turquía, Irán, Tailandia
- **América (10)**: Estados Unidos, Brasil, México, Canadá, Argentina, Colombia, Perú, Venezuela, Chile, Ecuador
- **África (9)**: Nigeria, Etiopía, Egipto, Sudáfrica, Tanzania, Kenia, Argelia, Sudán, Uganda
- **Oceanía (10)**: Australia, Papúa Nueva Guinea, Nueva Zelanda, Fiyi, Islas Salomón, Samoa, Vanuatu, Kiribati, Tonga, Micronesia

### Variables Climáticas

- Temperatura superficial (°C)
- Precipitación total (mm)
- Presión superficial (Pa)
- Punto de rocío (K)
- Velocidad del viento (m/s)

### Causas de Muerte Analizadas

31 causas incluyendo:
- Neoplasms (cáncer)
- Enfermedades cardiovasculares
- Enfermedades respiratorias
- Alzheimer y demencias
- Diabetes
- Enfermedades infecciosas
- Entre otras

## Instalación

### Requisitos Previos

- Python 3.11 o superior
- Cuenta en Copernicus Climate Data Store (CDS)

### Pasos de Instalación

1. **Clonar el repositorio:**

```bash
git clone https://github.com/tu-usuario/global-weather-analysis.git
cd global-weather-analysis
```

2. **Instalar dependencias:**

```bash
pip install -r requirements.txt
```

3. **Configurar credenciales de Copernicus CDS:**

Crea un archivo `.env` en la raíz del proyecto:

```
CDS_URL=https://cds.climate.copernicus.eu/api
CDS_API_KEY=tu_api_key_aqui
```

O crea el archivo `.cdsapirc` en tu directorio home:

```
url: https://cds.climate.copernicus.eu/api
key: tu_api_key_aqui
```

**Nota:** El archivo `.env` está incluido en `.gitignore` y no se subirá a GitHub.

## Uso

### Pipeline Completo de Procesamiento

Ejecuta los scripts en orden:

```bash
# 1. Seleccionar países para análisis
python scripts/01_select_countries.py

# 2. Descargar datos climáticos (tarda 10-30 minutos)
python scripts/02_download_climate_data.py

# 3. Procesar datos de población
python scripts/03_process_population_data.py

# 4. Procesar datos climáticos
python scripts/04_process_climate_data.py

# 5. Integrar datasets y calcular tasas por 100k habitantes
python scripts/05_integrate_datasets.py

# 6. Análisis exploratorio y correlaciones
python scripts/06_exploratory_analysis.py

# 7. Crear visualizaciones
python scripts/07_create_visualizations.py

# 8. Entrenar modelo predictivo
python scripts/08_predictive_modeling.py
```

### Ejecutar Dashboard Interactivo

```bash
streamlit run dashboard/app.py
```

El dashboard se abrirá automáticamente en `http://localhost:8501`

## Resultados Principales

### Correlaciones Clima-Mortalidad

**Hallazgos clave:**

1. **Temperatura y Cáncer (Neoplasms)**: Correlación negativa fuerte (r = -0.73)
   - Temperaturas más altas se asocian con menores tasas de mortalidad por cáncer
   - Posible influencia de factores socioeconómicos

2. **Temperatura y Enfermedades Cardiovasculares**: r = -0.70
   - Relación inversa significativa

3. **Temperatura y Enfermedad de Parkinson**: r = -0.61
   - Correlación moderada-fuerte negativa

4. **Precipitación y Ahogamientos**: r = 0.46
   - Correlación positiva moderada

5. **Temperatura y Trastornos Maternos**: r = 0.46
   - Correlación positiva en países más cálidos

### Modelo Predictivo

**Random Forest para predicción de mortalidad por cáncer:**

- **R² Score**: 0.970 (explica el 97% de la varianza)
- **MAE**: 10.81 muertes por 100,000 habitantes
- **RMSE**: 15.46

**Importancia de variables climáticas:**

| Variable | Importancia |
|----------|-------------|
| Temperatura | 67.6% |
| Presión superficial | 27.0% |
| Punto de rocío | 2.2% |
| Velocidad del viento | 1.7% |
| Precipitación | 1.5% |

### Estadísticas del Dataset

- **Total de registros**: 1,470 (49 países × 30 años)
- **Temperatura promedio global**: 18.9°C
- **Rango de temperatura**: -7.8°C a 28.6°C
- **Precipitación promedio**: 34.8 mm/mes
- **Población total analizada**: ~5.2 mil millones (promedio)

## Dashboard

### 🌐 Demo Online

**[Ver Dashboard en vivo →](https://tu-url-aqui.streamlit.app)**

### Local

```bash
streamlit run dashboard/app.py
```

El dashboard interactivo incluye 5 módulos principales:

### 📊 Overview
- Métricas globales del dataset
- Tendencias de temperatura y población
- Estadísticas descriptivas

### 🌡️ Climate Analysis
- Evolución temporal de variables climáticas
- Distribución por país/continente
- Cambios año a año

### 💀 Mortality Trends
- Tendencias de mortalidad por causa
- Ranking de países por tasa de mortalidad
- Comparativas temporales

### 🔗 Correlations
- Top correlaciones clima-mortalidad
- Matriz de correlación interactiva
- Gráficos de dispersión

### 🤖 ML Predictions
- Métricas del modelo Random Forest
- Importancia de features
- Comparación predicciones vs valores reales

## Deployment

### Opción 1: Local

```bash
streamlit run dashboard/app.py
```

### Opción 2: Streamlit Cloud (Gratuito)

1. Sube el proyecto a GitHub
2. Ve a https://streamlit.io/cloud
3. Inicia sesión con GitHub
4. Click en "New app"
5. Selecciona tu repositorio
6. Main file path: `dashboard/app.py`
7. Click "Deploy"

**Nota:** Asegúrate de que los archivos procesados estén en el repositorio.

## Visualizaciones Generadas

El proyecto genera las siguientes visualizaciones en `results/figures/`:

1. **01_top_correlations.png**: Top 20 correlaciones clima-mortalidad
2. **02_temp_vs_neoplasms.png**: Scatter plot temperatura vs mortalidad por cáncer
3. **03_temp_evolution_by_continent.png**: Evolución de temperatura por continente

## Conclusiones

### Principales Hallazgos

1. **La temperatura es el predictor climático más importante** de tasas de mortalidad (67.6% de importancia en el modelo)

2. **Relación inversa temperatura-mortalidad**: Los países con temperaturas más altas tienden a tener menores tasas de mortalidad por enfermedades crónicas (cáncer, cardiovasculares, Alzheimer)

3. **Posible confusión con desarrollo socioeconómico**: La correlación negativa puede reflejar que países de clima templado/frío tienen mayor desarrollo industrial, mejor acceso a salud, pero también mayor esperanza de vida (más tiempo para desarrollar enfermedades crónicas)

4. **Variables climáticas extremas**: La precipitación muestra correlación directa con ahogamientos, como era de esperar

5. **Modelo altamente predictivo**: El Random Forest alcanza un R² de 0.97, sugiriendo que las variables climáticas (o sus proxies socioeconómicos) son excelentes predictores de tasas de mortalidad

### Limitaciones

- Las correlaciones no implican causalidad
- Falta incorporar datos de contaminación atmosférica (PM2.5, NO₂, O₃)
- No se controlan variables socioeconómicas directamente
- Análisis agregado por año (se pierde variabilidad estacional)

## Próximos Pasos

1. **Incorporar datos de calidad del aire**: PM2.5, PM10, NO₂, O₃, CO, SO₂
2. **Análisis de series temporales**: Modelos ARIMA, Prophet para predicciones
3. **Modelos de causalidad**: Inferencia causal para identificar relaciones directas
4. **Análisis geoespacial**: Mapas interactivos con Folium/Plotly
5. **Más algoritmos de ML**: XGBoost, redes neuronales, ensemble methods
6. **Análisis estacional**: Descomposición temporal mensual
7. **Variables socioeconómicas**: GDP, HDI, urbanización, políticas ambientales

## Tecnologías Utilizadas

- **Python 3.11**
- **Pandas**: Procesamiento de datos
- **NumPy**: Cálculos numéricos
- **XArray**: Manejo de archivos NetCDF
- **Scikit-learn**: Modelos de Machine Learning
- **Matplotlib/Seaborn**: Visualizaciones estáticas
- **Plotly**: Visualizaciones interactivas
- **Streamlit**: Dashboard web interactivo
- **CDS API**: Descarga de datos climáticos

## Autor

**Ignacio**

## Licencia

MIT License

---

## Referencias

- ERA5 Reanalysis: [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
- Mortality Data: [Our World in Data](https://ourworldindata.org/)
- Population Data: [World Bank](https://data.worldbank.org/)
