# Prototipe UMKM Recommender (Streamlit)

Antarmuka web untuk hasil analisis di `outputs/hasil/` dan `data/cleaned/`.
Aplikasi hanya membaca CSV: tidak ada scraping, pelatihan model, atau basis data.

## Menjalankan

Dari root repo:

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate    |  Linux/macOS: source .venv/bin/activate
pip install -r prototype/requirements.txt
streamlit run prototype/app.py
```

Buka http://localhost:8501.

## Agar teman satu Wi-Fi bisa melihat

```bash
streamlit run prototype/app.py --server.address 0.0.0.0
```

Teman membuka `http://<IP-laptop-Anda>:8501` (IP tampil sebagai "Network URL" di terminal).
Izinkan Python lewat firewall Windows bila diminta. Aplikasi hanya hidup selama terminal terbuka.

## Struktur

| Berkas | Fungsi |
|---|---|
| `app.py` | Titik masuk, navigasi 5 menu |
| `config.py` | Path berkas, label, warna status |
| `core/` | Pemuat data ber-cache dan pemformat angka |
| `components/` | Kartu, lencana, dan grafik Plotly |
| `halaman/` | Satu berkas per menu |
| `assets/style.css` | CSS tambahan di atas tema `.streamlit/config.toml` |

Memperbarui hasil: jalankan `python models/run_all_models.py`, lalu muat ulang halaman.
Keterangan periode data dibaca dari `data/cleaned/metadata_data.json`.
