# -*- coding: utf-8 -*-
"""
Procesamiento completo del dataset NASA C-MAPSS (FD001–FD004)
Autor: David (AeroGPT)
Descripción: Limpieza, cálculo de RUL y combinación de todos los escenarios en un único dataset.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ==============================
# 📂 1. Configuración
# ==============================
base_path = r"C:\Users\David\Documents\Master-Big-Data-Data-Sciencee-e-Inteligencia-Artificial\TFM\Datos"
datasets = ["FD001", "FD002", "FD003", "FD004"]

cols = ['unit', 'time'] + \
       [f'op_setting_{i}' for i in range(1, 4)] + \
       [f'sensor_{i}' for i in range(1, 27)]

def procesar_dataset(fd_id):
    print(f"\n📘 Procesando dataset {fd_id}...")
    train_file = os.path.join(base_path, f"train_{fd_id}.txt")
    test_file = os.path.join(base_path, f"test_{fd_id}.txt")
    rul_file = os.path.join(base_path, f"RUL_{fd_id}.txt")

    # Leer archivos
    train_df = pd.read_csv(train_file, sep=r"\s+", header=None, names=cols)
    test_df = pd.read_csv(test_file, sep=r"\s+", header=None, names=cols)
    rul_df = pd.read_csv(rul_file, sep=r"\s+", header=None, names=['RUL'])

    # Calcular RUL en entrenamiento
    rul_train = train_df.groupby('unit')['time'].max().reset_index()
    rul_train.columns = ['unit', 'max_time']
    train_df = train_df.merge(rul_train, on='unit', how='left')
    train_df['RUL'] = train_df['max_time'] - train_df['time']

    # Calcular RUL en test
    rul_test = test_df.groupby('unit')['time'].max().reset_index()
    rul_test.columns = ['unit', 'max_time']
    rul_test['RUL'] = rul_df['RUL']
    test_df = test_df.merge(rul_test[['unit', 'RUL']], on='unit', how='left')

    # Añadir columnas auxiliares
    train_df['dataset_id'] = fd_id
    test_df['dataset_id'] = fd_id
    train_df['type'] = 'train'
    test_df['type'] = 'test'

    print(f"✅ {fd_id} procesado -> Train: {train_df.shape}, Test: {test_df.shape}")
    return train_df, test_df


# ==============================
# 🧩 2. Procesar todos los datasets
# ==============================
train_total = pd.DataFrame()
test_total = pd.DataFrame()

for fd in datasets:
    train_df, test_df = procesar_dataset(fd)
    train_total = pd.concat([train_total, train_df], ignore_index=True)
    test_total = pd.concat([test_total, test_df], ignore_index=True)

print("\n📊 Resumen general:")
print(f"Entrenamiento total: {train_total.shape}")
print(f"Prueba total: {test_total.shape}")

# ==============================
# 📈 3. Visualización comparativa
# ==============================
plt.figure(figsize=(10, 5))
for fd in datasets:
    subset = train_total[train_total['dataset_id'] == fd]
    plt.plot(subset.groupby('time')['RUL'].mean(), label=fd)
plt.title("⚙️ Degradación promedio por dataset (C-MAPSS)")
plt.xlabel("Ciclos")
plt.ylabel("RUL promedio")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# ==============================
# 💾 4. Guardar datasets combinados
# ==============================
train_out = os.path.join(base_path, "CMAPSS_Train_Completo.csv")
test_out = os.path.join(base_path, "CMAPSS_Test_Completo.csv")
total_out = os.path.join(base_path, "CMAPSS_Completo.csv")

train_total.to_csv(train_out, index=False)
test_total.to_csv(test_out, index=False)
pd.concat([train_total, test_total], ignore_index=True).to_csv(total_out, index=False)

print(f"\n💾 Archivos guardados:")
print(f"  - {train_out}")
print(f"  - {test_out}")
print(f"  - {total_out}")
