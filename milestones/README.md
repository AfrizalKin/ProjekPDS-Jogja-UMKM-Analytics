# 🎯 Berkas Penyerahan Tugas Milestone (Mata Kuliah Pengantar Data Sains)
**Projek:** Sistem Rekomendasi Kelayakan Sektor Usaha UMKM Berbasis Data di D.I. Yogyakarta  
**Mata Kuliah:** Pengantar Data Sains (PDS) — Semester 3  

Repositori folder `milestones/` ini berisi dokumentasi resmi dan laporan penyerahan berkas tugas terstruktur per pertemuan kuliah:

---

## 📑 Daftar Berkas Milestone

| Milestone | Topik & Pertemuan | Berkas Laporan | Status |
| :--- | :--- | :--- | :---: |
| **Milestone 4** | Clean Dataset & Data Preparation *(Pertemuan 5)* | [`MILESTONE_4_CLEAN_DATASET.md`](./MILESTONE_4_CLEAN_DATASET.md) | **SIAP KUMPUL (100%)** |
| **Milestone 5** | Data Quality Audit & Analytical Task Selection *(Pertemuan 6)* | [`MILESTONE_5_DATA_QUALITY_AUDIT.md`](./MILESTONE_5_DATA_QUALITY_AUDIT.md) | **SIAP KUMPUL (100%)** |
| **Milestone 6** | Analytical Task, Modeling & Preliminary Analysis *(Menuju UTS)* | Terimplementasi di folder [`models/`](../models/) | **SELESAI (100%)** |

---

## 📊 Ringkasan Dataset Bersih yang Diserahkan
Seluruh dataset hasil pembersihan dan transformasi telah disimpan dalam format CSV standar di direktori `data/processed/`:
1. `kompetitor_per_wilayah.csv` (Dataset 1: POI Kompetitor UMKM dari OpenStreetMap — 2.796 baris)
2. `kondisi_ekonomi_wilayah.csv` (Dataset 2: Makroekonomi BPS 2024 & UMKM SiBakul 2025 — 5 baris)
3. `biaya_operasional.csv` (Dataset 3: Indeks Biaya Sewa Properti Komersial — 5 baris)
4. `tren_sektor.csv` (Dataset 4: Laju Pertumbuhan Usaha Time Series & Google Trends — 125 baris)
5. `umkm_sibakul.csv` (Dataset 5: Statistik UMKM Resmi Dinas Koperasi & UKM DIY 2025)

Skrip pembersihan otomatis terpadu: `python scripts/run_all_pipelines.py`  
Skrip pemodelan analitik terpadu: `python models/run_all_models.py`
