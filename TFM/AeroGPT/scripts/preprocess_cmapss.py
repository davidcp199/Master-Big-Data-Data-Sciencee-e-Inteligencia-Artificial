import os
import pandas as pd

# === Configuración de rutas ===
BASE_PATH = r"C:\Users\David\Documents\Master-Big-Data-Data-Sciencee-e-Inteligencia-Artificial\TFM\AeroGPT\data\CMAPSS"
RAW_PATH = os.path.join(BASE_PATH, "raw")
PROCESSED_PATH = os.path.join(BASE_PATH, "processed")
os.makedirs(PROCESSED_PATH, exist_ok=True)

# === Datasets y columnas ===
datasets = ['FD001', 'FD002', 'FD003', 'FD004']
cols = ['unit', 'cycle', 'setting_1', 'setting_2', 'setting_3'] + [f'sensor_{i}' for i in range(1, 22)]

# === Paso 1: Convertir TXT a Excel y calcular RUL ===
for ds in datasets:
    print(f"\nProcesando {ds}...")

    train_path = os.path.join(RAW_PATH, f"train_{ds}.txt")
    test_path  = os.path.join(RAW_PATH, f"test_{ds}.txt")
    rul_path   = os.path.join(RAW_PATH, f"RUL_{ds}.txt")

    train_df = pd.read_csv(train_path, sep=r'\s+', header=None, names=cols)
    test_df  = pd.read_csv(test_path, sep=r'\s+', header=None, names=cols)
    rul_df   = pd.read_csv(rul_path, sep=r'\s+', header=None, names=['RUL'])

    # Calcular RUL para train
    max_cycle_train = train_df.groupby('unit')['cycle'].max().reset_index()
    max_cycle_train.columns = ['unit', 'max_cycle']
    train_df = train_df.merge(max_cycle_train, on='unit', how='left')
    train_df['RUL'] = train_df['max_cycle'] - train_df['cycle']
    train_df.drop(columns=['max_cycle'], inplace=True)

    # Calcular RUL para test
    test_df = test_df.copy()
    test_df['RUL'] = 0
    for idx, rul in rul_df.iterrows():
        unit_id = idx + 1
        mask = test_df['unit'] == unit_id
        max_cycle = test_df.loc[mask, 'cycle'].max()
        test_df.loc[mask, 'RUL'] = rul['RUL'] + max_cycle - test_df.loc[mask, 'cycle']

    # Guardar Excel inicial
    train_df.to_excel(os.path.join(PROCESSED_PATH, f"{ds}_Train.xlsx"), index=False)
    test_df.to_excel(os.path.join(PROCESSED_PATH, f"{ds}_Test.xlsx"), index=False)
    print(f"Archivos Excel iniciales guardados: {ds}_Train.xlsx y {ds}_Test.xlsx")

# === Paso 2: Limpieza de datos ===
for ds in datasets:
    for split in ['Train', 'Test']:
        file_path = os.path.join(PROCESSED_PATH, f"{ds}_{split}.xlsx")
        print(f"\nLeyendo {file_path} para limpieza...")

        df = pd.read_excel(file_path)

        # Comprobar valores nulos
        nulls = df.isnull().sum().sum()
        if nulls > 0:
            print(f"Se encontraron {nulls} nulos")
            df = df.dropna()
        else:
            print("No hay valores nulos.")

        # Detectar columnas sin varianza
        sensor_cols = [c for c in df.columns if c.startswith('sensor_')]
        zero_var = [c for c in sensor_cols if df[c].std() == 0]
        if zero_var:
            print(f"Columnas sin varianza ({len(zero_var)}): {zero_var}")
            df = df.drop(columns=zero_var)
        else:
            print("Todos los sensores tienen variabilidad.")

        # Guardar Excel cleaned (sobrescribe)
        df.to_excel(file_path, index=False)
        print(f"Archivo limpio guardado: {file_path}")

