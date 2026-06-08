# Proyek Prediksi Tegangan Panel Surya

Proyek ini mengambil data prakiraan cuaca BMKG, mengubah JSON ke CSV, lalu membuat prediksi tegangan panel surya menggunakan Random Forest.

## Struktur Folder

```text
.
├── data/
│   ├── raw/                 # Data JSON mentah dari BMKG
│   ├── processed/           # Data CSV hasil konversi
│   └── last_update.txt      # Penanda update harian
├── outputs/                 # Hasil prediksi model
├── src/                     # Script Python utama
├── web/                     # Tampilan HTML
├── main.py                  # Runner pipeline
├── requirements.txt         # Dependency Python
└── .venv/                   # Virtual environment lokal
```

## Menjalankan Proyek

Aktifkan virtual environment:

```powershell
.\.venv\Scripts\activate
```

Jalankan pipeline:

```powershell
python main.py
```

Output prediksi akan tersimpan di `outputs/hasil_prediksi_tegangan.csv`.
