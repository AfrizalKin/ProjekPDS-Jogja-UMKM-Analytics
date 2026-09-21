# 📋 LAPORAN TUGAS MILESTONE 5: DATA QUALITY AUDIT & ANALYTICAL TASK SELECTION
**Mata Kuliah:** Pengantar Data Sains (Pertemuan 6)  
**Judul Projek:** Pemodelan Kelayakan Sektor Usaha UMKM Menggunakan Pendekatan Machine Learning dan Time Series untuk Rekomendasi Lokasi Berbasis Data di D.I. Yogyakarta  

---

## 1. Data Quality Scorecard (Audit 4 Dimensi Kualitas Data)

Audit kualitas data dilakukan secara kuantitatif dan kualitatif mengacu pada 4 dimensi standar Data Science: **Completeness**, **Consistency**, **Uniqueness**, dan **Timeliness / Validity**.

```text
                                 DATA QUALITY SCORECARD
┌─────────────────────────┬─────────────────────────────────────────────────────────────────────────┐
│ Dimensi Kualitas Data   │ Indikator & Metrik Evaluasi                                             │
├─────────────────────────┼─────────────────────────────────────────────────────────────────────────┤
│ 1. Completeness         │ % Nilai terisi (non-null), kelengkapan atribut spasial dan demografi    │
│ 2. Consistency          │ Keseragaman ejaan entitas wilayah, standar format, dan satuan finansial  │
│ 3. Uniqueness           │ Bebas dari duplikasi ID, baris ganda, dan tumpang tindih koordinat      │
│ 4. Timeliness & Validity│ Kemutakhiran tahun rujukan dan validitas batas geografis Bounding Box   │
└─────────────────────────┴─────────────────────────────────────────────────────────────────────────┘
```

### Matriks Scorecard per Dataset:

| Dataset | Completeness *(Kelengkapan)* | Consistency *(Konsistensi)* | Uniqueness *(Keunikan)* | Timeliness & Validity *(Kemutakhiran & Validitas)* | Skor Kualitas Akhir |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Dataset 1 (OSM Kompetitor)** | **98.2%**<br>• `lat` & `lon`: 100% lengkap<br>• `nama_tempat`: 100% lengkap<br>• Minor: ~1.8% nama generik | **99.5%**<br>ID wilayah seragam 5 kab/kota. 5 tag kategori terstandardisasi. | **100%**<br>773 duplikasi ID dan 3 duplikasi koordinat spasial dieliminasi. | **99.0%**<br>100% koordinat valid di Bounding Box DIY. Data crowdsourced 2026. | **99.1% (Sangat Baik)** |
| **Dataset 2 (BPS Ekonomi)** | **100%**<br>Semua indikator (PDRB, kepadatan, luas, pengeluaran) lengkap 5 wilayah. | **100%**<br>Inkonsistensi ejaan diselesaikan via *dictionary mapping*. | **100%**<br>Tidak ada baris ganda setelah eliminasi baris agregat DIY. | **100%**<br>Publikasi resmi BPS DIY terbaru (Tahun Rilis 2024). | **100% (Sempurna)** |
| **Dataset 3 (Biaya Sewa)** | **100%**<br>Tersedia representasi harga sewa untuk 5 kabupaten/kota. | **100%**<br>Diseragamkan ke tarif `Rp/m²/tahun` menggunakan faktor konversi 12. | **100%**<br>Tepat 1 baris per kabupaten/kota (5 baris total). | **98.5%**<br>Rujukan survei properti Bank Indonesia & Property Flash Index 2024. | **99.6% (Sangat Baik)** |
| **Dataset 4 (Tren Usaha)** | **95.0%**<br>125 baris lengkap 2019–2023. Google Trends lengkap 2021–2023. | **98.0%**<br>Mapping sektor KBLI konsisten antar wilayah dan kategori projek. | **100%**<br>Deduplikasi subset `(wilayah, sektor, tahun)`. | **97.5%**<br>Deret waktu historis resmi 5 tahun terakhir (2019–2023). | **97.6% (Sangat Baik)** |
| **Dataset 5 (SiBakul UMKM)** | **100%**<br>Data agregat UMKM terdaftar 2025 lengkap 5 wilayah. | **100%**<br>Nama 5 kabupaten/kota konsisten dengan Dataset 1, 2, dan 3. | **100%**<br>Data validasi tunggal dari Dinas Koperasi & UKM DIY. | **100%**<br>Data termutakhir (Tahun 2025). | **100% (Sempurna)** |

---

## 2. Dokumentasi 4 Temuan Konkret & Rekomendasi Solusi

Berdasarkan audit teknis terhadap pipeline dan data mentah, tim menemukan 4 isu konkret yang berhasil dimitigasi:

### 🔴 Temuan 1: Percampuran Baris Agregat Provinsi pada Tabel BPS
* **Kondisi / Masalah:** Berkas mentah BPS DIY menyertakan baris agregat `"D.I. Yogyakarta"` bersama dengan 5 kabupaten/kota di kolom yang sama. Jika data langsung dihitung rata-rata atau di-clustering, data provinsi akan dihitung sebagai "wilayah ke-6" sehingga terjadi *double counting* (distorsi statistik).
* **Dimensi Kualitas:** *Consistency & Validity*.
* **Solusi / Perbaikan:** Membangun *filter blacklist* pada fungsi pembersih:
  ```python
  PROVINSI_AGREGAT = {"d.i. yogyakarta", "di yogyakarta", "daerah istimewa yogyakarta", "diy"}
  df_clean = df_raw[~df_raw["kabupaten_kota"].str.lower().isin(PROVINSI_AGREGAT)]
  ```

### 🔴 Temuan 2: Duplikasi Spasial POI Akibat Grid Sampling Overpass API
* **Kondisi / Masalah:** Untuk mencegah *HTTP 504 Gateway Timeout* pada area padat, query Overpass dipecah menjadi sub-grid geografis. Hal ini menyebabkan objek usaha yang berada di batas (*border*) antar-grid terunduh lebih dari satu kali (ditemukan 773 duplikasi ID dan 3 tumpang tindih radius koordinat < 5 meter).
* **Dimensi Kualitas:** *Uniqueness*.
* **Solusi / Perbaikan:** Menerapkan deduplikasi 2 lapis pada `clean_dedup.py`:
  1. Deduplikasi eksak berbasis `id` node/way OSM.
  2. Deduplikasi spasial berbasis koordinat dengan pembulatan 5 desimal (~1,1 meter).

### 🔴 Temuan 3: Keragaman Satuan Waktu Tarif Sewa Properti Komersial
* **Kondisi / Masalah:** Berkas mentah tarif sewa properti mencampuradukkan penawaran berbasis bulanan (misal Rp 35.000/bulan) dan tahunan (Rp 450.000/tahun). Perbedaan skala ini dapat merusak perhitungan rasio biaya operasional.
* **Dimensi Kualitas:** *Consistency*.
* **Solusi / Perbaikan:** Standardisasi seragam ke basis tahunan per m²:
  $$\text{Harga Tahun} = \text{Harga Bulan} \times 12$$

### 🔴 Temuan 4: Bias Representasi Sektor Informal & Tagging Toko Kelontong OSM
* **Kondisi / Masalah:** Pada Dataset 1 (OSM), query tag `shop=grocery` (toko kelontong) hanya menghasilkan **1 titik** di Sleman dan 0 di 4 wilayah lainnya. Padahal data BPS mencatat ~11.000 toko kelontong dan SiBakul mencatat 170.000+ usaha perdagangan. Audit membuktikan adanya:
  1. *Mapping Convention:* Kontributor OSM Indonesia lebih sering menandai warung/toko lokal sebagai `shop=convenience` (ditemukan 70+ warung tradisional tercampur dengan minimarket berjaringan seperti Alfamart/Indomaret).
  2. *Under-representation Bias:* Usaha mikro informal berbasis perumahan tidak memiliki insentif komersial untuk mendaftarkan titiknya ke peta digital global.
* **Dimensi Kualitas:** *Completeness & Representation Bias*.
* **Solusi / Perbaikan:** 
  - Tidak mengandalkan data `shop=grocery` OSM yang timpang untuk menghitung kejenuhan kelontong.
  - Memanfaatkan **Dataset 5 (SiBakul Jogja)** untuk menghitung **Rasio Total UMKM per 1.000 Penduduk** sebagai indikator kejenuhan struktural riil per kabupaten/kota.
  - Mengelompokkan ritel sembako OSM bersama kategori *convenience*.

---

## 3. Penentuan Jenis Analytical Task & Justifikasi Metodologis

### 🎯 Keputusan Pemilihan:
> **UNSUPERVISED LEARNING (Composite Index Feasibility Scoring + K-Means Clustering)**

Tim memilih pendekatan **Unsupervised Learning** yang dipadukan dengan **Multi-Criteria Decision Analysis (MCDA)**, bukan Supervised Learning (klasifikasi/regresi dengan label target).

---

### 📚 Alasan Akademis & Metodologis:

#### 1. Ketiadaan Data Target Biner (*No Ground Truth Target Label*)
* Dalam machine learning supervised, model membutuhkan kolom target ($y$) yang terdefinisi secara pasti (misalnya $y=1$ untuk *"Lokasi Berhasil"* dan $y=0$ untuk *"Lokasi Bangkrut"*).
* Pada data publik agregat wilayah (BPS, OSM, SiBakul), **tidak tersedia label historis kelayakan ataupun status kebangkrutan gerai per titik lokasi**. Menciptakan label buatan (*pseudo-label*) tanpa data performa penjualan riil akan menghasilkan bias yang menyesatkan (*label leakage / artificial target*).

#### 2. Karakteristik Masalah Bisnis Adalah Perankingan & Segmentasi
Masalah riil yang dihadapi calon pelaku UMKM adalah:
* *"Wilayah mana yang memiliki rasio peluang tertinggi untuk kategori usaha saya?"* $\rightarrow$ Diselesaikan dengan **Location Feasibility Index (Perankingan)**.
* *"Bagaimana karakteristik lingkungan bisnis di kabupaten ini?"* $\rightarrow$ Diselesaikan dengan **K-Means Clustering (Segmentasi Wilayah)**.

---

### 📐 Desain Pemodelan Analitik (Proposed Architecture):

```text
                            MASTER DATA PANEL
            (Kompetitor OSM + Makro BPS + Sewa Properti + SiBakul)
                                    │
                  ┌─────────────────┴─────────────────┐
                  ▼                                   ▼
         [TASK 1: CLUSTERING]               [TASK 2: SKORING KELAYAKAN]
         K-Means Clustering                 Multi-Criteria Decision Analysis
      (Level Wilayah, n=5, k=3)             (Level Sektor x Wilayah, ~25 Baris)
                  │                                   │
                  ▼                                   ▼
           Label Profil Pasar                    Location Feasibility
      (Padat, Potensial, Perintis)                 Score (Skala 0 - 100)
                  │                                   │
                  └─────────────────┬─────────────────┘
                                    ▼
                         REKOMENDASI PERSONAL UMKM
                 (Ranking Wilayah Terbaik + Konteks Pasar)
```

#### Formulasi Matematis Indeks Kelayakan (Pilar 1):
Seluruh fitur dinormalisasi ke skala $[0, 1]$ menggunakan *Min-Max Normalization*:

$$X_{\text{norm}} = \frac{X - X_{\min}}{X_{\max} - X_{\min}}$$

Skor Kelayakan dihitung melalui pembobotan multi-kriteria:
$$\text{Feasibility Score} = 100 \times \left[ w_1 (\text{PDRB}_{\text{norm}}) + w_2 (\text{Pengeluaran}_{\text{norm}}) + w_3 (\text{Kepadatan}_{\text{norm}}) - w_4 (\text{Rasio Kompetitor}_{\text{norm}}) - w_5 (\text{Harga Sewa}_{\text{norm}}) - w_6 (\text{Rasio UMKM}_{\text{norm}}) \right]$$

*Catatan:*
- Fitur penarik pasar (+): PDRB, pengeluaran masyarakat, kepadatan populasi.
- Fitur beban / penghambat (-): Kejenuhan kompetitor sejenis, beban sewa kios, rasio total UMKM.
- Pembagian kategori hasil: **Sangat Layak ($\ge 75$)**, **Cukup Layak ($50 - 74$)**, dan **Kurang Layak ($< 50$)**.
