"""
Modul Pengambil Data Google Trends Opsional (Dataset 4)
Projek PDS - Sistem Rekomendasi Kelayakan Usaha UMKM

Modul ini mengambil tren minat pencarian (Interest Over Time) sebagai
sinyal tambahan (leading indicator).
Karakteristik penting:
1. Penuh try-except & retry logic (karena pytrends rawan HTTP 429).
2. Jeda (sleep) minimal 12 detik antar keyword.
3. Jika gagal setelah 3x percobaan, keyword dilewati (skip) & dicatat ke log,
   TIDAK menghentikan pipeline.
4. Granularitas data: Nasional (geo='ID') atau Provinsi DIY.
"""

import sys
import time
from pathlib import Path
from datetime import datetime
import pandas as pd

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset4_tren.config import (
    TRENDS_RAW_CSV,
    LOG_TRENDS_ERROR,
    TRENDS_CONFIG,
    TRENDS_KEYWORDS
)


def log_error(pesan: str):
    """Mencatat pesan error atau warning ke file log."""
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_TRENDS_ERROR, "a", encoding="utf-8") as f:
        f.write(f"[{waktu}] {pesan}\n")


def fetch_keyword_interest(pytrends_client, keyword: str, sektor: str, geo: str, timeframe: str) -> pd.DataFrame:
    """
    Mengambil interest over time untuk 1 keyword dengan mekanisme retry 3 kali.
    """
    max_retries = TRENDS_CONFIG.get("max_retries", 3)
    backoff = TRENDS_CONFIG.get("retry_backoff", 15)

    for attempt in range(1, max_retries + 1):
        try:
            print(f"  [Attempt {attempt}/{max_retries}] Mengambil data trends untuk: '{keyword}'...")
            pytrends_client.build_payload(
                kw_list=[keyword],
                timeframe=timeframe,
                geo=geo
            )
            df_interest = pytrends_client.interest_over_time()

            if df_interest is not None and not df_interest.empty:
                df_res = df_interest.reset_index()
                # Kolom biasanya: 'date', keyword, 'isPartial'
                date_col = "date" if "date" in df_res.columns else df_res.columns[0]

                records = []
                for _, row in df_res.iterrows():
                    records.append({
                        "sektor_usaha": sektor,
                        "keyword": keyword,
                        "tanggal": pd.to_datetime(row[date_col]).strftime("%Y-%m-%d"),
                        "tahun": pd.to_datetime(row[date_col]).year,
                        "trend_index": float(row[keyword]) if keyword in row else 0.0
                    })
                return pd.DataFrame(records)
            else:
                print(f"  [Warning] Respons kosong untuk keyword '{keyword}'.")
                return pd.DataFrame()

        except Exception as e:
            err_msg = f"Percobaan {attempt} gagal untuk keyword '{keyword}': {e}"
            print(f"  -> {err_msg}")
            log_error(err_msg)

            if attempt < max_retries:
                sleep_time = backoff * attempt
                print(f"  -> Menunggu jeda backoff {sleep_time} detik sebelum retry...")
                time.sleep(sleep_time)

    # Jika semua percobaan habis
    pesan_skip = f"GAGAL TOTAL: Keyword '{keyword}' (sektor: {sektor}) dilewati setelah {max_retries} kali percobaan."
    print(f"  [SKIP] {pesan_skip}")
    log_error(pesan_skip)
    return pd.DataFrame()


def fetch_google_trends() -> pd.DataFrame:
    """
    Menjalankan loop pengambilan data Google Trends untuk daftar keyword di config.py.
    """
    print("=" * 70)
    print("DATASET 4: PENGAMBILAN GOOGLE TRENDS (SINYAL TAMBAHAN OPSIONAL)")
    print("=" * 70)

    # 1. Cek ketersediaan library pytrends
    try:
        from pytrends.request import TrendReq
    except ImportError:
        pesan = "Library 'pytrends' belum terpasang. Lewati pengambilan Google Trends."
        print(f"[INFO] {pesan}")
        print("Jika ingin mengaktifkan Google Trends, jalankan: pip install pytrends")
        log_error(pesan)
        return pd.DataFrame()

    geo = TRENDS_CONFIG.get("geo", "ID")
    timeframe = TRENDS_CONFIG.get("timeframe", "today 5-y")
    sleep_sec = TRENDS_CONFIG.get("sleep_seconds", 12)

    try:
        pytrends = TrendReq(hl="id-ID", tz=420, timeout=(10, 25))
    except Exception as e:
        pesan = f"Gagal inisialisasi TrendReq client: {e}"
        print(f"[Error] {pesan}")
        log_error(pesan)
        return pd.DataFrame()

    all_results = []
    total_kw = len(TRENDS_KEYWORDS)

    for i, item in enumerate(TRENDS_KEYWORDS, 1):
        sektor = item["sektor"]
        kw = item["keyword"]
        print(f"\n({i}/{total_kw}) Memproses sektor: {sektor} -> Keyword: '{kw}'")

        df_kw = fetch_keyword_interest(
            pytrends_client=pytrends,
            keyword=kw,
            sektor=sektor,
            geo=geo,
            timeframe=timeframe
        )

        if not df_kw.empty:
            all_results.append(df_kw)
            print(f"  [Sukses] Berhasil mengambil {len(df_kw)} titik data.")

        # Jeda wajib antar request agar tidak diblokir Google
        if i < total_kw:
            print(f"  Jeda {sleep_sec} detik untuk mencegah rate-limit (HTTP 429)...")
            time.sleep(sleep_sec)

    if all_results:
        df_trends = pd.concat(all_results, ignore_index=True)
        df_trends.to_csv(TRENDS_RAW_CSV, index=False, encoding="utf-8")
        print("\n" + "-" * 70)
        print(f"[SUKSES] Data Google Trends disimpan di: {TRENDS_RAW_CSV}")
        print(f"Total Baris Data : {len(df_trends)}")
        print("=" * 70)
        return df_trends
    else:
        pesan_akhir = "Tidak ada data Google Trends yang berhasil diambil (semua request diskip/gagal)."
        print(f"\n[PERINGATAN] {pesan_akhir}")
        log_error(pesan_akhir)
        print("Catatan: Pipeline tetap akan berjalan normal menggunakan data BPS.")
        print("=" * 70)
        return pd.DataFrame()


if __name__ == "__main__":
    fetch_google_trends()
