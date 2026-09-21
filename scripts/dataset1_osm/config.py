"""
Konfigurasi Dataset 1: Kepadatan Kompetitor UMKM dari OpenStreetMap (Overpass API)
Projek PDS - Rekomendasi Kelayakan Usaha UMKM
"""

from pathlib import Path

# ==============================================================================
# 1. DIREKTORI PROJEK
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_RAW_OSM_DIR = BASE_DIR / "data" / "raw" / "osm"
DATA_INTERIM_DIR = BASE_DIR / "data" / "interim"
DATA_PROCESSED_DIR = BASE_DIR / "data" / "processed"
OUTPUTS_LOGS_DIR = BASE_DIR / "outputs" / "logs"

# Pastikan seluruh direktori target telah terbentuk
for d in [DATA_RAW_OSM_DIR, DATA_INTERIM_DIR, DATA_PROCESSED_DIR, OUTPUTS_LOGS_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ==============================================================================
# 2. KONFIGURASI OVERPASS API
# ==============================================================================
OVERPASS_ENDPOINTS = [
    "https://overpass-api.de/api/interpreter",
    "https://lz4.overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]
OVERPASS_ENDPOINT = OVERPASS_ENDPOINTS[0]
REQUEST_TIMEOUT = 35          # detik per request
MAX_RETRIES = 3              # maksimum percobaan ulang jika gagal / timeout
RETRY_DELAY = 10             # detik jeda jika terjadi error HTTP 429 atau 504
SLEEP_BETWEEN_REQUESTS = 3.0 # jeda minimal antar request berturut-turut (detik)
USER_AGENT = "ProjekPDS-UMKM-Recommender/1.0 (Academic Research)"

# ==============================================================================
# 3. DAFTAR WILAYAH TARGET (KABUPATEN / KOTA)
# Di D.I. Yogyakarta, batas administratif kabupaten/kota di OpenStreetMap
# bertingkat admin_level="5" (admin_level="6" adalah batas Kecamatan).
# 
# Catatan Validasi OSM:
# - Kota Yogyakarta: name="Kota Yogyakarta", admin_level="5"
# - Sleman: name="Sleman", admin_level="5"
# - Bantul: name="Bantul", admin_level="5"
# - Kulon Progo: name="Kulonprogo" (tanpa spasi di OSM), admin_level="5"
# - Gunungkidul: name="Gunungkidul", admin_level="5"
#
# BBox format: (min_lat, min_lon, max_lat, max_lon)
# ==============================================================================
TARGET_WILAYAH = [
    {
        "id": "sleman",
        "nama_query": "Sleman",
        "label": "Kabupaten Sleman",
        "admin_level": "5",
        "bbox": (-7.8376, 110.2159, -7.5413, 110.5499)
    },
    {
        "id": "kota_yogyakarta",
        "nama_query": "Kota Yogyakarta",
        "label": "Kota Yogyakarta",
        "admin_level": "5",
        "bbox": (-7.8402, 110.3443, -7.7665, 110.4068)
    },
    {
        "id": "bantul",
        "nama_query": "Bantul",
        "label": "Kabupaten Bantul",
        "admin_level": "5",
        "bbox": (-8.0282, 110.2039, -7.7680, 110.5213)
    },
    {
        "id": "kulon_progo",
        "nama_query": "Kulonprogo",
        "label": "Kabupaten Kulon Progo",
        "admin_level": "5",
        "bbox": (-7.9832, 110.0036, -7.6416, 110.2741)
    },
    {
        "id": "gunungkidul",
        "nama_query": "Gunungkidul",
        "label": "Kabupaten Gunungkidul",
        "admin_level": "5",
        "bbox": (-8.2043, 110.3306, -7.7820, 110.8387)
    }
]

# ==============================================================================
# 4. DAFTAR KATEGORI USAHA UMKM & TAG OSM
# Kategori diverifikasi berdasarkan OpenStreetMap Wiki:
# - amenity=restaurant: Tempat makan & minum dengan layanan meja/makanan olahan
# - shop=convenience: Minimarket / toko serba ada skala kecil
# - shop=laundry: Jasa pencucian pakaian (kiloan/self-service)
# - amenity=cafe: Kafe / kedai kopi / tempat nongkrong santai
# - shop=grocery: Toko kelontong tradisional / sembako
# ==============================================================================
KATEGORI_UMKM = [
    {
        "id": "restaurant",
        "label": "Restoran / Warung Makan",
        "key": "amenity",
        "value": "restaurant"
    },
    {
        "id": "convenience",
        "label": "Minimarket / Convenience Store",
        "key": "shop",
        "value": "convenience"
    },
    {
        "id": "laundry",
        "label": "Jasa Laundry",
        "key": "shop",
        "value": "laundry"
    },
    {
        "id": "cafe",
        "label": "Kafe / Coffee Shop",
        "key": "amenity",
        "value": "cafe"
    },
    {
        "id": "grocery",
        "label": "Toko Kelontong Tradisional",
        "key": "shop",
        "value": "grocery"
    }
]
