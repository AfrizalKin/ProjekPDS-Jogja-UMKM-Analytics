"""
Orchestrator Pipeline Dataset 4: Tren Pertumbuhan Sektor Usaha UMKM
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM

Alur Eksekusi:
1. Menjalankan fetch_bps.py (WAJIB - Sumber data utama time series resmi)
2. Menjalankan fetch_trends.py (OPSIONAL - Pelengkap sinyal minat pencarian, toleran terhadap kegagalan)
3. Menjalankan clean_tren.py (Standardisasi, kalkulasi laju pertumbuhan, dan ekspor ke processed)
"""

import sys
import argparse
from pathlib import Path

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset4_tren.fetch_bps import load_bps_files
from scripts.dataset4_tren.fetch_trends import fetch_google_trends
from scripts.dataset4_tren.clean_tren import process_and_merge_tren


def run_pipeline(skip_trends: bool = False):
    """
    Menjalankan pipeline Dataset 4 secara berurutan.
    """
    print("#" * 75)
    print("MEMULAI PIPELINE DATASET 4: TREN PERTUMBUHAN SEKTOR USAHA (FORECASTING INPUT)")
    print("#" * 75)

    # --------------------------------------------------------------------------
    # TAHAP 1: EKSTRAKSI DATA RESMI BPS (WAJIB)
    # --------------------------------------------------------------------------
    print("\n[LANGKAH 1/3] Membaca dan Membersihkan Data Resmi BPS...")
    df_bps = load_bps_files()

    if df_bps.empty:
        print("\n[GAGAL] Data BPS tidak dapat dimuat. Pipeline dihentikan.")
        print("Pastikan file BPS (CSV/Excel) tersedia di data/raw/bps/.")
        sys.exit(1)

    # --------------------------------------------------------------------------
    # TAHAP 2: PENGAMBILAN GOOGLE TRENDS (OPSIONAL / PELENGKAP)
    # --------------------------------------------------------------------------
    if skip_trends:
        print("\n[LANGKAH 2/3] Pengambilan Google Trends DILEWATI (--skip-trends aktif).")
    else:
        print("\n[LANGKAH 2/3] Mengambil Sinyal Google Trends (Opsional)...")
        try:
            fetch_google_trends()
        except Exception as e:
            print(f"[Warning] Proses Google Trends mengalami error: {e}")
            print("Pipeline tetap dilanjutkan menggunakan data BPS sebagai basis utama.")

    # --------------------------------------------------------------------------
    # TAHAP 3: PENGGABUNGAN & KALKULASI LAJU PERTUMBUHAN
    # --------------------------------------------------------------------------
    print("\n[LANGKAH 3/3] Melakukan Standardisasi & Kalkulasi Pertumbuhan...")
    df_final = process_and_merge_tren()

    print("\n" + "#" * 75)
    print("[SELESAI] PIPELINE DATASET 4 BERHASIL DIJALANKAN LENGKAP!")
    print(f"File Hasil Akhir Siap Pakai: data/processed/tren_sektor.csv ({len(df_final)} baris)")
    print("#" * 75)


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline Dataset 4 - Tren Pertumbuhan Sektor Usaha UMKM untuk Forecasting"
    )
    parser.add_argument(
        "--skip-trends",
        action="store_true",
        help="Lewati pengambilan Google Trends dan hanya gunakan data resmi BPS"
    )
    args = parser.parse_args()

    run_pipeline(skip_trends=args.skip_trends)


if __name__ == "__main__":
    main()
