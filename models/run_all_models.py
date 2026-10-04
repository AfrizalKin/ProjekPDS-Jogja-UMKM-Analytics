"""
Orkestrator Pemodelan Analitik (Fase 2: models/)
Projek PDS - Rekomendasi Kelayakan Usaha UMKM D.I. Yogyakarta

Menjalankan seluruh pilar analitik batch (Pilar 1, 2, 3) dan menguji coba Pilar 4 sekali jalan.

Penggunaan:
    python models/run_all_models.py
"""

import sys
from pathlib import Path

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Nama modul diawali angka (01_skoring, dst.) sehingga tidak dapat diimpor dengan
# pernyataan `import` biasa; dimuat melalui importlib.
import importlib

_skoring = importlib.import_module("models.01_skoring")
_clustering = importlib.import_module("models.02_clustering")
_forecasting = importlib.import_module("models.03_forecasting")
_rekomendasi = importlib.import_module("models.04_rekomendasi")

run_skoring, OUTPUT_SKORING_CSV = _skoring.run_skoring, _skoring.OUTPUT_SKORING_CSV
run_clustering, OUTPUT_CLUSTERING_CSV = _clustering.run_clustering, _clustering.OUTPUT_CLUSTERING_CSV
run_forecasting, OUTPUT_FORECAST_CSV = _forecasting.run_forecasting, _forecasting.OUTPUT_FORECAST_CSV
UMKMRecommender = _rekomendasi.UMKMRecommender


def run_all_models():
    print("\n" + "=" * 80)
    print("[FASE 2] MENJALANKAN SELURUH PEMODELAN ANALITIK UMKM (PILAR 1, 2, 3)")
    print("=" * 80 + "\n")

    # 1. Eksekusi Pilar 1: Skoring Kelayakan Sektor (MCDA)
    df_skor = run_skoring()

    # 2. Eksekusi Pilar 2: Clustering Wilayah (K-Means + PCA)
    df_cluster = run_clustering()

    # 3. Eksekusi Pilar 3: Forecasting Tren Pertumbuhan Sektor (Linear Trend)
    df_forecast = run_forecasting()

    # 4. Validasi Keberadaan Seluruh Berkas Output
    print("\n" + "=" * 80)
    print("[VALIDASI] MEMERIKSA KELENGKAPAN ARTEFAK ANALISIS DI outputs/hasil/:")
    print("=" * 80)
    artifacts = [
        ("Pilar 1 (Skor Kelayakan)", OUTPUT_SKORING_CSV, len(df_skor)),
        ("Pilar 2 (Klaster Wilayah)", OUTPUT_CLUSTERING_CSV, len(df_cluster)),
        ("Pilar 3 (Proyeksi Tren)", OUTPUT_FORECAST_CSV, len(df_forecast)),
    ]

    all_ok = True
    for name, path_file, row_count in artifacts:
        if path_file.exists():
            print(f"  [OK] {name:<26} -> {path_file.name} ({row_count} baris)")
        else:
            print(f"  [GAGAL] {name:<26} -> File tidak ditemukan: {path_file}")
            all_ok = False

    # 5. Uji Coba Engine Rekomendasi (Pilar 4)
    print("\n" + "-" * 80)
    print("[TESTING] Menguji Coba Inferensi Engine Rekomendasi (Pilar 4)...")
    recommender = UMKMRecommender()
    sample_rec = recommender.recommend(sektor="cafe", wilayah=None)
    top_1 = sample_rec["ranking_wilayah"][0]
    print(f"  -> Uji coba sukses! Rekomendasi Top 1 untuk Sektor Kafe: {top_1['wilayah_label']} (Skor: {top_1['skor']})")

    if all_ok:
        print("\n" + "=" * 80)
        print("[SUKSES] SELURUH PEMODELAN FASE 2 SELESAI DAN SIAP DIGUNAKAN DI WEBSITE!")
        print("=" * 80 + "\n")


if __name__ == "__main__":
    run_all_models()
