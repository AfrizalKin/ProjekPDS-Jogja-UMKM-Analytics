"""
Pilar 4: Rekomendasi Personal UMKM (Rule-based Matching Engine)
Projek PDS - Rekomendasi Kelayakan Usaha UMKM D.I. Yogyakarta

Sifat:
- Real-time function (membaca input pengguna).
- BUKAN model ML terpisah: Berupa fungsi lookup + if-else cerdas yang membaca
  hasil batch dari Pilar 1, Pilar 2, dan Pilar 3 (TIDAK menghitung ulang dataset mentah).
- Siap diimpor secara modular oleh aplikasi web/dashboard (Fase 3).
"""

import sys
import argparse
from pathlib import Path
import pandas as pd

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Path berkas hasil dari Pilar 1, 2, dan 3
SKORING_CSV = BASE_DIR / "data" / "processed" / "hasil_skoring_sektor.csv"
CLUSTERING_CSV = BASE_DIR / "data" / "processed" / "hasil_clustering_wilayah.csv"
FORECAST_CSV = BASE_DIR / "data" / "processed" / "hasil_forecasting_sektor.csv"


class UMKMRecommender:
    """Engine inferensi rekomendasi kelayakan lokasi UMKM berbasis data."""

    def __init__(self):
        self.load_artifacts()

    def load_artifacts(self):
        """Memuat tabel hasil olahan Pilar 1, 2, dan 3."""
        for p in [SKORING_CSV, CLUSTERING_CSV, FORECAST_CSV]:
            if not p.exists():
                raise FileNotFoundError(
                    f"Berkas hasil analisis tidak ditemukan: {p}\n"
                    f"Pastikan telah menjalankan Pilar 1, 2, dan 3 terlebih dahulu."
                )

        self.df_skoring = pd.read_csv(SKORING_CSV)
        self.df_cluster = pd.read_csv(CLUSTERING_CSV)
        self.df_forecast = pd.read_csv(FORECAST_CSV)

        # Lookup cluster per id wilayah
        self.cluster_map = self.df_cluster.set_index("wilayah").to_dict(orient="index")

        # Lookup tren per id sektor
        self.trend_map = (
            self.df_forecast.drop_duplicates(subset=["sektor"])
            .set_index("sektor")["arah_tren"]
            .to_dict()
        )

    def recommend(
        self,
        sektor: str,
        wilayah: str | None = None,
        budget_tahunan: float | None = None
    ) -> dict:
        """
        Menghasilkan rekomendasi kelayakan usaha berdasarkan input pengguna.

        Args:
            sektor: ID kategori usaha ('cafe', 'restaurant', 'convenience', 'laundry', 'grocery')
            wilayah: ID wilayah spesifik ('sleman', 'bantul', dll.) atau None/'all' untuk terbuka
            budget_tahunan: Anggaran sewa tempat per tahun dalam Rupiah (opsional)

        Returns:
            dict: Struktur data rekomendasi siap pakai untuk UI/API.
        """
        sektor_clean = str(sektor).strip().lower()

        # Filter skor untuk sektor yang diminta
        df_sec = self.df_skoring[self.df_skoring["sektor"] == sektor_clean].copy()
        if df_sec.empty:
            pilihan_tersedia = self.df_skoring["sektor"].unique().tolist()
            raise ValueError(
                f"Sektor '{sektor}' tidak valid. Pilihan tersedia: {pilihan_tersedia}"
            )

        sektor_label = df_sec.iloc[0]["sektor_label"]
        arah_tren = self.trend_map.get(sektor_clean, "Stabil")

        # Asumsi luas ruko standar UMKM = 30 m2 untuk komparasi budget sewa
        LUAS_RUKO_STANDAR = 30.0

        # KASUS A: PENGGUNA MEMILIH WILAYAH SPESIFIK
        if wilayah and wilayah.lower() not in ["all", "semua", "terbuka"]:
            w_clean = str(wilayah).strip().lower()
            match_row = df_sec[df_sec["wilayah"] == w_clean]

            if match_row.empty:
                raise ValueError(f"Wilayah '{wilayah}' tidak ditemukan.")

            row = match_row.iloc[0]
            cluster_info = self.cluster_map.get(w_clean, {})
            harga_sewa_m2 = float(row["harga_sewa_per_m2_tahun"])
            estimasi_sewa_tahunan = harga_sewa_m2 * LUAS_RUKO_STANDAR

            # Pengecekan kecukupan budget (jika diinput)
            budget_status = "Sesuai"
            budget_catatan = ""
            if budget_tahunan is not None and budget_tahunan > 0:
                if budget_tahunan < estimasi_sewa_tahunan:
                    budget_status = "Kurang"
                    budget_catatan = (
                        f"Perhatian: Estimasi sewa tempat ukuran 30m2 di wilayah ini sekitar "
                        f"Rp {estimasi_sewa_tahunan:,.0f}/tahun, lebih tinggi dari budget Anda "
                        f"(Rp {budget_tahunan:,.0f})."
                    )
                else:
                    budget_status = "Mencukupi"
                    budget_catatan = (
                        f"Budget Anda (Rp {budget_tahunan:,.0f}) mencukupi estimasi sewa tempat "
                        f"(sekitar Rp {estimasi_sewa_tahunan:,.0f}/tahun)."
                    )

            # Analisis kejenuhan kompetitor
            kejenuhan_warning = None
            if row["rasio_kompetitor_per_1000"] > 0.20:
                kejenuhan_warning = (
                    f"Peringatan Kejenuhan: Kepadatan kompetitor di {row['wilayah_label']} "
                    f"tergolong tinggi ({row['rasio_kompetitor_per_1000']:.2f} gerai per 1.000 jiwa). "
                    f"Dibutuhkan diferensiasi produk/branding yang kuat."
                )

            # Narasi Rekomendasi
            narasi = (
                f"Sektor usaha {sektor_label} di {row['wilayah_label']} memiliki skor kelayakan "
                f"{row['skor']}/100 ({row['kategori']}). Wilayah ini tergolong dalam klaster "
                f"'{cluster_info.get('cluster_label', '-')}' dengan tren pertumbuhan sektor se-DIY {arah_tren}."
            )

            return {
                "mode": "spesifik",
                "sektor": sektor_clean,
                "sektor_label": sektor_label,
                "arah_tren_sektor": arah_tren,
                "wilayah": w_clean,
                "wilayah_label": row["wilayah_label"],
                "skor": float(row["skor"]),
                "kategori": row["kategori"],
                "cluster_label": cluster_info.get("cluster_label", "-"),
                "cluster_deskripsi": cluster_info.get("cluster_deskripsi", "-"),
                "estimasi_sewa_tahunan_30m2": estimasi_sewa_tahunan,
                "budget_status": budget_status,
                "budget_catatan": budget_catatan,
                "kejenuhan_warning": kejenuhan_warning,
                "narasi_rekomendasi": narasi
            }

        # KASUS B: TERBUKA KE SEMUA WILAYAH (RANKING TOP-3)
        ranked = df_sec.sort_values(by="skor", ascending=False).reset_index(drop=True)
        top_recommendations = []

        for rank_idx, r in ranked.iterrows():
            w_id = r["wilayah"]
            c_info = self.cluster_map.get(w_id, {})
            est_sewa = float(r["harga_sewa_per_m2_tahun"]) * LUAS_RUKO_STANDAR

            is_affordable = True
            if budget_tahunan is not None and budget_tahunan > 0:
                is_affordable = budget_tahunan >= est_sewa

            top_recommendations.append({
                "rank": rank_idx + 1,
                "wilayah": w_id,
                "wilayah_label": r["wilayah_label"],
                "skor": float(r["skor"]),
                "kategori": r["kategori"],
                "cluster_label": c_info.get("cluster_label", "-"),
                "estimasi_sewa_tahunan": est_sewa,
                "is_affordable": is_affordable,
                "alasan": (
                    f"Skor {r['skor']} ({r['kategori']}). Klaster: {c_info.get('cluster_label', '-')}. "
                    f"Estimasi sewa 30m2: Rp {est_sewa:,.0f}/tahun."
                )
            })

        top_wilayah = top_recommendations[0]["wilayah_label"]
        narasi = (
            f"Berdasarkan analisis multi-kriteria untuk sektor {sektor_label}, lokasi rekomendasi "
            f"terbaik peringkat 1 adalah {top_wilayah} dengan skor kelayakan {top_recommendations[0]['skor']}/100. "
            f"Tren sektor ini di tingkat provinsi terindikasi {arah_tren}."
        )

        return {
            "mode": "terbuka",
            "sektor": sektor_clean,
            "sektor_label": sektor_label,
            "arah_tren_sektor": arah_tren,
            "narasi_rekomendasi": narasi,
            "ranking_wilayah": top_recommendations[:3],  # Top 3 sesuai spesifikasi
            "semua_wilayah": top_recommendations
        }


def print_recommendation_card(rec: dict):
    """Mencetak kartu rekomendasi dalam format yang menarik di terminal."""
    print("\n" + "=" * 75)
    print(f"[REKOMENDASI LOKASI UMKM]: {rec['sektor_label'].upper()}")
    print("=" * 75)
    print(f"Tren Sektor di DIY : {rec['arah_tren_sektor']}")

    if rec["mode"] == "spesifik":
        print(f"Wilayah Target     : {rec['wilayah_label']}")
        print(f"Skor Kelayakan     : {rec['skor']} / 100")
        print(f"Kategori Kelayakan : {rec['kategori']}")
        print(f"Klaster Pasar      : {rec['cluster_label']}")
        print(f"Profil Wilayah     : {rec['cluster_deskripsi']}")
        print(f"Estimasi Sewa Ruko : Rp {rec['estimasi_sewa_tahunan_30m2']:,.0f} / tahun (asumsi 30m2)")
        if rec["budget_catatan"]:
            print(f"Status Budget      : {rec['budget_status']} -> {rec['budget_catatan']}")
        if rec["kejenuhan_warning"]:
            print(f"Catatan Kompetisi  : {rec['kejenuhan_warning']}")
    else:
        print("\n--- PERINGKAT TOP 3 WILAYAH REKOMENDASI TERBAIK ---")
        print("-" * 75)
        for item in rec["ranking_wilayah"]:
            aff_badge = "[Budget Cukup]" if item["is_affordable"] else "[Budget Kurang]"
            print(f"  Peringkat #{item['rank']}: {item['wilayah_label']}")
            print(f"    * Skor Kelayakan : {item['skor']} ({item['kategori']})")
            print(f"    * Profil Pasar   : {item['cluster_label']}")
            print(f"    * Estimasi Sewa  : Rp {item['estimasi_sewa_tahunan']:,.0f}/tahun {aff_badge}")
            print()

    print("Ringkasan:")
    print(f"  \"{rec['narasi_rekomendasi']}\"")
    print("=" * 75 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Engine Rekomendasi Lokasi UMKM DIY (Pilar 4)")
    parser.add_argument(
        "--sektor",
        type=str,
        default="cafe",
        help="ID sektor usaha (cafe, restaurant, convenience, laundry, grocery)"
    )
    parser.add_argument(
        "--wilayah",
        type=str,
        default=None,
        help="ID wilayah spesifik (sleman, bantul, kota_yogyakarta, kulon_progo, gunungkidul). Kosongkan untuk terbuka."
    )
    parser.add_argument(
        "--budget",
        type=float,
        default=None,
        help="Anggaran sewa tahunan dalam Rupiah (opsional)"
    )
    args = parser.parse_args()

    recommender = UMKMRecommender()
    result = recommender.recommend(
        sektor=args.sektor,
        wilayah=args.wilayah,
        budget_tahunan=args.budget
    )
    print_recommendation_card(result)


if __name__ == "__main__":
    main()
