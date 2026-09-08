"""
Grid Sampling Generator untuk Membagi Area Query Overpass API.
Projek PDS - UMKM Recommender
"""

from typing import List, Tuple, Dict
import numpy as np


def create_bbox_grid(
    bbox: Tuple[float, float, float, float], 
    n_rows: int = 2, 
    n_cols: int = 2
) -> List[Dict[str, any]]:
    """
    Membagi sebuah bounding box menjadi n_rows x n_cols sub-bounding box (grid).
    Berguna untuk menghindari HTTP 504 Gateway Timeout dari Overpass API
    pada wilayah padat penduduk.

    Args:
        bbox: Tuple (south, west, north, east) / (min_lat, min_lon, max_lat, max_lon)
        n_rows: Jumlah baris pembagian latitude
        n_cols: Jumlah kolom pembagian longitude

    Returns:
        List of dict berisi informasi sub-bbox dan koordinatnya:
        [
            {
                "grid_id": "grid_0_0",
                "bbox": (south, west, north, east),
                "center": (lat, lon)
            },
            ...
        ]
    """
    min_lat, min_lon, max_lat, max_lon = bbox

    lats = np.linspace(min_lat, max_lat, n_rows + 1)
    lons = np.linspace(min_lon, max_lon, n_cols + 1)

    grid_cells = []
    cell_idx = 0

    for i in range(n_rows):
        for j in range(n_cols):
            s = round(float(lats[i]), 6)
            n = round(float(lats[i + 1]), 6)
            w = round(float(lons[j]), 6)
            e = round(float(lons[j + 1]), 6)

            grid_cells.append({
                "grid_id": f"cell_{i}_{j}",
                "index": cell_idx,
                "bbox": (s, w, n, e),
                "center": (round((s + n) / 2, 6), round((w + e) / 2, 6))
            })
            cell_idx += 1

    return grid_cells


def create_step_grid(
    bbox: Tuple[float, float, float, float], 
    step_lat: float = 0.05, 
    step_lon: float = 0.05
) -> List[Dict[str, any]]:
    """
    Membagi bounding box berdasarkan ukuran derajat step (sekitar 0.05 deg ~ 5.5 km).
    """
    min_lat, min_lon, max_lat, max_lon = bbox
    
    n_rows = max(1, int(np.ceil((max_lat - min_lat) / step_lat)))
    n_cols = max(1, int(np.ceil((max_lon - min_lon) / step_lon)))

    return create_bbox_grid(bbox, n_rows=n_rows, n_cols=n_cols)


if __name__ == "__main__":
    # Test sederhana
    test_bbox = (-6.9700, 107.5400, -6.8500, 107.7200) # Kota Bandung
    grids = create_bbox_grid(test_bbox, n_rows=2, n_cols=2)
    print(f"Total grid dibuat: {len(grids)}")
    for g in grids:
        print(f"[{g['grid_id']}] Bbox: {g['bbox']}, Center: {g['center']}")
