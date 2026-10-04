# Catatan Desain (dari Google Stitch)

Sumber: proyek Stitch "UMKM Recommender Dashboard" (`projects/8062756417359735442`).
Berkas di folder ini: `*.jpg` (pratinjau layar, resolusi rendah dari Stitch) dan `html/*.html` (acuan visual saja, tidak dipakai langsung).
Layar tersedia: Beranda (`beranda_dark.jpg`; `beranda_alt.jpg` adalah varian lain tanpa HTML), Skoring Kelayakan, Peta dan Klaster, Forecasting Tren, Rekomendasi.

## Palet (tema gelap, diambil dari konfigurasi Tailwind pada layar Beranda)
| Token | Hex | Pemakaian |
|---|---|---|
| surface | #070d14 | latar halaman |
| sidebar | #0b1118 | latar sidebar |
| surface-container-low | #0d1520 | panel/kartu dasar |
| surface-container | #111c26 | kartu |
| surface-container-high | #162534 | kartu terangkat, input |
| surface-container-highest | #1d2f42 | hover/aktif |
| border-card | #223244 | garis kartu |
| outline-variant | #1e293b | garis sidebar |
| on-surface | #f1f5f9 | teks utama |
| on-surface-variant | #94a3b8 | teks sekunder |
| primary | #4fdbc8 | aksen (teal) |
| primary-container | #14b8a6 | tombol/aksen |
| secondary | #89ceff | aksen biru muda |
| biru navigasi aktif | #3b82f6 / #60a5fa | item menu aktif, angka kunci |
| status Layak | emerald-400 (#34d399) | lencana |
| status Cukup Layak | amber-400 (#fbbf24) | lencana |
| status Kurang Layak | rose-400 (#fb7185) | lencana |
| klaster (peta/skoring) | #17a398, #2e86ab, #7b5ea7, #8b5e3c, #e4572e | seri kategori |

Radius sudut 4px (kartu dan tombol), pil 9999px. Palet "terang" pada tema proyek Stitch (#0E7C86 dst.) TIDAK dipakai: PRD menetapkan tema gelap.

## Tipografi
Inter (semua peran). Judul halaman ~28px semibold, judul kartu ~16-18px semibold, isi 14-15px, label 11-13px uppercase dengan jarak huruf. Angka memakai tabular-nums. Ikon: Material Symbols Outlined.

## Tata letak umum
Sidebar tetap 280px: merek "UMKM Recommender" + "D.I. YOGYAKARTA", label "NAVIGASI ANALISIS", 5 item menu berikon (item aktif: latar biru transparan + garis kiri 4px). Kanvas: judul halaman, paragraf pengantar, kotak info biru, lalu konten.

## Komponen per layar
- **Beranda**: judul + pengantar; kotak info; 3 kartu angka kunci (titik pesaing, wilayah, sektor); 4 kartu fitur dengan tombol ke menu; kotak peringatan satu baris.
- **Skoring Kelayakan**: filter wilayah dan sektor + Reset; kartu ringkasan (rata-rata skor, jumlah kombinasi, kategori terbanyak); diagram batang skor per wilayah/sektor (garis ambang); tabel 25 kombinasi dengan lencana kategori.
- **Peta dan Klaster**: dua tab (Peta Pesaing, Klaster Wilayah); filter wilayah; legenda sektor berwarna dengan jumlah; peta titik; kartu profil wilayah; diagram sebar PCA; kartu klaster.
- **Forecasting Tren**: filter sektor; kartu ringkasan (arah tren, data historis terakhir, proyeksi 2026 + rentang 95%); grafik garis historis + proyeksi + pita; catatan sinyal arah.
- **Rekomendasi**: panel parameter (sektor, wilayah, anggaran); tombol "Lihat Rekomendasi"; dua tab hasil (wilayah spesifik: kartu skor + lencana kategori, klaster, tren, estimasi sewa, status anggaran, peringatan kejenuhan, narasi; semua wilayah: peringkat).

## Isi Stitch yang TIDAK diikuti (tidak sesuai PRD/data)
Angka tulisan tangan (mis. 1.428 unit, +8,4%/thn, 842 kafe, "+12%", skor rata-rata 67,4), model "Holt-Winters & ARIMA", enam sektor dan filter sektor KBLI/industri kreatif, "per kecamatan", tombol Unduh GeoJSON/Ekspor CSV/Sinkronisasi, "Update Geodatabase Q3 2024", "Diperbarui Q2 2024", footer "Projek Pengantar Data Sains", deskripsi wilayah kualitatif (Koridor Kampus, dst.). Semua angka akan dibaca dari CSV/metadata.
