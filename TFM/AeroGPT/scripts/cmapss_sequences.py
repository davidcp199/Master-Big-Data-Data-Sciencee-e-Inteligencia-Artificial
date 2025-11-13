import os
import pandas as pd
import numpy as np
import joblib

# === CONFIGURACIÓN DE RUTAS ===
BASE_PATH = r"C:\Users\David\Documents\Master-Big-Data-Data-Sciencee-e-Inteligencia-Artificial\TFM\AeroGPT\data\CMAPSS"
SCALED_PATH = os.path.join(BASE_PATH, "scaled")
SEQUENCES_PATH = os.path.join(BASE_PATH, "sequences")
os.makedirs(SEQUENCES_PATH, exist_ok=True)

# === PARÁMETROS ===
WINDOW_SIZE = 30  # número de ciclos por secuencia
FEATURES_EXCLUDE = ['unit', 'cycle', 'RUL']

def create_sequences(df, window_size=WINDOW_SIZE):
    """
    Crea secuencias deslizantes de longitud `window_size`.
    Devuelve X (features) y y (RUL) para cada secuencia.
    """
    X = []
    y = []

    feature_cols = df.columns.difference(FEATURES_EXCLUDE)

    # Agrupar por motor
    for unit in df['unit'].unique():
        unit_df = df[df['unit'] == unit].reset_index(drop=True)
        for start in range(len(unit_df) - window_size + 1):
            end = start + window_size
            seq_x = unit_df.loc[start:end-1, feature_cols].values
            seq_y = unit_df.loc[end-1, 'RUL']
            X.append(seq_x)
            y.append(seq_y)

    X = np.array(X)
    y = np.array(y)
    return X, y

def process_fd(fd_number):
    """Procesa un FD normalizado y genera secuencias."""
    print(f"\n--- Generando secuencias FD00{fd_number} ---")
    train_path = os.path.join(SCALED_PATH, f"train_FD00{fd_number}_scaled.csv")
    test_path = os.path.join(SCALED_PATH, f"test_FD00{fd_number}_scaled.csv")

    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)

    X_train, y_train = create_sequences(train_df)
    X_test, y_test = create_sequences(test_df)

    # Guardar secuencias
    np.save(os.path.join(SEQUENCES_PATH, f"X_train_FD00{fd_number}.npy"), X_train)
    np.save(os.path.join(SEQUENCES_PATH, f"y_train_FD00{fd_number}.npy"), y_train)
    np.save(os.path.join(SEQUENCES_PATH, f"X_test_FD00{fd_number}.npy"), X_test)
    np.save(os.path.join(SEQUENCES_PATH, f"y_test_FD00{fd_number}.npy"), y_test)

    print(f"✅ FD00{fd_number}: {X_train.shape[0]} secuencias de entrenamiento, {X_test.shape[0]} secuencias de test generadas.")

    return X_train, y_train, X_test, y_test

# === EJECUCIÓN PRINCIPAL ===
if __name__ == "__main__":
    for fd in [1, 2, 3, 4]:
        X_train, y_train, X_test, y_test = process_fd(fd)
