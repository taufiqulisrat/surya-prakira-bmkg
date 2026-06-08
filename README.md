# Proyek Prediksi Tegangan Panel Surya

Aplikasi ini merupakan sebuah prototype sistem prediksi tegangan panel surya berbasis data cuaca BMKG yang sudah disesuaikan untuk wilayah tertentu. Sistem ini dibuat untuk menunjukkan bagaimana data cuaca dapat dimanfaatkan sebagai masukan dalam proses Machine Learning untuk memperkirakan nilai tegangan panel surya. Data cuaca yang digunakan berasal dari API BMKG dengan kode wilayah 13.01.05.2003, yaitu wilayah Salido, Kecamatan IV Jurai, Kabupaten Pesisir Selatan, Sumatera Barat. Dengan demikian, aplikasi ini tidak mengambil data cuaca secara umum untuk seluruh Indonesia, tetapi sudah diarahkan secara khusus ke wilayah tersebut.

Pengaturan wilayah dilakukan melalui kode administrasi BMKG atau adm4. Pada aplikasi ini, kode yang digunakan adalah 13.01.05.2003. Kode tersebut dimasukkan ke dalam URL API BMKG sehingga data yang diambil hanya data prakiraan cuaca untuk lokasi Salido. Karena itu, hasil prakiraan cuaca, suhu, kelembapan, curah hujan, arah angin, dan kecepatan angin yang tampil di dashboard merupakan data yang berkaitan dengan wilayah tersebut. Jika aplikasi ingin digunakan untuk wilayah lain, maka kode adm4 perlu diganti sesuai lokasi yang diinginkan.

Pada tahap awal, aplikasi mengambil data cuaca dari BMKG menggunakan script Python. Data yang diperoleh masih berbentuk JSON mentah, kemudian disimpan ke dalam folder data/raw. Setelah itu, data JSON tersebut diproses dan dikonversi menjadi file CSV agar lebih mudah digunakan untuk proses analisis dan pelatihan model Machine Learning. File CSV hasil konversi disimpan di folder data/processed. Proses ini termasuk tahap pengolahan data awal, yaitu mengambil data, merapikan format data, memilih kolom yang dibutuhkan, dan menyiapkan data agar dapat digunakan oleh model.

Karena pada proyek ini belum tersedia sensor panel surya untuk mengambil data tegangan secara langsung, maka nilai voltase yang digunakan masih berupa data simulasi. Artinya, nilai tegangan tidak berasal dari alat ukur atau sensor nyata, melainkan dihitung menggunakan rumus berdasarkan beberapa parameter cuaca. Rumus yang digunakan adalah voltage = 0.8*t - 0.5*hu + 0.3*ws + noise + 20, dengan t sebagai suhu, hu sebagai kelembapan, ws sebagai kecepatan angin, dan noise sebagai variasi acak kecil. Data simulasi ini digunakan sebagai target pembelajaran model agar sistem dapat menunjukkan alur kerja prediksi menggunakan Machine Learning.

Model Machine Learning yang digunakan dalam aplikasi ini adalah Random Forest Regressor. Random Forest merupakan algoritma yang terdiri dari banyak pohon keputusan dan cocok digunakan untuk kasus regresi, yaitu prediksi nilai numerik seperti tegangan. Dalam sistem ini, model dilatih menggunakan fitur cuaca seperti suhu, curah hujan, kecepatan angin, kelembapan, jam, hari dalam tahun, dan kode deskripsi cuaca. Model kemudian mempelajari pola hubungan antara fitur cuaca tersebut dengan nilai voltase simulasi, lalu menghasilkan prediksi berupa predicted_voltage.

Setelah model dilatih, aplikasi melakukan evaluasi menggunakan metrik seperti Mean Squared Error dan R2 Score. Mean Squared Error digunakan untuk melihat seberapa besar rata-rata kesalahan prediksi model, sedangkan R2 Score digunakan untuk melihat seberapa baik model menjelaskan variasi data target. Hasil evaluasi model disimpan dalam file model_metrics.json, sedangkan hasil prediksi tegangan disimpan dalam file hasil_prediksi_tegangan.csv. Kedua file ini kemudian dibaca oleh halaman HTML untuk ditampilkan dalam bentuk dashboard.

Dashboard aplikasi menampilkan informasi prakiraan cuaca dan hasil prediksi tegangan panel surya secara visual. Pada tampilan dashboard, pengguna dapat melihat kondisi cuaca, suhu, kelembapan, kecepatan angin, curah hujan, jarak pandang, serta prediksi tegangan. Selain itu, dashboard juga menampilkan informasi hasil Random Forest dan penjelasan asal perhitungan voltase. Hal ini penting agar pengguna memahami bahwa data cuaca berasal dari BMKG untuk wilayah Salido, sedangkan data voltase masih bersifat simulasi karena belum menggunakan sensor asli.

Secara keseluruhan, aplikasi ini sudah diatur khusus untuk mengambil data cuaca wilayah Salido, Kecamatan IV Jurai, Kabupaten Pesisir Selatan, Sumatera Barat. Aplikasi ini belum dapat disebut sebagai sistem monitoring panel surya nyata, karena belum mengambil data tegangan langsung dari perangkat fisik. Namun, aplikasi ini sudah dapat disebut sebagai prototype atau simulasi sistem prediksi berbasis Machine Learning. Sistem ini menunjukkan alur lengkap mulai dari pengambilan data cuaca wilayah tertentu, pengolahan data, pembuatan target simulasi, pelatihan model Random Forest, evaluasi model, penyimpanan hasil prediksi, hingga visualisasi dalam dashboard web.

Untuk pengembangan lebih lanjut, sistem ini dapat dibuat lebih valid dengan menambahkan sensor panel surya seperti sensor tegangan, sensor arus, sensor daya, sensor intensitas cahaya, dan sensor suhu panel. Data dari sensor tersebut perlu dicatat berdasarkan waktu pengukuran, lalu disesuaikan dengan data cuaca BMKG pada waktu yang sama. Dengan begitu, model Random Forest dapat dilatih menggunakan data tegangan asli, bukan data simulasi, sehingga hasil prediksi menjadi lebih akurat dan relevan untuk kondisi panel surya yang sebenarnya.

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
