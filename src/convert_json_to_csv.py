# -*- coding: utf-8 -*-
import csv
import json
import sys

from paths import PROCESSED_DATA_DIR, RAW_WEATHER_JSON, WEATHER_CSV

FIELDS = [
    "datetime",
    "local_datetime",
    "t",
    "tcc",
    "tp",
    "weather_desc",
    "wd",
    "wd_deg",
    "ws",
    "hu",
    "vs",
    "vs_text",
    "image",
]


def convert_json_to_csv():
    with open(RAW_WEATHER_JSON, "r", encoding="utf-8") as file:
        data = json.load(file)

    flattened_data = [item for sublist in data for item in sublist]

    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(WEATHER_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=FIELDS)
        writer.writeheader()
        for entry in flattened_data:
            writer.writerow({field: entry.get(field, "") for field in FIELDS})

    print(f"CSV berhasil diperbarui: {WEATHER_CSV}")


def main():
    if not RAW_WEATHER_JSON.exists():
        print(f"File tidak ditemukan: {RAW_WEATHER_JSON}")
        return 1

    try:
        convert_json_to_csv()
    except Exception as error:
        print(f"Gagal memperbarui CSV: {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
