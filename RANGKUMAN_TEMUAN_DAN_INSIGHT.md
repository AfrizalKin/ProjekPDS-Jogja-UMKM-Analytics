# 📑 RANGKUMAN UTUH PROJEK, METODOLOGI & INSIGHT DATA
## Sistem Rekomendasi Kelayakan Sektor Usaha UMKM Berbasis Data di D.I. Yogyakarta
> **Mata Kuliah:** Pengantar Data Sains (PDS) — Semester 3  
> **Status:** Dokumen Konsolidasi Eksekusi & Temuan Riil (*Update Per Hari Ini*)

---

## 1. 💡 Ide & Konsep Ringkas

### Inti Masalah:
Calon pelaku UMKM di D.I. Yogyakarta sering kali membuka usaha hanya berlandaskan **intuisi atau rasa optimisme semata**, tanpa memeriksa:
1. Berapa kepadatan pesaing langsung di radius wilayah tersebut?
2. Apakah daya beli masyarakat lokal memadai untuk menyerap harga produk?
3. Apakah biaya sewa tempat usaha rasional terhadap potensi omzet?

### Solusi yang Dibangun:
Sistem analitik berbasis data (*Decision Support System*) yang mengintegrasikan **5 dataset multi-sumber** dan memprosesnya melalui **4 pilar analitik terpadu (MCDA, Clustering K-Means, Forecasting Time Series, dan Inference Matching Engine)** guna memberikan rekomendasi objektif mengenai kelayakan sektor usaha dan lokasi pembukaan bisnis di 5 kabupaten/kota DIY (*Kota Yogyakarta, Sleman, Bantul, Kulon Progo, dan Gunungkidul*).

---

## 2. 📊 5 Dataset yang Digunakan

| # | Dataset | Cakupan & Volume Data | Sumber Resmi | Berkas Output Bersih |
|---|---|---|---|---|
| **1** | **Kompetitor Usaha (POI)** | 2.796 titik koordinat usaha aktif (5 sektor target) | OpenStreetMap (Overpass API) | `data/processed/kompetitor_per_wilayah.csv` |
| **2** | **Kondisi Makroekonomi** | PDRB per kapita, kepadatan penduduk, pengeluaran per kapita (2024) | BPS Provinsi D.I. Yogyakarta | `data/processed/kondisi_ekonomi_wilayah.csv` |
| **3** | **Biaya Sewa Komersial** | Tarif sewa properti per m²/tahun per wilayah | Riset Properti & Bank Indonesia Index | `data/processed/biaya_operasional.csv` |
| **4** | **Tren Pertumbuhan Usaha** | Panel time series 2019–2023 (125 baris) + skor Google Trends | BPS DIY & Google Trends | `data/processed/tren_sektor.csv` |
| **5** | **Statistik UMKM Pemda** | 342.463 total UMKM terdaftar 2025 + tren provinsi 2021-2025 | SiBakul Jogja (Dinas Koperasi & UKM DIY) | `data/processed/umkm_sibakul.csv` |

---

## 3. 🛠️ Bagaimana Cara Mendapatkan Datasetnya? (Metode Ekstraksi)

Setiap dataset diperoleh melalui pipeline rekayasa data (*ETL Pipeline*) yang dibangun mandiri pada folder `scripts/`:

### A. Dataset 1: OpenStreetMap (Scraping via Overpass API)
- **Modul:** `scripts/dataset1_osm/`
- **Metode & Tantangan:**
  - Mengirim kueri Overpass QL dengan filter tag `amenity` (`cafe`, `restaurant`, `fast_food`), `shop` (`convenience`, `supermarket`, `grocery`), dan `craft` (`laundry`).
  - **Grid Sampling (Mitigasi HTTP 504 Gateway Timeout):** Wilayah padat (seperti Sleman dan Kota Yogyakarta) dipecah menjadi sub-grid spasial $2 \times 2$ dan $3 \times 3$ berkoordinat presisi agar server Overpass tidak *timeout*.
  - **Failover & Exponential Backoff:** Diterapkan fallback otomatis ke 3 server mirror (*de*, *kumi*, *openstreetmap.fr*) serta jeda *sleep* adaptif saat terkena *HTTP 429 Too Many Requests*.

### B. Dataset 2: BPS Makroekonomi Wilayah
- **Modul:** `scripts/dataset2_ekonomi/`
- **Metode & Tantangan:**
  - Mengunduh publikasi statistik BPS DIY 2024 (*D.I. Yogyakarta Dalam Angka 2024*).
  - Melakukan *parsing* tabel multi-header BPS (skip 4 baris pertama, penanganan encoding `utf-8-sig`).
  - Menghapus karakter pemisah ribuan titik/koma agar angka PDRB dan pengeluaran terkonversi menjadi nilai numerik murni.

### C. Dataset 3: Biaya Sewa Properti Komersial
- **Modul:** `scripts/dataset3_sewa/`
- **Metode & Tantangan:**
  - Mengumpulkan sampel sewa kios, ruko, dan tempat usaha komersial dari agregator properti dan laporan Indeks Perkembangan Properti Komersial Bank Indonesia.
  - Menerapkan fungsi normalisasi `normalize_rental_price()` untuk menyetarakan sewa bulanan menjadi satuan standar baku: **Rp / m² / tahun**.

### D. Dataset 4: Tren Sektor Usaha (BPS + Google Trends)
- **Modul:** `scripts/dataset4_tren/`
- **Metode & Tantangan:**
  - Ekstraksi data deret waktu jumlah usaha aktif BPS DIY (2019–2023) per kabupaten/kota.
  - Memanggil Google Trends via library `pytrends` untuk mengambil volume minat pencarian masyarakat lokal DIY pada kata kunci sektor terkait (*"cafe jogja"*, *"laundry terdekat"*, dll.) dengan skala 0–100.
  - Menghitung persentase pertumbuhan tahunan (*Year-over-Year / YoY Growth*).

### E. Dataset 5: SiBakul Jogja (Dinas Koperasi & UKM DIY)
- **Modul:** `scripts/dataset2_ekonomi/`
- **Metode & Tantangan:**
  - Ekstraksi data resmi sensus UMKM daerah terdaftar dari sistem SiBakul Pemprov DIY per 2025.
  - Menghitung rasio kepadatan struktural riil: **Jumlah UMKM per 1.000 Penduduk**.

---

## 4. 🔍 Bagaimana Kualitas Datasetnya? (Audit & Temuan Riil)

Berdasarkan audit kualitas data pada 4 dimensi standar (*Completeness, Consistency, Uniqueness, Timeliness/Validity*), ditemukan **4 anomali data riil penting beserta solusinya**:

```
[AUDIT HASIL]:
- Completeness : 100% pada variabel esensial (koordinat, nama wilayah, angka makroekonomi).
- Consistency  : Ejaan kabupaten/kota diseragamkan 100% menggunakan mapping dictionary.
- Uniqueness   : 773 duplikasi ID dan 3 tumpang tindih spasial OSM dieliminasi.
- Validity     : Seluruh koordinat tervalidasi berada di BBox DIY (Lat [-8.25 s/d -7.50], Lon [110.00 s/d 110.85]).
```

### 🚨 4 Temuan Krusial & Solusi Teknis:

1. **Temuan 1 — BPS Menyisipkan Baris Agregat Provinsi di Tengah Data:**
   - *Masalah:* File BPS menyertakan baris "D.I. Yogyakarta" di dalam daftar kabupaten/kota. Jika tidak difilter, angka provinsi akan terhitung ganda sebagai kabupaten ke-6 dan merusak kalkulasi rata-rata statistik.
   - *Solusi:* Filtering otomatis menggunakan blacklist set kata kunci agregasi `{"D.I. Yogyakarta", "DI Yogyakarta", "Jumlah"}`.

2. **Temuan 2 — Duplikasi Titik Akibat Grid Sampling OSM:**
   - *Masalah:* Karena wilayah padat dipecah menjadi sub-grid, tempat usaha yang tepat berada di garis batas antar grid ter-download dua kali.
   - *Solusi:* Deduplikasi dua lapis: `drop_duplicates(subset=['id'])` untuk ID OSM dan pembulatan koordinat 4 desimal untuk titik spasial yang berjarak $<5$ meter.

3. **Temuan 3 — Inkonsistensi Periode Satuan Sewa:**
   - *Masalah:* Data iklan properti mencampuradukkan sewa per bulan dan per tahun dengan luas bangunan yang berbeda-beda.
   - *Solusi:* Fungsi standarisasi yang mengonversi seluruh tarif ke basis luas $1\text{ m}^2$ per periode $1\text{ tahun}$.

4. **⭐ Temuan 4 (TEMUAN KUNCI) — Bias Tagging & Underrepresentation Toko Kelontong OSM:**
   - *Masalah:* Pada data OSM, pencarian tag `shop=grocery` (toko kelontong) **hanya menemukan 1 titik di Sleman** ("Warung Mbak Nining") dan **0 titik di 4 kabupaten/kota lainnya**! Padahal BPS mencatat ribuan warung kelontong tradisional di Jogja.
   - *Akar Masalah:*
     1. **Mapping Convention Lokal:** Kontributor OSM Indonesia menandai warung kelontong sebagai `shop=convenience` (ditemukan 70+ toko/warung kelontong lokal bercampur baur dengan 313 gerai minimarket waralaba Alfamart/Indomaret).
     2. **Underrepresentation Bias (Sektor Informal):** Pemilik warung kelontong rumahan berskala mikro tidak memiliki insentif digital untuk mendaftarkan titik usahanya ke OpenStreetMap.
   - *Solusi & Nilai Tambah Akademis:* **Kami tidak memaksakan data OSM yang bias.** Sebagai gantinya, kami memasukkan **Dataset 5 (SiBakul Jogja)** yang mencatat data riil 170.000+ UMKM sektor perdagangan untuk menghitung rasio kepadatan usaha di Pilar 1 dan Pilar 2. Kasus ini menjadi bahan pembahasan ilmiah yang sangat berharga di laporan Milestone 5.

---

## 5. 📈 Hasil Analisis, Pemodelan & Insight yang Kita Miliki Saat Ini

Seluruh komputasi pemodelan analitik telah dieksekusi melalui `models/run_all_models.py` dan menghasilkan *insight* konkret:

### A. Pilar 1: Skoring Kelayakan Sektor Usaha (MCDA 0–100)
- Menghasilkan 25 kombinasi penilaian kelayakan usaha di D.I. Yogyakarta:
  - **Sleman & Bantul** mendominasi kelayakan untuk sektor **Kafe (Skor: 83.2)** dan **Laundry (Skor: 86.8)** karena didukung oleh konsentrasi mahasiswa, populasi usia produktif, dan daya beli pengeluaran tinggi.
  - **Kota Yogyakarta** memiliki daya beli tertinggi (PDRB Rp 126,8 juta), namun skor kelayakan tertekan ke kategori *Cukup Layak* untuk usaha kafe baru (Skor: 69.1) akibat **tingginya beban sewa (Rp 850.000/m²)** dan **kepadatan kompetitor kafe/resto yang sudah jenuh (651 titik)**.
  - **Kulon Progo & Gunungkidul** muncul sebagai lokasi paling layak untuk **Sektor Ritel / Toko Kebutuhan Harian & Kuliner Wisata** karena rasio kompetisi modern masih sangat rendah dan biaya sewa sangat terjangkau (Rp 220.000–275.000/m²).

### B. Pilar 2: Clustering Wilayah (K-Means $k=3$ & PCA 2D)
Pengelompokan 5 kabupaten/kota menghasilkan **3 Klaster Karakteristik Ekonomi** yang sangat tegas:
- **Klaster 0 — Urban Padat, Jenuh & Biaya Tinggi:**
  - *Wilayah:* **Kota Yogyakarta**
  - *Ciri:* Kepadatan penduduk ekstrem (11.517 jiwa/km²), PDRB per kapita tertinggi, biaya sewa tertinggi, dan pasar sangat padat. Cocok untuk usaha dengan margin tebal atau konsep diferensiasi unik.
- **Klaster 1 — Semi-Urban Bertumbuh (*Sweet Spot* Ekspansi):**
  - *Wilayah:* **Kabupaten Sleman dan Kabupaten Bantul**
  - *Ciri:* Wilayah penyangga (*buffer zone*) dengan daya beli masyarakat tinggi, pertumbuhan pesat, dan populasi terpadat di DIY. Menjadi destinasi paling seimbang antara potensi pasar dan biaya operasional.
- **Klaster 2 — Rural Potensial & Biaya Rendah (*Perintis Pasar*):**
  - *Wilayah:* **Kabupaten Kulon Progo dan Kabupaten Gunungkidul**
  - *Ciri:* Kepadatan penduduk relatif rendah (514–773 jiwa/km²), biaya sewa sangat murah, penetrasi kompetitor digital rendah. Sangat potensial untuk usaha ritel esensial dan pariwisata.
- **Evaluasi Reduksi Dimensi (PCA 2D):**
  - Komponen Utama 1 (PC1) menjelaskan **80,34%** variansi.
  - Komponen Utama 2 (PC2) menjelaskan **13,75%** variansi.
  - **Total Variansi Terjelaskan: 94,09%** (artinya proyeksi grafik 2D mencerminkan kondisi data asli hampir sempurna).

### C. Pilar 3: Forecasting Tren Pertumbuhan Sektor (2019–2026)
- **Sektor F&B (Kafe & Restoran):** Menunjukkan kurva tren *V-shaped recovery* pasca-pandemi 2021 dan diproyeksikan terus **Naik Signifikan** hingga 2026 didorong oleh pariwisata dan gaya hidup *nongkrong*.
- **Sektor Laundry & Jasa Mandiri:** Menunjukkan tren **Stabil Bertumbuh Moderat**, dengan risiko fluktuasi pasar yang sangat rendah.
- **Sektor Toko Kelontong / Perdagangan Tradisional:** Pada pencatatan historis cenderung **Stagnan / Melambat**, memperlihatkan tekanan struktural akibat penetrasi ritel modern waralaba.

### D. Pilar 4: Mesin Rekomendasi Personal (`UMKMRecommender`)
- Telah teruji secara inferensi:
  - Mampu mencocokkan sektor yang dipilih user dengan tabel skor kelayakan.
  - Memvalidasi kecukupan anggaran modal sewa pengguna terhadap rata-rata tarif sewa di wilayah target.
  - Mampu mengeluarkan peringkat **Top 3 Wilayah Alternatif Terbaik** jika pengguna memilih opsi "Terbuka ke semua wilayah".

---

## 6. 🎯 Posisi Projek di Detik Ini & Langkah Lanjutan

```text
[ FASE 1: Data Pipeline ] ──► SELESAI & BERSIH (5 Dataset, 10 CSV di data/processed/)
[ FASE 2: Modeling Engine ] ──► SELESAI & TERUJI (Pilar 1, 2, 3, 4 di folder models/)
[ FASE 3: Web Application ] ──► SIAP DIMULAI (Folder app/)
```

Dengan seluruh komputasi dan analisis yang sudah 100% selesai dan tersimpan rapi dalam format `.csv` dan `.joblib`, langkah selanjutnya adalah **membangun antarmuka Website (Fase 3 di folder `app/`)** agar seluruh insight dan mesin rekomendasi ini dapat digunakan secara interaktif oleh publik dan dosen.
