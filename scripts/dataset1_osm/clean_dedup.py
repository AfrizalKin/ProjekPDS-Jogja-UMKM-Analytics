"""
Modul Pembersihan, Parsing, dan Deduplikasi Data Mentah OSM
Projek PDS - Rekomendasi Kelayakan Usaha UMKM
"""

import json
import sys
from pathlib import Path
from typing import List, Dict
import pandas as pd

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

from scripts.dataset1_osm.config import (
    DATA_RAW_OSM_DIR,
    DATA_PROCESSED_DIR
)


def extract_poi_from_json(json_path: Path) -> List[Dict]:
    """
    Mengekstrak data POI dari sebuah berkas JSON Overpass API mentah.
    Nama file diasumsikan berformat: {wilayah}_{kategori}.json
    """
    stem = json_path.stem
    parts = stem.split("_", 1)
    wilayah_id = parts[0] if len(parts) > 0 else "unknown"
    kategori_id = parts[1] if len(parts) > 1 else "unknown"

    with open(json_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print(f"[Warning] Gagal membaca JSON: {json_path}")
            return []

    elements = data.get("elements", [])
    records = []

    for el in elements:
        el_type = el.get("type")
        el_id = el.get("id")

        # Koordinat: node memiliki 'lat' & 'lon', way memiliki 'center' jika diminta out center
        lat = el.get("lat")
        lon = el.get("lon")
        if lat is None or lon is None:
            center = el.get("center", {})
            lat = center.get("lat")
            lon = center.get("lon")

        # Lewati jika tidak ada koordinat yang valid
        if lat is None or lon is None:
            continue

        tags = el.get("tags", {})
        nama_tempat = tags.get("name", "Tanpa Nama").strip()

        records.append({
            "osm_id": f"{el_type}_{el_id}",
            "nama_tempat": nama_tempat,
            "lat": float(lat),
            "lon": float(lon),
            "kategori": kategori_id,
            "wilayah": wilayah_id
        })

    return records


def clean_and_deduplicate() -> pd.DataFrame:
    """
    Membaca semua file JSON di data/raw/osm/, mem-parsing, menghapus duplikasi,
    dan menyimpan hasilnya ke data/processed/kompetitor_per_wilayah.csv.
    """
    json_files = list(DATA_RAW_OSM_DIR.glob("*.json"))

    if not json_files:
        print(f"[Perhatian] Tidak ada file JSON ditemukan di: {DATA_RAW_OSM_DIR}")
        print("Silakan jalankan main.py terlebih dahulu untuk mengambil data.")
        return pd.DataFrame()

    print(f"Membaca {len(json_files)} file JSON dari {DATA_RAW_OSM_DIR}...")
    all_records = []
    for jf in json_files:
        records = extract_poi_from_json(jf)
        all_records.extend(records)

    if not all_records:
        print("[Perhatian] Tidak ada POI yang berhasil diekstrak dari file JSON.")
        return pd.DataFrame()

    df = pd.DataFrame(all_records)
    total_awal = len(df)

    # 1. Hapus duplikat berdasarkan osm_id (dan kategori)
    df_dedup = df.drop_duplicates(subset=["osm_id", "kategori"]).copy()
    total_dedup_id = len(df_dedup)

    # 2. Hapus duplikat spasial (koordinat sama persis + nama tempat sama)
    df_dedup["lat_rounded"] = df_dedup["lat"].round(5)
    df_dedup["lon_rounded"] = df_dedup["lon"].round(5)

    mask_named = df_dedup["nama_tempat"] != "Tanpa Nama"
    named_df = df_dedup[mask_named].drop_duplicates(
        subset=["nama_tempat", "lat_rounded", "lon_rounded", "kategori"]
    )
    unnamed_df = df_dedup[~mask_named].drop_duplicates(
        subset=["lat_rounded", "lon_rounded", "kategori"]
    )

    df_final = pd.concat([named_df, unnamed_df], ignore_index=True)
    total_final = len(df_final)

    # Pilih kolom final sesuai spesifikasi: nama_tempat, lat, lon, kategori, wilayah
    kolom_final = ["nama_tempat", "lat", "lon", "kategori", "wilayah"]
    df_output = df_final[kolom_final].copy()

    output_path = DATA_PROCESSED_DIR / "kompetitor_per_wilayah.csv"
    df_output.to_csv(output_path, index=False, encoding="utf-8")

    print("\n" + "=" * 70)
    print("HASIL PEMBERSIHAN & DEDUPLIKASI DATASET 1")
    print("=" * 70)
    print(f"Total POI Awal                 : {total_awal}")
    print(f"Setelah Dedup ID               : {total_dedup_id} (-{total_awal - total_dedup_id})")
    print(f"Total Bersih Final             : {total_final} (-{total_dedup_id - total_final})")
    print(f"File Hasil Disimpan ke         : {output_path}")
    print("\nRekap Jumlah Kompetitor per Kategori:")
    print(df_output["kategori"].value_counts().to_string())
    print("\nRekap Jumlah Kompetitor per Wilayah:")
    print(df_output["wilayah"].value_counts().to_string())
    print("=" * 70)

    return df_output


if __name__ == "__main__":
    clean_and_deduplicate()
