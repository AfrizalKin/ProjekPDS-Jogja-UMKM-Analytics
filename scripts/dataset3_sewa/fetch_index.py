"""
Modul Fetcher Indeks Sewa Properti Komersial (Dataset 3)
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM

Modul ini mengumpulkan data rata-rata/indeks harga sewa properti komersial
(ruang usaha, ruko, kios) per wilayah di D.I. Yogyakarta dari publikasi resmi
laporan riset properti (Bank Indonesia PPKom, Rumah123 Property Flash Report,
dan Indonesia Property Watch).
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional
import pandas as pd
import requests
from bs4 import BeautifulSoup

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset3_sewa.config import (
    RAW_OUTPUT_CSV,
    BENCHMARK_INDEX_DATA
)


def parse_html_property_article(url: str) -> Optional[List[Dict]]:
    """
    Mengurai data ringkasan harga properti dari artikel web statis
    menggunakan requests dan BeautifulSoup.

    Args:
        url: Alamat URL publikasi artikel/laporan riset

    Returns:
        List of dictionaries data sewa atau None jika gagal
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }

    try:
        response = requests.get(url, headers=headers, timeout=20)
        if response.status_code != 200:
            print(f"[Warning] Gagal mengakses {url} (Status: {response.status_code})")
            return None

        soup = BeautifulSoup(response.text, "html.parser")
        # Contoh ekstraksi tabel jika artikel memuat elemen <table>
        tables = soup.find_all("table")
        if tables:
            print(f"[Info] Ditemukan {len(tables)} tabel di halaman artikel.")
            # Dapat di-parse menggunakan pd.read_html
            dfs = pd.read_html(response.text)
            print(f"[Info] Berhasil mengekstrak {len(dfs)} DataFrame dari tabel HTML.")
            return dfs
        return None

    except Exception as e:
        print(f"[Error] Terjadi kesalahan saat membaca URL artikel: {e}")
        return None


def extract_table_from_pdf(pdf_path: Path) -> Optional[pd.DataFrame]:
    """
    Mengekstrak tabel ringkasan indeks harga properti dari berkas laporan PDF
    (seperti Laporan Survei Properti Bank Indonesia atau Whitepaper Pasar Properti).

    Args:
        pdf_path: Path berkas PDF

    Returns:
        DataFrame gabungan tabel dari PDF
    """
    try:
        import pdfplumber
        print(f"[Info] Membaca berkas PDF: {pdf_path}")
        all_rows = []
        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        if any(row):  # abaikan baris kosong
                            all_rows.append(row)

        if all_rows:
            header = all_rows[0]
            df = pd.DataFrame(all_rows[1:], columns=header)
            return df
        return None

    except ImportError:
        print("[Info] Library pdfplumber belum terpasang. Lewati ekstraksi PDF lokal.")
        return None
    except Exception as e:
        print(f"[Error] Gagal membaca PDF: {e}")
        return None


def fetch_official_rental_index() -> pd.DataFrame:
    """
    Mengumpulkan data indeks harga sewa properti komersial per m2 per wilayah
    berdasarkan kompilasi publikasi resmi Bank Indonesia (Survei Perkembangan
    Properti Komersial - Ruang Ritel & Ruko) dan riset indeks harga Rumah123.

    Returns:
        DataFrame dengan kolom: wilayah, harga_per_m2, satuan_waktu, sumber, tahun
    """
    print("=" * 70)
    print("DATASET 3: PENGAMBILAN INDEKS HARGA SEWA PROPERTI KOMERSIAL")
    print("=" * 70)
    print("Mengumpulkan data indeks sewa resmi per wilayah D.I. Yogyakarta...")

    records = []
    for item in BENCHMARK_INDEX_DATA:
        records.append({
            "wilayah": item["wilayah_raw"],
            "harga_per_m2": item["harga_per_m2"],
            "satuan_waktu": item["satuan_waktu"],
            "sumber": item["sumber"],
            "tahun": item["tahun"]
        })

    df = pd.DataFrame(records)

    # Simpan ke data/raw/sewa_index.csv
    df.to_csv(RAW_OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"[Sukses] Data mentah indeks sewa tersimpan di: {RAW_OUTPUT_CSV}")
    print(f"Total Baris Data : {len(df)}")
    print("=" * 70)

    return df


if __name__ == "__main__":
    fetch_official_rental_index()
