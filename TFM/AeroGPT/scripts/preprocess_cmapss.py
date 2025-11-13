import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# === CONFIGURACIÓN DE RUTAS ===
BASE_PATH = r"C:\Users\David\Documents\Master-Big-Data-Data-Sciencee-e-Inteligencia-Artificial\TFM\AeroGPT\data\CMAPSS"
RAW_PATH = os.path.join(BASE_PATH, "raw")
PROCESSED_PATH = os.path.join(BASE_PATH, "processed")
os.makedirs(PROCESSED_PATH, exist_ok=True)

# === COLUMNAS CMAPSS ===
columns = ['unit', 'cycle'] + [f'op_setting_{i}' for i in range(1,4)] + [f'sensor_{i}' for i in range(1,22)]

# === FUNCIONES DE CARGA Y VERIFICACIÓN ===
def load_fd(fd_number):
    train_path = os.path.join(RAW_PATH, f"train_FD00{fd_number}.txt")
    test_path  = os.path.join(RAW_PATH, f"test_FD00{fd_number}.txt")
    rul_path   = os.path.join(RAW_PATH, f"RUL_FD00{fd_number}.txt")
    
    train = pd.read_csv(train_path, sep=r'\s+', header=None, names=columns, engine='python')
    test  = pd.read_csv(test_path, sep=r'\s+', header=None, names=columns, engine='python')
    rul   = pd.read_csv(rul_path, header=None, names=['RUL'])
    
    # Eliminar última columna si está vacía
    if train.iloc[:, -1].isna().all():
        train = train.iloc[:, :-1]
    if test.iloc[:, -1].isna().all():
        test = test.iloc[:, :-1]
    
    return train, test, rul

def verify_df(train, test):
    print(f"Train shape: {train.shape}, Test shape: {test.shape}")
    total_nulls = train.isnull().sum().sum() + test.isnull().sum().sum()
    print(f"Valores nulos totales: {total_nulls}")
    if train.shape[1] != 26:
        print(f"¡Atención! Número de columnas inesperado: {train.shape[1]}")

# === CALCULO DE RUL ===
def add_rul(df, rul_df=None):
    if rul_df is None:
        max_cycle = df.groupby('unit')['cycle'].max().reset_index()
        max_cycle.columns = ['unit', 'max_cycle']
        df = df.merge(max_cycle, on='unit', how='left')
        df['RUL'] = df['max_cycle'] - df['cycle']
        df.drop(columns=['max_cycle'], inplace=True)
    else:
        max_cycle = df.groupby('unit')['cycle'].max().reset_index()
        max_cycle.columns = ['unit', 'max_cycle']
        df = df.merge(max_cycle, on='unit', how='left')
        # CORRECCIÓN AQUÍ
        df = df.merge(rul_df, left_on='unit', right_index=True, how='left')
        df['RUL'] = df['RUL'].values - df['cycle']
        df.drop(columns=['max_cycle'], inplace=True)
    return df


# === NORMALIZACIÓN ===
def normalize_features(train, test):
    feature_cols = train.columns.difference(['unit','cycle','RUL'])
    scaler = MinMaxScaler()
    train[feature_cols] = scaler.fit_transform(train[feature_cols])
    test[feature_cols]  = scaler.transform(test[feature_cols])
    return train, test, feature_cols

# === GENERACIÓN DE SECUENCIAS ===
def create_sequences(df, window_size=30):
    feature_cols = df.columns.difference(['unit','cycle','RUL'])
    X, y = [], []
    for unit in df['unit'].unique():
        unit_df = df[df['unit']==unit].reset_index(drop=True)
        for start in range(len(unit_df)-window_size+1):
            end = start + window_size
            X.append(unit_df.loc[start:end-1, feature_cols].values)
            y.append(unit_df.loc[end-1, 'RUL'])
    return np.array(X), np.array(y)

# === GUARDAR DATA ===
def save_processed(fd, X_train, y_train, X_test, y_test):
    np.save(os.path.join(PROCESSED_PATH, f'X_train_FD00{fd}.npy'), X_train)
    np.save(os.path.join(PROCESSED_PATH, f'y_train_FD00{fd}.npy'), y_train)
    np.save(os.path.join(PROCESSED_PATH, f'X_test_FD00{fd}.npy'), X_test)
    np.save(os.path.join(PROCESSED_PATH, f'y_test_FD00{fd}.npy'), y_test)
    print(f"FD00{fd} secuencias guardadas en 'processed/'")

# === SCRIPT PRINCIPAL ===
if __name__ == "__main__":
    for fd in [1,2,3,4]:
        print(f"\n=== Procesando FD00{fd} ===")
        train, test, rul = load_fd(fd)
        verify_df(train, test)
        
        # Calcular RUL real
        train = add_rul(train)
        test  = add_rul(test, rul)
        
        # Normalización
        train, test, feature_cols = normalize_features(train, test)
        
        # Generar secuencias
        X_train, y_train = create_sequences(train)
        X_test, y_test   = create_sequences(test)
        
        # Guardar secuencias
        save_processed(fd, X_train, y_train, X_test, y_test)
