"""
Modul Pembersihan, Penggabungan, dan Standarisasi Dataset 4: Tren Sektor Usaha
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM

Modul ini:
1. Membaca bps_cleaned.csv sebagai sumber time series utama (ground truth).
2. Menstandarkan wilayah agar 100% konsisten dengan Dataset 1 dan Dataset 3.
3. Menggabungkan data tren pencarian dari trends_raw.csv (jika ada) menggunakan LEFT JOIN,
   sehingga tidak ada satu baris pun data BPS yang hilang.
4. Menghitung laju pertumbuhan tahunan (YoY Growth Rate) per sektor per wilayah.
5. Mengekspor hasil final ke data/processed/tren_sektor.csv (siap pakai untuk forecasting Pilar 3).
"""

import sys
import re
from pathlib import Path
import pandas as pd
import numpy as np

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset4_tren.config import (
    BPS_CLEANED_CSV,
    TRENDS_RAW_CSV,
    PROCESSED_TREN_CSV,
    WILAYAH_MAPPING,
    WILAYAH_LABELS
)


def standardize_wilayah(raw_val: str) -> str:
    """Menstandardisasi ID wilayah agar identik dengan dataset 1 & 3."""
    val = str(raw_val).strip().lower()
    val = re.sub(r"^(kabupaten|kab\.|kota)\s+", "", val)
    return WILAYAH_MAPPING.get(val, val.replace(" ", "_"))


def process_and_merge_tren() -> pd.DataFrame:
    """
    Melakukan standardisasi, penggabungan BPS + Trends, dan penghitungan laju pertumbuhan.
    """
    print("=" * 70)
    print("DATASET 4: PEMBERSIHAN & STANDARDISASI TREN SEKTOR USAHA")
    print("=" * 70)

    # 1. Validasi keberadaan file utama BPS
    if not BPS_CLEANED_CSV.exists():
        print(f"[Error] File BPS bersih tidak ditemukan di: {BPS_CLEANED_CSV}")
        print("Jalankan 'fetch_bps.py' terlebih dahulu.")
        return pd.DataFrame()

    df_bps = pd.read_csv(BPS_CLEANED_CSV)
    print(f"Membaca {len(df_bps)} baris data BPS dari {BPS_CLEANED_CSV.name}...")

    # 2. Standardisasi Wilayah
    df_bps["wilayah"] = df_bps["wilayah"].apply(standardize_wilayah)
    df_bps["wilayah_label"] = df_bps["wilayah"].map(WILAYAH_LABELS).fillna(df_bps["wilayah"])

    # Pastikan tipe data tahun dan jumlah usaha valid
    df_bps["tahun"] = df_bps["tahun"].astype(int)
    df_bps["jumlah_usaha"] = pd.to_numeric(df_bps["jumlah_usaha"], errors="coerce").fillna(0.0)

    # 3. Urutkan berdasarkan wilayah, sektor, dan tahun untuk kalkulasi tren
    df_bps = df_bps.sort_values(by=["wilayah", "sektor_usaha", "tahun"]).reset_index(drop=True)

    # 4. Hitung Pertumbuhan Tahunan (YoY Growth %)
    df_bps["pertumbuhan_tahunan_unit"] = df_bps.groupby(["wilayah", "sektor_usaha"])["jumlah_usaha"].diff()
    df_bps["pertumbuhan_tahunan_pct"] = (
        df_bps.groupby(["wilayah", "sektor_usaha"])["jumlah_usaha"].pct_change() * 100.0
    ).round(2)

    # 5. Gabungkan dengan data Google Trends jika tersedia (LEFT JOIN)
    if TRENDS_RAW_CSV.exists():
        try:
            df_trends = pd.read_csv(TRENDS_RAW_CSV)
            if not df_trends.empty and "sektor_usaha" in df_trends.columns and "tahun" in df_trends.columns:
                print(f"Menemukan data Google Trends ({len(df_trends)} baris). Melakukan agregasi tahunan...")
                # Agregasi rata-rata indeks tren per sektor dan tahun
                df_trends_annual = df_trends.groupby(["sektor_usaha", "tahun"])["trend_index"].mean().round(2).reset_index()
                df_trends_annual.rename(columns={"trend_index": "google_trends_score"}, inplace=True)

                # LEFT JOIN: tidak boleh ada baris BPS yang hilang
                df_merged = pd.merge(
                    df_bps,
                    df_trends_annual,
                    on=["sektor_usaha", "tahun"],
                    how="left"
                )
                print("  -> Google Trends berhasil digabungkan sebagai fitur 'google_trends_score'.")
            else:
                print("[Info] Data Google Trends kosong atau tidak valid. Melanjutkan tanpa data trends.")
                df_merged = df_bps.copy()
                df_merged["google_trends_score"] = np.nan
        except Exception as e:
            print(f"[Warning] Gagal membaca data Google Trends ({e}). Melanjutkan dengan data BPS saja.")
            df_merged = df_bps.copy()
            df_merged["google_trends_score"] = np.nan
    else:
        print("[Info] File trends_raw.csv tidak ditemukan. Melanjutkan murni dengan data BPS.")
        df_merged = df_bps.copy()
        df_merged["google_trends_score"] = np.nan

    # 6. Susun kolom akhir
    kolom_final = [
        "wilayah",
        "wilayah_label",
        "sektor_usaha",
        "kbli",
        "tahun",
        "jumlah_usaha",
        "pertumbuhan_tahunan_unit",
        "pertumbuhan_tahunan_pct",
        "google_trends_score"
    ]
    # Filter kolom yang ada
    kolom_ada = [c for c in kolom_final if c in df_merged.columns]
    df_output = df_merged[kolom_ada].copy()

    # 7. Simpan ke data/processed/tren_sektor.csv
    df_output.to_csv(PROCESSED_TREN_CSV, index=False, encoding="utf-8")

    print("\n" + "=" * 70)
    print("HASIL AKHIR STANDARISASI TREN SEKTOR USAHA (DATASET 4)")
    print("=" * 70)
    print(f"Output File Tersimpan di : {PROCESSED_TREN_CSV}")
    print(f"Total Baris Data         : {len(df_output)}")
    print(f"Jumlah Wilayah Tercover  : {df_output['wilayah'].nunique()} ({', '.join(df_output['wilayah'].unique())})")
    print(f"Jumlah Sektor Tercover   : {df_output['sektor_usaha'].nunique()} ({', '.join(df_output['sektor_usaha'].unique())})")
    print(f"Rentang Periode          : {df_output['tahun'].min()} - {df_output['tahun'].max()}")
    print("\nSampel 10 Baris Pertama:")
    print(df_output.head(10).to_string(index=False))
    print("=" * 70)

    return df_output


if __name__ == "__main__":
    process_and_merge_tren()
