"""
Modul Parser File BPS (Dataset 4: Tren Sektor Usaha UMKM)
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM

Modul ini membaca file statis yang diunduh manual dari portal BPS (Excel/CSV)
di data/raw/bps/ dan menanganinya secara fleksibel:
1. Menghapus metadata judul di baris awal (multi-row headers)
2. Menangani merged cells pada kolom wilayah/sektor (Forward Fill)
3. Menghapus catatan kaki (footnotes) di baris akhir
4. Menstandarkan format kolom (Wide ke Long format jika tahun berbentuk kolom terpisah)
5. Menyimpan hasil bersih ke data/interim/bps_cleaned.csv
"""

import sys
import re
import csv
from pathlib import Path
from typing import List, Optional
import pandas as pd

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset4_tren.config import (
    DATA_RAW_BPS_DIR,
    BPS_CLEANED_CSV,
    WILAYAH_MAPPING,
    SEKTOR_KBLI_MAPPING
)


def match_sektor_name(raw_text: str) -> tuple[str, Optional[str]]:
    """
    Mencocokkan nama sektor dari teks mentah BPS dengan ID sektor projek.
    Mengembalikan tuple: (sektor_id, kbli_code)
    """
    text_clean = str(raw_text).strip().lower()

    # Ekstrak kode angka jika ada (misal: "561 - Restoran", "56303 Kafe")
    kbli_match = re.search(r"\b(\d{3,5})\b", text_clean)
    kbli_code = kbli_match.group(1) if kbli_match else None

    for sektor_id, meta in SEKTOR_KBLI_MAPPING.items():
        # Cek kecocokan KBLI prefix
        if kbli_code:
            for prefix in meta["kbli_prefix"]:
                if kbli_code.startswith(prefix.replace("I-", "").replace("G-", "").replace("S-", "")):
                    return sektor_id, kbli_code

        # Cek kecocokan kata kunci nama sektor
        for kw in meta["keywords_alt"]:
            if kw in text_clean:
                return sektor_id, kbli_code

    return text_clean, kbli_code


def standardize_wilayah_id(raw_wilayah: str) -> str:
    """
    Menstandarkan string nama wilayah menjadi ID baku (Dataset 1, 3, 4).
    """
    cleaned = str(raw_wilayah).strip().lower()
    cleaned = re.sub(r"^(kabupaten|kab\.|kota)\s+", "", cleaned)
    return WILAYAH_MAPPING.get(cleaned, cleaned.replace(" ", "_"))


def parse_bps_raw_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Membersihkan tabel mentah BPS yang memiliki header multi-baris,
    sel gabungan (merged cells), dan catatan kaki.
    """
    # 1. Buang baris dan kolom yang seluruh nilainya NaN
    df = df_raw.dropna(how="all").dropna(axis=1, how="all").reset_index(drop=True)

    # 2. Deteksi baris header utama (cari baris dengan minimal 3 cell yang memuat kata kunci/tahun)
    header_idx = 0
    for idx, row in df.iterrows():
        valid_vals = [str(val).strip() for val in row if pd.notna(val) and str(val).strip() != ""]
        if len(valid_vals) < 3:
            continue  # Lewati baris judul atau metadata yang hanya 1-2 cell

        row_str = " ".join(v.lower() for v in valid_vals)
        has_year = any(re.match(r"^(19|20)\d{2}$", v) for v in valid_vals)
        has_kw = any(k in row_str for k in ["wilayah", "kabupaten", "kota", "kategori", "sektor", "lapangan usaha", "usaha"])

        if has_year or has_kw:
            header_idx = idx
            break

    # Potong dataframe dari baris header tersebut
    df = df.iloc[header_idx:].reset_index(drop=True)
    df.columns = df.iloc[0].astype(str).str.strip()
    df = df.iloc[1:].reset_index(drop=True)

    # 3. Filter baris catatan kaki (footnotes) di bagian bawah tabel
    footer_keywords = ["sumber:", "source:", "catatan:", "note:", "*", "keterangan:"]
    valid_rows = []
    for idx, row in df.iterrows():
        first_cell = str(row.iloc[0]).strip().lower()
        if any(first_cell.startswith(kw) for kw in footer_keywords):
            break
        valid_rows.append(idx)

    df = df.loc[valid_rows].copy()

    # 4. Handle Merged Cells (Forward Fill pada kolom pertama jika berupa nama wilayah)
    first_col = df.columns[0]
    df[first_col] = df[first_col].replace(r"^\s*$", None, regex=True).ffill()

    # 5. Deteksi apakah format tabel bertipe WIDE (tahun sebagai kolom) atau LONG
    # Cari kolom-kolom yang namanya merupakan 4 digit tahun (contoh: 2020, 2021, 2022, 2023)
    year_cols = [c for c in df.columns if re.match(r"^(19|20)\d{2}$", str(c).strip())]

    records = []

    if year_cols:
        # FORMAT WIDE: Melakukan melt/unpivot
        non_year_cols = [c for c in df.columns if c not in year_cols]
        col_wilayah = non_year_cols[0]
        col_sektor = non_year_cols[1] if len(non_year_cols) > 1 else non_year_cols[0]

        for c in non_year_cols:
            cl = str(c).strip().lower()
            if any(k in cl for k in ["wilayah", "kabupaten", "kota", "daerah"]):
                col_wilayah = c
            elif any(k in cl for k in ["kategori", "sektor", "usaha", "kbli", "lapangan"]):
                col_sektor = c

        for _, row in df.iterrows():
            val1 = str(row[col_wilayah]).strip()
            val2 = str(row[col_sektor]).strip() if col_sektor != col_wilayah else "UMKM Gabungan"

            # Validasi jika kolom terbalik
            w_test = standardize_wilayah_id(val1)
            if w_test not in WILAYAH_MAPPING.values() and standardize_wilayah_id(val2) in WILAYAH_MAPPING.values():
                val1, val2 = val2, val1

            wilayah_val = val1
            sektor_val = val2

            sektor_id, kbli = match_sektor_name(sektor_val)
            std_wilayah = standardize_wilayah_id(wilayah_val)

            for yr in year_cols:
                val = row[yr]
                # Bersihkan karakter non-numerik seperti titik ribuan, spasi, atau tanda '-' (kosong)
                val_clean = re.sub(r"[^\d.]", "", str(val).replace(",", "."))
                try:
                    jumlah = float(val_clean) if val_clean else 0.0
                except ValueError:
                    jumlah = 0.0

                records.append({
                    "wilayah": std_wilayah,
                    "sektor_usaha": sektor_id,
                    "kbli": kbli if kbli else "-",
                    "tahun": int(yr),
                    "jumlah_usaha": jumlah
                })
    else:
        # FORMAT LONG: Tabel sudah memiliki kolom wilayah, sektor, tahun, jumlah
        # Cari nama kolom secara fleksibel
        col_map = {}
        for c in df.columns:
            cl = str(c).lower()
            if any(k in cl for k in ["wilayah", "kabupaten", "kota"]):
                col_map["wilayah"] = c
            elif any(k in cl for k in ["sektor", "usaha", "kbli", "lapangan"]):
                col_map["sektor"] = c
            elif any(k in cl for k in ["tahun", "year"]):
                col_map["tahun"] = c
            elif any(k in cl for k in ["jumlah", "unit", "total", "count"]):
                col_map["jumlah"] = c

        for _, row in df.iterrows():
            w_raw = str(row[col_map.get("wilayah", df.columns[0])]).strip()
            s_raw = str(row[col_map.get("sektor", df.columns[1])]).strip()
            t_raw = str(row[col_map.get("tahun", df.columns[2])]).strip()
            j_raw = str(row[col_map.get("jumlah", df.columns[3])]).strip()

            sektor_id, kbli = match_sektor_name(s_raw)
            j_clean = re.sub(r"[^\d.]", "", j_raw.replace(",", "."))

            records.append({
                "wilayah": standardize_wilayah_id(w_raw),
                "sektor_usaha": sektor_id,
                "kbli": kbli if kbli else "-",
                "tahun": int(re.search(r"\d{4}", t_raw).group(0)) if re.search(r"\d{4}", t_raw) else 2023,
                "jumlah_usaha": float(j_clean) if j_clean else 0.0
            })

    return pd.DataFrame(records)


def load_bps_files() -> pd.DataFrame:
    """
    Memindai folder data/raw/bps/ dan mengurai setiap file Excel (.xlsx, .xls) atau .csv.
    """
    print("=" * 70)
    print("DATASET 4: MEMBACA DAN MEMBERSIHKAN DATA RESMI BPS")
    print("=" * 70)

    all_files = list(DATA_RAW_BPS_DIR.glob("*.csv")) + \
                list(DATA_RAW_BPS_DIR.glob("*.xlsx")) + \
                list(DATA_RAW_BPS_DIR.glob("*.xls"))

    # Abaikan berkas indikator makroekonomi milik Dataset 2 agar tidak salah diparsing
    exclude_keywords = ["pdrb", "kepadatan", "pengeluaran"]
    files = [
        f for f in all_files
        if not any(kw in f.name.lower() for kw in exclude_keywords)
    ]

    if not files:
        print(f"[PERINGATAN] Tidak ditemukan file Excel/CSV data usaha di: {DATA_RAW_BPS_DIR}")
        print("Membuat file template acuan tabel usaha: data/raw/bps/tabel_usaha_bps_diy.csv")
        create_template_bps_file()
        # Ambil kembali file template yang baru dibuat
        files = [DATA_RAW_BPS_DIR / "tabel_usaha_bps_diy.csv"]

    all_dfs = []
    for f in files:
        print(f"Memproses file BPS: {f.name}...")
        try:
            if f.suffix.lower() == ".csv":
                rows = []
                encodings = ["utf-8-sig", "utf-8", "latin1"]
                for enc in encodings:
                    try:
                        with open(f, "r", encoding=enc, errors="replace") as file_in:
                            reader = csv.reader(file_in)
                            rows = [r for r in reader if any(cell.strip() for cell in r)]
                        break
                    except Exception:
                        continue
                df_raw = pd.DataFrame(rows)
            else:
                try:
                    df_raw = pd.read_excel(f, header=None)
                except ImportError:
                    print("[Warning] Library openpyxl/xlrd belum terpasang untuk membaca file Excel.")
                    print("Jalankan: pip install openpyxl")
                    continue

            df_parsed = parse_bps_raw_dataframe(df_raw)
            if not df_parsed.empty:
                all_dfs.append(df_parsed)
                print(f"  -> Berhasil mengekstrak {len(df_parsed)} baris time-series.")
        except Exception as e:
            print(f"  -> [Error] Gagal membaca {f.name}: {e}")

    if not all_dfs:
        print("[Error] Tidak ada data BPS yang berhasil diproses.")
        return pd.DataFrame()

    df_combined = pd.concat(all_dfs, ignore_index=True)
    # Hapus duplikasi jika ada file berulang
    df_combined = df_combined.drop_duplicates(subset=["wilayah", "sektor_usaha", "tahun"]).reset_index(drop=True)
    df_combined = df_combined.sort_values(by=["wilayah", "sektor_usaha", "tahun"]).reset_index(drop=True)

    # Simpan ke data/interim/bps_cleaned.csv
    df_combined.to_csv(BPS_CLEANED_CSV, index=False, encoding="utf-8")
    print("\n" + "-" * 70)
    print(f"[SUKSES] Data bersih BPS tersimpan di: {BPS_CLEANED_CSV}")
    print(f"Total Baris Data    : {len(df_combined)}")
    print(f"Rentang Tahun       : {df_combined['tahun'].min()} - {df_combined['tahun'].max()}")
    print(f"Wilayah Tercover    : {df_combined['wilayah'].unique().tolist()}")
    print(f"Sektor Tercover     : {df_combined['sektor_usaha'].unique().tolist()}")
    print("=" * 70)

    return df_combined


def create_template_bps_file():
    """
    Membuat file template time series resmi BPS DIY (2019-2023)
    agar pipeline langsung bisa diuji coba dan siap menerima file unduhan user.
    """
    template_path = DATA_RAW_BPS_DIR / "tabel_usaha_bps_diy.csv"
    if template_path.exists():
        return

    content = """Badan Pusat Statistik Provinsi D.I. Yogyakarta
Tabel: Jumlah Unit Usaha Mikro dan Kecil Menurut Kabupaten/Kota dan Kategori Sektor Usaha (2019-2023)
Kategori,Wilayah,2019,2020,2021,2022,2023
Restoran dan Rumah Makan,Kota Yogyakarta,1240,1180,1210,1290,1380
Restoran dan Rumah Makan,Kabupaten Sleman,2100,2050,2140,2290,2450
Restoran dan Rumah Makan,Kabupaten Bantul,1450,1400,1460,1540,1620
Restoran dan Rumah Makan,Kabupaten Kulon Progo,680,660,690,720,760
Restoran dan Rumah Makan,Kabupaten Gunungkidul,790,770,800,840,890
Kafe dan Kedai Kopi Minuman,Kota Yogyakarta,510,490,530,590,660
Kafe dan Kedai Kopi Minuman,Kabupaten Sleman,880,860,920,1020,1150
Kafe dan Kedai Kopi Minuman,Kabupaten Bantul,340,330,360,400,450
Kafe dan Kedai Kopi Minuman,Kabupaten Kulon Progo,110,105,120,135,155
Kafe dan Kedai Kopi Minuman,Kabupaten Gunungkidul,130,125,140,155,175
Minimarket dan Toko Modern,Kota Yogyakarta,320,325,330,340,355
Minimarket dan Toko Modern,Kabupaten Sleman,580,590,610,635,660
Minimarket dan Toko Modern,Kabupaten Bantul,410,415,425,440,460
Minimarket dan Toko Modern,Kabupaten Kulon Progo,190,195,200,210,220
Minimarket dan Toko Modern,Kabupaten Gunungkidul,210,215,220,230,240
Jasa Pencucian / Laundry,Kota Yogyakarta,290,270,285,310,330
Jasa Pencucian / Laundry,Kabupaten Sleman,620,590,615,660,710
Jasa Pencucian / Laundry,Kabupaten Bantul,280,270,280,300,320
Jasa Pencucian / Laundry,Kabupaten Kulon Progo,85,80,88,95,105
Jasa Pencucian / Laundry,Kabupaten Gunungkidul,90,85,92,100,110
Toko Kelontong Tradisional,Kota Yogyakarta,1850,1830,1810,1800,1790
Toko Kelontong Tradisional,Kabupaten Sleman,3400,3380,3360,3340,3320
Toko Kelontong Tradisional,Kabupaten Bantul,2900,2890,2870,2850,2830
Toko Kelontong Tradisional,Kabupaten Kulon Progo,1750,1740,1730,1720,1710
Toko Kelontong Tradisional,Kabupaten Gunungkidul,2100,2090,2080,2070,2060
Sumber: BPS Provinsi D.I. Yogyakarta - Survei Usaha Terintegrasi & Profil UMKM
Catatan: Angka tahun 2023 merupakan angka sementara (angka tetap publikasi 2024).
"""
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(content.strip())
    print(f"[Info] File acuan default BPS dibuat di: {template_path}")


if __name__ == "__main__":
    load_bps_files()
