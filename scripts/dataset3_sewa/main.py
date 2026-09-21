"""
Orchestrator Pipeline Dataset 3: Biaya Operasional / Sewa Properti Komersial
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM
"""

import sys
from pathlib import Path

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset3_sewa.fetch_index import fetch_official_rental_index
from scripts.dataset3_sewa.clean_harga import clean_and_standardize_harga


def run_pipeline():
    """
    Menjalankan seluruh tahapan pipeline Dataset 3:
    1. Pengambilan data indeks harga sewa properti komersial (fetch_index.py)
    2. Pembersihan, normalisasi harga, dan standardisasi wilayah (clean_harga.py)
    """
    print("*" * 70)
    print("MEMULAI PIPELINE DATASET 3: ESTIMASI BIAYA OPERASIONAL UMKM")
    print("*" * 70)

    # Langkah 1: Ambil data indeks sewa
    df_raw = fetch_official_rental_index()

    # Langkah 2: Bersihkan dan standardisasi
    df_clean = clean_and_standardize_harga()

    print("\n[SELESAI] Pipeline Dataset 3 telah berhasil dijalankan.")


if __name__ == "__main__":
    run_pipeline()
