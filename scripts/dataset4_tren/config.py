"""
Konfigurasi Dataset 4: Tren Pertumbuhan Sektor Usaha UMKM (BPS & Google Trends)
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM
"""

from pathlib import Path

# ==============================================================================
# 1. DIREKTORI PROYEK
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_RAW_BPS_DIR = BASE_DIR / "data" / "raw" / "bps"
DATA_RAW_TRENDS_DIR = BASE_DIR / "data" / "raw" / "trends"
DATA_INTERIM_DIR = BASE_DIR / "data" / "interim"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_LOGS_DIR = BASE_DIR / "outputs" / "logs"

# Pastikan folder target tersedia
for d in [DATA_RAW_BPS_DIR, DATA_RAW_TRENDS_DIR, DATA_INTERIM_DIR, DATA_PROCESSED_DIR, OUTPUTS_LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

BPS_CLEANED_CSV = DATA_INTERIM_DIR / "bps_cleaned.csv"
TRENDS_RAW_CSV = DATA_RAW_TRENDS_DIR / "trends_raw.csv"
PROCESSED_TREN_CSV = DATA_PROCESSED_DIR / "tren_sektor.csv"
LOG_TRENDS_ERROR = OUTPUTS_LOGS_DIR / "fetch_trends_errors.log"

# ==============================================================================
# 2. STANDARISASI WILAYAH TARGET (D.I. YOGYAKARTA)
# Konsisten 100% dengan Dataset 1 (OSM) dan Dataset 3 (Biaya Operasional)
# ==============================================================================
WILAYAH_MAPPING = {
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
    "kabupaten gunungkidul": "gunungkidul",
    "d.i. yogyakarta": "diy",
    "di yogyakarta": "diy",
    "daerah istimewa yogyakarta": "diy"
}

WILAYAH_LABELS = {
    "sleman": "Kabupaten Sleman",
    "kota_yogyakarta": "Kota Yogyakarta",
    "bantul": "Kabupaten Bantul",
    "kulon_progo": "Kabupaten Kulon Progo",
    "gunungkidul": "Kabupaten Gunungkidul",
    "diy": "D.I. Yogyakarta (Provinsi)"
}

# ==============================================================================
# 3. PEMETAAN SEKTOR USAHA & KODE KBLI TERKAIT
# Sinkron dengan kategori UMKM pada Dataset 1
# ==============================================================================
SEKTOR_KBLI_MAPPING = {
    "restaurant": {
        "label": "Restoran / Penyediaan Makanan",
        "kbli_prefix": ["561", "I-561"],
        "keywords_alt": ["restoran", "rumah makan", "kuliner", "warung makan"]
    },
    "cafe": {
        "label": "Kafe / Kedai Minuman",
        "kbli_prefix": ["563", "I-563"],
        "keywords_alt": ["kafe", "cafe", "kedai kopi", "coffee shop"]
    },
    "convenience": {
        "label": "Minimarket / Toko Modern",
        "kbli_prefix": ["471", "G-471"],
        "keywords_alt": ["minimarket", "swalayan", "toko serba ada"]
    },
    "grocery": {
        "label": "Toko Kelontong Tradisional",
        "kbli_prefix": ["471", "G-471"],
        "keywords_alt": ["toko kelontong", "sembako", "warung kelontong"]
    },
    "laundry": {
        "label": "Jasa Laundry / Pencucian",
        "kbli_prefix": ["962", "S-962"],
        "keywords_alt": ["laundry", "binatu", "cuci pakaian"]
    }
}

# ==============================================================================
# 4. KONFIGURASI GOOGLE TRENDS (OPSIONAL & PELENGKAP)
# ==============================================================================
TRENDS_CONFIG = {
    "geo": "ID",              # Wilayah Indonesia (lebih stabil & tidak banyak zero-values)
    "timeframe": "today 5-y", # 5 tahun terakhir
    "sleep_seconds": 12,      # Jeda minimal 10-12 detik per request untuk hindari 429
    "max_retries": 3,         # Maksimal percobaan ulang per keyword
    "retry_backoff": 15       # Jeda tambahan bila terkena rate-limit
}

# Keyword target yang dipetakan ke sektor usaha
TRENDS_KEYWORDS = [
    {"sektor": "cafe", "keyword": "coffee shop jogja"},
    {"sektor": "restaurant", "keyword": "kuliner jogja"},
    {"sektor": "laundry", "keyword": "laundry jogja"},
    {"sektor": "convenience", "keyword": "minimarket"},
    {"sektor": "grocery", "keyword": "toko kelontong"}
]
