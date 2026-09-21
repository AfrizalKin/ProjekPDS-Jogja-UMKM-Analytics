"""
Modul Grid Sampling
Projek PDS - Rekomendasi Kelayakan Usaha UMKM

Modul ini menyediakan fungsi untuk membagi area studi (Bounding Box)
menjadi grid-grid yang lebih kecil jika wilayah target sangat luas
atau padat POI.
"""

from typing import List, Dict, Tuple


def create_bbox_grid(
    bbox: Tuple[float, float, float, float],
    n_rows: int = 2,
    n_cols: int = 2
) -> List[Dict]:
    """
    Membagi sebuah Bounding Box menjadi beberapa sel sub-grid yang lebih kecil.

    Args:
        bbox: Tuple (min_lat, min_lon, max_lat, max_lon)
        n_rows: Jumlah pembagian baris (arah latitude)
        n_cols: Jumlah pembagian kolom (arah longitude)

    Returns:
        Daftar dictionary berisi informasi tiap sel:
        [{'grid_id': 'r0_c0', 'bbox': (s, w, n, e)}, ...]
    """
    min_lat, min_lon, max_lat, max_lon = bbox

    lat_step = (max_lat - min_lat) / n_rows
    lon_step = (max_lon - min_lon) / n_cols

    cells = []
    for r in range(n_rows):
        cell_min_lat = min_lat + r * lat_step
        cell_max_lat = min_lat + (r + 1) * lat_step

        for c in range(n_cols):
            cell_min_lon = min_lon + c * lon_step
            cell_max_lon = min_lon + (c + 1) * lon_step

            cells.append({
                "grid_id": f"r{r}_c{c}",
                "bbox": (
                    round(cell_min_lat, 6),
                    round(cell_min_lon, 6),
                    round(cell_max_lat, 6),
                    round(cell_max_lon, 6)
                )
            })

    return cells
