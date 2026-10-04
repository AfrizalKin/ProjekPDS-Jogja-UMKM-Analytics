"""Konfigurasi prototipe: path berkas, label tampilan, dan aturan tetap.

Tidak ada angka hasil analisis di sini; semua angka dibaca dari CSV/metadata.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PROTOTYPE_DIR = ROOT / "prototype"

# Agar paket `models` dapat dimuat via importlib (nama berkas diawali angka)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

HASIL_DIR = ROOT / "outputs" / "hasil"
CLEANED_DIR = ROOT / "data" / "cleaned"

BERKAS = {
    "skoring": HASIL_DIR / "hasil_skoring_sektor.csv",
    "cluster": HASIL_DIR / "hasil_clustering_wilayah.csv",
    "forecast": HASIL_DIR / "hasil_forecasting_sektor.csv",
    "kompetitor": CLEANED_DIR / "kompetitor_per_wilayah.csv",
    "ekonomi": CLEANED_DIR / "kondisi_ekonomi_wilayah.csv",
    "sewa": CLEANED_DIR / "biaya_operasional.csv",
    "umkm": CLEANED_DIR / "umkm_sibakul.csv",
    "metadata": CLEANED_DIR / "metadata_data.json",
}

CSS_PATH = PROTOTYPE_DIR / "assets" / "style.css"

NAMA_APLIKASI = "UMKM Recommender"
SUBJUDUL_APLIKASI = "D.I. YOGYAKARTA"

PERINGATAN = "Hasil bersifat alat bantu pertimbangan, bukan jaminan keberhasilan usaha."

# Urutan menu: (kunci, judul, berkas halaman, ikon Material)
MENU = [
    ("beranda", "Beranda", "halaman/1_beranda.py", ":material/dashboard:"),
    ("skoring", "Skoring Kelayakan", "halaman/2_skoring.py", ":material/fact_check:"),
    ("peta_klaster", "Peta dan Klaster", "halaman/3_peta_klaster.py", ":material/map:"),
    ("forecasting", "Forecasting Tren", "halaman/4_forecasting.py", ":material/trending_up:"),
    ("rekomendasi", "Rekomendasi", "halaman/5_rekomendasi.py", ":material/recommend:"),
]

# Ambang kategori skor (aturan Pilar 1)
AMBANG_LAYAK = 70
AMBANG_CUKUP = 50

KATEGORI_URUT = ["Layak", "Cukup Layak", "Kurang Layak"]

# Warna dan ikon status (selalu dipasangkan dengan teks)
KATEGORI_STYLE = {
    "Layak": {"warna": "#1E8E5A", "bg": "#EBF7F0", "border": "#C2E7D2", "ikon": "✔"},
    "Cukup Layak": {"warna": "#966B00", "bg": "#FDF8E8", "border": "#F7E5A9", "ikon": "!"},
    "Kurang Layak": {"warna": "#C8453B", "bg": "#FDF1F0", "border": "#F8CECB", "ikon": "✖"},
    # Status anggaran memakai warna yang sama
    "Mencukupi": {"warna": "#1E8E5A", "bg": "#EBF7F0", "border": "#C2E7D2", "ikon": "✔"},
    "Tidak terjangkau": {"warna": "#C8453B", "bg": "#FDF1F0", "border": "#F8CECB", "ikon": "✖"},
}

# Warna seri per ID sektor
WARNA_SEKTOR = {
    "cafe": "#17a398",
    "restaurant": "#e4572e",
    "convenience": "#2e86ab",
    "laundry": "#7b5ea7",
    "grocery": "#F2A33A",
}

# Warna klaster menurut cluster_label (bukan nomor klaster); cadangan bila label baru
WARNA_KLASTER = {
    "Pasar Padat & Biaya Tinggi": "#e4572e",
    "Pasar Berkembang & Biaya Menengah": "#F2A33A",
    "Pasar Perintis & Biaya Terjangkau": "#17a398",
}
WARNA_KLASTER_CADANGAN = ["#7b5ea7", "#2e86ab", "#8b5e3c", "#5B6B76"]
