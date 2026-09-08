# Projek PDS - Sistem Rekomendasi Lokasi UMKM

Repositori ini berisi implementasi pipeline data, pembersihan, eksplorasi spasial, dan pemodelan sistem rekomendasi lokasi strategis bagi UMKM (*Micro, Small, and Medium Enterprises*).

Pada tahap **Dataset 1**, pipeline difokuskan pada ekstraksi dan standardisasi data *Point of Interest* (POI) dari **OpenStreetMap (OSM)** menggunakan **Overpass API**.

---

## 📁 Struktur Direktori

```text
Projek PDS/
├── data/
│   ├── raw/
│   │   └── osm/                  # Hasil mentah query Overpass (JSON)
│   ├── interim/                  # Hasil ekstraksi/dedup tahap awal (CSV)
│   └── processed/                # Tabel final siap pakai (CSV per wilayah-sektor)
├── notebooks/
│   └── 01_eksplorasi_osm.ipynb   # Eksplorasi manual / EDA & visualisasi peta
├── scripts/
│   └── dataset1_osm/
│       ├── config.py             # Daftar wilayah, kategori usaha, bounding box
│       ├── fetch_overpass.py     # Fungsi request ke Overpass API (retry & failover)
│       ├── grid_sampling.py      # Pembagian area query ke sub-grid
│       ├── clean_dedup.py        # Dedup hasil, standardisasi sektor UMKM
│       └── main.py               # Orchestrator, menjalankan seluruh pipeline
├── outputs/
│   └── logs/                     # Log request (status request, retry, error)
├── requirements.txt              # Daftar dependensi Python
└── README.md                     # Dokumentasi projek
```

---

## 🚀 Panduan Memulai

### 1. Instalasi Dependensi
Pastikan Anda menggunakan Python 3.10+ (disarankan menggunakan *virtual environment*):

```bash
# Buat dan aktifkan virtual environment (opsional)
python -m venv venv
venv\Scripts\activate      # Windows

# Install dependensi yang dibutuhkan
pip install -r requirements.txt
```

### 2. Menjalankan Pipeline Ekstraksi Data OSM
Jalankan orchestrator `main.py` untuk mengunduh, membersihkan, dan menstandardisasi data UMKM secara otomatis:

```bash
# Menjalankan untuk wilayah default (Kota Bandung) dengan grid sampling 2x2
python scripts/dataset1_osm/main.py --wilayah bandung_kota

# Pilihan wilayah lainnya:
python scripts/dataset1_osm/main.py --wilayah jakarta_selatan
python scripts/dataset1_osm/main.py --wilayah surabaya_pusat
python scripts/dataset1_osm/main.py --wilayah yogyakarta_kota

# Opsi kustomisasi grid:
python scripts/dataset1_osm/main.py --wilayah bandung_kota --grid-rows 3 --grid-cols 3
```

### 3. Eksplorasi Data (EDA) di Jupyter Notebook
Buka Jupyter Notebook untuk melihat visualisasi sebaran dan eksplorasi data:

```bash
jupyter lab
# atau
jupyter notebook
```
Buka file `notebooks/01_eksplorasi_osm.ipynb`.

---

## 🛠️ Penjelasan Modul `scripts/dataset1_osm/`

| File | Peran & Deskripsi |
|---|---|
| `config.py` | Berisi koordinat *Bounding Box* (BBox), daftar tag OSM target (`amenity`, `shop`, `craft`), mapping sektor UMKM, dan endpoint mirror Overpass API. |
| `grid_sampling.py` | Membagi wilayah BBox menjadi sel-sel grid yang lebih kecil untuk mencegah error HTTP 504 Gateway Timeout pada wilayah padat. |
| `fetch_overpass.py` | Mengirim query Overpass QL dengan penanganan timeout, backoff rate limit (HTTP 429), dan multi-mirror fallback. Hasil mentah disimpan ke `data/raw/osm/`. |
| `clean_dedup.py` | Mem-parsing nodes/ways, membersihkan missing values, melakukan deduplikasi spasial/ID, dan memetakan ke sektor UMKM (Kuliner, Ritel, Jasa, dsb.). |
| `main.py` | Skrip orchestrator utama dengan dukungan CLI argument yang menggabungkan seluruh tahapan dari *fetch* hingga ekspor ke `data/processed/`. |

---

## 📊 Standardisasi Sektor UMKM

Kategori mentah dari OSM dikelompokkan ke dalam beberapa sektor utama:
- **Kuliner / F&B**: Kafe, restoran, fast food, food court, bakery, dsb.
- **Ritel & Kelontong**: Toko kelontong, minimarket, supermarket, kios, dsb.
- **Fesyen & Kecantikan**: Pakaian, butik, salon, penjahit, dsb.
- **Jasa & Reparasi**: Laundry, servis elektronik, reparasi hp, tukang kayu, dsb.
- **Otomotif & Bengkel**: Bengkel motor/mobil, cuci kendaraan, dsb.
- **Kesehatan & Farmasi**: Apotek, klinik, dsb.
