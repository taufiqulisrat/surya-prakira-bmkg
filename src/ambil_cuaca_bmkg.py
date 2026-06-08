# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime

import requests

from paths import LAST_UPDATE_FILE, RAW_DATA_DIR, RAW_WEATHER_JSON

ADM4_CODE = "13.01.05.2003"  # Salido
URL = f"https://api.bmkg.go.id/publik/prakiraan-cuaca?adm4={ADM4_CODE}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}


def sudah_diperbarui_hari_ini(file_path=LAST_UPDATE_FILE):
    if not file_path.exists():
        return False

    with open(file_path, "r", encoding="utf-8") as file:
        last_date = file.read().strip()

    return last_date == datetime.today().strftime("%Y-%m-%d")


def perbarui_tanggal_hari_ini(file_path=LAST_UPDATE_FILE):
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(datetime.today().strftime("%Y-%m-%d"))


def main():
    if sudah_diperbarui_hari_ini():
        print("Info: Data sudah diperbarui hari ini. Tidak mengambil ulang.")
        return 0

    try:
        response = requests.get(URL, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()
    except Exception as error:
        print(f"Gagal mengambil data dari BMKG: {error}")
        return 1

    raw_entries = []
    if "data" in data:
        for lokasi in data["data"]:
            if "cuaca" in lokasi and isinstance(lokasi["cuaca"], list):
                raw_entries.extend(lokasi["cuaca"])

    if not raw_entries:
        print("Tidak ada entri cuaca ditemukan.")
        return 1

    try:
        RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
        with open(RAW_WEATHER_JSON, "w", encoding="utf-8") as file:
            json.dump(raw_entries, file, indent=2, ensure_ascii=False)
        perbarui_tanggal_hari_ini()
    except Exception as error:
        print(f"Gagal menyimpan data: {error}")
        return 1

    print(f"Data mentah berhasil disimpan ke '{RAW_WEATHER_JSON}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
