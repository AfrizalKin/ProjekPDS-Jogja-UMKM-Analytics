"""
Orchestrator Pipeline Pengambilan Data Kompetitor UMKM (Overpass API)
Projek PDS - Rekomendasi Kelayakan Usaha UMKM
"""

import sys
import time
from pathlib import Path
from tqdm import tqdm

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset1_osm.config import (
    TARGET_WILAYAH,
    KATEGORI_UMKM,
    DATA_RAW_OSM_DIR,
    OUTPUTS_LOGS_DIR
)
from scripts.dataset1_osm.fetch_overpass import fetch_overpass_data


def run_pipeline():
    """
    Menjalankan loop pengambilan data untuk setiap kombinasi wilayah x kategori.
    """
    total_kombinasi = len(TARGET_WILAYAH) * len(KATEGORI_UMKM)
    
    print("=" * 70)
    print("DATASET 1: PENGAMBILAN DATA KOMPETITOR UMKM (OVERPASS API)")
    print("=" * 70)
    print(f"Total Wilayah Target  : {len(TARGET_WILAYAH)}")
    print(f"Total Kategori UMKM   : {len(KATEGORI_UMKM)}")
    print(f"Total Kombinasi Query : {total_kombinasi}")
    print(f"Direktori Output Raw  : {DATA_RAW_OSM_DIR}")
    print(f"Direktori Output Log  : {OUTPUTS_LOGS_DIR}")
    print("=" * 70)

    # Buat daftar seluruh kombinasi task
    tasks = []
    for w in TARGET_WILAYAH:
        for k in KATEGORI_UMKM:
            tasks.append((w, k))

    sukses_count = 0
    gagal_count = 0

    # Progress bar interaktif menggunakan tqdm
    with tqdm(total=len(tasks), desc="Progress Fetching", unit="query") as pbar:
        for wilayah, kategori in tasks:
            desc_text = f"{wilayah['id']} x {kategori['id']}"
            pbar.set_postfix_str(desc_text)

            sukses, _, pesan = fetch_overpass_data(
                wilayah_id=wilayah["id"],
                nama_wilayah_query=wilayah["nama_query"],
                kategori_id=kategori["id"],
                tag_key=kategori["key"],
                tag_value=kategori["value"],
                admin_level=wilayah.get("admin_level", "6")
            )

            if sukses:
                sukses_count += 1
            else:
                gagal_count += 1

            pbar.update(1)

    print("\n" + "=" * 70)
    print("PENGAMBILAN DATA SELESAI")
    print("=" * 70)
    print(f"Query Sukses : {sukses_count}/{total_kombinasi}")
    print(f"Query Gagal  : {gagal_count}/{total_kombinasi}")
    if gagal_count > 0:
        print(f"Detail error tercatat di: {OUTPUTS_LOGS_DIR / 'fetch_errors.log'}")
    print("Langkah berikutnya: Jalankan clean_dedup.py untuk memproses data mentah.")
    print("=" * 70)


if __name__ == "__main__":
    run_pipeline()
