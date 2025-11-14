import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Bidirectional
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.preprocessing import StandardScaler

# === Configuración de rutas ===
BASE_PATH = r"C:\Users\David\Documents\Master-Big-Data-Data-Sciencee-e-Inteligencia-Artificial\TFM\AeroGPT\data\CMAPSS\processed"
DATASETS = ['FD001', 'FD002', 'FD003', 'FD004']

# === Parámetros de entrenamiento ===
WINDOW_SIZE = 30          # Ventana temporal
BATCH_SIZE = 64
EPOCHS = 100
LEARNING_RATE = 0.001
MAX_RUL = 130             # Limite máximo de RUL

# Crear carpeta de modelos
MODEL_PATH = os.path.join(BASE_PATH, "models")
os.makedirs(MODEL_PATH, exist_ok=True)

# Función para construir LSTM bidireccional
def build_model(input_shape):
    model = Sequential()
    model.add(Bidirectional(LSTM(128, return_sequences=True), input_shape=input_shape))
    model.add(Dropout(0.2))
    model.add(Bidirectional(LSTM(128)))
    model.add(Dropout(0.2))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(1))  # RUL predicción
    model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE),
                  loss='mse', metrics=['mae'])
    return model

# Entrenamiento por dataset
for ds in DATASETS:
    print(f"\n=== {ds} ===")
    
    # Cargar secuencias
    X_train = np.load(os.path.join(BASE_PATH, f"{ds}_Train_X.npy"))
    y_train = np.load(os.path.join(BASE_PATH, f"{ds}_Train_y.npy"))
    X_test  = np.load(os.path.join(BASE_PATH, f"{ds}_Test_X.npy"))
    y_test  = np.load(os.path.join(BASE_PATH, f"{ds}_Test_y.npy"))
    
    # Limitar RUL máximo
    y_train = np.clip(y_train, 0, MAX_RUL)
    y_test  = np.clip(y_test, 0, MAX_RUL)
    
    # StandardScaler opcional (aplicado por features)
    n_features = X_train.shape[2]
    for i in range(n_features):
        scaler = StandardScaler()
        X_train[:,:,i] = scaler.fit_transform(X_train[:,:,i])
        X_test[:,:,i]  = scaler.transform(X_test[:,:,i])
    
    print(f"Shapes -> X_train: {X_train.shape}, y_train: {y_train.shape}, X_test: {X_test.shape}, y_test: {y_test.shape}")
    
    # Construir modelo
    model = build_model(input_shape=(WINDOW_SIZE, n_features))
    
    # Callbacks
    es = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    ckpt = ModelCheckpoint(os.path.join(MODEL_PATH, f"{ds}_best_model.h5"), save_best_only=True, monitor='val_loss')
    
    # Entrenamiento
    history = model.fit(X_train, y_train, 
                        validation_data=(X_test, y_test),
                        epochs=EPOCHS, batch_size=BATCH_SIZE, 
                        callbacks=[es, ckpt], verbose=2)
    
    # Evaluación final
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"{ds} -> RMSE: {np.sqrt(loss):.4f}, MAE: {mae:.4f}")
