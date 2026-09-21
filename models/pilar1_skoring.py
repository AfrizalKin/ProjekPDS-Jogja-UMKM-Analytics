"""
Pilar 1: Skoring Kelayakan Sektor Usaha (Multi-Criteria Decision Analysis)
Projek PDS - Rekomendasi Kelayakan Usaha UMKM D.I. Yogyakarta

Sifat:
- Batch process (offline, tanpa input user).
- Menghasilkan tabel skor kelayakan untuk setiap kombinasi wilayah x sektor usaha (25 baris).
- Output disimpan ke: data/processed/hasil_skoring_sektor.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# Path berkas input & output
KOMPETITOR_CSV = BASE_DIR / "data" / "processed" / "kompetitor_per_wilayah.csv"
EKONOMI_CSV = BASE_DIR / "data" / "processed" / "kondisi_ekonomi_wilayah.csv"
SEWA_CSV = BASE_DIR / "data" / "processed" / "biaya_operasional.csv"
OUTPUT_SKORING_CSV = BASE_DIR / "data" / "processed" / "hasil_skoring_sektor.csv"

# Daftar Wilayah & Sektor Baku
WILAYAH_CONFIG = [
    {"id": "kota_yogyakarta", "nama_match": "Kota Yogyakarta", "label": "Kota Yogyakarta"},
    {"id": "sleman", "nama_match": "Sleman", "label": "Kabupaten Sleman"},
    {"id": "bantul", "nama_match": "Bantul", "label": "Kabupaten Bantul"},
    {"id": "kulon_progo", "nama_match": "Kulon Progo", "label": "Kabupaten Kulon Progo"},
    {"id": "gunungkidul", "nama_match": "Gunung Kidul", "label": "Kabupaten Gunungkidul"},
]

SEKTOR_CONFIG = [
    {"id": "restaurant", "label": "Restoran / Warung Makan"},
    {"id": "convenience", "label": "Minimarket / Toko Kelontong"},
    {"id": "cafe", "label": "Kafe / Kedai Kopi"},
    {"id": "laundry", "label": "Jasa Laundry"},
    {"id": "grocery", "label": "Toko Kelontong Tradisional"},
]


def min_max_norm(series: pd.Series) -> pd.Series:
    """Normalisasi seri ke skala [0, 1]."""
    s_min = series.min()
    s_max = series.max()
    if s_max == s_min:
        return pd.Series(0.5, index=series.index)
    return (series - s_min) / (s_max - s_min)


def run_pilar1_skoring() -> pd.DataFrame:
    print("=" * 75)
    print("MEMULAI PILAR 1: SKORING KELAYAKAN SEKTOR USAHA (BATCH PROCESS)")
    print("=" * 75)

    # 1. Validasi keberadaan dataset input
    for path_file in [KOMPETITOR_CSV, EKONOMI_CSV, SEWA_CSV]:
        if not path_file.exists():
            raise FileNotFoundError(f"Berkas tidak ditemukan: {path_file}")

    df_kompetitor = pd.read_csv(KOMPETITOR_CSV)
    df_ekonomi = pd.read_csv(EKONOMI_CSV)
    df_sewa = pd.read_csv(SEWA_CSV)

    # Buat lookup agregasi kompetitor per (wilayah, kategori)
    kompetitor_counts = (
        df_kompetitor.groupby(["wilayah", "kategori"])
        .size()
        .to_dict()
    )

    # Buat lookup ekonomi per nama wilayah
    ekonomi_lookup = {}
    for _, row in df_ekonomi.iterrows():
        k_nama = str(row["kabupaten_kota"]).strip().lower()
        ekonomi_lookup[k_nama] = row

    # Buat lookup biaya sewa per id wilayah
    sewa_lookup = {}
    for _, row in df_sewa.iterrows():
        w_id = str(row["wilayah"]).strip().lower()
        sewa_lookup[w_id] = row

    rows = []
    for w in WILAYAH_CONFIG:
        w_id = w["id"]
        w_label = w["label"]
        w_key = w["nama_match"].strip().lower()
        ek_data = ekonomi_lookup.get(w_key)
        sewa_data = sewa_lookup.get(w_id)

        if ek_data is None:
            raise KeyError(f"Data ekonomi untuk wilayah {w_key} tidak ditemukan.")

        kepadatan = float(ek_data["kepadatan_penduduk"])
        luas = float(ek_data["luas_km2"])
        populasi = kepadatan * luas
        pdrb = float(ek_data["pdrb_per_kapita"])
        pengeluaran = float(ek_data["pengeluaran_per_kapita"])
        umkm_total = float(ek_data.get("jumlah_umkm_2025", 50000))
        rasio_umkm_total = float(ek_data.get("rasio_umkm_per_1000_penduduk", (umkm_total / populasi) * 1000))

        harga_sewa = float(sewa_data["harga_sewa_per_m2_tahun"]) if sewa_data is not None else 400000.0

        for s in SEKTOR_CONFIG:
            s_id = s["id"]
            s_label = s["label"]

            # Jumlah kompetitor spesifik sektor di wilayah ini
            jml_kompetitor = kompetitor_counts.get((w_id, s_id), 0)
            rasio_kompetitor = (jml_kompetitor / populasi) * 1000.0

            rows.append({
                "sektor": s_id,
                "sektor_label": s_label,
                "wilayah": w_id,
                "wilayah_label": w_label,
                "jumlah_kompetitor": jml_kompetitor,
                "rasio_kompetitor_per_1000": round(rasio_kompetitor, 4),
                "pdrb_per_kapita": pdrb,
                "pengeluaran_per_kapita": pengeluaran,
                "kepadatan_penduduk": kepadatan,
                "estimasi_penduduk": int(populasi),
                "harga_sewa_per_m2_tahun": harga_sewa,
                "rasio_umkm_total_per_1000": round(rasio_umkm_total, 2)
            })

    df_panel = pd.DataFrame(rows)

    # 2. Normalisasi fitur lintas data
    # Fitur Penarik Pasar (+): PDRB, Pengeluaran, Kepadatan
    df_panel["pdrb_norm"] = min_max_norm(df_panel["pdrb_per_kapita"])
    df_panel["pengeluaran_norm"] = min_max_norm(df_panel["pengeluaran_per_kapita"])
    df_panel["kepadatan_norm"] = min_max_norm(df_panel["kepadatan_penduduk"])

    # Fitur Beban / Penghambat (-): Sewa, Kejenuhan Total UMKM, Rasio Kompetitor per Sektor
    df_panel["sewa_norm"] = min_max_norm(df_panel["harga_sewa_per_m2_tahun"])
    df_panel["umkm_total_norm"] = min_max_norm(df_panel["rasio_umkm_total_per_1000"])

    # Normalisasi rasio kompetitor dilakukan PER SEKTOR agar adil (karena baseline resto > laundry)
    df_panel["kompetitor_norm"] = df_panel.groupby("sektor")["rasio_kompetitor_per_1000"].transform(min_max_norm)

    # 3. Formulasi Skor Kelayakan Komposit (MCDA)
    # Bobot:
    # + Daya Beli & Pengeluaran : 25% + 25% = 50%
    # + Kepadatan Penduduk       : 15%
    # - Kepadatan Kompetitor     : 15%
    # - Biaya Sewa Operasional   : 10%
    # - Kejenuhan Total UMKM     : 10%
    daya_tarik = (
        0.25 * df_panel["pdrb_norm"] +
        0.25 * df_panel["pengeluaran_norm"] +
        0.15 * df_panel["kepadatan_norm"]
    )

    beban = (
        0.15 * df_panel["kompetitor_norm"] +
        0.10 * df_panel["sewa_norm"] +
        0.10 * df_panel["umkm_total_norm"]
    )

    skor_raw = daya_tarik - beban

    # Skalakan ke rentang 0 - 100 dengan baseline 50
    df_panel["skor"] = (50.0 + (skor_raw * 70.0)).clip(0.0, 100.0).round(2)

    # 4. Kategori Kelayakan
    def label_kategori(val: float) -> str:
        if val >= 70.0:
            return "Layak"
        elif val >= 50.0:
            return "Cukup Layak"
        else:
            return "Kurang Layak"

    df_panel["kategori"] = df_panel["skor"].apply(label_kategori)

    # 5. Pilih dan urutkan kolom final untuk website & reporting
    final_cols = [
        "sektor",
        "sektor_label",
        "wilayah",
        "wilayah_label",
        "jumlah_kompetitor",
        "rasio_kompetitor_per_1000",
        "pdrb_per_kapita",
        "pengeluaran_per_kapita",
        "harga_sewa_per_m2_tahun",
        "rasio_umkm_total_per_1000",
        "skor",
        "kategori"
    ]
    df_result = df_panel[final_cols].sort_values(by=["sektor", "skor"], ascending=[True, False]).reset_index(drop=True)

    # 6. Simpan ke data/processed/
    OUTPUT_SKORING_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_result.to_csv(OUTPUT_SKORING_CSV, index=False)

    print(f"\n[SUKSES] Tabel Skor Kelayakan Sektor berhasil disimpan ke:\n  -> {OUTPUT_SKORING_CSV}")
    print(f"Total Kombinasi Sektor x Wilayah: {len(df_result)} baris")

    # Tampilkan sampel output
    print("\n--- SAMPEL 10 BARIS HASIL SKORING KELAYAKAN ---")
    print(df_result[["sektor", "wilayah", "rasio_kompetitor_per_1000", "harga_sewa_per_m2_tahun", "skor", "kategori"]].head(10).to_string(index=False))
    print("=" * 75 + "\n")

    return df_result


if __name__ == "__main__":
    run_pilar1_skoring()
