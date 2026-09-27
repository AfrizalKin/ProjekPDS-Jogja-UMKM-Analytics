# 📐 PANDUAN DESAIN SISTEM & BLUEPRINT PROJEK
## Sistem Rekomendasi Kelayakan Sektor Usaha UMKM Berbasis Data (D.I. Yogyakarta)
> **Mata Kuliah:** Pengantar Data Sains (PDS) — Semester 3  
> **Status Dokumen:** Dokumen Panduan Perancangan Arsitektur (Pra-Eksekusi)

---

## 1. 💡 Ide & Konsep Dasar Projek

### A. Latar Belakang Masalah
Di Provinsi D.I. Yogyakarta, sektor UMKM merupakan tulang punggung ekonomi daerah. Namun, sebagian besar calon wirausahawan pemula memilih jenis usaha dan lokasi pembukaan cabang **hanya berdasarkan intuisi, tren sesaat di media sosial, atau ikut-ikutan kerabat**. 

Dampaknya sangat fatal:
1. **Perang Harga & Kanibalisasi:** Terjadi over-saturasi usaha sejenis pada titik tertentu (contoh: kafe dan gerai minuman kekinian di koridor perkuliahan Sleman dan Kota Yogyakarta).
2. **Kesesuaian Daya Beli:** Banyak usaha gagal karena tidak memperhitungkan apakah daya beli (PDRB dan pengeluaran per kapita) masyarakat sekitar cukup kuat untuk menyerap harga produk mereka.
3. **Beban Biaya Sewa:** Tarif sewa properti komersial yang tinggi di pusat kota menggerus margin keuntungan sebelum bisnis mencapai *break-even point* (titik impas).

### B. Rumusan Solusi & Nilai Tambah
Membangun **Sistem Rekomendasi Lokasi dan Sektor Usaha Berbasis Data Multidimensi** yang memandu calon pelaku usaha untuk menentukan:
- Sektor usaha mana yang paling potensial di kabupaten/kota tertentu.
- Di kabupaten/kota mana sebuah sektor usaha memiliki peluang keberhasilan tertinggi dengan rasio kompetisi yang sehat dan biaya sewa yang realistis.

---

## 2. 📊 Rencana & Spesifikasi Dataset (Multi-Sumber)

Sistem dirancang untuk menggabungkan **5 dataset lintas domain** agar analisis tidak bias hanya pada satu sudut pandang:

| # | Nama Dataset | Cakupan Data | Sumber Data | Peran dalam Sistem |
|---|---|---|---|---|
| **1** | **Kompetitor Usaha (POI)** | Titik lokasi usaha aktif per sektor (*cafe, restaurant, convenience, grocery, laundry*) | OpenStreetMap (Overpass API) | Mengukur tingkat kejenuhan kompetisi lokal per sektor per wilayah. |
| **2** | **Kondisi Makroekonomi** | PDRB per kapita, kepadatan penduduk, pengeluaran per kapita (2024) | BPS Provinsi D.I. Yogyakarta | Mengukur daya beli masyarakat dan kepadatan pasar sasaran. |
| **3** | **Biaya Sewa Komersial** | Estimasi tarif sewa kios/ruko per m² per tahun per kabupaten/kota | Platform Properti & Bank Indonesia Index | Mengukur beban *capital expenditure* (sewa) awal bagi pelaku usaha. |
| **4** | **Tren Pertumbuhan Usaha** | Deret waktu (time series) jumlah unit usaha 2019–2023 + indeks tren Google | BPS DIY & Google Trends | Mengidentifikasi apakah suatu sektor sedang *sunrise* (naik) atau *sunset* (lesu). |
| **5** | **Statistik UMKM Resmi** | Jumlah total UMKM terdaftar 2025, tren tahunan, dan komposisi sektor | SiBakul Jogja (Dinas Koperasi & UKM DIY) | Data pembanding resmi pemerintah untuk memvalidasi kejenuhan struktural agregat. |

---

## 3. 🧠 Desain Arsitektur 4 Pilar Pemodelan (`models/`)

Sistem pemodelan analitik dibagi menjadi 4 pilar modular yang dijalankan sebelum website dibangun:

```text
Dataset 1, 2, 3, 5  ───► PILAR 1: Skoring Kelayakan (MCDA) ───────┐
Dataset 1, 2, 3, 5  ───► PILAR 2: Clustering Profil Wilayah ──────┼──► PILAR 4: Mesin Rekomendasi
Dataset 4           ───► PILAR 3: Forecasting Pertumbuhan Sektor ─┘     (Lookup Real-Time User)
```

### Pilar 1: Skoring Kelayakan Sektor Usaha (MCDA Rule-Based)
- **Sifat:** Batch processing, tidak ada input user runtime.
- **Tujuan:** Menghitung skor kelayakan komposit (skala 0–100) untuk seluruh 25 kombinasi sektor $\times$ wilayah (5 wilayah $\times$ 5 sektor).
- **Logika Pembobotan (Multi-Criteria Decision Analysis):**
  $$\text{Skor} = w_1(\text{Daya Beli}) + w_2(\text{Kepadatan}) + w_3(\text{Total UMKM SiBakul}) - w_4(\text{Densitas Kompetitor OSM}) - w_5(\text{Biaya Sewa})$$
- **Output:** `data/processed/hasil_skoring_sektor.csv` dengan kolom: `sektor`, `wilayah`, `skor`, `kategori` (*Layak, Cukup Layak, Kurang Layak*).

### Pilar 2: Clustering Profil Karakteristik Wilayah
- **Sifat:** Batch processing, unsupervised learning.
- **Metode:** K-Means Clustering ($k=3$) dikombinasikan dengan PCA 2D (*Principal Component Analysis*) untuk visualisasi sebaran spasial.
- **Tujuan:** Mengelompokkan 5 kabupaten/kota ke dalam klaster karakteristik pasar (misal: *Urban Padat*, *Semi-Urban Bertumbuh*, *Rural Potensial*).
- **Output:** `data/processed/hasil_clustering_wilayah.csv` dan berkas serialisasi model di `models/saved/`.

### Pilar 3: Forecasting Tren Pertumbuhan Sektor
- **Sifat:** Batch processing, time series regression.
- **Metode:** Regresi tren linear deret waktu tahunan panel BPS (2019–2023) dengan interval kepercayaan 95% (*Confidence Interval*) untuk memproyeksikan tahun 2024–2026.
- **Tujuan:** Menghasilkan arah pergerakan pasar (*Naik Signifikan*, *Stabil / Bertumbuh*, *Melambat*).
- **Output:** `data/processed/hasil_forecasting_sektor.csv`.

### Pilar 4: Mesin Rekomendasi Personal (`UMKMRecommender`)
- **Sifat:** Real-time inference, **satu-satunya pilar dengan input pengguna**.
- **Logika:** Mengambil input pengguna (Jenis usaha yang diminati, modal sewa yang dimiliki, dan pilihan target wilayah), lalu melakukan *rule-based lookup & matching* ke artefak hasil Pilar 1, 2, dan 3 tanpa perlu menghitung ulang dataset mentah.
- **Output:** Kartu rekomendasi personal berisi perankingan wilayah terbaik, kesesuaian budget, arah tren sektor, dan peringatan tingkat kompetisi.

---

## 4. 🌐 Rencana Antarmuka Web App (Fase 3: `app/`)

### Prinsip Utama Aplikasi Web:
1. **Read-Only Data:** Web hanya membaca file hasil olahan di `data/processed/` dan `models/saved/`. Web tidak pernah menjalankan ulang scraping atau pelatihan model dari nol saat dibuka.
2. **Cepat & Responsif:** Komputasi analitik sudah selesai sebelumnya, sehingga antarmuka pengguna dapat menampilkan visualisasi seketika.

### Struktur 5 Menu Navigasi:
1. **Beranda:** Ringkasan masalah, tujuan, dan KPI ringkas data (2.796 titik kompetitor, 5 wilayah, 5 sektor).
2. **Peta & Clustering Wilayah (Pilar 2):** Peta interaktif DIY diwarnai berdasarkan klaster ekonomi + kartu rincian profil daerah saat diklik.
3. **Skoring Kelayakan Sektor (Pilar 1):** Tabel interaktif dengan filter dropdown (wilayah & sektor) + Bar Chart perbandingan skor.
4. **Forecasting Tren Sektor (Pilar 3):** Line chart interaktif tren historis BPS & proyeksi 2024–2026 per sektor.
5. **Coba Rekomendasi (Pilar 4):** Formulir simulasi input pengguna untuk menghasilkan rekomendasi lokasi personal secara seketika.
