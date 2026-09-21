"""
Master Runner Pipeline Data Projek PDS
Menjalankan seluruh pipeline pembersihan data (Dataset 1, 2, 3, 4) dengan 1 perintah.

Penggunaan:
    python scripts/run_all_pipelines.py
    python scripts/run_all_pipelines.py --skip-osm-fetch  # Gunakan data mentah OSM yang sudah ada
"""

import sys
import argparse
from pathlib import Path

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset1_osm.clean_dedup import clean_and_deduplicate
from scripts.dataset2_ekonomi.clean_ekonomi import (
    clean_pdrb,
    clean_kepadatan,
    clean_pengeluaran,
    clean_sibakul,
    merge_and_validate,
    find_file,
    resolve_input_dir,
    PROCESSED_OUTPUT_CSV as P2_OUT,
    PROCESSED_SIBAKUL_CSV as P5_OUT
)
from scripts.dataset3_sewa.clean_harga import clean_and_standardize_harga
from scripts.dataset4_tren.clean_tren import process_and_merge_tren
from scripts.dataset4_tren.fetch_bps import load_bps_files


def run_all(skip_osm_fetch: bool = True):
    print("\n" + "=" * 80)
    print("[PIPELINE] MENJALANKAN PIPELINE LENGKAP PEMBERSIHAN DATA (PROJEK PDS)")
    print("=" * 80)

    # 1. Dataset 1: OpenStreetMap (Kompetitor UMKM)
    print("\n[DATASET 1/4] Pembersihan & Deduplikasi POI OpenStreetMap...")
    df_osm = clean_and_deduplicate()
    print(f"  [OK] Sukses: {len(df_osm)} titik lokasi usaha UMKM siap di data/processed/kompetitor_per_wilayah.csv")

    # 2. Dataset 2 & 5: BPS Kondisi Ekonomi Wilayah & Data UMKM SiBakul
    print("\n[DATASET 2 & 5] Pembersihan & Integrasi Indikator Ekonomi BPS & SiBakul DIY...")
    input_dir_bps = resolve_input_dir()
    df_pdrb = clean_pdrb(find_file(input_dir_bps, "*PDRB*"))
    df_kepadatan = clean_kepadatan(find_file(input_dir_bps, "*Kepadatan*"))
    df_pengeluaran = clean_pengeluaran(find_file(input_dir_bps, "*Pengeluaran*"))
    df_sibakul = clean_sibakul()

    df_ekonomi, df_sibakul_out = merge_and_validate(df_pdrb, df_kepadatan, df_pengeluaran, df_sibakul)
    P2_OUT.parent.mkdir(parents=True, exist_ok=True)
    df_ekonomi.to_csv(P2_OUT, index=False)
    print(f"  [OK] Sukses: 5 kabupaten/kota DIY tersimpan di {P2_OUT}")

    if df_sibakul_out is not None:
        P5_OUT.parent.mkdir(parents=True, exist_ok=True)
        df_sibakul_out.to_csv(P5_OUT, index=False)
        print(f"  [OK] Sukses: Data SiBakul tersimpan di {P5_OUT}")

    # 3. Dataset 3: Indeks Biaya Sewa Properti Komersial
    print("\n[DATASET 3/4] Standardisasi Biaya Operasional Sewa Lokasi...")
    df_sewa = clean_and_standardize_harga()
    print(f"  [OK] Sukses: {len(df_sewa)} wilayah terdata di data/processed/biaya_operasional.csv")

    # 4. Dataset 4: Tren Permintaan Pasar & Pertumbuhan Usaha
    print("\n[DATASET 4/4] Pengolahan Laju Pertumbuhan Usaha & Google Trends...")
    load_bps_files()
    df_tren = process_and_merge_tren()
    print(f"  [OK] Sukses: {len(df_tren)} data tren tersimpan di data/processed/tren_sektor.csv")

    print("\n" + "=" * 80)
    print("[SUKSES] SEMUA DATASET (1-4) BERHASIL DIBERSIHKAN DAN SIAP DIGUNAKAN!")
    print("Lokasi data siap pakai: data/processed/")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Master Runner Pipeline Data Projek PDS")
    parser.add_argument(
        "--skip-osm-fetch",
        action="store_true",
        default=True,
        help="Gunakan data mentah OSM lokal tanpa fetch ulang ke API (default: True)"
    )
    args = parser.parse_args()
    run_all(skip_osm_fetch=args.skip_osm_fetch)
