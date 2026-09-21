"""
Modul Pembersihan dan Standardisasi Harga Sewa (Dataset 3)
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM

Modul ini:
1. Menstandardisasi penulisan nama wilayah agar 100% konsisten dengan Dataset 1 & 2
2. Menormalisasi seluruh harga sewa ke satuan standar: Rp per m2 per tahun
3. Menyimpan hasil bersih ke data/processed/biaya_operasional.csv
"""

import sys
from pathlib import Path
import pandas as pd

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset3_sewa.config import (
    RAW_OUTPUT_CSV,
    PROCESSED_OUTPUT_CSV,
    WILAYAH_MAPPING,
    WILAYAH_LABELS
)


def normalize_rental_price(row: pd.Series) -> float:
    """
    Mengubah nilai sewa ke satuan seragam: Rp per m2 per tahun.
    Jika satuan bulan, dikali 12. Jika tahun, tetap.
    """
    harga = float(row["harga_per_m2"])
    satuan = str(row.get("satuan_waktu", "tahun")).strip().lower()

    if satuan in ["bulan", "month", "bln"]:
        return harga * 12.0
    elif satuan in ["hari", "day"]:
        return harga * 365.0
    else:
        # Default diasumsikan tahunan
        return harga


def standardize_wilayah_id(raw_name: str) -> str:
    """
    Menstandardisasi string nama wilayah menjadi ID baku (seperti Dataset 1).
    Contoh: 'Kabupaten Sleman' -> 'sleman', 'Kota Yogyakarta' -> 'kota_yogyakarta'
    """
    cleaned = str(raw_name).strip().lower()
    return WILAYAH_MAPPING.get(cleaned, cleaned.replace(" ", "_"))


def clean_and_standardize_harga() -> pd.DataFrame:
    """
    Membaca data/raw/sewa_index.csv, melakukan normalisasi harga dan wilayah,
    lalu mengekspor ke data/processed/biaya_operasional.csv.
    """
    if not RAW_OUTPUT_CSV.exists():
        print(f"[Error] Berkas mentah tidak ditemukan: {RAW_OUTPUT_CSV}")
        print("Silakan jalankan fetch_index.py terlebih dahulu.")
        return pd.DataFrame()

    df_raw = pd.read_csv(RAW_OUTPUT_CSV)
    print(f"Membaca {len(df_raw)} baris data mentah dari {RAW_OUTPUT_CSV}...")

    df = df_raw.copy()

    # 1. Standardisasi ID Wilayah (konsisten dengan Dataset 1)
    df["wilayah"] = df["wilayah"].apply(standardize_wilayah_id)

    # 2. Tambahkan Label Wilayah Resmi
    df["wilayah_label"] = df["wilayah"].map(WILAYAH_LABELS).fillna(df["wilayah"])

    # 3. Normalisasi Harga Sewa (Rp per m2 per tahun)
    df["harga_sewa_per_m2_tahun"] = df.apply(normalize_rental_price, axis=1)

    # 4. Kategori Biaya Operasional (Tinggi, Sedang, Terjangkau)
    # Bermanfaat untuk fitur clustering/rekomendasi
    def kategorisasi_biaya(harga: float) -> str:
        if harga >= 700000:
            return "Tinggi"
        elif harga >= 400000:
            return "Menengah"
        else:
            return "Terjangkau"

    df["kategori_biaya"] = df["harga_sewa_per_m2_tahun"].apply(kategorisasi_biaya)

    # 5. Pilih dan susun kolom final
    kolom_final = [
        "wilayah",
        "wilayah_label",
        "harga_sewa_per_m2_tahun",
        "kategori_biaya",
        "sumber",
        "tahun"
    ]
    df_output = df[kolom_final].sort_values(by="harga_sewa_per_m2_tahun", ascending=False).reset_index(drop=True)

    # Simpan ke data/processed/biaya_operasional.csv
    df_output.to_csv(PROCESSED_OUTPUT_CSV, index=False, encoding="utf-8")

    print("\n" + "=" * 70)
    print("HASIL STANDARISASI BIAYA OPERASIONAL (DATASET 3)")
    print("=" * 70)
    print(f"File Hasil Disimpan ke : {PROCESSED_OUTPUT_CSV}")
    print(f"Total Wilayah          : {len(df_output)}")
    print("\nTabel Data Biaya Operasional Properti Komersial:")
    print(df_output[["wilayah", "wilayah_label", "harga_sewa_per_m2_tahun", "kategori_biaya"]].to_string(index=False))
    print("=" * 70)

    return df_output


if __name__ == "__main__":
    clean_and_standardize_harga()
