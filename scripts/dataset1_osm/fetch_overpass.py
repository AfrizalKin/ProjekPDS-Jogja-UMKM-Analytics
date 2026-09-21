"""
Modul Fetcher Overpass API untuk Dataset 1 OSM
Projek PDS - Rekomendasi Kelayakan Usaha UMKM
"""

import json
import time
import logging
from pathlib import Path
from typing import Dict, Optional, Tuple
import requests

from .config import (
    OVERPASS_ENDPOINT,
    OVERPASS_ENDPOINTS,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    SLEEP_BETWEEN_REQUESTS,
    USER_AGENT,
    DATA_RAW_OSM_DIR,
    OUTPUTS_LOGS_DIR
)

# Inisialisasi Logger
log_file = OUTPUTS_LOGS_DIR / "fetch_errors.log"
logger = logging.getLogger("FetchOverpass")
logger.setLevel(logging.INFO)

# Handler untuk file log khusus error & info
if not logger.handlers:
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    fh.setFormatter(formatter)
    logger.addHandler(fh)


def build_overpass_query(
    nama_query: str,
    tag_key: str,
    tag_value: str,
    admin_level: str = "5",
    bbox: Optional[Tuple[float, float, float, float]] = None,
    timeout: int = REQUEST_TIMEOUT
) -> str:
    """
    Membangun query Overpass QL secara dinamis berdasarkan batas wilayah administratif
    dan tag OSM (node & way dengan out center). Jika bbox diberikan, ditambahkan
    sebagai filter koordinat untuk mencegah HTTP 504 Gateway Timeout pada server Overpass.

    Args:
        nama_query: Nama wilayah administratif di OSM (misal: 'Sleman', 'Kota Yogyakarta')
        tag_key: Kunci tag OSM (misal: 'amenity', 'shop')
        tag_value: Nilai tag OSM (misal: 'restaurant', 'cafe', 'convenience')
        admin_level: Tingkat wilayah administratif di OSM (default: '5' untuk Kab/Kota DIY)
        bbox: Opsional bounding box (min_lat, min_lon, max_lat, max_lon)
        timeout: Batas waktu timeout server dalam detik

    Returns:
        String Overpass QL
    """
    if bbox:
        s, w, n, e = bbox
        bbox_filter = f"({s}, {w}, {n}, {e})"
    else:
        bbox_filter = ""

    query = f"""[out:json][timeout:{timeout}];
area["name"="{nama_query}"]["admin_level"="{admin_level}"]->.searchArea;
(
  node["{tag_key}"="{tag_value}"](area.searchArea){bbox_filter};
  way["{tag_key}"="{tag_value}"](area.searchArea){bbox_filter};
);
out center;
"""
    return query


def build_bbox_fallback_query(
    bbox: Tuple[float, float, float, float],
    tag_key: str,
    tag_value: str,
    timeout: int = REQUEST_TIMEOUT
) -> str:
    """
    Membangun query murni berbasis Bounding Box (BBox) sebagai fallback jika
    query area relasi administratif Overpass tidak mengembalikan hasil.
    """
    s, w, n, e = bbox
    query = f"""[out:json][timeout:{timeout}];
(
  node["{tag_key}"="{tag_value}"]({s}, {w}, {n}, {e});
  way["{tag_key}"="{tag_value}"]({s}, {w}, {n}, {e});
);
out center;
"""
    return query


def fetch_overpass_data(
    wilayah_id: str,
    nama_wilayah_query: str,
    kategori_id: str,
    tag_key: str,
    tag_value: str,
    admin_level: str = "5",
    bbox: Optional[Tuple[float, float, float, float]] = None,
    save_raw: bool = True
) -> Tuple[bool, Optional[Dict], str]:
    """
    Mengirimkan request ke Overpass API dengan mekanisme multi-mirror failover,
    retry exponential backoff, optimasi BBox, dan fallback.

    Args:
        wilayah_id: Identifier ringkas wilayah (misal: 'sleman')
        nama_wilayah_query: Nama untuk query area OSM (misal: 'Sleman')
        kategori_id: Identifier kategori (misal: 'restaurant')
        tag_key: Key tag OSM (misal: 'amenity')
        tag_value: Value tag OSM (misal: 'restaurant')
        admin_level: Level admin di OSM (default: '5')
        bbox: Bounding box wilayah (min_lat, min_lon, max_lat, max_lon)
        save_raw: Apakah menyimpan langsung ke file JSON mentah

    Returns:
        Tuple (status_sukses: bool, data_json: Optional[Dict], pesan: str)
    """
    query = build_overpass_query(
        nama_query=nama_wilayah_query,
        tag_key=tag_key,
        tag_value=tag_value,
        admin_level=admin_level,
        bbox=bbox,
        timeout=REQUEST_TIMEOUT
    )

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    endpoints = OVERPASS_ENDPOINTS if OVERPASS_ENDPOINTS else [OVERPASS_ENDPOINT]
    last_error = ""

    for attempt in range(1, MAX_RETRIES + 1):
        # Rotasi endpoint jika percobaan sebelumnya gagal
        endpoint = endpoints[(attempt - 1) % len(endpoints)]

        try:
            response = requests.post(
                endpoint,
                data={"data": query},
                headers=headers,
                timeout=REQUEST_TIMEOUT + 15
            )

            # Jeda sopan agar tidak membebani server publik Overpass
            time.sleep(SLEEP_BETWEEN_REQUESTS)

            if response.status_code == 200:
                data = response.json()
                total_elements = len(data.get("elements", []))

                # Jika area query mengembalikan 0 tapi BBox tersedia, coba fallback BBox
                if total_elements == 0 and bbox:
                    logger.info(f"[{wilayah_id} x {kategori_id}] Hasil area kosong, mencoba fallback pure BBox...")
                    fb_query = build_bbox_fallback_query(bbox, tag_key, tag_value, timeout=REQUEST_TIMEOUT)
                    fb_res = requests.post(
                        endpoint,
                        data={"data": fb_query},
                        headers=headers,
                        timeout=REQUEST_TIMEOUT + 15
                    )
                    if fb_res.status_code == 200:
                        fb_data = fb_res.json()
                        fb_elements = len(fb_data.get("elements", []))
                        if fb_elements > 0:
                            data = fb_data
                            total_elements = fb_elements
                            logger.info(f"[{wilayah_id} x {kategori_id}] Fallback BBox berhasil ({total_elements} POI).")

                if save_raw:
                    filename = f"{wilayah_id}_{kategori_id}.json"
                    filepath = DATA_RAW_OSM_DIR / filename
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

                return True, data, f"Sukses ({total_elements} POI)"

            elif response.status_code == 429:
                wait_time = RETRY_DELAY * attempt
                last_error = f"HTTP 429 Too Many Requests ({endpoint}). Menunggu {wait_time} detik..."
                logger.warning(f"[{wilayah_id} x {kategori_id}] {last_error} (Percobaan {attempt}/{MAX_RETRIES})")
                time.sleep(wait_time)

            elif response.status_code in [500, 502, 503, 504]:
                last_error = f"HTTP {response.status_code} Gateway/Server Error ({endpoint})."
                logger.warning(f"[{wilayah_id} x {kategori_id}] {last_error} (Percobaan {attempt}/{MAX_RETRIES})")
                if bbox:
                    logger.info(f"[{wilayah_id} x {kategori_id}] Mencoba fallback BBox akibat HTTP {response.status_code}...")
                    fb_query = build_bbox_fallback_query(bbox, tag_key, tag_value, timeout=REQUEST_TIMEOUT)
                    try:
                        time.sleep(2.0)
                        fb_res = requests.post(endpoint, data={"data": fb_query}, headers=headers, timeout=REQUEST_TIMEOUT + 10)
                        if fb_res.status_code == 200:
                            fb_data = fb_res.json()
                            fb_elems = len(fb_data.get("elements", []))
                            if save_raw:
                                filepath = DATA_RAW_OSM_DIR / f"{wilayah_id}_{kategori_id}.json"
                                with open(filepath, "w", encoding="utf-8") as f:
                                    json.dump(fb_data, f, ensure_ascii=False, indent=2)
                            logger.info(f"[{wilayah_id} x {kategori_id}] Fallback BBox sukses ({fb_elems} POI).")
                            return True, fb_data, f"Sukses via BBox ({fb_elems} POI)"
                    except Exception as fb_err:
                        logger.warning(f"[{wilayah_id} x {kategori_id}] Fallback BBox error: {fb_err}")
                time.sleep(RETRY_DELAY)

            else:
                last_error = f"HTTP Error {response.status_code} ({endpoint}): {response.text[:200]}"
                logger.error(f"[{wilayah_id} x {kategori_id}] {last_error}")
                time.sleep(RETRY_DELAY)

        except requests.exceptions.Timeout:
            last_error = f"Request Timeout setelah {REQUEST_TIMEOUT}s ({endpoint})."
            logger.warning(f"[{wilayah_id} x {kategori_id}] {last_error} (Percobaan {attempt}/{MAX_RETRIES})")
            if bbox:
                logger.info(f"[{wilayah_id} x {kategori_id}] Mencoba fallback BBox akibat timeout...")
                fb_query = build_bbox_fallback_query(bbox, tag_key, tag_value, timeout=REQUEST_TIMEOUT)
                try:
                    time.sleep(2.0)
                    fb_res = requests.post(endpoint, data={"data": fb_query}, headers=headers, timeout=REQUEST_TIMEOUT + 10)
                    if fb_res.status_code == 200:
                        fb_data = fb_res.json()
                        fb_elems = len(fb_data.get("elements", []))
                        if save_raw:
                            filepath = DATA_RAW_OSM_DIR / f"{wilayah_id}_{kategori_id}.json"
                            with open(filepath, "w", encoding="utf-8") as f:
                                json.dump(fb_data, f, ensure_ascii=False, indent=2)
                        logger.info(f"[{wilayah_id} x {kategori_id}] Fallback BBox sukses ({fb_elems} POI).")
                        return True, fb_data, f"Sukses via BBox ({fb_elems} POI)"
                except Exception as fb_err:
                    logger.warning(f"[{wilayah_id} x {kategori_id}] Fallback BBox error: {fb_err}")
            time.sleep(RETRY_DELAY)

        except requests.exceptions.RequestException as e:
            last_error = f"Network Exception ({endpoint}): {str(e)}"
            logger.error(f"[{wilayah_id} x {kategori_id}] {last_error} (Percobaan {attempt}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)

    # Catat error permanen setelah percobaan habis
    msg_gagal = f"Gagal mengambil data untuk {wilayah_id} x {kategori_id}. Alasan: {last_error}"
    logger.error(msg_gagal)
    return False, None, msg_gagal
