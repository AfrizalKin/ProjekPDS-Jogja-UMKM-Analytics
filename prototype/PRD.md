# PRD: UMKM Recommender (Prototipe Streamlit)

**Versi:** 0.1 | **Tanggal:** 4 Oktober 2026 | **Status:** Draf | 

---

## 1. Ringkasan
UMKM Recommender adalah aplikasi web untuk membantu calon pelaku UMKM di Daerah Istimewa Yogyakarta memilih **sektor usaha** dan **lokasi (kabupaten/kota)** berdasarkan data. Aplikasi menampilkan skor kelayakan, karakter wilayah, arah tren sektor, dan rekomendasi personal yang memperhitungkan anggaran sewa pengguna.

Dokumen ini mendefinisikan kebutuhan **prototipe berbasis Streamlit**. Prototipe adalah antarmuka untuk hasil analisis yang sudah dihitung sebelumnya. Aplikasi tidak melatih model dan tidak mengambil data baru saat dijalankan.

## 2. Latar Belakang dan Masalah
- Calon pelaku usaha sering memilih lokasi dan sektor berdasarkan intuisi atau tren sesaat, tanpa memeriksa kepadatan pesaing, daya beli warga, dan biaya sewa.
- Informasi yang dibutuhkan tersebar pada banyak sumber (data statistik, peta, indeks properti) dan tidak mudah dibandingkan.
- Hasil analisis sudah tersedia dalam bentuk berkas CSV, tetapi belum dapat dipakai oleh pengguna non-teknis.

## 3. Tujuan dan Metrik Keberhasilan
| Tujuan | Metrik | Target |
|---|---|---|
| Pengguna dapat memperoleh rekomendasi tanpa keahlian teknis | Langkah dari halaman pertama sampai kartu rekomendasi | ≤ 3 interaksi (pilih sektor, pilih wilayah, isi anggaran opsional) |
| Seluruh hasil analisis dapat dijelajahi | Menu yang berfungsi penuh | 5 dari 5 menu |
| Angka yang ditampilkan dapat dipercaya | Kesesuaian dengan berkas hasil | 100% sama dengan CSV sumber |
| Aplikasi responsif | Waktu muat awal dan waktu pembaruan hasil | ≤ 3 detik dan ≤ 1 detik pada laptop standar |
| Pengguna tidak menyalahartikan hasil | Peringatan satu baris ("alat bantu pertimbangan") terlihat pada Beranda dan kartu rekomendasi | Selalu tampil |

**Bukan tujuan (non-goals):**
- Menjamin keberhasilan usaha. Hasil adalah alat bantu pertimbangan.
- Melatih ulang model atau mengambil data baru dari sumber luar.
- Akun pengguna, penyimpanan data pengguna, dan basis data.
- Situs final (Laravel) dan aplikasi seluler.

## 4. Pengguna
| Persona | Kebutuhan | Kendala |
|---|---|---|
| **Calon pelaku UMKM** (pengguna utama) | Mengetahui sektor dan wilayah yang layak untuk anggaran yang dimiliki | Tidak terbiasa membaca tabel statistik |
| **Peninjau hasil analisis** | Menelusuri skor, klaster, dan proyeksi per wilayah dan sektor | Perlu melihat asal angka dan keterbatasannya |

## 5. Ruang Lingkup
**Termasuk (in scope):**
- Lima menu: Beranda, Skoring Kelayakan, Peta dan Klaster, Forecasting Tren, Rekomendasi.
- Membaca berkas hasil analisis dan data bersih yang sudah ada.
- Antarmuka berbahasa Indonesia, mengikuti desain acuan (lihat bagian 9).

**Tidak termasuk (out of scope):**
- Halaman khusus keterbatasan dan metodologi. Prototipe cukup memuat peringatan satu baris (FR-06); penjelasan rinci tersedia di dokumen proyek.
- Login, basis data, atau penyimpanan masukan pengguna.
- Pengambilan data baru (scraping) dan pelatihan model.
- Penggantian metode analisis. Metode mengikuti implementasi yang ada.

**Fase:** Prototipe Streamlit (dokumen ini), kemudian situs final pada tahap berikutnya.

## 6. User Stories
| ID | Sebagai | Saya ingin | Agar | Prioritas |
|---|---|---|---|---|
| US-01 | Calon pelaku UMKM | memilih sektor, wilayah (atau "semua wilayah"), dan anggaran sewa | memperoleh rekomendasi sesuai kondisi saya | Must |
| US-02 | Calon pelaku UMKM | melihat tiga wilayah terbaik untuk sektor pilihan saya | membandingkan pilihan lokasi | Must |
| US-03 | Calon pelaku UMKM | mengetahui apakah anggaran saya cukup untuk sewa | menghindari lokasi di luar kemampuan | Must |
| US-04 | Peninjau | melihat tabel skor 25 kombinasi wilayah dan sektor dengan filter | menelusuri hasil secara rinci | Must |
| US-05 | Peninjau | melihat peta sebaran pesaing dan klaster wilayah | memahami karakter tiap wilayah | Should |
| US-06 | Peninjau | melihat proyeksi tren sektor 2024–2026 | memahami arah pertumbuhan sektor | Should |
| US-07 | Pengguna | melihat peringatan singkat bahwa hasil adalah alat bantu serta periode data yang dipakai | tidak menyalahartikan hasil | Must |
| US-08 | Peninjau | mengatur bobot kriteria skor dengan nilai bawaan yang dapat dikembalikan | menguji kepekaan hasil terhadap bobot | Could |

## 7. Kebutuhan Fungsional

### 7.1 Beranda (FR-01)
- Menampilkan ringkasan masalah dan tujuan, serta angka kunci: jumlah titik pesaing (2.796), jumlah wilayah (5), jumlah sektor (5).
- Menyediakan tautan ke empat menu lainnya.
- **Kriteria penerimaan:** angka kunci dibaca dari data, bukan ditulis manual di kode.

### 7.2 Peta dan Klaster Wilayah (FR-02)
- Menampilkan peta sebaran titik pesaing dengan warna berdasarkan sektor.
- Menampilkan klaster wilayah (3 klaster) beserta label dan deskripsinya.
- Menyediakan kartu profil wilayah (PDRB, pengeluaran, kepadatan, sewa, rasio kompetitor, rasio UMKM) saat wilayah dipilih.
- Menampilkan diagram sebar PCA dua dimensi untuk lima wilayah.
- **Kriteria penerimaan:** warna klaster mengikuti `cluster_label` dari berkas hasil, bukan nomor klaster.

### 7.3 Skoring Kelayakan (FR-03)
- Menampilkan tabel 25 kombinasi dengan kolom sektor, wilayah, jumlah kompetitor, rasio kompetitor, sewa, skor, dan kategori.
- Filter berdasarkan wilayah dan sektor; tabel dapat diurutkan.
- Menampilkan diagram batang perbandingan skor antar wilayah dan sektor, dengan garis ambang 70 dan 50.
- **Kriteria penerimaan:** kategori memakai ambang Layak ≥ 70, Cukup Layak ≥ 50, Kurang Layak < 50; hasil filter selalu konsisten dengan tabel penuh.

### 7.4 Forecasting Tren (FR-04)
- Menampilkan grafik garis per sektor: data historis 2019–2023 dan proyeksi 2024–2026 dengan pita interval 95%.
- Menampilkan label arah tren dan nilai proyeksi.
- Menampilkan catatan bahwa proyeksi adalah sinyal arah (berdasarkan lima titik data).
- **Kriteria penerimaan:** titik historis dan proyeksi dibedakan secara visual.

### 7.5 Rekomendasi (FR-05)
**Masukan:**
| Masukan | Jenis | Nilai |
|---|---|---|
| Sektor usaha | Wajib, pilihan | restoran, kafe, minimarket, laundry, kelontong |
| Wilayah | Wajib, pilihan | 5 wilayah, atau "Semua wilayah" |
| Anggaran sewa tahunan | Opsional, angka (Rp) | ≥ 0 |

**Keluaran, wilayah spesifik:** skor dan kategori; label dan deskripsi klaster; arah tren sektor; estimasi sewa tahunan (tarif × 30 m²); status anggaran; peringatan kejenuhan (bila ada); narasi rekomendasi.
**Keluaran, semua wilayah:** peringkat seluruh wilayah dengan tiga teratas disorot, beserta skor, kategori, klaster, estimasi sewa, dan penanda kecukupan anggaran.

**Kriteria penerimaan:**
- Status anggaran hanya "Mencukupi" atau "Kurang" bila anggaran diisi. Bila tidak diisi, antarmuka menampilkan "Anggaran tidak dievaluasi".
- Anggaran 0 atau negatif ditolak dengan pesan yang jelas.
- Pada mode semua wilayah dengan anggaran terisi, wilayah yang tidak terjangkau diberi tanda jelas.
- Bila tidak ada wilayah berkategori Layak (skor tertinggi di bawah 70), antarmuka menampilkan pesan bahwa tidak ada wilayah berkategori Layak; kalimatnya membedakan skor tertinggi 50-69 (Cukup Layak) dan di bawah 50 (Kurang Layak).
- Asumsi luas 30 m² ditampilkan di dekat hasil.

### 7.6 Peringatan dan Keterangan Periode Data (FR-06)
- Satu baris peringatan pada Beranda dan kartu rekomendasi: "Hasil bersifat alat bantu pertimbangan, bukan jaminan keberhasilan usaha."
- Satu baris keterangan periode data di bawah judul tiap halaman, misalnya "Data pesaing per 8 September 2026; ekonomi dan sewa 2024; UMKM terdaftar 2025".
- **Kriteria penerimaan:** keterangan periode dibaca dari berkas metadata (bukan ditulis manual di kode); tidak ada halaman keterbatasan terpisah pada prototipe.
- **Ketergantungan:** berkas metadata periode data (misalnya `data/cleaned/metadata_data.json`) perlu dibuat.

### 7.7 Pengaturan Bobot (FR-07, prioritas Could)
- Penggeser bobot untuk enam kriteria dengan **nilai awal sama dengan bawaan** (PDRB 0,25; pengeluaran 0,25; kepadatan 0,15; kompetitor 0,15; sewa 0,10; rasio UMKM 0,10), tombol "Kembalikan ke bawaan", dan normalisasi otomatis agar total 1,0.
- Hasil dengan bobot kustom diberi label "bobot kustom", dan bobot yang dipakai selalu terlihat.
- **Ketergantungan:** berkas hasil Pilar 1 perlu memuat enam kolom kriteria ternormalisasi agar skor dapat dihitung ulang tanpa menjalankan pipeline.

## 8. Kebutuhan Non-Fungsional
- **Kinerja:** data dimuat satu kali dan disimpan sementara (cache); waktu muat awal ≤ 3 detik.
- **Hanya-baca:** aplikasi tidak menulis ke folder data dan tidak memanggil skrip pengambilan data atau pelatihan.
- **Keterlacakan:** setiap angka harus berasal dari berkas hasil atau data bersih, tanpa angka yang ditulis manual.
- **Ketahanan:** bila berkas data tidak ditemukan, aplikasi menampilkan pesan yang jelas, bukan galat teknis.
- **Bahasa:** seluruh teks antarmuka berbahasa Indonesia.
- **Tampilan:** mengikuti desain acuan (tema terang). Tema dan warna dasar diatur lewat `.streamlit/config.toml`. **CSS tambahan wajib** (disimpan di satu berkas, misalnya `prototype/assets/style.css`, dan dimuat saat aplikasi mulai) untuk kartu, lencana status, dan tata letak yang tidak tersedia di komponen bawaan. Komponen yang tetap tidak mungkin dibuat diganti padanan terdekat.
- **Kompatibilitas:** peramban modern pada laptop; tampilan telepon seluler tidak menjadi prioritas.
- **Pemeliharaan:** pembaruan hasil cukup dengan mengganti berkas CSV, tanpa mengubah kode antarmuka.

## 9. Alur Pengguna
1. Pengguna membuka **Beranda** dan membaca ringkasan.
2. Pengguna memilih **Rekomendasi**, lalu memilih sektor, wilayah, dan (opsional) anggaran.
3. Aplikasi menampilkan **kartu rekomendasi** (satu wilayah) atau **peringkat tiga teratas** (semua wilayah).
4. Pengguna dapat membuka **Skoring Kelayakan**, **Peta dan Klaster**, atau **Forecasting Tren** untuk menelusuri dasar hasil.

**Struktur menu (5):** Beranda, Skoring Kelayakan, Peta dan Klaster, Forecasting Tren, Rekomendasi.

**Desain acuan:** antarmuka dirancang di Google Stitch dengan tema terang, terdiri dari lima layar (Beranda, Skoring Kelayakan, Peta dan Klaster, Forecasting Tren, Rekomendasi) beserta palet warna. Tangkapan layar dan palet disimpan di `prototype/design/` (rencana). Desain berfungsi sebagai acuan visual, bukan kode yang dipakai langsung.

## 10. Data dan Integrasi
| Sumber | Isi | Dipakai oleh |
|---|---|---|
| `outputs/hasil/hasil_skoring_sektor.csv` | Skor dan kategori 25 kombinasi | FR-03, FR-05 |
| `outputs/hasil/hasil_clustering_wilayah.csv` | Klaster dan koordinat PCA 5 wilayah | FR-02, FR-05 |
| `outputs/hasil/hasil_forecasting_sektor.csv` | Historis dan proyeksi 2019–2026 | FR-04, FR-05 |
| `data/cleaned/kompetitor_per_wilayah.csv` | 2.796 titik pesaing | FR-02 |
| `data/cleaned/kondisi_ekonomi_wilayah.csv`, `biaya_operasional.csv`, `umkm_sibakul.csv` | Profil wilayah | FR-02 |
| `models/04_rekomendasi.py` | Kelas `UMKMRecommender` | FR-05 |

**Catatan integrasi:** nama berkas `models/` diawali angka sehingga tidak dapat diimpor dengan `import` biasa. Aplikasi memuatnya dengan `importlib.import_module("models.04_rekomendasi")`, seperti pada `models/run_all_models.py`.

## 11. Asumsi, Batasan, dan Risiko
| Item | Jenis | Dampak | Mitigasi |
|---|---|---|---|
| Data pesaing bersumber dari peta terbuka yang tidak lengkap untuk usaha informal | Batasan | Skor sektor tertentu dapat terlalu tinggi | Peringatan satu baris (FR-06); penjelasan rinci di dokumen proyek |
| Skor lebih mencerminkan karakter wilayah dibanding sektor | Batasan | Selisih antar-sektor di satu wilayah kecil | Penjelasan di dokumen proyek (`milestones/konsep_pemahaman.md`) |
| Bobot ditetapkan peneliti | Batasan | Hasil dapat bergeser bila bobot berubah | FR-07 dan keterangan pada hasil |
| Luas ruko 30 m² untuk semua sektor | Asumsi | Estimasi sewa kurang tepat untuk sektor tertentu | Tampilkan asumsi; pertimbangkan masukan luas pada fase berikutnya |
| Hasil dapat berubah bila analisis dijalankan ulang | Risiko | Angka di aplikasi tidak sesuai dokumen | Aplikasi membaca CSV terbaru; tidak ada angka manual |
| Pustaka Streamlit dan visualisasi belum tercantum di `requirements.txt` | Risiko | Aplikasi tidak dapat dijalankan di lingkungan baru | Tambahkan dependensi sebelum rilis prototipe |

## 12. Rencana Rilis
| Tonggak | Isi | Target |
|---|---|---|
| M1 | Kerangka aplikasi, pemuatan data, Beranda, Skoring (FR-01, FR-03) | [isi] |
| M2 | Rekomendasi (FR-05) serta peringatan dan periode data (FR-06) | [isi] |
| M3 | Peta dan Klaster, Forecasting Tren (FR-02, FR-04) | [isi] |
| M4 | Pengaturan bobot (FR-07, opsional), uji menyeluruh, dokumentasi | [isi] |

**Cara menjalankan (rencana):** `streamlit run prototype/app.py`.

## 13. Pertanyaan Terbuka
- [ ] Apakah pengaturan bobot (FR-07) masuk prototipe atau fase berikutnya?
- [ ] Peta dasar apa yang dipakai (peta bawaan Streamlit atau pustaka peta lain)?
- [ ] Prototipe di-deploy publik atau dijalankan lokal?
- [ ] Apakah masukan luas ruko perlu ditambahkan ke formulir rekomendasi?
- [ ] Apakah desain acuan (tema terang) dipertahankan seluruhnya, atau disederhanakan agar sesuai komponen bawaan Streamlit?

## 14. Lampiran
- Glosarium dan penjelasan metode: `milestones/konsep_pemahaman.md`
- Evaluasi metodologi dan usulan perbaikan: `milestones/evaluasi.md`
- Desain antarmuka (Google Stitch): `prototype/design/` (rencana)
