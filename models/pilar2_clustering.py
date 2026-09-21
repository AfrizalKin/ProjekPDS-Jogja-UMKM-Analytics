"""
Pilar 2: Clustering Karakteristik Ekonomi Wilayah (K-Means Clustering & PCA)
Projek PDS - Rekomendasi Kelayakan Usaha UMKM D.I. Yogyakarta

Sifat:
- Batch process (offline, tanpa input user).
- Level analisis: Wilayah administratif (5 baris data kabupaten/kota).
- Mengelompokkan wilayah berdasarkan multivariat ekonomi, demografi, kompetisi, dan biaya sewa.
- Mereduksi dimensi dengan PCA (2 Komponen) untuk koordinat visualisasi 2D pada website.
- Output disimpan ke: data/processed/hasil_clustering_wilayah.csv
- Model tersimpan di: models/saved/kmeans_wilayah.joblib
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Path berkas input & output
KOMPETITOR_CSV = BASE_DIR / "data" / "processed" / "kompetitor_per_wilayah.csv"
EKONOMI_CSV = BASE_DIR / "data" / "processed" / "kondisi_ekonomi_wilayah.csv"
SEWA_CSV = BASE_DIR / "data" / "processed" / "biaya_operasional.csv"
OUTPUT_CLUSTERING_CSV = BASE_DIR / "data" / "processed" / "hasil_clustering_wilayah.csv"
SAVED_MODELS_DIR = BASE_DIR / "models" / "saved"

WILAYAH_CONFIG = [
    {"id": "kota_yogyakarta", "nama_match": "Kota Yogyakarta", "label": "Kota Yogyakarta"},
    {"id": "sleman", "nama_match": "Sleman", "label": "Kabupaten Sleman"},
    {"id": "bantul", "nama_match": "Bantul", "label": "Kabupaten Bantul"},
    {"id": "kulon_progo", "nama_match": "Kulon Progo", "label": "Kabupaten Kulon Progo"},
    {"id": "gunungkidul", "nama_match": "Gunung Kidul", "label": "Kabupaten Gunungkidul"},
]


def run_pilar2_clustering(n_clusters: int = 3) -> pd.DataFrame:
    print("=" * 75)
    print("MEMULAI PILAR 2: CLUSTERING KARAKTERISTIK EKONOMI WILAYAH (K-MEANS & PCA)")
    print("=" * 75)

    # Validasi file input
    for p in [KOMPETITOR_CSV, EKONOMI_CSV, SEWA_CSV]:
        if not p.exists():
            raise FileNotFoundError(f"Berkas tidak ditemukan: {p}")

    df_kompetitor = pd.read_csv(KOMPETITOR_CSV)
    df_ekonomi = pd.read_csv(EKONOMI_CSV)
    df_sewa = pd.read_csv(SEWA_CSV)

    # 1. Agregasi total kompetitor per wilayah
    kompetitor_per_wilayah = df_kompetitor.groupby("wilayah").size().to_dict()

    # 2. Susun tabel profil wilayah tingkat kabupaten/kota (5 baris)
    ekonomi_lookup = {str(r["kabupaten_kota"]).strip().lower(): r for _, r in df_ekonomi.iterrows()}
    sewa_lookup = {str(r["wilayah"]).strip().lower(): r for _, r in df_sewa.iterrows()}

    rows = []
    for w in WILAYAH_CONFIG:
        w_id = w["id"]
        w_label = w["label"]
        w_key = w["nama_match"].strip().lower()

        ek_data = ekonomi_lookup.get(w_key)
        sewa_data = sewa_lookup.get(w_id)

        if ek_data is None or sewa_data is None:
            raise KeyError(f"Data tidak lengkap untuk wilayah: {w_label}")

        kepadatan = float(ek_data["kepadatan_penduduk"])
        luas = float(ek_data["luas_km2"])
        populasi = kepadatan * luas
        pdrb = float(ek_data["pdrb_per_kapita"])
        pengeluaran = float(ek_data["pengeluaran_per_kapita"])
        umkm_total = float(ek_data.get("jumlah_umkm_2025", 50000))
        rasio_umkm_total = float(ek_data.get("rasio_umkm_per_1000_penduduk", (umkm_total / populasi) * 1000))

        harga_sewa = float(sewa_data["harga_sewa_per_m2_tahun"])
        total_komp = kompetitor_per_wilayah.get(w_id, 0)
        rasio_komp_total = (total_komp / populasi) * 1000.0

        rows.append({
            "wilayah": w_id,
            "wilayah_label": w_label,
            "pdrb_per_kapita": pdrb,
            "pengeluaran_per_kapita": pengeluaran,
            "kepadatan_penduduk": kepadatan,
            "harga_sewa_per_m2_tahun": harga_sewa,
            "avg_rasio_kompetitor_per_1000": round(rasio_komp_total, 4),
            "rasio_umkm_total_per_1000": round(rasio_umkm_total, 2),
            "total_kompetitor": total_komp,
            "luas_km2": luas
        })

    df_wilayah = pd.DataFrame(rows)

    # 3. Fitur clustering
    feature_cols = [
        "pdrb_per_kapita",
        "pengeluaran_per_kapita",
        "kepadatan_penduduk",
        "harga_sewa_per_m2_tahun",
        "avg_rasio_kompetitor_per_1000",
        "rasio_umkm_total_per_1000"
    ]
    X = df_wilayah[feature_cols].values

    # 4. Standardisasi Fitur (Z-Score Scaling)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # 5. K-Means Clustering
    # Catatan limitasi metodologis: n=5 relatif kecil secara statistik,
    # namun K-Means digunakan untuk mengelompokkan profil pasar secara kuantitatif.
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    raw_clusters = kmeans.fit_predict(X_scaled)
    df_wilayah["cluster_id"] = raw_clusters

    # 6. Reduksi Dimensi dengan PCA (2D) untuk Visualisasi Website
    pca = PCA(n_components=2, random_state=42)
    X_pca = pca.fit_transform(X_scaled)
    df_wilayah["pca_x"] = np.round(X_pca[:, 0], 4)
    df_wilayah["pca_y"] = np.round(X_pca[:, 1], 4)

    # 7. Penamaan Label Klaster yang Informatif Berdasarkan Karakteristik
    # Urutkan klaster berdasarkan rata-rata PDRB & Kepadatan
    cluster_means = df_wilayah.groupby("cluster_id")["pdrb_per_kapita"].mean().sort_values(ascending=False)
    cluster_rank_order = list(cluster_means.index)

    # Label interpretatif:
    # Rank 0 (Tertinggi): Pasar Matang & Biaya Tinggi
    # Rank 1 (Menengah): Pasar Berkembang & Biaya Menengah
    # Rank 2 (Terendah): Pasar Perintis & Biaya Terjangkau
    label_map = {
        cluster_rank_order[0]: "Pasar Padat & Biaya Tinggi",
        cluster_rank_order[1]: "Pasar Berkembang & Biaya Menengah",
        cluster_rank_order[2]: "Pasar Perintis & Biaya Terjangkau"
    }
    df_wilayah["cluster_label"] = df_wilayah["cluster_id"].map(label_map)

    # Deskripsi profil pasar untuk laporan & tooltip website
    deskripsi_map = {
        cluster_rank_order[0]: "Daya beli & densitas penduduk sangat tinggi, namun harga sewa tinggi dan kompetisi ketat.",
        cluster_rank_order[1]: "Keseimbangan yang baik antara biaya sewa terjangkau dan populasi berkembang pesat.",
        cluster_rank_order[2]: "Biaya sewa sangat ekonomis, cocok untuk usaha perintis dan segmen pasar berbasis komunitas lokal."
    }
    df_wilayah["cluster_deskripsi"] = df_wilayah["cluster_id"].map(deskripsi_map)

    # 8. Simpan Model & Scaler ke models/saved/
    SAVED_MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, SAVED_MODELS_DIR / "scaler_clustering.joblib")
    joblib.dump(kmeans, SAVED_MODELS_DIR / "kmeans_wilayah.joblib")
    joblib.dump(pca, SAVED_MODELS_DIR / "pca_wilayah.joblib")

    # 9. Simpan Hasil ke data/processed/hasil_clustering_wilayah.csv
    output_cols = [
        "wilayah",
        "wilayah_label",
        "cluster_id",
        "cluster_label",
        "cluster_deskripsi",
        "pca_x",
        "pca_y",
        "pdrb_per_kapita",
        "pengeluaran_per_kapita",
        "kepadatan_penduduk",
        "harga_sewa_per_m2_tahun",
        "avg_rasio_kompetitor_per_1000",
        "rasio_umkm_total_per_1000"
    ]
    df_output = df_wilayah[output_cols].sort_values(by="cluster_id").reset_index(drop=True)
    OUTPUT_CLUSTERING_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_output.to_csv(OUTPUT_CLUSTERING_CSV, index=False)

    print(f"\n[SUKSES] Hasil K-Means Clustering berhasil disimpan ke:\n  -> {OUTPUT_CLUSTERING_CSV}")
    print(f"Variance Rasio PCA (2 Komponen): {pca.explained_variance_ratio_.round(4)}")
    print(f"Total Variansi Tertangkap: {pca.explained_variance_ratio_.sum() * 100:.2f}%")

    print("\n--- HASIL PROFIL KLASTER 5 WILAYAH DIY ---")
    print(df_output[["wilayah_label", "cluster_id", "cluster_label", "pca_x", "pca_y", "harga_sewa_per_m2_tahun"]].to_string(index=False))
    print("\nCatatan Metodologi: n=5 wilayah tergolong kecil secara statistik, dicatat transparan pada laporan.")
    print("=" * 75 + "\n")

    return df_output


if __name__ == "__main__":
    run_pilar2_clustering()
