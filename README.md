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
│   ├── 08_predictive_modeling.py     # Modelo Random Forest
│   └── 09_temporal_prediction_model.py  # Modelo Prophet (predicciones 2020-2030)
├── dashboard/                    # Dashboard interactivo
│   └── app.py                    # Aplicación Streamlit
├── models/                       # Modelos ML entrenados
│   └── rf_neoplasms_model.pkl
├── results/                      # Resultados y visualizaciones
│   ├── climate_mortality_correlations.csv
│   ├── model_predictions.csv
│   ├── temporal_predictions.csv      # Predicciones 2020-2030 (Prophet)
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

# 9. Generar predicciones temporales 2020-2030
python scripts/09_temporal_prediction_model.py
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
   - Posible influencia de factores socioeconómicos (países desarrollados tienen clima templado)

2. **Temperatura y Enfermedades Cardiovasculares**: r = -0.70
   - Relación inversa significativa
   - Países más fríos muestran mayores tasas de mortalidad cardiovascular

3. **Temperatura y Enfermedad de Parkinson**: r = -0.61
   - Correlación moderada-fuerte negativa

4. **Precipitación y Ahogamientos**: r = 0.46
   - Correlación positiva moderada (esperada)

5. **Temperatura y Trastornos Maternos**: r = 0.46
   - Correlación positiva en países más cálidos

### Modelos Predictivos

#### 1. Random Forest - Predicción Espacial (Cross-sectional)

**Objetivo**: Predecir mortalidad por cáncer basándose en condiciones climáticas

**Rendimiento del modelo:**
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

**Interpretación**: La temperatura es por mucho el predictor más importante, sugiriendo que diferencias climáticas (o sus proxies socioeconómicos) explican gran parte de la variabilidad en tasas de cáncer entre países.

#### 2. Prophet - Predicciones Temporales (Time Series)

**Objetivo**: Predecir evolución de mortalidad por 10 causas principales del 2020 al 2030

**Configuración del modelo:**
- **Algoritmo**: Facebook Prophet con regresores climáticos
- **Datos de entrenamiento**: 1990-2019 (30 años)
- **Horizonte de predicción**: 2020-2030 (11 años)
- **Regresores adicionales**: Temperature_C, Precipitation_mm, Surface_Pressure_Pa, Dewpoint_K, Wind_Speed_ms

**Cobertura de predicciones:**
- **Total de predicciones**: 880 (8 países × 10 causas × 11 años)
- **Países**: United States, Germany, China, Brazil, India, Nigeria, Australia, Japan
- **Top 10 causas por mortalidad total**:
  1. Cardiovascular Diseases (349M muertes)
  2. Neoplasms (190M muertes)
  3. Chronic Respiratory Diseases (91M muertes)
  4. Digestive Diseases (68M muertes)
  5. Neonatal Disorders (62M muertes)
  6. Alzheimer's Disease and Dementias (53M muertes)
  7. Diabetes Mellitus (45M muertes)
  8. Lower Respiratory Infections (43M muertes)
  9. Diarrheal Diseases (40M muertes)
  10. Chronic Kidney Disease (28M muertes)

**Ejemplo de proyecciones** (Estados Unidos - Enfermedades Cardiovasculares):
- 2019 (último histórico): 961,668 muertes
- 2020 (primera predicción): 974,234 muertes
- 2030 (proyección final): 1,125,584 muertes
- Tendencia: Aumento del 17% en la década

**Características del modelo Prophet:**
- Captura tendencias de largo plazo
- Intervalos de confianza del 95% para cada predicción
- Incorpora efectos de cambio climático mediante regresores
- Extrapolación lineal de tendencias climáticas observadas

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

El dashboard interactivo incluye 6 módulos principales:

### Overview
- Métricas globales del dataset
- Estadísticas de 49 países y 30 años de datos
- Muestra de datos procesados

### Climate Trends
- Evolución temporal de variables climáticas
- Gráficos interactivos por país/continente
- Análisis de temperatura, precipitación, presión, viento

### Mortality Analysis
- Tendencias de mortalidad por causa de muerte
- Comparativas entre países
- Visualización de las 31 causas de muerte analizadas

### Correlations
- Top 20 correlaciones clima-mortalidad
- Matriz de correlación interactiva
- Scatter plots con líneas de tendencia
- Identificación de relaciones clave

### Predictions 2020-2030
- **Modelo Prophet** para forecasting temporal
- Predicciones de mortalidad por 10 causas principales
- 8 países analizados: USA, Germany, China, Brazil, India, Nigeria, Australia, Japan
- Intervalos de confianza del 95%
- Gráficos históricos (1990-2019) vs predicciones (2020-2030)
- Métricas de tendencia y cambio porcentual
- Incorpora regresores climáticos (temperatura, precipitación, presión, punto de rocío, viento)

### ML Model Analysis
- **Random Forest Regressor** para predicción de cáncer basada en clima
- Métricas del modelo: MAE, RMSE, R² Score
- Feature Importance: qué variables climáticas son más predictivas
- Scatter plot: Predicciones vs Valores Reales
- Distribución de errores del modelo
- **Predictor Interactivo**: Ajusta variables climáticas y obtén predicciones en tiempo real

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

1. **La temperatura es el predictor climático más importante** de tasas de mortalidad (67.6% de importancia en el modelo Random Forest)

2. **Relación inversa temperatura-mortalidad**: Los países con temperaturas más altas tienden a tener menores tasas de mortalidad por enfermedades crónicas (cáncer, cardiovasculares, Alzheimer)

3. **Posible confusión con desarrollo socioeconómico**: La correlación negativa puede reflejar que países de clima templado/frío tienen mayor desarrollo industrial, mejor acceso a salud, pero también mayor esperanza de vida (más tiempo para desarrollar enfermedades crónicas)

4. **Variables climáticas extremas**: La precipitación muestra correlación directa con ahogamientos, como era de esperar

5. **Modelos altamente predictivos**: 
   - Random Forest alcanza R² = 0.97 para predicción espacial
   - Prophet captura tendencias temporales con intervalos de confianza robustos

6. **Proyecciones 2020-2030**: Las predicciones de Prophet sugieren aumentos sostenidos en mortalidad por enfermedades cardiovasculares y cáncer en países desarrollados, consistente con envejecimiento poblacional

7. **Complementariedad de modelos**: Random Forest explica diferencias entre países (análisis espacial), mientras Prophet predice evolución temporal (análisis longitudinal)

### Limitaciones

- Las correlaciones no implican causalidad directa
- Falta incorporar datos de contaminación atmosférica (PM2.5, NO₂, O₃)
- No se controlan variables socioeconómicas directamente (GDP, HDI, urbanización)
- Análisis agregado por año (se pierde variabilidad estacional y mensual)
- Predicciones de Prophet asumen continuidad de tendencias sin eventos disruptivos
- No se modelan políticas de salud pública o cambios demográficos abruptos

## Próximos Pasos

### Mejoras Planificadas

1. **Incorporar datos de calidad del aire**: PM2.5, PM10, NO₂, O₃, CO, SO₂ desde OpenAQ o CAMS
2. **Modelos de causalidad**: Inferencia causal (DoWhy, CausalML) para identificar relaciones directas vs correlaciones espurias
3. **Análisis geoespacial**: Mapas interactivos con Folium/Plotly mostrando patrones geográficos
4. **Más algoritmos de ML**: XGBoost, LightGBM, redes neuronales (LSTM para series temporales)
5. **Análisis estacional**: Descomposición temporal mensual, efectos de estacionalidad en mortalidad
6. **Variables socioeconómicas**: GDP, HDI, urbanización, políticas ambientales, gasto en salud
7. **Jupyter Notebooks**: Análisis paso a paso reproducible para fines educativos
8. **Reporte técnico PDF**: Metodología completa, resultados, interpretaciones estadísticas
9. **Tests unitarios**: Cobertura de funciones críticas de procesamiento y modelado
10. **Power BI Dashboard**: Dashboard alternativo para stakeholders empresariales

## Tecnologías Utilizadas

### Core
- **Python 3.11**: Lenguaje principal

### Data Processing
- **Pandas**: Procesamiento y manipulación de dataframes
- **NumPy**: Cálculos numéricos y arrays multidimensionales
- **XArray**: Manejo eficiente de archivos NetCDF (datos climáticos)

### Machine Learning
- **Scikit-learn**: Random Forest, métricas de evaluación (MAE, RMSE, R²)
- **Prophet**: Series temporales, forecasting 2020-2030 con regresores
- **Joblib**: Serialización y carga de modelos entrenados

### Visualización
- **Matplotlib**: Visualizaciones estáticas, gráficos de alta calidad
- **Seaborn**: Gráficos estadísticos avanzados
- **Plotly**: Visualizaciones interactivas (scatter, line, bar charts) con hover
- **Streamlit**: Framework para dashboard web interactivo y responsivo

### Data Sources
- **CDS API**: Descarga automatizada de datos ERA5 desde Copernicus Climate Data Store

## Características Destacadas del Proyecto

- **Pipeline completo end-to-end**: Desde descarga de datos hasta dashboard interactivo
- **Múltiples fuentes de datos**: Integración de datos climáticos (ERA5), mortalidad (OWID), y población (World Bank)
- **Dos enfoques de ML complementarios**: 
  - Random Forest para análisis espacial (cross-sectional)
  - Prophet para análisis temporal (time series forecasting)
- **Dashboard profesional**: Interfaz dark theme con animaciones, 6 módulos interactivos
- **880 predicciones futuras**: Forecasting de mortalidad 2020-2030 para 8 países y 10 causas
- **Predictor interactivo**: Ajusta condiciones climáticas y obtén predicciones en tiempo real
- **Reproducibilidad**: Scripts numerados, documentación completa, requirements.txt
- **Escalabilidad**: Fácil agregar más países, variables o modelos
- **Deployment ready**: Compatible con Streamlit Cloud para hosting gratuito

## Autor

**Luis Ignacio**

## Licencia

MIT License

---

## Referencias

- ERA5 Reanalysis: [Copernicus Climate Data Store](https://cds.climate.copernicus.eu/)
- Mortality Data: [Our World in Data](https://ourworldindata.org/)
- Population Data: [World Bank](https://data.worldbank.org/)
