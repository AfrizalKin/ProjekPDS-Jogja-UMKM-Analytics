"""
Modul Pembersihan dan Penggabungan Data Ekonomi BPS DIY (Dataset 2)
Projek PDS - Sistem Rekomendasi Lokasi Kelayakan Usaha UMKM

Skrip ini melakukan:
1. Membaca 3 berkas CSV mentah dari BPS DIY (PDRB per kapita, Kepadatan Penduduk, Pengeluaran per kapita).
2. Mengecualikan baris agregat provinsi ("D.I. Yogyakarta" / "DI Yogyakarta").
3. Menstandarisasi penulisan nama wilayah ke 5 kabupaten/kota resmi di DIY dengan format spasi:
   ['Kulon Progo', 'Bantul', 'Gunung Kidul', 'Sleman', 'Kota Yogyakarta'] menggunakan dictionary mapping eksplisit.
4. Mengekstrak kolom indikator yang dibutuhkan:
   - pdrb_per_kapita (dari "Harga Berlaku", satuan: Ribu Rupiah)
   - kepadatan_penduduk (satuan: jiwa/km2)
   - luas_km2 (satuan: km2)
   - pengeluaran_per_kapita (dari "Jumlah", total makanan + bukan makanan, satuan: Rupiah/kapita/bulan)
5. Menggabungkan (inner join) ketiga dataset berdasarkan 'kabupaten_kota' dan memverifikasi integritas join.
6. Menyimpan hasil bersih ke 'data/processed/kondisi_ekonomi_wilayah.csv' dan menampilkan hasil verifikasi.
"""

import sys
import argparse
from pathlib import Path
import pandas as pd

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

# ==============================================================================
# 1. KONFIGURASI PATH
# ==============================================================================
DATA_RAW_BPS = BASE_DIR / "data" / "raw" / "bps"
DATA_RAW_BPS_EKONOMI = BASE_DIR / "data" / "raw" / "bps_ekonomi"
DATA_RAW_SIBAKUL = BASE_DIR / "data" / "raw" / "sibakul"
DATA_RAW_UMKM_SIBAKUL = BASE_DIR / "data" / "raw" / "umkm_sibakul"
PROCESSED_OUTPUT_CSV = BASE_DIR / "data" / "processed" / "kondisi_ekonomi_wilayah.csv"
PROCESSED_SIBAKUL_CSV = BASE_DIR / "data" / "processed" / "umkm_sibakul.csv"

# ==============================================================================
# 2. DICTIONARY MAPPING DAN FILTER AGREGAT PROVINSI
# ==============================================================================
# Baris agregat provinsi yang harus diexclude
PROVINSI_AGREGAT = {
    "d.i. yogyakarta",
    "di yogyakarta",
    "daerah istimewa yogyakarta",
    "diy",
    "provinsi d.i. yogyakarta",
    "provinsi di yogyakarta"
}

# Mapping eksplisit dan hardcoded untuk 5 wilayah administratif DIY
# Menghindari fuzzy matching otomatis agar 100% deterministik & aman
WILAYAH_MAPPING = {
    # Kulon Progo (menangani variasi tanpa spasi 'Kulonprogo' dan dengan awalan)
    "kulonprogo": "Kulon Progo",
    "kulon progo": "Kulon Progo",
    "kab. kulonprogo": "Kulon Progo",
    "kab. kulon progo": "Kulon Progo",
    "kabupaten kulonprogo": "Kulon Progo",
    "kabupaten kulon progo": "Kulon Progo",

    # Bantul
    "bantul": "Bantul",
    "kab. bantul": "Bantul",
    "kabupaten bantul": "Bantul",

    # Gunung Kidul (menangani variasi tanpa spasi 'Gunungkidul' dan dengan awalan)
    "gunungkidul": "Gunung Kidul",
    "gunung kidul": "Gunung Kidul",
    "kab. gunungkidul": "Gunung Kidul",
    "kab. gunung kidul": "Gunung Kidul",
    "kabupaten gunungkidul": "Gunung Kidul",
    "kabupaten gunung kidul": "Gunung Kidul",

    # Sleman
    "sleman": "Sleman",
    "kab. sleman": "Sleman",
    "kabupaten sleman": "Sleman",

    # Kota Yogyakarta
    "kota yogyakarta": "Kota Yogyakarta",
    "yogyakarta": "Kota Yogyakarta",
    "kota jogja": "Kota Yogyakarta"
}

WILAYAH_TARGET = {
    "Kulon Progo",
    "Bantul",
    "Gunung Kidul",
    "Sleman",
    "Kota Yogyakarta"
}


def standardize_wilayah(raw_name: str) -> str:
    """
    Membersihkan string nama wilayah dan memetakan ke format standar menggunakan dictionary.
    """
    cleaned_key = str(raw_name).strip().lower()
    return WILAYAH_MAPPING.get(cleaned_key, str(raw_name).strip())


def resolve_input_dir(custom_dir: Path | None = None) -> Path:
    """
    Menentukan direktori input data mentah BPS:
    1. Custom dir jika diisi argumen
    2. data/raw/bps jika ada
    3. data/raw/bps_ekonomi jika ada
    """
    if custom_dir and custom_dir.exists():
        return custom_dir
    if DATA_RAW_BPS.exists():
        return DATA_RAW_BPS
    if DATA_RAW_BPS_EKONOMI.exists():
        return DATA_RAW_BPS_EKONOMI
    raise FileNotFoundError(
        f"Direktori data mentah BPS tidak ditemukan di '{DATA_RAW_BPS}' maupun '{DATA_RAW_BPS_EKONOMI}'"
    )


def find_file(input_dir: Path, pattern: str) -> Path:
    """Mencari berkas CSV berdasarkan pola nama."""
    matches = list(input_dir.glob(pattern))
    if not matches:
        raise FileNotFoundError(f"Berkas dengan pola '{pattern}' tidak ditemukan di {input_dir}")
    return matches[0]


# ==============================================================================
# 3. PEMBACAAN & PEMBERSIHAN MASING-MASING DATASET
# ==============================================================================

def clean_pdrb(file_path: Path) -> pd.DataFrame:
    """
    Membaca dan membersihkan berkas PDRB per kapita BPS 2024.
    Mengambil kolom 'Harga Berlaku' sebagai 'pdrb_per_kapita'.
    
    CATATAN SATUAN:
    - Kolom 'pdrb_per_kapita' bersumber dari kolom 'Harga Berlaku' dengan SATUAN RIBU RUPIAH (BPS DIY).
      Contoh: 37976.68 berarti Rp 37.976.680 per kapita per tahun.
    """
    print(f"[1/4] Memproses PDRB dari: {file_path.name}")
    
    # Format tabel BPS memiliki baris header bertingkat; baris data dimulai setelah baris ke-4
    df_raw = pd.read_csv(
        file_path,
        skiprows=4,
        header=None,
        names=["kabupaten_kota", "pdrb_per_kapita", "pdrb_konstan_2010"],
        encoding="utf-8-sig"
    )

    # Identifikasi & exclude agregat provinsi
    is_agregat = df_raw["kabupaten_kota"].astype(str).str.strip().str.lower().isin(PROVINSI_AGREGAT)
    excluded_rows = df_raw[is_agregat]["kabupaten_kota"].tolist()
    if excluded_rows:
        print(f"      - Mengecualikan agregat provinsi: {excluded_rows}")
    df_clean = df_raw[~is_agregat].copy()

    # Standardisasi nama wilayah
    df_clean["kabupaten_kota"] = df_clean["kabupaten_kota"].apply(standardize_wilayah)

    # Konversi nilai numerik (Harga Berlaku dalam Ribu Rupiah)
    df_clean["pdrb_per_kapita"] = pd.to_numeric(df_clean["pdrb_per_kapita"], errors="coerce")

    # Ambil kolom yang dibutuhkan
    return df_clean[["kabupaten_kota", "pdrb_per_kapita"]].reset_index(drop=True)


def clean_kepadatan(file_path: Path) -> pd.DataFrame:
    """
    Membaca dan membersihkan berkas Kepadatan Penduduk & Luas Wilayah BPS 2024.
    Mengambil kolom:
    - 'kepadatan_penduduk' (satuan: jiwa/km2)
    - 'luas_km2' (satuan: km2)
    """
    print(f"[2/4] Memproses Kepadatan Penduduk dari: {file_path.name}")

    # Format tabel BPS: baris data dimulai setelah baris ke-4
    df_raw = pd.read_csv(
        file_path,
        skiprows=4,
        header=None,
        names=["kabupaten_kota", "luas_km2", "kepadatan_penduduk"],
        encoding="utf-8-sig"
    )

    # Identifikasi & exclude agregat provinsi
    is_agregat = df_raw["kabupaten_kota"].astype(str).str.strip().str.lower().isin(PROVINSI_AGREGAT)
    excluded_rows = df_raw[is_agregat]["kabupaten_kota"].tolist()
    if excluded_rows:
        print(f"      - Mengecualikan agregat provinsi: {excluded_rows}")
    df_clean = df_raw[~is_agregat].copy()

    # Standardisasi nama wilayah
    df_clean["kabupaten_kota"] = df_clean["kabupaten_kota"].apply(standardize_wilayah)

    # Konversi numerik
    df_clean["luas_km2"] = pd.to_numeric(df_clean["luas_km2"], errors="coerce")
    df_clean["kepadatan_penduduk"] = pd.to_numeric(df_clean["kepadatan_penduduk"], errors="coerce")

    # Ambil kolom yang dibutuhkan
    return df_clean[["kabupaten_kota", "kepadatan_penduduk", "luas_km2"]].reset_index(drop=True)


def clean_pengeluaran(file_path: Path) -> pd.DataFrame:
    """
    Membaca dan membersihkan berkas Rata-rata Pengeluaran per Kapita Sebulan BPS 2024.
    Mengambil kolom 'Jumlah' (total makanan + non-makanan) sebagai 'pengeluaran_per_kapita'.
    
    CATATAN SATUAN:
    - Satuan: Rupiah per kapita per bulan.
    """
    print(f"[3/4] Memproses Pengeluaran per Kapita dari: {file_path.name}")

    df_raw = pd.read_csv(file_path, encoding="utf-8-sig")

    # Cari kolom wilayah (kolom pertama atau yang mengandung 'kabupaten') dan kolom total 'Jumlah'
    kab_cols = [c for c in df_raw.columns if "kabupaten" in c.lower()]
    col_wilayah = kab_cols[0] if kab_cols else df_raw.columns[0]

    jumlah_cols = [c for c in df_raw.columns if "jumlah" in c.lower()]
    if not jumlah_cols:
        raise KeyError(
            f"Kolom 'Jumlah' tidak ditemukan dalam file pengeluaran. Kolom tersedia: {list(df_raw.columns)}"
        )
    col_jumlah = jumlah_cols[0]

    df_clean = df_raw[[col_wilayah, col_jumlah]].copy()
    df_clean.columns = ["kabupaten_kota", "pengeluaran_per_kapita"]

    # Identifikasi & exclude agregat provinsi
    is_agregat = df_clean["kabupaten_kota"].astype(str).str.strip().str.lower().isin(PROVINSI_AGREGAT)
    excluded_rows = df_clean[is_agregat]["kabupaten_kota"].tolist()
    if excluded_rows:
        print(f"      - Mengecualikan agregat provinsi: {excluded_rows}")
    df_clean = df_clean[~is_agregat].copy()

    # Standardisasi nama wilayah
    df_clean["kabupaten_kota"] = df_clean["kabupaten_kota"].apply(standardize_wilayah)

    # Konversi numerik
    df_clean["pengeluaran_per_kapita"] = pd.to_numeric(df_clean["pengeluaran_per_kapita"], errors="coerce")

    return df_clean[["kabupaten_kota", "pengeluaran_per_kapita"]].reset_index(drop=True)


def resolve_sibakul_dir(custom_dir: Path | None = None) -> Path | None:
    """Mencari direktori data mentah SiBakul."""
    if custom_dir and custom_dir.exists():
        return custom_dir
    if DATA_RAW_SIBAKUL.exists():
        return DATA_RAW_SIBAKUL
    if DATA_RAW_UMKM_SIBAKUL.exists():
        return DATA_RAW_UMKM_SIBAKUL
    return None


def clean_sibakul(sibakul_dir: Path | None = None) -> pd.DataFrame | None:
    """
    Membaca dan membersihkan berkas Dataset 5 (SiBakul Jogja / Diskop UKM DIY).
    Mengambil data jumlah UMKM terdaftar tahun 2025 per kabupaten/kota.
    """
    target_dir = resolve_sibakul_dir(sibakul_dir)
    if not target_dir:
        return None

    target_file = target_dir / "umkm_sibakul.csv"
    if not target_file.exists():
        matches = list(target_dir.glob("*sibakul*.csv"))
        if not matches:
            return None
        target_file = matches[0]

    print(f"[Ekstensi Dataset 5] Memproses SiBakul dari: {target_file.name}")
    df_raw = pd.read_csv(target_file, encoding="utf-8-sig")

    # Cari kolom wilayah
    col_wilayah = [c for c in df_raw.columns if "kabupaten" in c.lower() or "wilayah" in c.lower()][0]
    df_raw["kabupaten_kota"] = df_raw[col_wilayah].apply(standardize_wilayah)

    # Konversi numerik untuk kolom jumlah
    for c in df_raw.columns:
        if "jumlah" in c.lower() or "umkm" in c.lower() and c != "kabupaten_kota":
            df_raw[c] = pd.to_numeric(df_raw[c], errors="coerce")

    cols = ["kabupaten_kota"] + [c for c in df_raw.columns if "jumlah" in c.lower()]
    df_clean = df_raw[cols].drop_duplicates(subset=["kabupaten_kota"]).reset_index(drop=True)

    # Cek & salin data pelengkap level DIY jika ada (tren tahunan & sektor makro)
    tren_file = target_dir / "umkm_tren_tahunan_diy.csv"
    if tren_file.exists():
        df_tren = pd.read_csv(tren_file, encoding="utf-8-sig")
        df_tren.to_csv(BASE_DIR / "data" / "processed" / "umkm_tren_tahunan_diy.csv", index=False)

    sektor_file = target_dir / "umkm_sektor_diy.csv"
    if sektor_file.exists():
        df_sektor = pd.read_csv(sektor_file, encoding="utf-8-sig")
        df_sektor.to_csv(BASE_DIR / "data" / "processed" / "umkm_sektor_diy.csv", index=False)

    return df_clean


# ==============================================================================
# 4. PENGGABUNGAN (JOIN) & VALIDASI
# ==============================================================================

def merge_and_validate(
    df_pdrb: pd.DataFrame,
    df_kepadatan: pd.DataFrame,
    df_pengeluaran: pd.DataFrame,
    df_sibakul: pd.DataFrame | None = None
) -> tuple[pd.DataFrame, pd.DataFrame | None]:
    """
    Menggabungkan ketiga dataframe (dan opsional SiBakul) dengan inner join pada 'kabupaten_kota'.
    Mencetak status integritas data dan mendeteksi jika ada wilayah yang gagal match.
    """
    print("\n[4/4] Menggabungkan ketiga dataset (Inner Join)...")

    # Himpunan wilayah di masing-masing dataset
    set_pdrb = set(df_pdrb["kabupaten_kota"])
    set_kepadatan = set(df_kepadatan["kabupaten_kota"])
    set_pengeluaran = set(df_pengeluaran["kabupaten_kota"])

    all_wilayah = set_pdrb | set_kepadatan | set_pengeluaran
    common_wilayah = set_pdrb & set_kepadatan & set_pengeluaran

    # Pengecekan kegagalan match
    unmatched_pdrb = all_wilayah - set_pdrb
    unmatched_kepadatan = all_wilayah - set_kepadatan
    unmatched_pengeluaran = all_wilayah - set_pengeluaran

    if unmatched_pdrb or unmatched_kepadatan or unmatched_pengeluaran:
        print("  [PERINGATAN] Terdapat wilayah yang gagal match!")
        if unmatched_pdrb:
            print(f"    - Hilang di dataset PDRB: {unmatched_pdrb}")
        if unmatched_kepadatan:
            print(f"    - Hilang di dataset Kepadatan: {unmatched_kepadatan}")
        if unmatched_pengeluaran:
            print(f"    - Hilang di dataset Pengeluaran: {unmatched_pengeluaran}")
    else:
        print(f"  [SUKSES] Semua {len(common_wilayah)} wilayah berhasil match 100% pada ketiga dataset.")

    # Lakukan inner join basis BPS
    df_merged = df_pdrb.merge(
        df_kepadatan,
        on="kabupaten_kota",
        how="inner"
    ).merge(
        df_pengeluaran,
        on="kabupaten_kota",
        how="inner"
    )

    df_sibakul_out = None
    target_columns = [
        "kabupaten_kota",
        "pdrb_per_kapita",
        "kepadatan_penduduk",
        "luas_km2",
        "pengeluaran_per_kapita"
    ]

    # Integrasi Dataset 5 (SiBakul) jika tersedia
    if df_sibakul is not None and not df_sibakul.empty:
        print("  [INTEGRASI] Menggabungkan data SiBakul ke kondisi ekonomi wilayah...")
        df_merged = df_merged.merge(df_sibakul, on="kabupaten_kota", how="left")

        # Hitung estimasi populasi penduduk & rasio UMKM per 1.000 penduduk
        df_merged["estimasi_penduduk"] = (df_merged["kepadatan_penduduk"] * df_merged["luas_km2"]).astype(int)
        
        if "jumlah_umkm_2025" in df_merged.columns:
            df_merged["rasio_umkm_per_1000_penduduk"] = (
                (df_merged["jumlah_umkm_2025"] / df_merged["estimasi_penduduk"]) * 1000
            ).round(2)
            target_columns.extend(["jumlah_umkm_2025", "rasio_umkm_per_1000_penduduk"])

        # Buat dataframe khusus processed SiBakul
        sibakul_cols = ["kabupaten_kota", "jumlah_umkm_2025"]
        if "jumlah_umkm_ktp_domisili_2025" in df_merged.columns:
            sibakul_cols.append("jumlah_umkm_ktp_domisili_2025")
        if "rasio_umkm_per_1000_penduduk" in df_merged.columns:
            sibakul_cols.append("rasio_umkm_per_1000_penduduk")
        df_sibakul_out = df_merged[sibakul_cols].copy()

    df_final = df_merged[target_columns].copy()

    # Validasi jumlah baris dan kelengkapan wilayah target DIY
    if len(df_final) != 5:
        print(f"  [PERINGATAN] Jumlah baris akhir ({len(df_final)}) tidak sama dengan 5!")
    else:
        print("  [VALIDASI] Terverifikasi tepat 5 kabupaten/kota Daerah Istimewa Yogyakarta.")

    missing_target = WILAYAH_TARGET - set(df_final["kabupaten_kota"])
    if missing_target:
        print(f"  [PERINGATAN] Wilayah target berikut tidak ditemukan: {missing_target}")

    return df_final, df_sibakul_out


# ==============================================================================
# 5. ORCHESTRATOR UTAMA
# ==============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Pipeline Pembersihan Data Ekonomi Wilayah BPS DIY (Dataset 2 & Dataset 5)"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default=None,
        help="Direktori berisi 3 CSV mentah BPS (default: data/raw/bps atau data/raw/bps_ekonomi)"
    )
    parser.add_argument(
        "--sibakul-dir",
        type=str,
        default=None,
        help="Direktori berisi data mentah SiBakul (default: data/raw/sibakul atau data/raw/umkm_sibakul)"
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=str(PROCESSED_OUTPUT_CSV),
        help="Path file CSV hasil (default: data/processed/kondisi_ekonomi_wilayah.csv)"
    )
    args = parser.parse_args()

    custom_input_dir = Path(args.input_dir) if args.input_dir else None
    input_dir = resolve_input_dir(custom_input_dir)
    output_file = Path(args.output_file)

    print("=" * 70)
    print("PIPELINE PEMBERSIHAN DATA EKONOMI BPS DIY (DATASET 2 & 5)")
    print("=" * 70)
    print(f"Direktori Input BPS  : {input_dir}")
    print(f"File Output Utama    : {output_file}\n")

    # Identifikasi 3 file CSV BPS
    pdrb_file = find_file(input_dir, "*PDRB*")
    kepadatan_file = find_file(input_dir, "*Kepadatan*")
    pengeluaran_file = find_file(input_dir, "*Pengeluaran*")

    # Proses masing-masing berkas BPS
    df_pdrb = clean_pdrb(pdrb_file)
    df_kepadatan = clean_kepadatan(kepadatan_file)
    df_pengeluaran = clean_pengeluaran(pengeluaran_file)

    # Proses berkas SiBakul jika tersedia
    custom_sibakul_dir = Path(args.sibakul_dir) if args.sibakul_dir else None
    df_sibakul = clean_sibakul(custom_sibakul_dir)

    # Gabungkan dan validasi
    df_final, df_sibakul_out = merge_and_validate(df_pdrb, df_kepadatan, df_pengeluaran, df_sibakul)

    # Simpan kondisi ekonomi wilayah ke data/processed/
    output_file.parent.mkdir(parents=True, exist_ok=True)
    df_final.to_csv(output_file, index=False)
    print(f"\n[SUKSES] Data gabungan berhasil disimpan ke: {output_file}")

    # Simpan berkas khusus SiBakul ke data/processed/ jika ada
    if df_sibakul_out is not None:
        PROCESSED_SIBAKUL_CSV.parent.mkdir(parents=True, exist_ok=True)
        df_sibakul_out.to_csv(PROCESSED_SIBAKUL_CSV, index=False)
        print(f"[SUKSES] Data SiBakul berhasil disimpan ke: {PROCESSED_SIBAKUL_CSV}")

    # Cetak hasil akhir untuk verifikasi manual user
    print("\n" + "=" * 70)
    print("HASIL AKHIR DATAFRAME KONDISI EKONOMI WILAYAH (5 BARIS KAB/KOTA DIY):")
    print("=" * 70)
    print(df_final.to_string(index=False))
    print("=" * 70)
    print("\nKeterangan Kolom & Satuan:")
    print("- pdrb_per_kapita              : Ribu Rupiah (Harga Berlaku 2024, BPS DIY)")
    print("- kepadatan_penduduk           : Jiwa / km2 (Tahun 2024, BPS DIY)")
    print("- luas_km2                     : Kilometer Persegi / km2 (BPS DIY)")
    print("- pengeluaran_per_kapita       : Rupiah / kapita / bulan (Total 2024, BPS DIY)")
    if "jumlah_umkm_2025" in df_final.columns:
        print("- jumlah_umkm_2025             : Unit UMKM Terdaftar (SiBakul Jogja / Diskop UKM 2025)")
        print("- rasio_umkm_per_1000_penduduk : Jumlah UMKM per 1.000 jiwa penduduk")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
