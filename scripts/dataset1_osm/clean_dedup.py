"""
Modul Pembersihan, Deduplikasi, dan Standardisasi Data OSM
Projek PDS - UMKM Recommender
"""

import logging
from typing import Dict, List, Optional
import pandas as pd
import numpy as np

from .config import (
    SEKTOR_MAPPING,
    INTERIM_DATA_DIR,
    PROCESSED_DATA_DIR
)

logger = logging.getLogger("CleanDedup")


def parse_osm_elements(elements: List[Dict]) -> pd.DataFrame:
    """
    Mengekstrak informasi penting dari elemen mentah Overpass API (node & way).

    Args:
        elements: list elemen dari respon JSON Overpass

    Returns:
        pd.DataFrame dengan atribut-atribut POI
    """
    records = []

    for el in elements:
        el_type = el.get("type")
        el_id = el.get("id")

        # Ambil koordinat
        lat, lon = None, None
        if el_type == "node":
            lat = el.get("lat")
            lon = el.get("lon")
        elif el_type == "way":
            # Way seringkali memiliki koordinat 'center' jika diminta 'out center'
            center = el.get("center", {})
            lat = center.get("lat")
            lon = center.get("lon")

        # Jika tidak ada koordinat valid, lewati
        if lat is None or lon is None:
            continue

        tags = el.get("tags", {})
        if not tags:
            continue

        name = tags.get("name", "Tanpa Nama").strip()
        amenity = tags.get("amenity")
        shop = tags.get("shop")
        craft = tags.get("craft")

        # Abaikan jika tidak memiliki tag usaha relevan
        if not (amenity or shop or craft):
            continue

        # Ekstrak metadata tambahan
        street = tags.get("addr:street")
        city = tags.get("addr:city")
        phone = tags.get("phone") or tags.get("contact:phone")
        website = tags.get("website") or tags.get("contact:website")
        opening_hours = tags.get("opening_hours")
        brand = tags.get("brand")

        records.append({
            "osm_id": f"{el_type}_{el_id}",
            "raw_id": el_id,
            "osm_type": el_type,
            "latitude": float(lat),
            "longitude": float(lon),
            "nama_usaha": name,
            "amenity": amenity,
            "shop": shop,
            "craft": craft,
            "brand": brand,
            "street": street,
            "city": city,
            "phone": phone,
            "website": website,
            "opening_hours": opening_hours,
        })

    df = pd.DataFrame(records)
    logger.info(f"Berhasil mem-parsing {len(df)} entitas POI mentah.")
    return df


def categorize_umkm(df: pd.DataFrame) -> pd.DataFrame:
    """
    Menentukan kategori primer dan menstandardisasi sektor UMKM.
    """
    if df.empty:
        df["subsektor"] = []
        df["sektor_umkm"] = []
        return df

    def get_subsektor(row):
        # Prioritas: shop -> amenity -> craft
        if pd.notna(row["shop"]):
            return row["shop"]
        if pd.notna(row["amenity"]):
            return row["amenity"]
        if pd.notna(row["craft"]):
            return row["craft"]
        return "unknown"

    df["subsektor"] = df.apply(get_subsektor, axis=1)
    df["sektor_umkm"] = df["subsektor"].map(SEKTOR_MAPPING).fillna("Lainnya / Umum")

    return df


def deduplicate_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Melakukan deduplikasi data:
    1. Berdasarkan osm_id unik (menghilangkan duplikasi akibat pembagian query grid).
    2. Berdasarkan nama usaha dan kedekatan koordinat yang identik.
    """
    initial_count = len(df)
    if initial_count == 0:
        return df

    # Dedup berdasarkan osm_id
    df_dedup = df.drop_duplicates(subset=["osm_id"]).copy()
    step1_count = len(df_dedup)
    logger.info(f"Deduplikasi OSM ID: dari {initial_count} menjadi {step1_count} baris (-{initial_count - step1_count}).")

    # Dedup berdasarkan kesamaan nama (selain 'Tanpa Nama') dan koordinat dibulatkan (~11 meter)
    df_dedup["lat_round4"] = df_dedup["latitude"].round(4)
    df_dedup["lon_round4"] = df_dedup["longitude"].round(4)

    mask_named = df_dedup["nama_usaha"] != "Tanpa Nama"
    named_df = df_dedup[mask_named].drop_duplicates(subset=["nama_usaha", "lat_round4", "lon_round4"])
    unnamed_df = df_dedup[~mask_named]

    final_df = pd.concat([named_df, unnamed_df], ignore_index=True)
    final_df.drop(columns=["lat_round4", "lon_round4"], inplace=True)

    final_count = len(final_df)
    logger.info(f"Deduplikasi Spasial/Nama: dari {step1_count} menjadi {final_count} baris (-{step1_count - final_count}).")
    return final_df


def save_interim_data(df: pd.DataFrame, filename: str) -> str:
    """
    Menyimpan hasil parsing awal ke data/interim/
    """
    path = INTERIM_DATA_DIR / filename
    df.to_csv(path, index=False, encoding="utf-8")
    logger.info(f"Data interim disimpan ke: {path}")
    return str(path)


def save_processed_data(df: pd.DataFrame, filename: str) -> str:
    """
    Menyimpan hasil final siap analisis ke data/processed/
    """
    path = PROCESSED_DATA_DIR / filename
    df.to_csv(path, index=False, encoding="utf-8")
    logger.info(f"Data processed final disimpan ke: {path}")
    return str(path)
