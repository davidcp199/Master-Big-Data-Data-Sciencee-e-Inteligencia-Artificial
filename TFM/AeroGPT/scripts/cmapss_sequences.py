import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# === Configuración de rutas ===
BASE_PATH = r"C:\Users\David\Documents\Master-Big-Data-Data-Sciencee-e-Inteligencia-Artificial\TFM\AeroGPT\data\CMAPSS"
PROCESSED_PATH = os.path.join(BASE_PATH, "processed")
os.makedirs(PROCESSED_PATH, exist_ok=True)

datasets = ['FD001', 'FD002', 'FD003', 'FD004']

# === Parámetros para generación de secuencias ===
WINDOW_SIZE = 30

for ds in datasets:
    for split in ['Train', 'Test']:
        # --- Lectura de datos cleaned ---
        input_file = os.path.join(PROCESSED_PATH, f"{ds}_{split}_Cleaned.xlsx")
        print(f"\nLeyendo {input_file} para normalización y secuencias...")

        df = pd.read_excel(input_file)

        # --- Normalización ---
        feature_cols = [c for c in df.columns if c.startswith('setting_') or c.startswith('sensor_')]
        scaler = MinMaxScaler()
        df[feature_cols] = scaler.fit_transform(df[feature_cols])
        print(f"Columnas normalizadas: {feature_cols}")

        # --- Guardar versión normalizada ---
        normalized_file = os.path.join(PROCESSED_PATH, f"{ds}_{split}_Normalized.xlsx")
        df.to_excel(normalized_file, index=False)
        print(f"Archivo normalizado guardado: {normalized_file}")

        # --- Generación de secuencias 3D para LSTM ---
        X, y = [], []
        for unit in df['unit'].unique():
            unit_df = df[df['unit'] == unit].reset_index(drop=True)
            for start in range(len(unit_df) - WINDOW_SIZE + 1):
                end = start + WINDOW_SIZE
                seq_x = unit_df.loc[start:end-1, feature_cols].values
                seq_y = unit_df.loc[end-1, 'RUL']
                X.append(seq_x)
                y.append(seq_y)

        X = np.array(X)  # shape: (n_muestras, window_size, n_features)
        y = np.array(y)  # shape: (n_muestras,)
        print(f"Secuencias generadas para {ds}_{split}: {X.shape[0]} muestras, ventana {WINDOW_SIZE}, {X.shape[2]} features")

        # --- Guardar secuencias como npy para LSTM ---
        np.save(os.path.join(PROCESSED_PATH, f"{ds}_{split}_X.npy"), X)
        np.save(os.path.join(PROCESSED_PATH, f"{ds}_{split}_y.npy"), y)
        print(f"Secuencias guardadas en .npy: {ds}_{split}_X.npy / {ds}_{split}_y.npy")
