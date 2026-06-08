# -*- coding: utf-8 -*-
import json
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from paths import MODEL_METRICS_JSON, OUTPUTS_DIR, PREDICTION_CSV, WEATHER_CSV

VOLTAGE_FORMULA = "voltage = 0.8*t - 0.5*hu + 0.3*ws + noise + 20"


def main():
    data = pd.read_csv(WEATHER_CSV, parse_dates=["local_datetime"])

    data["hour"] = data["local_datetime"].dt.hour
    data["day_of_year"] = data["local_datetime"].dt.dayofyear

    voltage_source = "data_asli"
    if "voltage" not in data.columns:
        voltage_source = "simulasi"
        np.random.seed(42)
        data["voltage"] = (
            0.8 * data["t"]
            - 0.5 * data["hu"]
            + 0.3 * data["ws"]
            + 0.2 * np.random.randn(len(data))
            + 20
        )

    data["weather_desc"] = data["weather_desc"].astype("category")
    data["weather_code"] = data["weather_desc"].cat.codes

    features = ["t", "tp", "ws", "hu", "hour", "day_of_year", "weather_code"]
    x = data[features]
    y = data["voltage"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=42
    )

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(x_train, y_train)

    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"Mean Squared Error: {mse:.3f}")
    print(f"R2 Score: {r2:.3f}")

    data["predicted_voltage"] = model.predict(x)
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    data.to_csv(PREDICTION_CSV, index=False)

    metrics = {
        "model": "RandomForestRegressor",
        "n_estimators": 100,
        "random_state": 42,
        "test_size": 0.2,
        "total_rows": int(len(data)),
        "train_rows": int(len(x_train)),
        "test_rows": int(len(x_test)),
        "mse": float(mse),
        "r2_score": float(r2),
        "voltage_source": voltage_source,
        "voltage_formula": VOLTAGE_FORMULA if voltage_source == "simulasi" else "",
        "voltage_note": (
            "Kolom voltage dibuat dari simulasi berbasis suhu, kelembapan, "
            "kecepatan angin, dan noise acak karena data sensor voltase asli belum tersedia."
        )
        if voltage_source == "simulasi"
        else "Kolom voltage berasal dari data input.",
    }
    with open(MODEL_METRICS_JSON, "w", encoding="utf-8") as file:
        json.dump(metrics, file, indent=2, ensure_ascii=False)

    print(f"Prediksi disimpan ke: {PREDICTION_CSV}")
    print(f"Metrik model disimpan ke: {MODEL_METRICS_JSON}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
