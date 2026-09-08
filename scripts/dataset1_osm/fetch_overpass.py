"""
Modul Fetcher Data dari Overpass API (OpenStreetMap)
Projek PDS - UMKM Recommender
"""

import json
import time
import logging
from typing import Dict, Tuple, List, Optional
import requests

from .config import (
    OVERPASS_ENDPOINTS,
    DEFAULT_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    USER_AGENT,
    LOG_DIR,
    RAW_DATA_DIR
)

# Inisialisasi logger modul
logger = logging.getLogger("OverpassFetcher")


def build_overpass_query(
    bbox: Tuple[float, float, float, float],
    tag_keys: List[str] = ["amenity", "shop", "craft"],
    timeout: int = DEFAULT_TIMEOUT
) -> str:
    """
    Menyusun query Overpass QL untuk mengekstrak POI UMKM (node dan way dengan out center).

    Args:
        bbox: (south, west, north, east)
        tag_keys: list key tag OSM target
        timeout: waktu timeout query dalam detik

    Returns:
        String query Overpass QL
    """
    s, w, n, e = bbox
    bbox_str = f"{s},{w},{n},{e}"

    # Susun klausa query untuk setiap tag
    statements = []
    for key in tag_keys:
        statements.append(f'node["{key}"]({bbox_str});')
        statements.append(f'way["{key}"]({bbox_str});')

    query_body = "\n  ".join(statements)

    query = f"""[out:json][timeout:{timeout}];
(
  {query_body}
);
out body center;
>;
out skel qt;"""
    return query


def fetch_osm_data(
    query: str,
    endpoints: List[str] = OVERPASS_ENDPOINTS,
    max_retries: int = MAX_RETRIES,
    retry_delay: int = RETRY_DELAY
) -> Optional[Dict]:
    """
    Mengirimkan query ke Overpass API dengan dukungan retry, delay,
    dan fallback endpoint jika terjadi timeout atau error HTTP 429 / 504.

    Args:
        query: Query Overpass QL
        endpoints: List URL Overpass API endpoint
        max_retries: Maksimum percobaan per endpoint
        retry_delay: Waktu tunggu (detik) sebelum mencoba kembali

    Returns:
        Dict JSON response dari Overpass, atau None jika gagal
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    for endpoint in endpoints:
        logger.info(f"Mencoba request ke endpoint: {endpoint}")
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(
                    endpoint,
                    data={"data": query},
                    headers=headers,
                    timeout=DEFAULT_TIMEOUT + 15
                )

                if response.status_code == 200:
                    logger.info(f"Berhasil fetch data dari {endpoint} (Percobaan {attempt})")
                    return response.json()

                elif response.status_code == 429:
                    logger.warning(
                        f"Rate limit terdeteksi (HTTP 429) pada {endpoint}. "
                        f"Tidur selama {retry_delay * attempt} detik..."
                    )
                    time.sleep(retry_delay * attempt)

                elif response.status_code in [500, 502, 503, 504]:
                    logger.warning(
                        f"Server error (HTTP {response.status_code}) pada {endpoint}. "
                        f"Percobaan {attempt}/{max_retries}."
                    )
                    time.sleep(retry_delay)

                else:
                    logger.error(
                        f"HTTP Error {response.status_code} dari {endpoint}: {response.text[:200]}"
                    )
                    break

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout pada {endpoint} (Percobaan {attempt}/{max_retries})")
                time.sleep(retry_delay)
            except requests.exceptions.RequestException as e:
                logger.error(f"Request exception pada {endpoint}: {e}")
                time.sleep(retry_delay)

        logger.warning(f"Gagal setelah {max_retries} percobaan pada {endpoint}. Beralih ke endpoint berikutnya jika ada.")

    logger.error("Semua endpoint Overpass API gagal merespons.")
    return None


def save_raw_response(data: Dict, filename: str) -> Path:
    """
    Menyimpan hasil mentah query Overpass ke format JSON di data/raw/osm/.
    """
    target_path = RAW_DATA_DIR / filename
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info(f"Data raw berhasil disimpan ke: {target_path}")
    return target_path
