from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

LAST_UPDATE_FILE = DATA_DIR / "last_update.txt"
RAW_WEATHER_JSON = RAW_DATA_DIR / "cuaca_mentah_pesisir_selatan.json"
WEATHER_CSV = PROCESSED_DATA_DIR / "cuaca.csv"
PREDICTION_CSV = OUTPUTS_DIR / "hasil_prediksi_tegangan.csv"
MODEL_METRICS_JSON = OUTPUTS_DIR / "model_metrics.json"
