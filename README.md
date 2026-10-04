# Sistem Rekomendasi Kelayakan Sektor Usaha UMKM Berbasis Data (D.I. Yogyakarta)

> **Projek Mata Kuliah:** Pengantar Data Sains (PDS) — Semester 3  
> **Judul Projek:** *Pemodelan Kelayakan Sektor Usaha UMKM Menggunakan Pendekatan Machine Learning dan Time Series untuk Rekomendasi Lokasi Berbasis Data di D.I. Yogyakarta*  
> **Cakupan Wilayah:** 5 Kabupaten/Kota di Provinsi D.I. Yogyakarta (*Kota Yogyakarta, Kabupaten Sleman, Kabupaten Bantul, Kabupaten Kulon Progo, dan Kabupaten Gunungkidul*).

---

## 📌 Latar Belakang & Tujuan

Banyak pelaku Usaha Mikro, Kecil, dan Menengah (UMKM) mengalami kegagalan pada tahun-tahun awal operasional karena memilih lokasi usaha dan sektor bisnis hanya berdasarkan intuisi atau tren sesaat tanpa validasi data pasar. Fenomena ini menyebabkan over-saturasi di kawasan perkotaan tertentu dan ketimpangan potensi di kawasan berkembang.

Projek ini bertujuan membangun **Sistem Pendukung Keputusan (Decision Support System)** yang terintegrasi secara *end-to-end* untuk membantu calon pelaku usaha dalam:
1. Menilai tingkat kejenuhan kompetisi lokal per sektor usaha.
2. Memahami profil karakteristik makroekonomi dan daya beli masyarakat di setiap kabupaten/kota.
3. Memproyeksikan tren pertumbuhan sektor usaha untuk 1–3 tahun ke depan.
4. Memberikan rekomendasi lokasi dan sektor yang paling layak secara personal berdasarkan preferensi usaha dan anggaran modal.

---

## 🏗️ Arsitektur Sistem

Sistem dirancang dengan arsitektur bertingkat yang memisahkan antara pengolahan data (*Data Pipeline*), pemodelan komputasi analitik (*Modeling Engine*), dan antarmuka pengguna (*Web Application*):

```text
[ Data Sources: OSM, BPS, Sewa Index, Google Trends, SiBakul ]
                             │
                             ▼
              scripts/run_all_pipelines.py
                             │
                             ▼
                      data/cleaned/
                             │
    ┌────────────────────────┼────────────────────────┐
    ▼                        ▼                        ▼
Pilar 1: Skoring         Pilar 2: Klaster        Pilar 3: Tren
(MCDA Rule-Based)        (K-Means + PCA 2D)      (Time Series Panel)
    │                        │                        │
    └────────────────────────┼────────────────────────┘
                             ▼
                      outputs/hasil/
                             │
                             ▼
                 Pilar 4: Rekomendasi Personal
                    (UMKMRecommender Engine)
                             │
                             ▼
                  Fase 3: Web Application (app/)
```

---

## 📊 Dataset Multi-Sumber

Projek ini mengintegrasikan **5 dataset lintas sumber** (pemerintah, data spasial terbuka, dan tren digital):

| # | Dataset | Deskripsi | Sumber | Berkas Bersih |
|---|---|---|---|---|
| **1** | **Kompetitor Usaha** | 2.796 titik POI usaha (*cafe, restaurant, convenience, grocery, laundry*) | OpenStreetMap (Overpass API) | `data/cleaned/kompetitor_per_wilayah.csv` |
| **2** | **Kondisi Ekonomi** | PDRB per kapita, kepadatan penduduk, pengeluaran per kapita 2024 | BPS Provinsi D.I. Yogyakarta | `data/cleaned/kondisi_ekonomi_wilayah.csv` |
| **3** | **Biaya Sewa** | Rata-rata tarif sewa properti komersial/ruko per m²/tahun | Platform Properti & BI Index | `data/cleaned/biaya_operasional.csv` |
| **4** | **Tren Sektor Usaha** | Time series jumlah usaha tahunan (2019–2023) + skor tren pencarian | BPS DIY & Google Trends | `data/cleaned/tren_sektor.csv` |
| **5** | **Statistik UMKM Resmi** | Jumlah total UMKM terdaftar 2025, tren tahunan, & distribusi sektor | SiBakul Jogja / Diskop UKM DIY | `data/cleaned/umkm_sibakul.csv` |

---

## 🧠 4 Pilar Analitik (`models/`)

Seluruh komputasi pemodelan analitik dikembangkan di folder `models/` secara modular dan independen dari antarmuka web:

### 1. Pilar 1: Skoring Kelayakan Sektor Usaha (`01_skoring.py`)
- **Metode:** *Multi-Criteria Decision Analysis* (MCDA) berbasis pembobotan linear.
- **Fitur Penentu:** Rasio kompetitor lokal (OSM), rasio kejenuhan UMKM agregat (SiBakul), PDRB per kapita, pengeluaran per kapita, dan beban biaya sewa wilayah.
- **Output:** Tabel skor kelayakan (skala 0–100) dan label kelayakan (*Layak*, *Cukup Layak*, *Kurang Layak*) untuk seluruh 25 kombinasi wilayah $\times$ sektor di `outputs/hasil/hasil_skoring_sektor.csv`.

### 2. Pilar 2: Clustering Karakteristik Ekonomi Wilayah (`02_clustering.py`)
- **Metode:** Unsupervised *K-Means Clustering* ($k=3$) dan reduksi dimensi *Principal Component Analysis* (PCA 2D, variansi terjelaskan $94,09\%$).
- **Hasil Segmentasi:**
  - **Klaster 0 (Urban Padat & Jenuh):** Kota Yogyakarta.
  - **Klaster 1 (Semi-Urban Bertumbuh):** Kabupaten Sleman dan Kabupaten Bantul.
  - **Klaster 2 (Rural Potensial & Biaya Rendah):** Kabupaten Kulon Progo dan Kabupaten Gunungkidul.
- **Output:** `outputs/hasil/hasil_clustering_wilayah.csv` dan model serialisasi di `models/saved/`.

### 3. Pilar 3: Forecasting Tren Pertumbuhan Sektor (`03_forecasting.py`)
- **Metode:** *Linear Trend Regression* pada data deret waktu tahunan BPS dengan estimasi *Confidence Interval* (CI) $95\%$ untuk proyeksi 2024–2026.
- **Output:** Estimasi jumlah unit usaha di masa depan beserta indikator arah tren (*Naik Signifikan*, *Stabil / Bertumbuh Moderat*, *Cenderung Melambat*) di `outputs/hasil/hasil_forecasting_sektor.csv`.

### 4. Pilar 4: Mesin Rekomendasi Personal (`04_rekomendasi.py`)
- **Metode:** Real-time lookup dan multi-criteria matching engine (`UMKMRecommender`).
- **Kapabilitas:**
  - Evaluasi wilayah spesifik disertai estimasi kebutuhan budget sewa tahunan.
  - Perankingan *Top 3 Wilayah Terbaik* apabila calon pelaku usaha memilih opsi terbuka ke seluruh wilayah DIY.

---

## 📁 Struktur Direktori Repositori

```text
Projek PDS/
├── app/                          # Fase 3: Antarmuka Web App & Dashboard
│   └── .gitkeep
├── data/
│   ├── raw/                      # Data mentah asli (BPS, OSM JSON, SiBakul, Trends, Sewa)
│   ├── interim/                  # Checkpoint data perantara
│   └── cleaned/                  # 7 CSV data bersih hasil pipeline (input pemodelan)
├── file/                         # Berkas presentasi (PDF) dan proposal
├── media/                        # Direncanakan: situs final (Laravel)
├── prototype/                    # Direncanakan: prototipe web (Streamlit)
├── milestones/                   # Laporan, panduan, dan materi presentasi
│   ├── MILESTONE_4_CLEAN_DATASET.md
│   ├── MILESTONE_5_DATA_QUALITY_AUDIT.md
│   ├── PANDUAN_PROPOSAL_UTS.md
│   ├── PANDUAN_SLIDE_PPT_UTS.md
│   ├── konsep_pemahaman.md       # Panduan pemahaman konseptual dan teknis (+ PDF)
│   ├── script_presentasi.md      # Script presentasi 15 menit (+ PDF)
│   └── evaluasi.md               # Evaluasi kritis metodologi
├── models/                       # Fase 2: Implementasi 4 Pilar Analitik
│   ├── 01_skoring.py             # Skoring Kelayakan MCDA
│   ├── 02_clustering.py          # K-Means & PCA Profil Wilayah
│   ├── 03_forecasting.py         # Regresi Tren Deret Waktu 2019-2026
│   ├── 04_rekomendasi.py         # Inference Engine Rekomendasi Personal
│   ├── run_all_models.py         # Master Runner seluruh model
│   └── saved/                    # Model serialisasi (.joblib)
├── notebooks/
│   ├── data_cleaning/            # 5 notebook pembersihan data (01_clean_*.ipynb dst.)
│   └── analisis/                 # 4 notebook analisis (01_mcda_*.ipynb dst.)
├── outputs/
│   ├── hasil/                    # CSV hasil Pilar 1-3 (skoring, klaster, forecasting)
│   ├── logs/                     # Folder log sistem
│   └── *.png                     # Gambar hasil analisis
├── scripts/                      # Fase 1: Pipeline ETL Data
│   ├── dataset1_osm/             # Pipeline ekstraksi OpenStreetMap
│   ├── dataset2_ekonomi/         # Pipeline data BPS Makroekonomi
│   ├── dataset3_sewa/            # Pipeline data harga sewa properti
│   ├── dataset4_tren/            # Pipeline data tren usaha & Google Trends
│   └── run_all_pipelines.py      # Master Runner pembersihan seluruh dataset
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🚀 Panduan Memulai

### 1. Kloning & Persiapan Lingkungan Virtual

```bash
# Kloning repositori
git clone https://github.com/username/projek-pds.git
cd "projek-pds"

# Buat virtual environment (disarankan Python 3.10+)
python -m venv .venv

# Aktivasi virtual environment
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Linux / macOS:
source .venv/bin/activate

# Pasang dependensi
pip install -r requirements.txt
```

### 2. Menjalankan Seluruh Pipeline Data (Fase 1)
Untuk memproses ulang seluruh data mentah dari sumber menjadi data bersih:
```bash
python scripts/run_all_pipelines.py
```

### 3. Menjalankan Seluruh Model Analitik (Fase 2)
Untuk menjalankan komputasi Pilar 1, Pilar 2, dan Pilar 3 secara serentak:
```bash
python models/run_all_models.py
```

### 4. Menguji Coba Rekomendasi Personal (Pilar 4)
Untuk melakukan simulasi inferensi mesin rekomendasi:
```bash
python models/04_rekomendasi.py
```

---

## 📑 Dokumentasi & Berkas Penyerahan Projek

### Panduan Arsitektur & Rangkuman Insight:
- [**konsep_pemahaman.md**](./milestones/konsep_pemahaman.md): Dokumen pemahaman konseptual dan teknis: latar belakang, alur data, metode 4 pilar, keputusan metodologis, keterbatasan, dan glosarium istilah.

### Laporan Akademik Terstruktur (Milestones PDS):
Laporan resmi untuk evaluasi mata kuliah Pengantar Data Sains pada folder [`milestones/`](./milestones/):
- [**Milestone 4 — Clean Dataset & Data Preparation**](./milestones/MILESTONE_4_CLEAN_DATASET.md): Dokumentasi pembersihan data, penanganan duplikasi OSM, normalisasi biaya sewa, transformasi BPS, dan Kamus Data (Data Dictionary) lengkap.
- [**Milestone 5 — Data Quality Audit & Analytical Task Selection**](./milestones/MILESTONE_5_DATA_QUALITY_AUDIT.md): *Data Quality Scorecard* 4 dimensi, 4 temuan data riil & mitigasi, serta justifikasi pemilihan pendekatan analitik.

---

## 👥 Tim Penyusun
Projek ini dikembangkan sebagai pemenuhan tugas mata kuliah **Pengantar Data Sains (PDS)**, Program Studi Data Science / Informatika, Semester 3.
