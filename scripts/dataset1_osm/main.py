"""
Orchestrator Pipeline Dataset 1: OpenStreetMap (Overpass API)
Projek PDS - UMKM Recommender
"""

import argparse
import datetime
import logging
import sys
import time
from pathlib import Path

# Memastikan import modul lokal bekerja dengan baik
current_dir = Path(__file__).resolve().parent
if str(current_dir.parent.parent) not in sys.path:
    sys.path.append(str(current_dir.parent.parent))

from scripts.dataset1_osm.config import (
    BBOX_WILAYAH,
    DEFAULT_WILAYAH,
    DEFAULT_TIMEOUT,
    LOG_DIR,
    RAW_DATA_DIR
)
from scripts.dataset1_osm.fetch_overpass import (
    build_overpass_query,
    fetch_osm_data,
    save_raw_response
)
from scripts.dataset1_osm.grid_sampling import create_bbox_grid
from scripts.dataset1_osm.clean_dedup import (
    parse_osm_elements,
    categorize_umkm,
    deduplicate_records,
    save_interim_data,
    save_processed_data
)


def setup_logger(log_filename: str = "pipeline_osm.log"):
    """
    Mengatur logging ke file dan konsol.
    """
    log_file = LOG_DIR / log_filename

    # Konfigurasi root logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        handlers=[
            logging.FileHandler(log_file, encoding="utf-8"),
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger("PipelineOSM")


def run_pipeline(
    wilayah_key: str = DEFAULT_WILAYAH,
    custom_bbox: tuple = None,
    use_grid: bool = True,
    grid_rows: int = 2,
    grid_cols: int = 2,
    timeout: int = DEFAULT_TIMEOUT
):
    logger = setup_logger()
    logger.info("=" * 60)
    logger.info("MEMULAI PIPELINE EKSTRAKSI DATASET 1 (OSM UMKM)")
    logger.info("=" * 60)

    # 1. Tentukan Bounding Box
    if custom_bbox:
        bbox = custom_bbox
        nama_wilayah = f"custom_{bbox[0]}_{bbox[1]}"
        logger.info(f"Menggunakan Custom BBox: {bbox}")
    else:
        info = BBOX_WILAYAH.get(wilayah_key, BBOX_WILAYAH[DEFAULT_WILAYAH])
        bbox = info["bbox"]
        nama_wilayah = wilayah_key
        logger.info(f"Target Wilayah: {info['nama']} (Key: {wilayah_key})")
        logger.info(f"Koordinat BBox: {bbox}")

    all_elements = []
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # 2. Pengambilan Data (Grid vs Single BBox)
    if use_grid:
        grid_cells = create_bbox_grid(bbox, n_rows=grid_rows, n_cols=grid_cols)
        logger.info(f"Mode Grid aktif: Membagi wilayah menjadi {len(grid_cells)} sub-grid ({grid_rows}x{grid_cols}).")

        for idx, cell in enumerate(grid_cells, 1):
            logger.info(f"--> [Grid {idx}/{len(grid_cells)}] Mengambil data untuk cell {cell['grid_id']}...")
            query = build_overpass_query(bbox=cell["bbox"], timeout=timeout)
            res_json = fetch_osm_data(query)

            if res_json and "elements" in res_json:
                elements = res_json["elements"]
                logger.info(f"    Ditemukan {len(elements)} elemen pada {cell['grid_id']}.")
                all_elements.extend(elements)

                # Simpan mentah per cell
                raw_filename = f"{nama_wilayah}_{cell['grid_id']}_{timestamp}.json"
                save_raw_response(res_json, raw_filename)
            else:
                logger.warning(f"    Gagal mengambil elemen untuk {cell['grid_id']}.")

            # Jeda sopan antar request agar tidak diblokir Overpass API
            if idx < len(grid_cells):
                time.sleep(3)
    else:
        logger.info("Mode Single BBox aktif.")
        query = build_overpass_query(bbox=bbox, timeout=timeout)
        res_json = fetch_osm_data(query)

        if res_json and "elements" in res_json:
            all_elements = res_json["elements"]
            raw_filename = f"{nama_wilayah}_single_{timestamp}.json"
            save_raw_response(res_json, raw_filename)
            logger.info(f"Ditemukan {len(all_elements)} elemen.")
        else:
            logger.error("Gagal mengambil data OSM.")
            return

    if not all_elements:
        logger.warning("Tidak ada elemen yang berhasil diambil dari Overpass API. Pipeline berhenti.")
        return

    # 3. Parsing Elemen Mentah
    logger.info("Mem-parsing elemen mentah...")
    df_raw = parse_osm_elements(all_elements)
    interim_file = f"{nama_wilayah}_interim_{timestamp}.csv"
    save_interim_data(df_raw, interim_file)

    # 4. Standardisasi Sektor & Deduplikasi
    logger.info("Menstandardisasi kategori UMKM...")
    df_categorized = categorize_umkm(df_raw)

    logger.info("Menjalankan deduplikasi...")
    df_final = deduplicate_records(df_categorized)

    # 5. Ekspor Data Final
    processed_file = f"{nama_wilayah}_umkm_final.csv"
    saved_path = save_processed_data(df_final, processed_file)

    # 6. Ringkasan Hasil
    logger.info("=" * 60)
    logger.info("RINGKASAN EKSTRAKSI & PEMBERSIHAN DATA UMKM")
    logger.info("=" * 60)
    logger.info(f"Total POI Mentah Terambil : {len(df_raw)}")
    logger.info(f"Total POI Bersih & Unik   : {len(df_final)}")
    logger.info(f"File Hasil Disimpan ke    : {saved_path}")
    logger.info("\nDistribusi Sektor UMKM:")
    for sektor, count in df_final["sektor_umkm"].value_counts().items():
        logger.info(f"  - {sektor:<25}: {count} POI")
    logger.info("=" * 60)
    logger.info("Pipeline Selesai dengan Sukses!")


def main():
    parser = argparse.ArgumentParser(description="Pipeline Dataset 1 OSM - Projek PDS UMKM Recommender")
    parser.add_argument(
        "--wilayah",
        type=str,
        default=DEFAULT_WILAYAH,
        choices=list(BBOX_WILAYAH.keys()),
        help=f"Pilihan preset wilayah (default: {DEFAULT_WILAYAH})"
    )
    parser.add_argument(
        "--no-grid",
        action="store_true",
        help="Gunakan single query BBox tanpa membagi menjadi grid"
    )
    parser.add_argument(
        "--grid-rows",
        type=int,
        default=2,
        help="Jumlah baris grid (default: 2)"
    )
    parser.add_argument(
        "--grid-cols",
        type=int,
        default=2,
        help="Jumlah kolom grid (default: 2)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help=f"Timeout query dalam detik (default: {DEFAULT_TIMEOUT})"
    )

    args = parser.parse_args()

    run_pipeline(
        wilayah_key=args.wilayah,
        use_grid=not args.no_grid,
        grid_rows=args.grid_rows,
        grid_cols=args.grid_cols,
        timeout=args.timeout
    )


if __name__ == "__main__":
    main()
