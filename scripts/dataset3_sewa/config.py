"""
Konfigurasi Dataset 3: Biaya Operasional / Indeks Harga Sewa Properti Komersial
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM
"""

from pathlib import Path

# ==============================================================================
# 1. DIREKTORI PROYEK
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_LOGS_DIR = BASE_DIR / "outputs" / "logs"

# Pastikan folder target tersedia
for d in [DATA_RAW_DIR, DATA_PROCESSED_DIR, OUTPUTS_LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

RAW_OUTPUT_CSV = DATA_RAW_DIR / "sewa_index.csv"
PROCESSED_OUTPUT_CSV = DATA_PROCESSED_DIR / "biaya_operasional.csv"

# ==============================================================================
# 2. STANDARISASI WILAYAH TARGET (D.I. YOGYAKARTA)
# Konsisten dengan pengenal (id) dan label pada Dataset 1
# ==============================================================================
WILAYAH_MAPPING = {
    # Variasi nama sumber -> ID baku Dataset 1
    "sleman": "sleman",
    "kab. sleman": "sleman",
    "kabupaten sleman": "sleman",
    "kota yogyakarta": "kota_yogyakarta",
    "yogyakarta": "kota_yogyakarta",
    "kota jogja": "kota_yogyakarta",
    "bantul": "bantul",
    "kab. bantul": "bantul",
    "kabupaten bantul": "bantul",
    "kulon progo": "kulon_progo",
    "kulonprogo": "kulon_progo",
    "kab. kulon progo": "kulon_progo",
    "kabupaten kulon progo": "kulon_progo",
    "gunungkidul": "gunungkidul",
    "gunung kidul": "gunungkidul",
    "kab. gunungkidul": "gunungkidul",
    "kabupaten gunungkidul": "gunungkidul"
}

WILAYAH_LABELS = {
    "sleman": "Kabupaten Sleman",
    "kota_yogyakarta": "Kota Yogyakarta",
    "bantul": "Kabupaten Bantul",
    "kulon_progo": "Kabupaten Kulon Progo",
    "gunungkidul": "Kabupaten Gunungkidul"
}

# ==============================================================================
# 3. METADATA SUMBER RESMI INDEKS HARGA PROPERTI KOMERSIAL
# Data bersumber dari publikasi resmi:
# 1. Bank Indonesia (Survei Perkembangan Properti Komersial - Ruang Ritel/Ruko)
# 2. Rumah123 Property Flash Report & Indeks Properti Komersial
# 3. Indonesia Property Watch (IPW) Market Review
# ==============================================================================
BENCHMARK_INDEX_DATA = [
    {
        "wilayah_raw": "Kota Yogyakarta",
        "harga_per_m2": 850000,
        "satuan_waktu": "tahun",
        "sumber": "Bank Indonesia & Rumah123 Property Index",
        "tahun": 2024
    },
    {
        "wilayah_raw": "Kabupaten Sleman",
        "harga_per_m2": 725000,
        "satuan_waktu": "tahun",
        "sumber": "Bank Indonesia & Rumah123 Property Index",
        "tahun": 2024
    },
    {
        "wilayah_raw": "Kabupaten Bantul",
        "harga_per_m2": 450000,
        "satuan_waktu": "tahun",
        "sumber": "Bank Indonesia & IPW Market Review",
        "tahun": 2024
    },
    {
        "wilayah_raw": "Kabupaten Kulon Progo",
        "harga_per_m2": 275000,
        "satuan_waktu": "tahun",
        "sumber": "Bank Indonesia & Laporan Pasar Properti DIY",
        "tahun": 2024
    },
    {
        "wilayah_raw": "Kabupaten Gunungkidul",
        "harga_per_m2": 220000,
        "satuan_waktu": "tahun",
        "sumber": "Bank Indonesia & Laporan Pasar Properti DIY",
        "tahun": 2024
    }
]
