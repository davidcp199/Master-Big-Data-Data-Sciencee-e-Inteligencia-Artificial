import os
import numpy as np
import pandas as pd
import torch
from torch import nn
import joblib


# ============================================================
# 1. MODELO GRU IDENTICO AL ENTRENADO
# ============================================================
class GRUModel(nn.Module):
    def __init__(self, input_dim=24, hidden_dim1=256, hidden_dim2=128, dropout=0.3):
        super(GRUModel, self).__init__()
        self.gru1 = nn.GRU(input_dim, hidden_dim1, num_layers=2, dropout=dropout, batch_first=True)
        self.gru2 = nn.GRU(hidden_dim1, hidden_dim2, num_layers=2, dropout=dropout, batch_first=True)
        self.linear = nn.Linear(hidden_dim2, 1)

    def forward(self, x):
        out, _ = self.gru1(x)
        out, _ = self.gru2(out)
        out = out[:, -1, :]
        return self.linear(out)


# ============================================================
# 2. FEATURE COLUMNS
# ============================================================
FEATURE_COLS = ['setting_1','setting_2','setting_3'] + [f's_{i}' for i in range(1,22)]


# ============================================================
# 3. CARGA DE MODELO + SCALER
# ============================================================
def load_model(base_path, fd_code="FD001", input_dim=24):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model_path = os.path.join(base_path, "models", f"best_model_{fd_code}.pth")
    scaler_path = os.path.join(base_path, "models", f"scaler_{fd_code}.pkl")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modelo no encontrado: {model_path}")

    if not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Scaler no encontrado: {scaler_path}")

    model = GRUModel(input_dim=input_dim)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()

    scaler = joblib.load(scaler_path)

    return model, scaler, device


# ============================================================
# 4. PREPROCESAMIENTO DEL INPUT DEL USUARIO
# ============================================================
def preprocess_user_data(df, scaler):
    df = df.copy()
    df[FEATURE_COLS] = df[FEATURE_COLS].fillna(df[FEATURE_COLS].mean())
    df[FEATURE_COLS] = scaler.transform(df[FEATURE_COLS])
    return df


def make_window(df, window_size=50):
    seq = df[FEATURE_COLS].values

    if len(seq) < window_size:
        pad = np.zeros((window_size - len(seq), seq.shape[1]))
        seq = np.vstack([pad, seq])
    else:
        seq = seq[-window_size:]

    return np.expand_dims(seq, axis=0)


# ============================================================
# 5. INTERPRETACION AERONAUTICA DEL RUL
# ============================================================
def interpret_rul(rul_value):
    rul_value = float(rul_value)

    if rul_value > 80:
        return "Desgaste bajo. Continuar operación normal."
    elif rul_value > 40:
        return "Desgaste moderado. Programar inspección preventiva."
    elif rul_value > 20:
        return "Desgaste significativo. Evaluar inspección avanzada."
    elif rul_value > 5:
        return "Riesgo elevado. Requiere monitorización constante."
    else:
        return "ALERTA CRÍTICA: Recomendada retirada inmediata del motor."


# ============================================================
# 6. DETECCION DE DEGRADACION POR SUBSISTEMAS (sensores)
# ============================================================
def detect_degradation(df):
    """
    Detecta degradación asociada a sensores clave del motor.
    Adaptado a las señales típicas de CMAPSS.
    """
    row = df.iloc[-1]
    degradations = []

    # Temperatura / Compresor
    if row["s_3"] > df["s_3"].mean() + 2 * df["s_3"].std():
        degradations.append("Temperatura anómala en compresor (s_3)")

    # Presión
    if row["s_4"] > df["s_4"].mean() + 2 * df["s_4"].std():
        degradations.append("Presión elevada en HPC (s_4)")

    # Vibraciones
    if row["s_7"] > df["s_7"].mean() + 2 * df["s_7"].std():
        degradations.append("Vibración elevada – posible desgaste mecánico (s_7)")

    # Fan speed / núcleo
    if row["s_9"] < df["s_9"].mean() - 2 * df["s_9"].std():
        degradations.append("RPM del fan bajas – pérdida de eficiencia (s_9)")

    # Fuel flow
    if row["s_14"] > df["s_14"].mean() + 2 * df["s_14"].std():
        degradations.append("Flujo de combustible alto – baja eficiencia térmica (s_14)")

    return degradations or ["Condición normal del motor"]


# ============================================================
# 7. MODOS DE FALLO (Failure Modes) BASADOS EN CMAPSS
# ============================================================
def infer_failure_modes(df, degradations):
    """
    Traduce los patrones de degradación a modos de fallo probables.
    Basado en relaciones sensor → componente del motor.
    """
    modes = []

    for d in degradations:

        if "compresor" in d.lower():
            modes.append("Degradación del compresor HPC (High Pressure Compressor)")

        if "presión" in d.lower():
            modes.append("Ineficiencia en el sistema de presurización del núcleo")

        if "vibración" in d.lower():
            modes.append("Desgaste mecánico – rodamientos o fan rotor")

        if "rpm" in d.lower():
            modes.append("Pérdida de empuje – posible daño en fan blades")

        if "combustible" in d.lower():
            modes.append("Baja eficiencia térmica – cámara de combustión degradada")

    return list(set(modes)) or ["No se detectan modos de fallo relevantes"]


# ============================================================
# 8. FUNCION PRINCIPAL DE PREDICCION
# ============================================================
def predict_RUL(user_df, base_path, fd="FD001", window_size=50):
    model, scaler, device = load_model(base_path, fd)

    df_clean = preprocess_user_data(user_df, scaler)

    X = make_window(df_clean, window_size)
    X_tensor = torch.tensor(X, dtype=torch.float32).to(device)

    with torch.no_grad():
        y_pred = model(X_tensor).cpu().numpy().flatten()[0]

    y_pred = max(0, y_pred)

    # Degradación y modos de fallo
    degradations = detect_degradation(df_clean)
    failure_modes = infer_failure_modes(df_clean, degradations)

    return {
        "predicted_RUL": float(y_pred),
        "interpretation": interpret_rul(y_pred),
        "suspected_components": degradations,
        "failure_modes": failure_modes
    }


# ============================================================
# 9. EJEMPLO DE USO LOCAL
# ============================================================
if __name__ == "__main__":
    data = {
        "setting_1": [0.5],
        "setting_2": [0.1],
        "setting_3": [0.3],
        **{f"s_{i}": [1.0] for i in range(1,22)}
    }
    df_user = pd.DataFrame(data)

    base_path = r"C:\Users\David\Documents\Master-Big-Data-Data-Sciencee-e-Inteligencia-Artificial\TFM\AeroGPT\data\CMAPSS"

    pred = predict_RUL(df_user, base_path, "FD001")
    print(pred)
