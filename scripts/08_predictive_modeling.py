import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os

PROJECT_DIR = r'c:\Users\Luis\Desktop\global-weather-analysis'
PROCESSED_DATA_DIR = os.path.join(PROJECT_DIR, 'data', 'processed')
MODELS_DIR = os.path.join(PROJECT_DIR, 'models')
RESULTS_DIR = os.path.join(PROJECT_DIR, 'results')
os.makedirs(MODELS_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, 'integrated_data_1990_2019.csv'))

climate_features = ['Temperature_C', 'Precipitation_mm', 'Surface_Pressure_Pa', 'Dewpoint_K', 'Wind_Speed_ms']
target = 'Neoplasms_Rate_per_100k'

print(f"\nModelo: Predicción de {target}")
print(f"Features climáticos: {climate_features}")

X = df[climate_features]
y = df[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"\nDatos de entrenamiento: {len(X_train)}")
print(f"Datos de prueba: {len(X_test)}")

print("\nEntrenando Random Forest...")
model = RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nResultados del modelo:")
print(f"  MAE: {mae:.2f}")
print(f"  RMSE: {rmse:.2f}")
print(f"  R2 Score: {r2:.3f}")

feature_importance = pd.DataFrame({
    'Feature': climate_features,
    'Importance': model.feature_importances_
}).sort_values('Importance', ascending=False)

print("\nImportancia de features:")
print(feature_importance)

model_file = os.path.join(MODELS_DIR, 'rf_neoplasms_model.pkl')
joblib.dump(model, model_file)
print(f"\nModelo guardado en: {model_file}")

results_df = pd.DataFrame({
    'Actual': y_test,
    'Predicted': y_pred,
    'Error': y_test - y_pred
})

results_file = os.path.join(RESULTS_DIR, 'model_predictions.csv')
results_df.to_csv(results_file, index=False)
print(f"Predicciones guardadas en: {results_file}")