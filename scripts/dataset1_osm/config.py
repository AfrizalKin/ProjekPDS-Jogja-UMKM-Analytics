"""
Konfigurasi Ekstraksi Dataset 1 (OpenStreetMap via Overpass API)
Projek PDS - UMKM Recommender
"""

from pathlib import Path

# ==========================================
# 1. PATH DIREKTORI PROYEK
# ==========================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw" / "osm"
INTERIM_DATA_DIR = DATA_DIR / "interim"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
LOG_DIR = BASE_DIR / "outputs" / "logs"

# Pastikan folder output tersedia
for folder in [RAW_DATA_DIR, INTERIM_DATA_DIR, PROCESSED_DATA_DIR, LOG_DIR]:
    folder.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. OVERPASS API ENDPOINTS & SETTINGS
# ==========================================
# Daftar mirror Overpass API untuk failover/retry
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter"
]

DEFAULT_TIMEOUT = 120  # detik per query
MAX_RETRIES = 3
RETRY_DELAY = 10       # detik jeda jika kena rate limit (HTTP 429)
USER_AGENT = "ProjekPDS-UMKM-Recommender/1.0 (Academic Research; Python requests)"

# ==========================================
# 3. BOUNDING BOX WILAYAH (BBOX)
# Format Overpass: (south, west, north, east) / (min_lat, min_lon, max_lat, max_lon)
# ==========================================
BBOX_WILAYAH = {
    "bandung_kota": {
        "nama": "Kota Bandung",
        "bbox": (-6.9700, 107.5400, -6.8500, 107.7200)
    },
    "jakarta_selatan": {
        "nama": "Jakarta Selatan",
        "bbox": (-6.3700, 106.7400, -6.2000, 106.8600)
    },
    "surabaya_pusat": {
        "nama": "Surabaya Pusat & Sekitarnya",
        "bbox": (-7.3300, 112.6800, -7.2200, 112.8000)
    },
    "yogyakarta_kota": {
        "nama": "Kota Yogyakarta",
        "bbox": (-7.8400, 110.3400, -7.7600, 110.4200)
    }
}

# Wilayah default yang digunakan jika tidak ditentukan
DEFAULT_WILAYAH = "bandung_kota"

# ==========================================
# 4. TAG OSM TARGET & KATEGORI UMKM
# ==========================================
# Tag OSM yang relevan untuk entitas usaha / UMKM
TARGET_TAG_KEYS = ["amenity", "shop", "craft"]

# Nilai tag yang dicakup
TARGET_TAG_VALUES = {
    "amenity": [
        "restaurant", "cafe", "fast_food", "food_court", "ice_cream", 
        "bar", "pub", "marketplace", "pharmacy", "clinic", "dentist", 
        "bank", "atm", "car_wash", "fuel"
    ],
    "shop": [
        "convenience", "supermarket", "bakery", "clothes", "hairdresser", 
        "beauty", "laundry", "car_repair", "motorcycle_repair", "hardware", 
        "electronics", "mobile_phone", "stationery", "tailor", "variety_store",
        "beverages", "kiosk", "department_store", "general", "florist"
    ],
    "craft": [
        "tailor", "carpenter", "shoemaker", "photographer", "caterer",
        "electronics_repair", "metal_construction"
    ]
}

# Standarisasi Sektor UMKM
SEKTOR_MAPPING = {
    # Kuliner / F&B
    "restaurant": "Kuliner / F&B",
    "cafe": "Kuliner / F&B",
    "fast_food": "Kuliner / F&B",
    "food_court": "Kuliner / F&B",
    "ice_cream": "Kuliner / F&B",
    "bakery": "Kuliner / F&B",
    "beverages": "Kuliner / F&B",
    "bar": "Kuliner / F&B",
    "pub": "Kuliner / F&B",
    "caterer": "Kuliner / F&B",

    # Ritel & Kelontong
    "convenience": "Ritel & Kelontong",
    "supermarket": "Ritel & Kelontong",
    "marketplace": "Ritel & Kelontong",
    "kiosk": "Ritel & Kelontong",
    "variety_store": "Ritel & Kelontong",
    "general": "Ritel & Kelontong",
    "department_store": "Ritel & Kelontong",
    "stationery": "Ritel & Kelontong",
    "florist": "Ritel & Kelontong",

    # Fesyen & Kecantikan
    "clothes": "Fesyen & Kecantikan",
    "hairdresser": "Fesyen & Kecantikan",
    "beauty": "Fesyen & Kecantikan",
    "tailor": "Fesyen & Kecantikan",
    "shoemaker": "Fesyen & Kecantikan",

    # Jasa & Reparasi
    "laundry": "Jasa & Reparasi",
    "photographer": "Jasa & Reparasi",
    "electronics": "Jasa & Reparasi",
    "electronics_repair": "Jasa & Reparasi",
    "mobile_phone": "Jasa & Reparasi",
    "carpenter": "Jasa & Reparasi",
    "metal_construction": "Jasa & Reparasi",
    "hardware": "Jasa & Reparasi",

    # Otomotif & Bengkel
    "car_repair": "Otomotif & Bengkel",
    "motorcycle_repair": "Otomotif & Bengkel",
    "car_wash": "Otomotif & Bengkel",
    "fuel": "Otomotif & Bengkel",

    # Kesehatan & Farmasi
    "pharmacy": "Kesehatan & Farmasi",
    "clinic": "Kesehatan & Farmasi",
    "dentist": "Kesehatan & Farmasi",

    # Keuangan
    "bank": "Keuangan & Perbankan",
    "atm": "Keuangan & Perbankan"
}
