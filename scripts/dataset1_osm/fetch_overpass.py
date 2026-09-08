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
    admin_level: str = "6",
    timeout: int = REQUEST_TIMEOUT
) -> str:
    """
    Membangun query Overpass QL secara dinamis berdasarkan batas wilayah administratif
    dan tag OSM (node & way dengan out center).

    Args:
        nama_query: Nama wilayah administratif di OSM (misal: 'Sleman', 'Kota Yogyakarta')
        tag_key: Kunci tag OSM (misal: 'amenity', 'shop')
        tag_value: Nilai tag OSM (misal: 'restaurant', 'cafe', 'convenience')
        admin_level: Tingkat wilayah administratif di OSM (default: '6' untuk Kabupaten/Kota)
        timeout: Batas waktu timeout server dalam detik

    Returns:
        String Overpass QL
    """
    query = f"""[out:json][timeout:{timeout}];
area["name"="{nama_query}"]["admin_level"="{admin_level}"]->.searchArea;
(
  node["{tag_key}"="{tag_value}"](area.searchArea);
  way["{tag_key}"="{tag_value}"](area.searchArea);
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
    admin_level: str = "6",
    save_raw: bool = True
) -> Tuple[bool, Optional[Dict], str]:
    """
    Mengirimkan request ke Overpass API dengan mekanisme retry dan logging kegagalan.

    Args:
        wilayah_id: Identifier ringkas wilayah (misal: 'sleman')
        nama_wilayah_query: Nama untuk query area OSM (misal: 'Sleman')
        kategori_id: Identifier kategori (misal: 'restaurant')
        tag_key: Key tag OSM (misal: 'amenity')
        tag_value: Value tag OSM (misal: 'restaurant')
        admin_level: Level admin di OSM (default: '6')
        save_raw: Apakah menyimpan langsung ke file JSON mentah

    Returns:
        Tuple (status_sukses: bool, data_json: Optional[Dict], pesan: str)
    """
    query = build_overpass_query(
        nama_query=nama_wilayah_query,
        tag_key=tag_key,
        tag_value=tag_value,
        admin_level=admin_level
    )

    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    last_error = ""

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = requests.post(
                OVERPASS_ENDPOINT,
                data={"data": query},
                headers=headers,
                timeout=REQUEST_TIMEOUT + 15
            )

            # Jeda sopan agar tidak membebani server publik Overpass
            time.sleep(SLEEP_BETWEEN_REQUESTS)

            if response.status_code == 200:
                data = response.json()
                total_elements = len(data.get("elements", []))

                if save_raw:
                    filename = f"{wilayah_id}_{kategori_id}.json"
                    filepath = DATA_RAW_OSM_DIR / filename
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=2)

                return True, data, f"Sukses ({total_elements} POI)"

            elif response.status_code == 429:
                last_error = f"HTTP 429 Too Many Requests (Rate Limit). Menunggu {RETRY_DELAY * attempt} detik..."
                logger.warning(f"[{wilayah_id} x {kategori_id}] {last_error} (Percobaan {attempt}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY * attempt)

            elif response.status_code in [500, 502, 503, 504]:
                last_error = f"HTTP {response.status_code} Gateway/Server Error."
                logger.warning(f"[{wilayah_id} x {kategori_id}] {last_error} (Percobaan {attempt}/{MAX_RETRIES})")
                time.sleep(RETRY_DELAY)

            else:
                last_error = f"HTTP Error {response.status_code}: {response.text[:200]}"
                logger.error(f"[{wilayah_id} x {kategori_id}] {last_error}")
                break

        except requests.exceptions.Timeout:
            last_error = f"Request Timeout setelah {REQUEST_TIMEOUT} detik."
            logger.warning(f"[{wilayah_id} x {kategori_id}] {last_error} (Percobaan {attempt}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)

        except requests.exceptions.RequestException as e:
            last_error = f"Network Exception: {str(e)}"
            logger.error(f"[{wilayah_id} x {kategori_id}] {last_error} (Percobaan {attempt}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)

    # Catat error permanen setelah percobaan habis
    msg_gagal = f"Gagal mengambil data untuk {wilayah_id} x {kategori_id}. Alasan: {last_error}"
    logger.error(msg_gagal)
    return False, None, msg_gagal
