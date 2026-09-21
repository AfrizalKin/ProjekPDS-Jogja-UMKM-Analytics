"""
Orchestrator Pipeline Pengambilan Data Kompetitor UMKM (Overpass API)
Projek PDS - Rekomendasi Kelayakan Usaha UMKM
"""

import sys
import argparse
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
from scripts.dataset1_osm.clean_dedup import clean_and_deduplicate


def run_pipeline(selected_wilayah: str = "all", selected_kategori: str = "all", run_clean: bool = True):
    """
    Menjalankan pipeline pengambilan data untuk kombinasi wilayah x kategori.

    Args:
        selected_wilayah: ID wilayah tertentu atau 'all'
        selected_kategori: ID kategori tertentu atau 'all'
        run_clean: Apakah langsung menjalankan pembersihan & deduplikasi setelah fetching
    """
    # Filter wilayah target
    if selected_wilayah != "all":
        wilayah_list = [w for w in TARGET_WILAYAH if w["id"] == selected_wilayah]
        if not wilayah_list:
            print(f"[Error] Wilayah '{selected_wilayah}' tidak ditemukan dalam config.")
            print(f"Pilihan yang tersedia: {[w['id'] for w in TARGET_WILAYAH]}")
            return
    else:
        wilayah_list = TARGET_WILAYAH

    # Filter kategori target
    if selected_kategori != "all":
        kategori_list = [k for k in KATEGORI_UMKM if k["id"] == selected_kategori]
        if not kategori_list:
            print(f"[Error] Kategori '{selected_kategori}' tidak ditemukan dalam config.")
            print(f"Pilihan yang tersedia: {[k['id'] for k in KATEGORI_UMKM]}")
            return
    else:
        kategori_list = KATEGORI_UMKM

    total_kombinasi = len(wilayah_list) * len(kategori_list)

    print("=" * 70)
    print("DATASET 1: PIPELINE PENGAMBILAN DATA KOMPETITOR UMKM (OVERPASS API)")
    print("=" * 70)
    print(f"Total Wilayah Target  : {len(wilayah_list)} ({', '.join([w['id'] for w in wilayah_list])})")
    print(f"Total Kategori UMKM   : {len(kategori_list)} ({', '.join([k['id'] for k in kategori_list])})")
    print(f"Total Kombinasi Query : {total_kombinasi}")
    print(f"Direktori Output Raw  : {DATA_RAW_OSM_DIR}")
    print(f"Direktori Output Log  : {OUTPUTS_LOGS_DIR}")
    print("=" * 70)

    tasks = []
    for w in wilayah_list:
        for k in kategori_list:
            tasks.append((w, k))

    sukses_count = 0
    gagal_count = 0
    total_poi_terkumpul = 0

    with tqdm(total=len(tasks), desc="Progress Fetching", unit="query") as pbar:
        for wilayah, kategori in tasks:
            desc_text = f"{wilayah['id']} x {kategori['id']}"
            pbar.set_postfix_str(desc_text)

            sukses, data_json, pesan = fetch_overpass_data(
                wilayah_id=wilayah["id"],
                nama_wilayah_query=wilayah["nama_query"],
                kategori_id=kategori["id"],
                tag_key=kategori["key"],
                tag_value=kategori["value"],
                admin_level=wilayah.get("admin_level", "5"),
                bbox=wilayah.get("bbox")
            )

            if sukses:
                sukses_count += 1
                if data_json and "elements" in data_json:
                    poi_count = len(data_json["elements"])
                    total_poi_terkumpul += poi_count
                    pbar.set_postfix_str(f"{desc_text} -> {poi_count} POI")
            else:
                gagal_count += 1
                pbar.set_postfix_str(f"{desc_text} -> GAGAL")

            pbar.update(1)

    print("\n" + "=" * 70)
    print("PENGAMBILAN DATA SELESAI")
    print("=" * 70)
    print(f"Query Sukses        : {sukses_count}/{total_kombinasi}")
    print(f"Query Gagal         : {gagal_count}/{total_kombinasi}")
    print(f"Total POI Mentah    : {total_poi_terkumpul}")
    if gagal_count > 0:
        print(f"Detail error tercatat di: {OUTPUTS_LOGS_DIR / 'fetch_errors.log'}")
    print("=" * 70)

    # Otomatis jalankan pembersihan & deduplikasi jika diminta
    if run_clean and sukses_count > 0:
        print("\nMenjalankan tahap pembersihan & deduplikasi data...")
        clean_and_deduplicate()


def main():
    parser = argparse.ArgumentParser(description="Pipeline Dataset 1 OSM - Pengambilan Data UMKM Overpass API")
    parser.add_argument(
        "--wilayah",
        type=str,
        default="all",
        help="Filter wilayah berdasarkan ID (default: 'all')"
    )
    parser.add_argument(
        "--kategori",
        type=str,
        default="all",
        help="Filter kategori berdasarkan ID (default: 'all')"
    )
    parser.add_argument(
        "--no-clean",
        action="store_true",
        help="Jangan jalankan pembersihan/deduplikasi otomatis setelah fetching"
    )

    args = parser.parse_args()
    run_pipeline(
        selected_wilayah=args.wilayah,
        selected_kategori=args.kategori,
        run_clean=not args.no_clean
    )


if __name__ == "__main__":
    main()
