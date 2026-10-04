# Dokumen Pemahaman Konseptual dan Teknis
## Sistem Rekomendasi Kelayakan Sektor Usaha UMKM Berbasis Data di Daerah Istimewa Yogyakarta

**Mata kuliah:** Pengantar Data Sains (PDS), Semester 3
**Judul formal proyek:** *Pemodelan Kelayakan Sektor Usaha UMKM Menggunakan Pendekatan Machine Learning dan Time Series untuk Rekomendasi Lokasi Berbasis Data di D.I. Yogyakarta*
**Nama sistem:** UMKM Recommender (UMKM-Jogja Analytics)

---

## Pengantar Dokumen

### Tujuan
Dokumen ini disusun sebagai bahan belajar bagi seluruh anggota tim agar memahami proyek secara menyeluruh, mencakup latar belakang, alur data, metode analisis, keputusan metodologis, hasil, dan keterbatasannya. Pemahaman tersebut diharapkan memungkinkan setiap anggota menjelaskan dan mempertanggungjawabkan proyek secara ilmiah.

### Rujukan dan Konvensi
- Implementasi yang menjadi rujukan adalah kode pada folder `scripts/` (pengambilan dan pembersihan data) dan `models/` (empat pilar analitik).
- Seluruh nilai numerik yang dikutip bersumber dari berkas hasil di `outputs/hasil/`, data bersih di `data/cleaned/`, serta berkas mentah di `data/raw/`. Nilai yang dihitung ulang secara manual untuk keperluan ilustrasi ditandai sebagai "perhitungan ilustratif".
- Istilah teknis dijelaskan pada **Lampiran A (Glosarium)**. Istilah yang pertama kali muncul dalam teks diberi tanda (lihat Glosarium).
- Dokumen ini membedakan secara tegas antara (a) hal yang telah dikerjakan dalam kode dan (b) hal yang masih berupa rencana atau saran pengembangan.

### Daftar Isi
1. Gambaran Umum Proyek
2. Data: Sumber, Akuisisi, Pembersihan, dan Karakteristik
3. Empat Pilar Analitik
4. Keterkaitan Antar Pilar dan Contoh Alur Menyeluruh
5. Arsitektur Implementasi dan Rencana Antarmuka
6. Keterbatasan dan Arah Pengembangan
7. Pertanyaan yang Mungkin Diajukan Penguji
- Lampiran A: Glosarium Istilah
- Lampiran B: Kamus Data
- Lampiran C: Tabel Hasil Lengkap
- Lampiran D: Peta Berkas Proyek

---

## 1. Gambaran Umum Proyek

### 1.1 Latar Belakang
Usaha Mikro, Kecil, dan Menengah (UMKM) merupakan penopang perekonomian daerah. Di Daerah Istimewa Yogyakarta (DIY), jumlah UMKM terdaftar pada tahun 2025 tercatat sebanyak 347.744 unit (SiBakul, Dinas Koperasi dan UKM DIY). Meskipun demikian, literatur yang dirujuk proyek ini menyebutkan bahwa sekitar separuh usaha baru tidak bertahan pada tiga hingga lima tahun pertama, dengan pemilihan lokasi yang kurang tepat sebagai salah satu penyebabnya.

Pemilihan lokasi dan sektor usaha oleh calon pelaku usaha sering kali didasarkan pada intuisi, kebiasaan lingkungan, atau tren sesaat di media sosial, tanpa pemeriksaan terhadap data. Terdapat tiga risiko utama yang menjadi dasar perumusan masalah:

1. **Kejenuhan kompetisi (kanibalisasi pasar).** Usaha sejenis yang menumpuk pada satu kawasan, misalnya kafe di sekitar kampus, menurunkan pangsa pasar tiap unit usaha dan mendorong persaingan harga.
2. **Ketidaksesuaian daya beli.** Harga produk yang tidak selaras dengan kemampuan belanja masyarakat setempat menurunkan peluang penyerapan produk.
3. **Beban biaya sewa.** Biaya sewa properti komersial yang tinggi, terutama di pusat kota, menyerap modal kerja sebelum usaha mencapai titik impas.

### 1.2 Rumusan Masalah dan Tujuan
**Rumusan masalah.** Bagaimana calon pelaku UMKM di DIY dapat memilih sektor usaha dan lokasi (kabupaten/kota) secara berbasis data, dengan mempertimbangkan kepadatan pesaing, daya beli, biaya sewa, dan arah pertumbuhan sektor?

**Tujuan.** Membangun Sistem Pendukung Keputusan (*Decision Support System*) yang:
1. menilai tingkat kelayakan setiap kombinasi wilayah dan sektor usaha;
2. memetakan karakteristik ekonomi setiap kabupaten/kota;
3. memproyeksikan arah pertumbuhan sektor usaha untuk tahun 2024–2026;
4. menghasilkan rekomendasi personal yang memperhitungkan sektor pilihan, wilayah, dan anggaran sewa pengguna.

### 1.3 Ruang Lingkup
- **Wilayah (5):** Kota Yogyakarta, Kabupaten Sleman, Kabupaten Bantul, Kabupaten Kulon Progo, dan Kabupaten Gunungkidul.
- **Sektor usaha (5):** restoran/warung makan, kafe/kedai kopi, minimarket/toko modern (*convenience*), jasa laundry, dan toko kelontong tradisional.
- **Kombinasi analisis:** 5 wilayah × 5 sektor = 25 kombinasi.
- **Tingkat analisis:** kabupaten/kota. Sistem tidak membedakan lokasi pada tingkat kecamatan atau ruas jalan, karena data ekonomi dan sewa tidak tersedia pada tingkat tersebut.

### 1.4 Pendekatan Analitik: Mengapa Bukan Pembelajaran Terawasi
Dalam pembelajaran mesin terawasi (*supervised learning*), model dilatih menggunakan data yang telah memiliki label target, misalnya "lokasi berhasil" atau "lokasi gagal". Data publik yang digunakan proyek ini (BPS, OpenStreetMap, SiBakul, indeks properti) bersifat agregat pada tingkat wilayah dan tidak memuat label keberhasilan usaha. Pembuatan label buatan tanpa data kinerja usaha yang nyata akan menghasilkan model yang hanya mereproduksi asumsi penyusunnya.

Oleh karena itu, proyek ini mengadopsi tiga pendekatan yang tidak memerlukan label:
- **Skoring berbasis aturan** (*Multi-Criteria Decision Analysis*) untuk penilaian dan perankingan kelayakan.
- **Pembelajaran tak terawasi** (*K-Means* dan *PCA*) untuk pengelompokan karakter wilayah.
- **Regresi tren linear** untuk proyeksi arah pertumbuhan sektor.
- Satu lapisan **mesin rekomendasi berbasis aturan** yang menggabungkan ketiga hasil tersebut.

### 1.5 Arsitektur dan Alur Kerja

```
Sumber data: OSM, BPS, indeks sewa, Google Trends, SiBakul
        |
        v   scripts/  (pengambilan dan pembersihan, dijalankan sekali)
data/cleaned/  (CSV bersih)
        |
  +-----+-----------------------+-----------------------+
  v                             v                       v
PILAR 1: Skoring (MCDA)   PILAR 2: Klaster         PILAR 3: Forecasting
hasil_skoring_sektor      hasil_clustering_wilayah  hasil_forecasting_sektor
  |                             |                       |
  +-----------------------------+-----------------------+
                                v
                    outputs/hasil/  (CSV hasil Pilar 1-3)
                                |
                                v
                    PILAR 4: Mesin Rekomendasi (UMKMRecommender)
                    (satu-satunya komponen dengan masukan pengguna)
                                v
         Antarmuka web: prototipe Streamlit, kemudian situs final Laravel
```

Prinsip rancangan yang disepakati: **antarmuka web hanya membaca berkas hasil** (`outputs/hasil/`, serta `data/cleaned/` dan `models/saved/` bila diperlukan) dan tidak menjalankan ulang pengambilan data maupun pelatihan model. Pemisahan ini disebut arsitektur *decoupled* (pemisahan antara komputasi dan penyajian).

### 1.6 Urutan Pelaksanaan
- **Fase 1, data:** lima dataset diambil, dibersihkan, dan disimpan (`scripts/`, notebook `data_cleaning`).
- **Fase 2, pemodelan:** empat pilar dikembangkan (`models/`, notebook `analisis`).
- **Fase 3, antarmuka:** prototipe Streamlit (`prototype/`) dan situs final Laravel (`media/`). Kedua folder tersebut sengaja masih kosong dan merupakan tahap berikutnya.

---

## 2. Data: Sumber, Akuisisi, Pembersihan, dan Karakteristik

### 2.1 Alur Umum (ETL)
Setiap dataset melalui rangkaian *Extract–Transform–Load*:

1. **Ekstraksi (extract):** pengambilan data dari sumber (API, berkas unduhan, atau kompilasi publikasi).
2. **Transformasi (transform):** pembersihan, penyeragaman nama wilayah dan satuan, penghapusan duplikasi, dan penurunan variabel baru.
3. **Pemuatan (load):** penyimpanan hasil bersih sebagai berkas CSV di `data/cleaned/`.

Orkestrasi dijalankan oleh `scripts/run_all_pipelines.py`. Terdapat satu prinsip yang diterapkan pada seluruh dataset: **penyeragaman nama wilayah menggunakan kamus pemetaan eksplisit (*dictionary mapping*)**, bukan pencocokan samar (*fuzzy matching*). Alasannya, cakupan wilayah hanya lima sehingga pemetaan manual dapat diverifikasi sepenuhnya dan bersifat deterministik. Contoh variasi penulisan yang disatukan: "Kulonprogo", "Kab. Kulon Progo", "Kabupaten Kulon Progo" menjadi satu identitas; "Gunungkidul" dan "Gunung Kidul" menjadi satu identitas; "Yogyakarta" dan "Kota Jogja" menjadi "Kota Yogyakarta".

Ringkasan kelima dataset:

| No | Dataset | Sumber | Granularitas | Berkas hasil |
|---|---|---|---|---|
| 1 | Kompetitor usaha | OpenStreetMap (Overpass API) | Titik usaha per sektor dan wilayah | `kompetitor_per_wilayah.csv` |
| 2 | Kondisi ekonomi wilayah | BPS DIY (2024) | Per kabupaten/kota | `kondisi_ekonomi_wilayah.csv` |
| 3 | Biaya sewa komersial | Bank Indonesia, Rumah123, IPW (2024) | Per kabupaten/kota | `biaya_operasional.csv` |
| 4 | Tren sektor usaha | BPS DIY (2019–2023), Google Trends | Per sektor, wilayah, tahun | `tren_sektor.csv` |
| 5 | UMKM terdaftar | SiBakul, Diskop UKM DIY (2025) | Per kabupaten/kota; tingkat DIY | `umkm_sibakul.csv` dan dua berkas rujukan |

### 2.2 Dataset 1: Kompetitor Usaha (OpenStreetMap)

**Deskripsi.** Dataset ini memuat titik lokasi usaha (*Point of Interest*, POI) pada lima kategori: restoran, kafe, minimarket (*convenience*), laundry, dan toko kelontong (*grocery*). Setelah pembersihan, tersisa **2.796 titik**. Fungsinya adalah mengukur kepadatan pesaing per sektor di setiap wilayah.

**Sumber.** OpenStreetMap (OSM) adalah basis data peta dunia yang dikontribusikan secara sukarela. Data diakses melalui Overpass API, yaitu layanan kueri yang memungkinkan pengambilan objek OSM berdasarkan tag dan wilayah.

**Teknik akuisisi.** Implementasi berada pada `scripts/dataset1_osm/`.
- **Penentuan wilayah dan kategori.** Setiap kombinasi dari 5 wilayah dan 5 kategori (25 kueri) diambil menggunakan tag OSM berikut: `amenity=restaurant`, `amenity=cafe`, `shop=convenience`, `shop=laundry`, dan `shop=grocery`. Wilayah dibatasi menggunakan batas administratif OSM tingkat 5 (`admin_level=5`, yaitu tingkat kabupaten/kota di DIY) dan, sebagai pembatas tambahan, *bounding box* tiap wilayah.
- **Jenis objek.** Kueri mengambil objek bertipe *node* (titik) dan *way* (bangunan/poligon). Untuk *way*, parameter `out center` meminta titik pusat poligon sehingga setiap usaha memiliki satu pasang koordinat.
- **Ketahanan terhadap kegagalan server.** Server publik Overpass memiliki batasan beban. Kode menerapkan beberapa mekanisme: (a) rotasi antar tiga alamat server cadangan (*mirror*) pada setiap percobaan ulang; (b) maksimum tiga kali percobaan ulang; (c) jeda tiga detik antar permintaan; (d) saat menerima kode HTTP 429 (*Too Many Requests*), kode menunggu 10 detik dikalikan nomor percobaan; (e) saat menerima kode HTTP 5xx atau *timeout*, kode mencoba kueri cadangan murni berbasis *bounding box*; dan (f) seluruh kegagalan dicatat pada berkas log.
- **Grid sampling.** Tersedia modul `grid_sampling.py` yang membagi *bounding box* menjadi sel-sel kecil (misalnya 2×2) agar satu kueri tidak terlalu besar pada wilayah yang padat.

**Pembersihan dan deduplikasi** (`clean_dedup.py`):
1. Membaca seluruh berkas JSON mentah (25 berkas) dan mengekstrak nama, koordinat, kategori, dan wilayah. Objek tanpa koordinat dilewati. Objek tanpa nama diberi nilai "Tanpa Nama".
2. **Deduplikasi lapis pertama:** objek dengan ID OSM dan kategori yang sama dihapus.
3. **Deduplikasi lapis kedua (spasial):** koordinat dibulatkan hingga lima desimal (sekitar 1,1 meter). Untuk objek bernama, duplikat ditentukan oleh kombinasi nama, koordinat bulat, dan kategori. Untuk objek tanpa nama, duplikat ditentukan oleh koordinat bulat dan kategori.
4. Menyimpan lima kolom akhir: `nama_tempat`, `lat`, `lon`, `kategori`, `wilayah`.

Menurut dokumen Milestone 4, data mentah sebanyak 3.572 elemen berkurang menjadi 2.796 baris bersih setelah eliminasi 773 duplikat ID dan 3 duplikat spasial.

**Distribusi hasil bersih** (dihitung dari tabel hasil):

| Wilayah | Kafe | Minimarket | Kelontong | Laundry | Restoran | Total |
|---|---|---|---|---|---|---|
| Kota Yogyakarta | 108 | 11 | 0 | 0 | 39 | 158 |
| Sleman | 200 | 292 | 1 | 46 | 854 | 1.393 |
| Bantul | 30 | 51 | 0 | 36 | 186 | 303 |
| Kulon Progo | 44 | 14 | 0 | 0 | 197 | 255 |
| Gunungkidul | 32 | 193 | 0 | 0 | 462 | 687 |
| **Total** | **414** | **561** | **1** | **82** | **1.738** | **2.796** |

**Keterbatasan data.**
1. **Representasi usaha informal rendah.** Kategori kelontong hanya memuat 1 titik (di Sleman). Hal ini mencerminkan karakteristik OSM, bukan kegagalan teknis: warung rumahan berskala mikro jarang didaftarkan pada peta digital, dan kontributor sering menandai warung sebagai `shop=convenience`. Sebagai pembanding, tabel BPS mencatat sekitar 11.700 unit toko kelontong pada tahun 2023.
2. **Kelengkapan tidak merata antar wilayah dan kategori.** Contohnya, laundry di Kota Yogyakarta tercatat nol di OSM, padahal tabel BPS mencatat sekitar 330 unit laundry di wilayah tersebut. Dengan demikian, angka nol pada OSM tidak dapat ditafsirkan sebagai ketiadaan pesaing.
3. **Batas antar kategori bergantung pada kontributor.** Beberapa usaha seperti angkringan atau warung sate tercatat dengan tag `amenity=cafe`. Kategori mengikuti penandaan kontributor, bukan klasifikasi baku.
4. **Atribusi wilayah pada irisan area.** Deduplikasi dilakukan berdasarkan ID objek dan kategori tanpa mempertimbangkan wilayah. Objek yang berada pada irisan *bounding box* dua wilayah hanya dipertahankan satu kali, dengan atribusi wilayah mengikuti berkas yang dibaca lebih dahulu.
5. **Validasi geografis.** Seluruh titik berada dalam batas wilayah karena kueri dibatasi oleh area administratif dan *bounding box*; kode produksi tidak melakukan penyaringan koordinat tambahan setelah pengunduhan.

### 2.3 Dataset 2: Kondisi Ekonomi Wilayah (BPS)

**Deskripsi.** Dataset ini memuat empat indikator tahun 2024 untuk lima wilayah.

| Wilayah | PDRB per kapita (ribu Rp, ADHB) | Pengeluaran per kapita (Rp/bulan) | Kepadatan (jiwa/km²) | Luas (km²) |
|---|---|---|---|---|
| Kota Yogyakarta | 131.433,33 | 2.248.145 | 11.562 | 32 |
| Sleman | 54.501,31 | 2.181.883 | 2.052 | 575 |
| Bantul | 35.842,51 | 1.730.515 | 2.024 | 507 |
| Kulon Progo | 37.976,68 | 1.152.288 | 763 | 586 |
| Gunungkidul | 35.503,53 | 1.163.499 | 507 | 1.485 |

**Sumber dan akuisisi.** Tiga tabel publikasi BPS DIY diunduh secara manual dalam format CSV: (1) PDRB per kapita menurut kabupaten/kota, (2) kepadatan penduduk dan luas wilayah, dan (3) rata-rata pengeluaran per kapita sebulan (makanan dan bukan makanan). Implementasi pembersihan berada pada `scripts/dataset2_ekonomi/clean_ekonomi.py`.

**Pembersihan.**
- **Struktur tabel BPS** memiliki beberapa baris judul dan sub-judul di bagian atas sehingga memerlukan pembacaan dengan melewati baris-baris tersebut dan penanganan penyandian `utf-8-sig`.
- **Penghapusan baris agregat provinsi.** Setiap tabel BPS menyertakan baris total "D.I. Yogyakarta" di antara data kabupaten/kota (misalnya PDRB per kapita DIY 51.473,44 dan pengeluaran DIY Rp1.758.865). Apabila dipertahankan, baris tersebut akan dihitung sebagai wilayah keenam dan mendistorsi statistik. Kode menerapkan daftar pengecualian (*blacklist*) untuk baris agregat.
- **Penyeragaman nama wilayah** dengan kamus pemetaan eksplisit.
- **Penggabungan** ketiga tabel menggunakan *inner join* pada nama wilayah dan verifikasi bahwa hasilnya tepat lima baris.

**Makna indikator.**
- *PDRB per kapita atas dasar harga berlaku* menggambarkan nilai tambah yang dihasilkan di suatu wilayah dibagi jumlah penduduknya, dalam harga tahun berjalan. Karena dihitung berdasarkan lokasi produksi, wilayah pusat kegiatan ekonomi cenderung memiliki angka tinggi. Proyek ini memakai PDRB per kapita sebagai penanda skala ekonomi dan potensi pasar.
- *Pengeluaran per kapita sebulan* adalah rata-rata belanja penduduk (makanan dan bukan makanan) dan digunakan sebagai penanda daya beli riil konsumen.
- *Kepadatan penduduk* digunakan sebagai penanda kedekatan akses terhadap pasar. Dari kepadatan dan luas wilayah, jumlah penduduk diestimasi sebagai kepadatan × luas: Kota Yogyakarta ± 369.984 jiwa; Sleman ± 1.179.900; Bantul ± 1.026.168; Kulon Progo ± 447.118; Gunungkidul ± 752.895. Estimasi ini digunakan sebagai penyebut seluruh rasio per 1.000 penduduk dalam proyek.

**Keterbatasan.** Hanya lima baris data; seluruh nilainya bersifat tingkat wilayah sehingga sama untuk semua sektor yang berada di wilayah yang sama.

### 2.4 Dataset 3: Biaya Sewa Komersial

**Deskripsi.** Satu nilai tarif sewa ruko/kios komersial untuk setiap wilayah, dinyatakan dalam rupiah per meter persegi per tahun, tahun rujukan 2024.

| Wilayah | Sewa (Rp/m²/tahun) | Kategori biaya | Rujukan |
|---|---|---|---|
| Kota Yogyakarta | 850.000 | Tinggi | Bank Indonesia dan Rumah123 Property Index |
| Sleman | 725.000 | Tinggi | Bank Indonesia dan Rumah123 Property Index |
| Bantul | 450.000 | Menengah | Bank Indonesia dan IPW Market Review |
| Kulon Progo | 275.000 | Terjangkau | Bank Indonesia dan laporan pasar properti DIY |
| Gunungkidul | 220.000 | Terjangkau | Bank Indonesia dan laporan pasar properti DIY |

**Akuisisi.** Nilai acuan per wilayah dikompilasi dari publikasi resmi: Survei Perkembangan Properti Komersial Bank Indonesia (PPKom), laporan indeks properti Rumah123, dan *Indonesia Property Watch* (IPW). Nilai-nilai tersebut tersimpan pada berkas konfigurasi `scripts/dataset3_sewa/config.py` dan dituliskan ke `data/raw/sewa_index.csv` oleh `fetch_index.py`. Modul tersebut juga menyediakan fungsi penguraian tabel dari halaman web (BeautifulSoup) dan dari berkas PDF (pdfplumber) bila diperlukan.

**Pembersihan.** Fungsi `normalize_rental_price` menyeragamkan satuan ke rupiah per meter persegi per tahun: tarif bulanan dikalikan 12, tarif harian dikalikan 365, dan tarif tahunan dipertahankan. Kategori biaya (Tinggi, Menengah, Terjangkau) adalah klasifikasi ordinal yang ditetapkan peneliti.

**Keterbatasan.** (1) Satu angka per wilayah tidak menggambarkan variasi antar kecamatan atau antara lokasi strategis dan pinggiran. (2) Angka bersifat indeks atau rata-rata acuan, bukan data transaksi per lokasi.

### 2.5 Dataset 4: Tren Sektor Usaha (BPS dan Google Trends)

**Deskripsi.** Panel data jumlah unit usaha mikro dan kecil per sektor, per wilayah, per tahun (2019–2023), sebanyak **125 baris** (5 sektor × 5 wilayah × 5 tahun), ditambah skor minat pencarian Google Trends.

**Sumber BPS.** Tabel "Jumlah Unit Usaha Mikro dan Kecil Menurut Kabupaten/Kota dan Kategori Sektor Usaha (2019–2023)", bersumber dari Survei Usaha Terintegrasi dan Profil UMKM BPS Provinsi DIY. Berkas mencatat bahwa angka tahun 2023 merupakan angka sementara. Parser `fetch_bps.py` menangani judul bertingkat, sel gabungan, catatan kaki, serta mengubah format lebar (tahun sebagai kolom) menjadi format panjang (satu baris per tahun) dan memetakan nama kategori ke lima sektor proyek melalui kata kunci dan kode KBLI.

**Google Trends.** `fetch_trends.py` memakai pustaka `pytrends` untuk mengambil indeks minat pencarian mingguan (skala 0–100) dengan cakupan nasional (`geo=ID`), jangka lima tahun, menggunakan kata kunci per sektor (misalnya "coffee shop jogja", "kuliner jogja", "laundry jogja", "minimarket", "toko kelontong"). Mekanisme ketahanan: jeda 12 detik antar permintaan dan tiga kali percobaan ulang; kata kunci yang gagal dilewati dan dicatat pada log tanpa menghentikan alur. Hasil mentah memuat 1.310 baris mingguan. Dalam `clean_tren.py`, data dirata-ratakan per sektor dan tahun, lalu digabungkan dengan data BPS melalui *left join* sehingga tidak ada baris BPS yang hilang. Skor Google Trends hanya tersedia untuk tahun 2021–2023.

**Penurunan variabel.** Pertumbuhan tahunan dihitung per sektor per wilayah: selisih unit terhadap tahun sebelumnya dan persentasenya (*Year-over-Year*, YoY).

**Agregasi untuk Pilar 3.** Jumlah unit usaha dijumlahkan dari lima wilayah sehingga diperoleh deret waktu tingkat DIY untuk setiap sektor:

| Sektor | 2019 | 2020 | 2021 | 2022 | 2023 |
|---|---|---|---|---|---|
| Kafe | 1.970 | 1.910 | 2.070 | 2.300 | 2.590 |
| Restoran | 6.260 | 6.060 | 6.300 | 6.680 | 7.100 |
| Minimarket | 1.710 | 1.740 | 1.785 | 1.855 | 1.935 |
| Laundry | 1.365 | 1.295 | 1.360 | 1.465 | 1.575 |
| Kelontong | 12.000 | 11.930 | 11.850 | 11.780 | 11.710 |

**Keterbatasan.** (1) Hanya lima titik waktu per sektor. (2) Angka 2023 bersifat sementara. (3) Skor Google Trends bersifat nasional sehingga bernilai sama untuk semua wilayah pada sektor dan tahun yang sama; indikator ini tidak digunakan sebagai masukan model peramalan. (4) Rentang 2019–2023 mencakup guncangan pandemi pada 2020 sehingga pola pertumbuhan tidak sepenuhnya mencerminkan kondisi normal.

### 2.6 Dataset 5: UMKM Terdaftar (SiBakul)

**Deskripsi dan sumber.** Data berasal dari booklet resmi Dinas Koperasi dan UKM DIY (SiBakul Jogja). Terdapat tiga tabel:
1. **Jumlah UMKM per kabupaten/kota 2025** (`umkm_sibakul.csv`): Sleman 113.691; Bantul 94.247; Gunungkidul 58.964; Kota Yogyakarta 42.500; Kulon Progo 38.342; jumlah 347.744. Terdapat pula kolom UMKM berdomisili sesuai KTP setempat (Sleman 89.746; wilayah lain sama dengan totalnya).
2. **Tren total UMKM DIY 2021–2025** (`umkm_tren_tahunan_diy.csv`): 337.060; 342.924; 342.586; 345.980; 347.744.
3. **Sebaran per sektor tingkat DIY** (`umkm_sektor_diy.csv`): antara lain perdagangan 170.396 dan industri pengolahan 112.555 (2025). Karena komposisi sektor tahun 2022 dan 2025 berbeda sangat besar, kedua tahun tersebut kemungkinan tidak sepenuhnya sebanding; tabel ini hanya digunakan sebagai konteks dan tidak menjadi masukan model.

**Variabel turunan.** *Rasio UMKM per 1.000 penduduk* = jumlah UMKM ÷ estimasi penduduk × 1.000. Hasilnya: Kota Yogyakarta 114,87; Sleman 96,36; Bantul 91,84; Kulon Progo 85,75; Gunungkidul 78,32. Rasio ini berfungsi sebagai ukuran kepadatan atau kejenuhan struktural ekosistem usaha pada tingkat wilayah.

**Alasan penggunaan.** OSM kurang merepresentasikan usaha informal; data SiBakul mencatat usaha mikro secara resmi sehingga melengkapi gambaran kejenuhan pasar. Namun, tidak tersedia pemisahan sektor × wilayah pada sumber yang dapat diakses publik. Oleh karena itu, SiBakul dipakai sebagai **fitur tambahan tingkat wilayah** pada Pilar 1 dan 2, bukan pengganti data OSM yang tetap menjadi satu-satunya sumber granularitas per sektor dan per wilayah.

### 2.7 Audit Kualitas Data

Audit dilakukan pada empat dimensi: *completeness* (kelengkapan), *consistency* (konsistensi), *uniqueness* (keunikan), dan *timeliness/validity* (kemutakhiran dan keabsahan).

| Dataset | Skor akhir | Catatan utama |
|---|---|---|
| 1. OSM | 99,1% | Koordinat 100% lengkap dan berada pada batas wilayah; sekitar 1,8% nama bersifat generik |
| 2. BPS | 100% | Tidak ada baris ganda setelah agregat provinsi dikeluarkan |
| 3. Sewa | 99,6% | Satuan diseragamkan; rujukan survei 2024 |
| 4. Tren | 97,6% | Google Trends hanya tersedia 2021–2023; angka 2023 sementara |
| 5. SiBakul | 100% | Data terkini (2025) dan nama wilayah konsisten |

Empat temuan utama dari audit dan penanganannya:

1. **Baris agregat provinsi pada tabel BPS.** Dihapus melalui daftar pengecualian agar tidak dihitung sebagai wilayah keenam.
2. **Duplikasi objek OSM.** Penumpukan unduhan menghasilkan 773 duplikat ID dan 3 duplikat spasial; dihapus melalui deduplikasi dua lapis.
3. **Satuan waktu tarif sewa yang tidak seragam.** Diseragamkan ke rupiah per meter persegi per tahun.
4. **Bias representasi usaha informal pada OSM** (kelontong hanya satu titik). Ditangani dengan menambahkan data SiBakul sebagai ukuran kepadatan usaha tingkat wilayah dan dengan mencatatnya sebagai keterbatasan.

---

## 3. Empat Pilar Analitik

Seluruh perhitungan pada bagian ini merujuk pada implementasi `models/01_skoring.py` hingga `models/04_rekomendasi.py`. Fungsi `models/run_all_models.py` menjalankan Pilar 1, 2, dan 3 secara berurutan, lalu menguji Pilar 4.

### 3.1 Pilar 1: Skoring Kelayakan Sektor Usaha (MCDA)

#### 3.1.1 Tujuan dan keluaran
Menghasilkan **skor kelayakan 0–100** untuk 25 kombinasi wilayah × sektor, disertai kategori **Layak** (skor ≥ 70), **Cukup Layak** (50 hingga kurang dari 70), dan **Kurang Layak** (di bawah 50). Keluaran disimpan pada `outputs/hasil/hasil_skoring_sektor.csv`. Pilar ini bersifat proses batch dan tidak memerlukan masukan pengguna.

#### 3.1.2 Landasan konsep
*Multi-Criteria Decision Analysis* (MCDA) adalah kerangka untuk menilai alternatif berdasarkan beberapa kriteria sekaligus. Teknik yang digunakan adalah *Weighted Linear Combination* (WLC): setiap kriteria diberi bobot, dan skor akhir merupakan jumlah terbobot. Kriteria dibedakan menjadi:
- **Kriteria keuntungan (benefit):** semakin tinggi nilainya semakin menguntungkan (PDRB per kapita, pengeluaran per kapita, kepadatan penduduk).
- **Kriteria biaya (cost):** semakin tinggi nilainya semakin merugikan (rasio kompetitor, biaya sewa, rasio UMKM sebagai penanda kejenuhan).

Analogi: menilai beberapa kos-kosan dengan memberi nilai pada harga, jarak, dan fasilitas, lalu menggabungkannya dengan bobot sesuai kepentingan.

#### 3.1.3 Langkah perhitungan
**Langkah 1. Penyusunan matriks.** Untuk setiap kombinasi wilayah dan sektor dikumpulkan: jumlah kompetitor sektor tersebut (OSM), rasio kompetitor per 1.000 penduduk, PDRB per kapita, pengeluaran per kapita, kepadatan, sewa, dan rasio UMKM total per 1.000 penduduk.

```
rasio kompetitor per 1.000 = jumlah kompetitor ÷ (kepadatan × luas) × 1.000
```

**Langkah 2. Normalisasi min-max** ke skala 0 sampai 1, agar kriteria dengan satuan berbeda (rupiah, jiwa/km², rasio) dapat dijumlahkan.

```
nilai_norm = (nilai − nilai minimum) ÷ (nilai maksimum − nilai minimum)
```

Normalisasi rasio kompetitor dilakukan **per sektor** (nilai minimum dan maksimum diambil di antara lima wilayah untuk sektor yang sama), karena tingkat dasar jumlah usaha berbeda antar sektor (restoran jauh lebih banyak daripada laundry). Kriteria lainnya dinormalisasi di antara lima wilayah.

**Langkah 3. Pembobotan.**

| Kelompok | Kriteria | Bobot |
|---|---|---|
| Daya tarik (benefit) | PDRB per kapita | 0,25 |
| | Pengeluaran per kapita | 0,25 |
| | Kepadatan penduduk | 0,15 |
| Beban (cost) | Rasio kompetitor sektor | 0,15 |
| | Biaya sewa | 0,10 |
| | Rasio UMKM total (kejenuhan) | 0,10 |

```
daya tarik = 0,25·PDRB_norm + 0,25·Pengeluaran_norm + 0,15·Kepadatan_norm
beban      = 0,15·Kompetitor_norm + 0,10·Sewa_norm + 0,10·UMKM_norm
Skor       = 50 + 70 × (daya tarik − beban), dibatasi pada rentang 0 hingga 100
```

Konstanta 50 merupakan titik tengah acuan, dan faktor 70 mengatur sebaran skor sehingga rentang teoretis berada kira-kira antara 25,5 dan 95,5.

#### 3.1.4 Perhitungan ilustratif

Nilai ternormalisasi lima wilayah (dihitung ulang dari data):

| Wilayah | PDRB | Pengeluaran | Kepadatan | Sewa | Rasio UMKM |
|---|---|---|---|---|---|
| Kota Yogyakarta | 1,000 | 1,000 | 1,000 | 1,000 | 1,000 |
| Sleman | 0,198 | 0,940 | 0,140 | 0,802 | 0,494 |
| Bantul | 0,004 | 0,528 | 0,137 | 0,365 | 0,370 |
| Kulon Progo | 0,026 | 0,000 | 0,023 | 0,087 | 0,203 |
| Gunungkidul | 0,000 | 0,010 | 0,000 | 0,000 | 0,000 |

**Contoh A: kafe di Kota Yogyakarta.** Kota bernilai maksimum pada seluruh kriteria wilayah. Rasio kafe per 1.000 penduduk di Kota (0,2919) juga tertinggi di antara kelima wilayah sehingga bernilai 1. Daya tarik = 0,25 + 0,25 + 0,15 = 0,65. Beban = 0,15 + 0,10 + 0,10 = 0,35. Selisih = 0,30. Skor = 50 + 70 × 0,30 = **71,0 (Layak)**.

**Contoh B: kafe di Sleman.** Rasio kafe Sleman 0,1695; nilai minimum 0,0292 (Bantul) dan maksimum 0,2919 (Kota), sehingga kompetitor_norm = (0,1695 − 0,0292) ÷ 0,2627 = 0,534. Daya tarik = 0,25×0,198 + 0,25×0,940 + 0,15×0,140 = 0,305. Beban = 0,15×0,534 + 0,10×0,802 + 0,10×0,494 = 0,210. Selisih = 0,096. Skor = 50 + 70 × 0,096 = **56,7 (Cukup Layak)**.

**Contoh C: laundry di Kota Yogyakarta.** Jumlah laundry di Kota pada data OSM adalah nol, sehingga kompetitor_norm = 0. Beban = 0,10 + 0,10 = 0,20. Selisih = 0,65 − 0,20 = 0,45. Skor = 50 + 70 × 0,45 = **81,5 (Layak)**. Skor ini sebagian besar mencerminkan angka nol pada data OSM (lihat Bagian 2.2).

**Hasil lengkap 25 kombinasi** disajikan pada Lampiran C. Ringkasnya: skor berkisar 39,68 hingga 81,50; terdapat 5 kombinasi Layak, 11 Cukup Layak, dan 9 Kurang Layak.

#### 3.1.5 Keputusan metodologis
| Keputusan | Alternatif | Alasan |
|---|---|---|
| MCDA berbasis aturan | Klasifikasi atau regresi terawasi | Tidak tersedia label keberhasilan usaha; label buatan hanya mereproduksi asumsi |
| Bobot ditetapkan peneliti | Bobot hasil optimasi atau metode AHP/entropi | Tidak ada data target untuk mengoptimasi; bobot disusun atas dasar penalaran bahwa daya beli menentukan terciptanya transaksi (total 50%). Uji sensitivitas bobot belum dilakukan |
| Normalisasi min-max | Standardisasi z-score | Menghasilkan skala 0 sampai 1 yang mudah diinterpretasi pada skor berbobot |
| Kompetitor dinormalisasi per sektor | Normalisasi global | Menghindari bias karena jumlah restoran secara alami jauh lebih besar daripada laundry |
| Rasio UMKM sebagai kriteria biaya | Sebagai kriteria keuntungan | Rasio yang tinggi dimaknai sebagai kejenuhan ekosistem usaha |

#### 3.1.6 Interpretasi dan keterbatasan
1. **Perbedaan antar sektor hanya bersumber dari kompetitor.** Kriteria lain bernilai sama untuk semua sektor dalam satu wilayah. Dengan bobot kompetitor 0,15, selisih skor antar sektor di satu wilayah paling besar 0,15 × 70 = 10,5 poin. Contoh: Kota Yogyakarta memperoleh 81,5 pada empat sektor dan 71,0 pada kafe, selisih tepat 10,5. Dengan demikian, skor lebih mencerminkan kekuatan wilayah dibandingkan keunggulan sektor.
2. **Dominasi daya beli.** PDRB dan pengeluaran berbobot total 50%, dan keduanya tertinggi di Kota Yogyakarta, sehingga Kota hampir selalu berskor tinggi.
3. **Dampak data OSM yang nol.** Untuk laundry dan kelontong di beberapa wilayah, nilai kompetitor nol meningkatkan skor.
4. **Sifat arbitrer ambang.** Ambang 70 dan 50 serta konstanta 50 dan 70 adalah pilihan peneliti, bukan hasil perhitungan statistik.
5. **Sensitivitas min-max terhadap nilai ekstrem.** Karena Kota Yogyakarta bernilai jauh di atas wilayah lain, ia menentukan skala normalisasi sehingga wilayah lain tampak berdekatan pada skala 0 sampai 1.
6. **Bobot belum diuji sensitivitasnya.** Pengujian sensitivitas bobot merupakan langkah lanjutan.

---

### 3.2 Pilar 2: Pengelompokan Karakteristik Wilayah (K-Means dan PCA)

#### 3.2.1 Tujuan dan keluaran
Mengelompokkan lima kabupaten/kota ke dalam tiga kelompok yang memiliki karakter pasar serupa, serta menghasilkan koordinat dua dimensi untuk visualisasi. Keluaran: `hasil_clustering_wilayah.csv` dan tiga model tersimpan (`scaler_clustering.joblib`, `kmeans_wilayah.joblib`, `pca_wilayah.joblib`) pada `models/saved/`.

#### 3.2.2 Variabel
Enam variabel tingkat wilayah: (1) PDRB per kapita, (2) pengeluaran per kapita, (3) kepadatan penduduk, (4) harga sewa, (5) rasio kompetitor total per 1.000 penduduk (seluruh sektor), dan (6) rasio UMKM per 1.000 penduduk.

| Wilayah | Rasio kompetitor total per 1.000 | Rasio UMKM per 1.000 |
|---|---|---|
| Kota Yogyakarta | 0,427 | 114,87 |
| Sleman | 1,181 | 96,36 |
| Bantul | 0,295 | 91,84 |
| Kulon Progo | 0,570 | 85,75 |
| Gunungkidul | 0,913 | 78,32 |

#### 3.2.3 Langkah dan konsep

**Langkah 1. Standardisasi (z-score).** Setiap variabel diubah menjadi `z = (x − rata-rata) ÷ simpangan baku`, sehingga seluruh variabel memiliki rata-rata 0 dan simpangan baku 1. Alasannya, K-Means dan PCA menggunakan jarak; variabel bernilai besar akan mendominasi apabila skala tidak disamakan. Ilustrasi: kepadatan Kota Yogyakarta berada pada ribuan jiwa/km² sedangkan rasio kompetitor di bawah 2. Setelah standardisasi, Kota Yogyakarta berada sekitar 1,96 simpangan baku di atas rata-rata untuk PDRB dan sekitar 1,98 untuk kepadatan (perhitungan ilustratif).

**Langkah 2. K-Means (K = 3).** Algoritma membagi data menjadi K kelompok dengan prosedur berikut: (a) memilih K titik pusat awal (*centroid*); (b) menempatkan setiap wilayah ke pusat terdekat; (c) memindahkan setiap pusat ke rata-rata anggota kelompoknya; (d) mengulang (b) dan (c) sampai penugasan tidak berubah. Tujuannya meminimalkan jumlah jarak kuadrat antar-anggota ke pusat kelompoknya (inersia). Parameter `random_state=42` dan `n_init=10` memastikan hasil dapat direproduksi dan dipilih dari sepuluh inisialisasi berbeda.

**Langkah 3. PCA dua dimensi.** *Principal Component Analysis* mencari kombinasi linear variabel (komponen utama) yang menangkap variasi data sebanyak mungkin. Dengan menahan dua komponen, enam variabel dapat digambarkan pada bidang dua dimensi. Total variansi yang dijelaskan dua komponen adalah **94,09%**, sehingga informasi yang hilang sekitar 5,91%. Analogi: memotret benda tiga dimensi dari sudut yang menampilkan bentuknya paling jelas. Karena hanya ada lima pengamatan, data yang telah dipusatkan memiliki peringkat paling banyak empat sehingga angka variansi yang tinggi pada dua komponen perlu dibaca dengan kehati-hatian. PCA digunakan hanya untuk visualisasi; K-Means tetap dihitung dari enam variabel terstandardisasi.

**Langkah 4. Pelabelan.** Kelompok diberi nama berdasarkan urutan rata-rata PDRB: tertinggi diberi label "Pasar Padat & Biaya Tinggi", menengah "Pasar Berkembang & Biaya Menengah", dan terendah "Pasar Perintis & Biaya Terjangkau". Label merupakan tafsiran manusia atas ciri kelompok, bukan keluaran algoritma.

#### 3.2.4 Hasil

| Kelompok | Wilayah | Ciri utama | Koordinat PCA (x, y) |
|---|---|---|---|
| Pasar Padat & Biaya Tinggi | Kota Yogyakarta | PDRB tertinggi, kepadatan sekitar 11.562 jiwa/km², sewa Rp850.000/m² | (3,77; −0,59) |
| Pasar Berkembang & Biaya Menengah | Sleman | Pengeluaran tinggi, sewa Rp725.000/m², rasio kompetitor tertinggi (1,18) | (0,56; 2,00) |
| Pasar Perintis & Biaya Terjangkau | Bantul | Sewa Rp450.000/m² | (−0,42; −0,93) |
| | Kulon Progo | Sewa Rp275.000/m² | (−1,68; −0,70) |
| | Gunungkidul | Sewa Rp220.000/m², kepadatan terendah | (−2,23; 0,21) |

Pada diagram sebar PCA, Kota Yogyakarta berada jauh di sisi kanan, Sleman di bagian atas, dan ketiga wilayah lainnya berkumpul di sisi kiri bawah. Jarak berdekatan menandakan profil ekonomi yang mirip.

#### 3.2.5 Keputusan metodologis
- **Mengapa tingkat kabupaten/kota (n = 5), bukan tingkat kecamatan?** Data PDRB, pengeluaran, dan sewa hanya tersedia pada tingkat kabupaten/kota. Akibatnya jumlah pengamatan sangat kecil, sehingga hasil perlu diposisikan sebagai **kategorisasi deskriptif** (pengelompokan untuk memudahkan penafsiran), bukan sebagai penemuan pola tersembunyi yang diuji secara statistik.
- **Mengapa K = 3?** Nilai K dipilih agar menghasilkan tiga tipologi yang mudah ditafsirkan (padat dan mahal, berkembang, perintis). Pada lima pengamatan, prosedur pemilihan K seperti metode siku (*elbow*) atau skor siluet tidak memberikan dasar yang kuat, dan perhitungan tersebut tidak dilakukan dalam kode.
- **Alternatif yang tidak diuji.** Pengelompokan hierarki (*hierarchical clustering*) juga dapat diterapkan pada lima pengamatan dan diperkirakan menghasilkan pengelompokan serupa. K-Means dipertahankan karena sederhana, menghasilkan pusat kelompok, dan modelnya dapat disimpan untuk digunakan kembali.

#### 3.2.6 Keterbatasan
1. Dua dari tiga kelompok beranggotakan satu wilayah, sehingga kelompok-kelompok tersebut pada dasarnya menandai wilayah yang sangat berbeda dari lainnya.
2. Sleman terpisah dari Bantul antara lain karena rasio kompetitor berbasis OSM yang tinggi (1.393 titik, terbanyak). Hal ini dapat mencerminkan kelengkapan pemetaan OSM di Sleman, bukan semata persaingan yang lebih ketat.
3. Tidak ada metrik validasi pengelompokan (inersia, siluet) yang dilaporkan.

---

### 3.3 Pilar 3: Peramalan Tren Pertumbuhan Sektor

#### 3.3.1 Tujuan dan keluaran
Memperkirakan jumlah unit usaha tiap sektor untuk tahun **2024–2026** beserta interval ketidakpastian 95%, dan mengklasifikasikan arah tren (Naik, Stabil, Turun). Keluaran: `hasil_forecasting_sektor.csv`, berisi baris historis (2019–2023) dan baris proyeksi (2024–2026) untuk tiap sektor.

#### 3.3.2 Data
Deret waktu tingkat DIY per sektor (Bagian 2.5), lima titik per sektor.

#### 3.3.3 Metode: regresi tren linear dengan kuadrat terkecil biasa (OLS)
Model: `Ŷ(t) = β₀ + β₁·t`, dengan t adalah tahun, β₀ adalah intersep, dan β₁ adalah kemiringan (pertambahan unit usaha per tahun). Parameter ditaksir dengan menarik satu garis lurus yang meminimalkan jumlah kuadrat selisih antara data dan garis (*Ordinary Least Squares*). Garis tersebut kemudian diperpanjang (ekstrapolasi) untuk tahun 2024, 2025, dan 2026.

Interval prediksi 95% dihitung dari galat baku regresi:

```
s = akar( jumlah kuadrat residual ÷ (n − 2) )
margin(t) = nilai kritis t × s × akar( 1 + 1/n + (t − t_rata-rata)² ÷ Σ(t_i − t_rata-rata)² )
interval = Ŷ(t) ± margin(t)
```

Suku di bawah akar membuat interval **semakin lebar untuk tahun yang makin jauh dari data**.

**Penentuan arah tren (sesuai kode):**
- *Naik (Ekspansif):* rata-rata pertumbuhan tahunan historis lebih dari +1% dan kemiringan positif.
- *Turun (Kontraksi):* rata-rata pertumbuhan kurang dari −1% dan kemiringan negatif.
- *Stabil:* selain kedua kondisi di atas.

#### 3.3.4 Perhitungan ilustratif: sektor kafe
Data: 1.970; 1.910; 2.070; 2.300; 2.590 (2019–2023).
- Rata-rata data = 2.168; rata-rata tahun = 2021; Σ(t − t̄)² = 10.
- Kemiringan β₁ = **+163 unit per tahun**. Proyeksi: 2024 ≈ 2.657; 2025 ≈ 2.820; 2026 ≈ 2.983.
- R² = 0,855: garis menjelaskan 85,5% variasi data.
- Jumlah kuadrat residual ≈ 45.190; dengan derajat kebebasan 3, s ≈ 122,7.
- Untuk 2026 (selisih tahun 5 dari rata-rata), akar(1 + 0,2 + 25/10) ≈ 1,924. Dengan nilai kritis 2,57 (nilai yang digunakan kode), margin ≈ 607, sehingga interval 2.376 hingga 3.590, sesuai berkas hasil.

**Ringkasan seluruh sektor** (dari berkas hasil dan perhitungan ilustratif):

| Sektor | Kemiringan (unit/tahun) | Rata-rata YoY | R² | Proyeksi 2026 (interval 95%) | Label tren |
|---|---|---|---|---|---|
| Kafe | +163,0 | +7,3% | 0,855 | 2.983 (2.376–3.590) | Naik (Ekspansif) |
| Restoran | +230,0 | +3,3% | 0,776 | 7.630 (6.515–8.745) | Naik (Ekspansif) |
| Minimarket | +56,5 | +3,1% | 0,966 | 2.088 (1.992–2.183) | Naik (Ekspansif) |
| Laundry | +59,0 | +3,8% | 0,726 | 1.707 (1.379–2.035) | Naik (Ekspansif) |
| Kelontong | −73,0 | −0,6% | 0,999 | 11.489 (11.473–11.505) | Stabil |

Kelontong memperoleh label "Stabil" karena rata-rata penurunannya (sekitar −0,6% per tahun) belum melewati ambang −1%, sehingga penurunan yang pelan namun konsisten tetap berlabel stabil menurut aturan tersebut.

#### 3.3.5 Mengapa regresi linear, bukan ARIMA, SARIMA, atau Prophet?
- **ARIMA/SARIMA** memodelkan ketergantungan antar-pengamatan (autokorelasi) dan pola musiman melalui beberapa parameter. Penaksiran parameter tersebut membutuhkan deret yang panjang, umumnya puluhan titik. Dengan lima titik, model berisiko menyesuaikan diri terhadap fluktuasi kebetulan.
- **Pola musiman tidak dapat dimodelkan.** Data bersifat tahunan sehingga tidak merekam pola dalam tahun (misalnya Ramadan atau musim liburan). Penambahan komponen musiman tanpa data pendukung justru menambah risiko *overfitting*.
- **Regresi linear** hanya menaksir dua parameter, sehingga paling aman terhadap *overfitting* pada data yang sangat pendek.
- **Status hasil.** Model ini disebut *baseline* eksploratif. Pengujian model lanjutan dijadwalkan setelah data yang lebih panjang tersedia.

#### 3.3.6 Subbagian: *bias–variance tradeoff* dan alasan tidak menambah prediktor

**Konsep.** Galat prediksi sebuah model dapat dipecah menjadi dua sumber utama.
- **Bias** adalah galat akibat model yang terlalu sederhana sehingga tidak menangkap pola nyata. Garis lurus tidak dapat menangkap kenaikan yang melengkung.
- **Varians** adalah galat akibat model yang terlalu fleksibel sehingga ikut menyesuaikan diri pada fluktuasi acak (*noise*). Model tersebut sangat cocok pada data yang dipakai untuk melatihnya, tetapi meleset pada data baru. Kondisi ini disebut *overfitting*.

Menambah kerumitan model (misalnya menambah prediktor) menurunkan bias tetapi menaikkan varians. Titik keseimbangan bergantung pada **perbandingan antara jumlah parameter yang harus ditaksir dan jumlah data yang tersedia**.

**Rasio parameter terhadap data pada proyek ini.**

| Model | Jumlah parameter | Jumlah titik data | Sisa derajat kebebasan |
|---|---|---|---|
| Regresi tren (digunakan) | 2 | 5 | 3 |
| + 1 prediktor (misalnya pertumbuhan PDRB) | 3 | 5 | 2 |
| + 2 prediktor (PDRB dan pertumbuhan UMKM) | 4 | 5 | 1 |
| + 3 prediktor (PDRB, UMKM, Google Trends) | 5 | 5 | **0** |

Derajat kebebasan galat (*residual degrees of freedom*) adalah jumlah data dikurangi jumlah parameter. Ketika sisa derajat kebebasan mencapai nol, model dapat melewati setiap titik data secara persis sehingga galat pada data pelatihan nol dan R² mencapai 100%. Hal itu bukan bukti akurasi, melainkan tanda model menghafal data. Pada kondisi tersebut tidak ada informasi tersisa untuk menaksir ketidakpastian, karena galat baku regresi dihitung dengan membagi jumlah kuadrat residual dengan sisa derajat kebebasan.

**Tiga alasan tambahan penambahan prediktor tidak dilakukan:**
1. **Kolinearitas dengan waktu.** PDRB, jumlah UMKM, dan indikator tren umumnya meningkat dari tahun ke tahun, sama seperti jumlah usaha sektor. Model tidak dapat membedakan pengaruh prediktor dari pengaruh tren waktu itu sendiri, sehingga koefisien menjadi tidak stabil.
2. **Kebutuhan nilai prediktor di masa depan.** Untuk meramal 2024–2026, nilai prediktor pada tahun-tahun tersebut juga harus diramal. Galat peramalan prediktor menumpuk ke galat peramalan sektor.
3. **Keterbatasan data.** Total UMKM DIY hanya tersedia pada tingkat provinsi (2021–2025) dan skor Google Trends hanya tersedia untuk 2021–2023, sehingga tidak sepanjang deret utama 2019–2023.

**Peran data eksternal.** Data tersebut digunakan sebagai **narasi pendukung kualitatif pada kesimpulan**, bukan sebagai masukan model. Contoh: total UMKM DIY naik dari 337.060 (2021) menjadi 347.744 (2025), atau sekitar 3,2% selama empat tahun (kurang lebih 0,8% per tahun). Sementara itu, jumlah kafe tumbuh rata-rata sekitar 7% per tahun pada 2019–2023. Pernyataan yang dapat diambil: pertumbuhan kafe tampak lebih cepat daripada pertumbuhan total UMKM sehingga arah naik konsisten dengan gambaran umum. Perlu dicatat bahwa periode kedua angka berbeda; pernyataan tersebut bersifat narasi, bukan bukti kuantitatif.

**Rencana lanjutan.** Penambahan kovariat dapat diuji pada tahap berikutnya apabila deret data lebih panjang atau tersedia data tingkat wilayah, disertai validasi yang memadai (misalnya pengujian pada data yang tidak dipakai melatih).

#### 3.3.7 Uji ketahanan *leave-one-out* (belum diimplementasikan)

**Status.** Pengujian ini **belum dikerjakan di dalam kode proyek**. Bagian ini menjelaskan konsepnya dan memuat hasil perhitungan manual ilustratif.

**Konsep.** Kemiringan garis dihitung ulang sebanyak lima kali dengan membuang satu tahun secara bergantian, lalu hasilnya dibandingkan dengan kemiringan penuh.
- Apabila kemiringan relatif tidak berubah, tren dinilai **kokoh** (tidak bergantung pada satu tahun tertentu).
- Apabila kemiringan berayun jauh atau berganti tanda, tren dinilai **rapuh** (bergantung pada satu atau dua titik) dan hal tersebut harus dinyatakan sebagai keterbatasan.

**Perhitungan ilustratif.**
- **Kafe** (kemiringan penuh +163): membuang 2019 menghasilkan ± +227; membuang 2020 ± +149; membuang 2021 ± +163; membuang 2022 ± +167; membuang 2023 ± +115. Seluruhnya positif, tetapi besarnya berayun antara 115 dan 227. Tafsir: **arah naik kokoh, besaran kecepatan kenaikan kurang pasti**.
- **Kelontong** (kemiringan penuh −73): hasil berkisar sekitar −72,6 hingga −74,0. Tafsir: **sangat kokoh**, karena data mendekati garis lurus.

**Implikasi.** Kesimpulan arah (kafe naik, kelontong turun) aman, sedangkan nilai tepat proyeksi (misalnya 2.983 kafe pada 2026) kurang aman. Hal ini menjadi alasan hasil Pilar 3 disajikan sebagai **sinyal arah**, bukan sebagai angka prediksi mutlak.

#### 3.3.8 Metrik evaluasi: cara menafsirkan
- **R²** menyatakan proporsi variasi data yang dijelaskan garis (nilai pada tabel di atas).
- **MAPE** (*Mean Absolute Percentage Error*) adalah rata-rata persentase selisih absolut antara data dan nilai model; **RMSE** (*Root Mean Squared Error*) adalah akar rata-rata kuadrat selisih dalam satuan data.
- Kedua metrik dihitung pada data yang sama dengan data yang dipakai membentuk garis (*in-sample*). Metrik tersebut mengukur kecocokan pada masa lalu, bukan akurasi masa depan. Garis yang disesuaikan ke lima titik hampir pasti tampak baik sehingga nilai R² tinggi tidak boleh dianggap sebagai pembuktian ketepatan ramalan.

#### 3.3.9 Keterbatasan
1. Lima titik data per sektor dan angka 2023 yang masih sementara.
2. Garis lurus tidak menangkap perubahan nonlinear, seperti pemulihan pasca-pandemi.
3. Nilai kritis distribusi t yang digunakan dalam kode adalah 2,57 (pendekatan), sedangkan untuk derajat kebebasan 3 nilai eksak adalah 3,182. Konsekuensinya, interval yang dilaporkan sedikit lebih sempit daripada interval eksak (untuk kafe 2026: sekitar 2.232–3.734 dengan nilai eksak).
4. Peramalan dilakukan pada tingkat DIY; tidak ada proyeksi per wilayah.

---

### 3.4 Pilar 4: Mesin Rekomendasi Personal

#### 3.4.1 Tujuan dan sifat
Pilar 4 menerima masukan pengguna dan menyusun rekomendasi dengan membaca hasil Pilar 1, 2, dan 3. Pilar ini bukan model pembelajaran mesin, melainkan **sistem berbasis aturan** (pencarian tabel dan percabangan logika) yang diimplementasikan sebagai kelas `UMKMRecommender` pada `models/04_rekomendasi.py`. Ia merupakan satu-satunya pilar yang beroperasi saat pengguna menggunakan sistem (*real-time inference*) dan tidak menghitung ulang dari data mentah.

#### 3.4.2 Masukan dan keluaran
- **Masukan:** sektor (lima pilihan), wilayah (spesifik atau terbuka), dan anggaran sewa tahunan (opsional).
- **Keluaran (wilayah spesifik):** skor dan kategori, label kelompok wilayah dan deskripsinya, arah tren sektor, estimasi sewa tahunan, status anggaran, peringatan kejenuhan (bila ada), dan narasi rekomendasi.
- **Keluaran (wilayah terbuka):** daftar seluruh wilayah terurut dari skor tertinggi, dengan tiga teratas sebagai rekomendasi utama beserta tanda kecukupan anggaran.

#### 3.4.3 Logika
1. **Pencarian skor** pada tabel Pilar 1 berdasarkan sektor (dan wilayah).
2. **Penambahan konteks wilayah** dari tabel Pilar 2 (label dan deskripsi kelompok).
3. **Penambahan arah tren** dari tabel Pilar 3. Label tren bersifat tingkat sektor se-DIY: kafe, restoran, minimarket, dan laundry berlabel Naik (Ekspansif); kelontong berlabel Stabil.
4. **Pemeriksaan anggaran.** Estimasi sewa tahunan = tarif sewa per m² × 30 m² (asumsi luas ruko standar UMKM yang ditetapkan peneliti). Bila anggaran lebih kecil daripada estimasi, status "Kurang" dan disertai catatan; bila cukup, status "Mencukupi".
5. **Peringatan kejenuhan** diberikan bila rasio kompetitor sektor lebih dari 0,20 gerai per 1.000 jiwa.
6. **Perankingan** bila wilayah terbuka: seluruh wilayah diurutkan berdasarkan skor.

Estimasi sewa tahunan 30 m² per wilayah: Kota Yogyakarta Rp25.500.000; Sleman Rp21.750.000; Bantul Rp13.500.000; Kulon Progo Rp8.250.000; Gunungkidul Rp6.600.000.

#### 3.4.4 Contoh keluaran
**Skenario 1: kafe di Sleman, anggaran Rp30.000.000 per tahun.**
- Skor 56,7; kategori Cukup Layak.
- Kelompok wilayah: Pasar Berkembang & Biaya Menengah.
- Tren sektor: Naik (Ekspansif).
- Estimasi sewa 30 m²: Rp21.750.000; anggaran mencukupi. Dengan tarif Rp725.000 per m², anggaran tersebut setara luas sekitar 41 m².
- Rasio kompetitor kafe Sleman 0,1695 per 1.000 jiwa, di bawah ambang 0,20, sehingga tidak ada peringatan kejenuhan.

**Skenario 2: kafe, wilayah terbuka.** Tiga teratas: Kota Yogyakarta (71,0; Layak), Sleman (56,7; Cukup Layak), dan Bantul (55,59; Cukup Layak). Untuk Kota Yogyakarta, rasio kompetitor kafe 0,2919 melampaui ambang sehingga sistem menampilkan peringatan kejenuhan.

**Skenario 3: laundry, wilayah terbuka.** Urutan: Kota Yogyakarta (81,5), Sleman (51,81), Gunungkidul (50,18), Kulon Progo (48,66), Bantul (46,14). Keunggulan Kota Yogyakarta sebagian dipengaruhi oleh nol laundry pada data OSM.

#### 3.4.5 Keputusan metodologis dan keterbatasan
- **Mengapa berbasis aturan:** seluruh komputasi berat telah diselesaikan pada Pilar 1–3. Pilar 4 hanya menggabungkan hasil sehingga ringan, deterministik, dan tidak membangkitkan angka baru yang tidak dapat ditelusuri.
- **Sifat *stateless*:** setiap permintaan dihitung secara terpisah dan tidak bergantung pada permintaan sebelumnya.
- **Asumsi luas 30 m²** ditetapkan peneliti; luas ruko riil dapat berbeda.
- **Label tren tingkat DIY:** tidak membedakan tren antar wilayah.
- **Tidak ada validasi terhadap keberhasilan usaha nyata:** rekomendasi merupakan alat bantu pertimbangan, bukan jaminan.

---

## 4. Keterkaitan Antar Pilar dan Contoh Alur Menyeluruh

Hubungan antar pilar:
- **Pilar 1, 2, dan 3 berdiri sendiri** dan dapat dijalankan paralel secara komputasi. Masing-masing menyimpan hasil sebagai CSV.
- **Pilar 4** adalah lapisan akhir yang membaca ketiga CSV tersebut untuk menjawab pertanyaan spesifik pengguna.
- Pilar 1 menjawab "seberapa layak", Pilar 2 menjawab "seperti apa karakter wilayahnya", Pilar 3 menjawab "ke mana arah sektornya", dan Pilar 4 menyatukan ketiganya dalam satu rekomendasi yang disesuaikan dengan anggaran.

Contoh alur menyeluruh (kafe di Sleman, anggaran Rp30 juta):

| Tahap | Sumber | Informasi yang diambil |
|---|---|---|
| 1. Skor | `hasil_skoring_sektor.csv` | 56,7; Cukup Layak; rasio kompetitor 0,1695 |
| 2. Konteks | `hasil_clustering_wilayah.csv` | Pasar Berkembang & Biaya Menengah |
| 3. Tren | `hasil_forecasting_sektor.csv` | Naik (Ekspansif); proyeksi 2026 sekitar 2.983 unit se-DIY |
| 4. Anggaran | `biaya_operasional` (melalui tabel skor) | Sewa 30 m² Rp21.750.000; anggaran mencukupi |
| 5. Peringatan | Aturan ambang 0,20 | Tidak ada peringatan kejenuhan |
| 6. Narasi | Penggabungan | Kartu rekomendasi |

---

## 5. Arsitektur Implementasi dan Rencana Antarmuka

### 5.1 Struktur dan Cara Menjalankan
```
python scripts/run_all_pipelines.py      # pembersihan data (Dataset 1-5)
python models/run_all_models.py          # Pilar 1, 2, 3 + uji Pilar 4
python models/04_rekomendasi.py --sektor cafe --wilayah sleman --budget 30000000
```
Catatan teknis: nama berkas pada `models/` diawali angka (`01_skoring.py` dan seterusnya) sehingga tidak dapat diimpor dengan pernyataan `import` biasa. Pemanggilan dari program lain (misalnya prototipe Streamlit) menggunakan `importlib.import_module("models.04_rekomendasi")`, seperti pada `models/run_all_models.py`.
Pipeline data memakai data OSM mentah lokal secara bawaan (tanpa mengunduh ulang dari API), sehingga dapat dijalankan ulang secara cepat dan konsisten.

### 5.2 Prinsip Antarmuka (rencana)
1. **Hanya-baca (*read-only*).** Antarmuka tidak menjalankan ulang pengambilan data atau pelatihan model.
2. **Respons cepat.** Karena komputasi telah selesai, antarmuka cukup memuat CSV dan memanggil `UMKMRecommender`.
3. **Menu yang direncanakan:** Beranda (ringkasan masalah dan angka kunci); Peta dan Klaster Wilayah (Pilar 2); Skoring Kelayakan (Pilar 1, tabel dengan filter dan diagram batang); Forecasting Tren (Pilar 3, grafik garis); dan Coba Rekomendasi (Pilar 4, formulir masukan).

### 5.3 Tahapan Teknologi (rencana)
- **Prototipe (folder `prototype/`): Streamlit.** Kerangka kerja Python untuk membangun aplikasi web data secara cepat. Karena seluruh logika proyek berbahasa Python, prototipe dapat langsung mengimpor kelas `UMKMRecommender` tanpa lapisan tambahan.
- **Situs final (folder `media/`): Laravel (PHP).** Kerangka kerja web berbahasa PHP. Karena logika analitik berbahasa Python, situs final perlu mengakses hasil analisis melalui salah satu cara: (a) membaca langsung berkas CSV hasil Pilar 1–3 dan mereplikasi logika aturan Pilar 4 di sisi PHP, atau (b) memanggil layanan Python (misalnya API tipis) yang membungkus `UMKMRecommender`. Pemilihan pendekatan merupakan keputusan rancangan yang belum ditetapkan. Pendekatan (a) lebih sederhana mengingat Pilar 4 hanya berupa pencarian tabel dan aturan sederhana.

---

## 6. Keterbatasan dan Arah Pengembangan

### 6.1 Keterbatasan Utama
1. **Bobot skor ditetapkan peneliti** dan belum diuji sensitivitasnya.
2. **Granularitas data wilayah.** Data ekonomi dan sewa hanya tersedia pada tingkat kabupaten/kota; sistem tidak membedakan lokasi di dalam satu wilayah.
3. **Kelengkapan OSM tidak merata** dan rendah untuk usaha informal; angka nol pada OSM tidak berarti ketiadaan pesaing.
4. **Satu angka sewa per wilayah** tidak menggambarkan variasi antar lokasi.
5. **Jumlah wilayah yang kecil (n = 5)** membatasi kekuatan statistik pengelompokan.
6. **Peramalan hanya berdasarkan lima titik** dengan angka 2023 sementara; hasil bersifat sinyal arah.
7. **Tidak ada validasi terhadap keberhasilan usaha nyata** karena data label tidak tersedia.
8. **Uji ketahanan leave-one-out dan uji sensitivitas bobot belum dilaksanakan.**
9. **Asumsi luas ruko 30 m²** bersifat tunggal untuk semua sektor.

### 6.2 Arah Pengembangan
- Menguji sensitivitas bobot (misalnya variasi bobot ±5 poin) dan melaporkan stabilitas peringkat.
- Menerapkan uji *leave-one-out* pada Pilar 3 dan menyajikan hasilnya.
- Memperpanjang deret waktu dan menguji model lanjutan (ARIMA/SARIMA, Prophet) serta kovariat dengan validasi pada data uji.
- Mencari data tingkat kecamatan atau data transaksi sewa untuk meningkatkan granularitas.
- Memperlengkapi data usaha informal melalui sumber tambahan.
- Menghitung metrik validasi pengelompokan (inersia, siluet) bila jumlah pengamatan bertambah.

---

## 7. Pertanyaan yang Mungkin Diajukan Penguji

**1. Mengapa proyek ini tidak menggunakan pembelajaran mesin terawasi?**
Pembelajaran terawasi memerlukan label target, misalnya keberhasilan atau kegagalan usaha pada suatu lokasi. Data publik yang digunakan bersifat agregat pada tingkat wilayah dan tidak memuat label tersebut. Pembuatan label buatan hanya akan mereproduksi asumsi penyusun. Oleh karena itu digunakan MCDA yang transparan, pengelompokan tak terawasi, dan regresi tren.

**2. Bagaimana bobot pada MCDA ditentukan, dan apakah telah diuji sensitivitasnya?**
Bobot ditetapkan berdasarkan penalaran peneliti: daya beli (PDRB dan pengeluaran) dianggap penentu terciptanya transaksi sehingga berbobot total 50%; kepadatan 15%; kompetitor 15%; sewa 10%; dan rasio UMKM 10%. Bobot tidak dipelajari dari data. Uji sensitivitas bobot belum dilakukan dan dicatat sebagai langkah lanjutan.

**3. Mengapa skor antar sektor dalam satu wilayah relatif berdekatan?**
Hanya jumlah kompetitor yang berbeda antar sektor; kriteria lain bernilai sama dalam satu wilayah. Karena bobot kompetitor 0,15, selisih antar sektor dalam satu wilayah maksimal sekitar 10,5 poin. Skor karenanya lebih mencerminkan kekuatan wilayah.

**4. Mengapa Kota Yogyakarta hampir selalu berskor tinggi?**
Kota Yogyakarta tertinggi pada PDRB dan pengeluaran, yang berbobot total 50%. Selain itu, pada sektor yang titiknya nol pada OSM (laundry dan kelontong), nilai kompetitor nol menaikkan skor. Hal ini dicatat sebagai keterbatasan data, bukan peluang nyata.

**5. Apakah K-Means dengan lima pengamatan dapat dipertanggungjawabkan?**
Secara statistik kekuatannya terbatas. Pengelompokan dilakukan pada tingkat kabupaten/kota karena data ekonomi hanya tersedia pada tingkat tersebut. Hasilnya diposisikan sebagai kategorisasi deskriptif. Jumlah kelompok K = 3 dipilih agar menghasilkan tipologi yang mudah ditafsirkan, bukan hasil optimasi.

**6. Apa fungsi PCA dan apa arti 94,09%?**
PCA merangkum enam variabel menjadi dua sumbu agar dapat divisualisasikan. Angka 94,09% menunjukkan bahwa dua sumbu tersebut menyimpan sekitar 94% variasi antar wilayah sehingga diagram dua dimensi tidak menyesatkan. PCA hanya untuk visualisasi, sedangkan K-Means dihitung dari enam variabel terstandardisasi.

**7. Mengapa peramalan menggunakan regresi linear, bukan ARIMA atau SARIMA?**
Hanya terdapat lima titik tahunan per sektor. ARIMA/SARIMA memerlukan deret yang jauh lebih panjang untuk menaksir parameternya, dan dengan lima titik model cenderung menghafal fluktuasi kebetulan. Regresi linear hanya menaksir dua parameter. Data tahunan juga tidak merekam pola musiman. Hasilnya diposisikan sebagai *baseline* dan sinyal arah.

**8. Mengapa tidak menambahkan prediktor seperti PDRB atau pertumbuhan UMKM ke model peramalan, padahal datanya tersedia?**
Setiap prediktor menambah satu parameter yang harus ditaksir, sedangkan data hanya lima titik. Model saat ini memiliki dua parameter, menyisakan tiga derajat kebebasan untuk menaksir galat. Dengan tiga prediktor tambahan, parameter menjadi lima untuk lima titik; sisa derajat kebebasan nol sehingga model dapat melewati semua titik secara sempurna, yang berarti menghafal, bukan belajar, dan cenderung meleset pada tahun baru. Selain itu, prediktor tersebut ikut meningkat seiring waktu sehingga pengaruhnya tidak dapat dipisahkan dari tren waktu, dan untuk meramal 2024–2026 prediktor itu sendiri harus diramal sehingga galat menumpuk. Karena itu data eksternal digunakan sebagai narasi pendukung pada kesimpulan, bukan masukan model. Penambahan kovariat dapat diuji bila deret lebih panjang dengan validasi yang memadai.

**9. Apakah nilai R² yang tinggi menjamin ramalan akurat? Bagaimana ketahanan tren diuji?**
Tidak. R² dihitung pada data yang sama dengan data pembentuk garis (in-sample), sehingga garis yang disesuaikan ke lima titik hampir pasti tampak baik. Untuk menilai ketahanan tren, pendekatan yang tepat adalah uji *leave-one-out*, yaitu menghitung ulang kemiringan dengan membuang satu tahun secara bergantian. Pengujian ini belum diimplementasikan dalam kode. Perhitungan manual pada sektor kafe menunjukkan kemiringan tetap positif pada setiap pembuangan (sekitar +115 hingga +227 unit per tahun), sehingga arah naik cukup kokoh, tetapi besarannya kurang pasti. Karena itu hasil disajikan sebagai sinyal arah.

**10. Mengapa data toko kelontong pada OSM hampir tidak ada dan apa dampaknya?**
Warung rumahan skala mikro jarang mendaftarkan diri pada peta digital, dan kontributor OSM sering menandainya sebagai minimarket. Untuk melengkapi, digunakan data SiBakul (rasio UMKM per 1.000 penduduk) sebagai penanda kejenuhan tingkat wilayah. Dampak yang masih ada: skor kelontong menggunakan nol kompetitor sehingga tidak mencerminkan kondisi nyata dan perlu ditafsirkan dengan hati-hati. Peramalan kelontong tidak terpengaruh karena memakai data BPS.

**11. Bagaimana mesin rekomendasi bekerja, dan dari mana asumsi 30 m²?**
Mesin hanya membaca tabel hasil Pilar 1 sampai 3, memeriksa kecukupan anggaran terhadap estimasi sewa, memberikan peringatan kejenuhan, dan menyusun peringkat. Luas 30 m² adalah asumsi ukuran ruko standar UMKM yang ditetapkan peneliti untuk membandingkan anggaran pengguna dengan estimasi sewa tahunan.

**12. Apa keterbatasan terbesar sistem ini?**
Pertama, bobot skor ditetapkan peneliti. Kedua, data ekonomi dan sewa hanya tingkat kabupaten/kota. Ketiga, OSM tidak lengkap untuk usaha informal. Keempat, peramalan hanya berdasar lima titik. Kelima, tidak ada validasi terhadap keberhasilan usaha nyata. Sistem ini adalah alat bantu pertimbangan, bukan jaminan keberhasilan usaha.

---

## Lampiran A. Glosarium Istilah

Entri disusun menurut abjad. Contoh dari proyek diberikan bila relevan.

**ADHB (Atas Dasar Harga Berlaku).** Penghitungan nilai ekonomi dengan harga pada tahun yang bersangkutan. Lawannya ADHK (Atas Dasar Harga Konstan), yang memakai harga tahun dasar untuk menghilangkan pengaruh inflasi. Proyek ini memakai PDRB per kapita ADHB.

**API (Application Programming Interface).** Antarmuka yang memungkinkan satu program meminta data atau layanan dari program lain melalui aturan yang telah ditentukan. Contoh: skrip proyek mengirim kueri ke Overpass API untuk memperoleh data usaha dari OpenStreetMap, tanpa membuka situs peta secara manual.

**ARIMA / SARIMA.** *AutoRegressive Integrated Moving Average* adalah keluarga model deret waktu yang memanfaatkan hubungan antara nilai sekarang dan nilai-nilai sebelumnya. SARIMA menambahkan komponen musiman. Model ini memerlukan deret data yang panjang untuk menaksir parameternya.

**Autokorelasi.** Korelasi antara nilai suatu deret waktu dengan nilai-nilainya pada waktu sebelumnya. Merupakan dasar model ARIMA.

**Baseline.** Model pembanding paling sederhana yang dijadikan titik awal. Regresi tren linear pada Pilar 3 disebut *baseline* karena model lanjutan diharapkan diuji terhadapnya.

**Batch (pemrosesan batch).** Perhitungan yang dijalankan sekali pada seluruh data, dan hasilnya disimpan untuk digunakan kemudian. Pilar 1, 2, dan 3 bersifat batch. Lawannya *real-time*, yaitu perhitungan yang dijalankan saat pengguna meminta, seperti Pilar 4.

**Bias dan varians (*bias–variance tradeoff*).** Dua sumber galat model. Bias adalah galat akibat model terlalu sederhana; varians adalah galat akibat model terlalu peka terhadap fluktuasi acak data pelatihan. Menurunkan satu cenderung menaikkan yang lain. Lihat Bagian 3.3.6.

**BFR (*Budget Feasibility Ratio*).** Rasio kecukupan anggaran, yaitu anggaran sewa pengguna dibandingkan estimasi sewa tahunan untuk luas ruko acuan (30 m²). Nilai satu atau lebih berarti anggaran memadai. Pada kode produksi, perbandingan ini diwujudkan sebagai status "Mencukupi" atau "Kurang".

**Bounding box.** Persegi panjang geografis yang dibatasi oleh lintang minimum dan maksimum serta bujur minimum dan maksimum. Dipakai untuk membatasi area pencarian kueri dan menandai wilayah. Contoh: bounding box DIY: lintang −8,25 sampai −7,50 dan bujur 110,00 sampai 110,85.

**BPS (Badan Pusat Statistik).** Lembaga pemerintah nonkementerian yang menyelenggarakan statistik resmi di Indonesia. BPS Provinsi DIY adalah sumber data PDRB, pengeluaran, kepadatan penduduk, dan jumlah unit usaha.

**CAGR (*Compound Annual Growth Rate*).** Laju pertumbuhan tahunan majemuk antara dua titik waktu: `(nilai akhir ÷ nilai awal)^(1/jumlah tahun) − 1`. Menggambarkan laju pertumbuhan rata-rata per tahun secara berbunga.

**Centroid (pusat kelompok).** Titik rata-rata seluruh anggota sebuah kelompok pada ruang variabel. Dalam K-Means, centroid digeser berulang kali sampai posisinya stabil.

**Clustering (pengelompokan).** Pembagian objek ke dalam kelompok sehingga objek dalam satu kelompok lebih mirip satu sama lain daripada dengan objek kelompok lain, tanpa menggunakan label. Contoh: lima kabupaten/kota dibagi menjadi tiga kelompok karakter pasar.

**Convenience store.** Toko serba ada skala kecil (minimarket). Pada OSM ditandai `shop=convenience`.

**CSV (*Comma-Separated Values*).** Format berkas teks untuk data tabel, dengan nilai dipisahkan koma. Seluruh hasil proyek disimpan dalam CSV.

**Data panel.** Data yang merekam banyak entitas pada banyak titik waktu. Dataset 4 adalah data panel: 5 sektor × 5 wilayah × 5 tahun = 125 baris.

**DataFrame.** Struktur tabel dua dimensi (baris dan kolom) pada pustaka `pandas` untuk pengolahan data dalam Python.

**Decision Support System (Sistem Pendukung Keputusan).** Sistem berbasis komputer yang membantu pengambil keputusan dengan informasi dan analisis, tanpa menggantikan penilaian manusia. Proyek ini adalah sistem pendukung keputusan lokasi dan sektor UMKM.

**Decoupled (arsitektur terpisah).** Rancangan yang memisahkan komputasi berat dari penyajian. Antarmuka hanya membaca hasil yang sudah dihitung.

**Deduplikasi.** Penghapusan data ganda. Pada Dataset 1 dilakukan dua lapis: berdasarkan ID objek OSM dan berdasarkan koordinat yang dibulatkan.

**Derajat kebebasan (*degrees of freedom*).** Banyaknya informasi independen yang tersisa untuk menaksir ketidakpastian setelah parameter ditaksir. Pada regresi linear sederhana: jumlah data dikurangi jumlah parameter. Dengan 5 data dan 2 parameter tersisa 3. Bila 0, model tidak punya informasi untuk menaksir galat.

**Distribusi t (Student).** Distribusi peluang yang dipakai untuk menaksir interval kepercayaan ketika jumlah data kecil. Nilai kritisnya bergantung pada derajat kebebasan: semakin kecil, semakin besar nilainya. Untuk derajat kebebasan 3, nilai kritis dua sisi 95% adalah 3,182.

**Endpoint.** Alamat layanan pada sebuah API tempat permintaan dikirim. Proyek memakai tiga *endpoint* Overpass secara bergantian.

**ETL (*Extract, Transform, Load*).** Rangkaian pengambilan data dari sumber, transformasi (pembersihan dan penyeragaman), dan penyimpanan hasil. Lihat Bagian 2.1.

**Failover (server cadangan).** Peralihan otomatis ke server lain ketika server utama gagal. Pada pengambilan OSM, kode berganti ke server *mirror* pada percobaan ulang.

**Forecasting (peramalan).** Pendugaan nilai masa depan berdasarkan data historis.

**Geospasial.** Berkaitan dengan lokasi di permukaan bumi yang dinyatakan melalui koordinat.

**Google Trends / pytrends.** Google Trends adalah layanan yang menyajikan indeks minat pencarian (skala 0–100) untuk suatu kata kunci menurut waktu dan wilayah. `pytrends` adalah pustaka Python tidak resmi yang digunakan untuk mengambil data tersebut.

**Grid sampling.** Teknik membagi area pencarian menjadi sel-sel kecil agar setiap permintaan tidak terlalu berat. Risikonya, objek pada batas antar-sel dapat terunduh lebih dari sekali, sehingga diperlukan deduplikasi.

**HTTP 429 (*Too Many Requests*).** Kode respons server yang menyatakan permintaan terlalu sering (*rate limit*). **HTTP 504 (*Gateway Timeout*)** menyatakan server perantara tidak menerima jawaban tepat waktu. Kode proyek menanggapi 429 dengan menunggu dan 504 dengan kueri cadangan.

**Hierarchical clustering.** Pengelompokan yang membangun hierarki penggabungan objek. Alternatif K-Means yang tidak diuji pada proyek ini.

**Imputasi.** Pengisian nilai yang hilang dengan nilai perkiraan (rata-rata, median, dan sebagainya). Tidak diterapkan dalam pipeline proyek.

**In-sample dan out-of-sample.** *In-sample* berarti evaluasi pada data yang sama dengan data yang dipakai membentuk model; *out-of-sample* berarti evaluasi pada data yang tidak dipakai membentuk model. Hanya evaluasi *out-of-sample* yang menunjukkan kemampuan prediksi nyata.

**Inersia (WCSS).** Jumlah jarak kuadrat antar-anggota ke pusat kelompoknya (*Within-Cluster Sum of Squares*). Nilai yang lebih kecil berarti kelompok lebih rapat. K-Means meminimalkan inersia.

**Inner join dan left join.** Cara menggabungkan dua tabel. *Inner join* hanya mempertahankan baris yang kuncinya ada pada kedua tabel; *left join* mempertahankan seluruh baris tabel kiri dan mengisi nilai kosong bila tidak ada pasangan.

**Interval kepercayaan dan interval prediksi.** Interval kepercayaan menyatakan rentang untuk nilai rata-rata yang ditaksir; interval prediksi menyatakan rentang untuk nilai pengamatan tunggal di masa depan dan lebih lebar. Rumus interval 95% pada Pilar 3 sesungguhnya adalah interval prediksi.

**Joblib dan serialisasi.** Serialisasi adalah penyimpanan objek program (misalnya model terlatih) menjadi berkas agar dapat dimuat kembali tanpa pelatihan ulang. `joblib` adalah pustaka Python yang digunakan untuk menyimpan model dalam berkas `.joblib`.

**JSON (*JavaScript Object Notation*).** Format teks terstruktur untuk menyimpan data bersarang. Respons mentah Overpass API disimpan dalam berkas JSON.

**K-Means.** Algoritma pengelompokan yang membagi data menjadi K kelompok dengan meminimalkan jarak ke pusat kelompok. Lihat Bagian 3.2.3.

**KBLI (Klasifikasi Baku Lapangan Usaha Indonesia).** Sistem kode resmi untuk mengklasifikasikan jenis kegiatan usaha. Contoh: 561 untuk restoran dan 563 untuk penyedia minuman, 471 untuk perdagangan eceran, 962 untuk jasa perorangan seperti laundry.

**Kepadatan penduduk.** Jumlah penduduk per kilometer persegi. Dari kepadatan dan luas wilayah, penduduk diestimasi sebagai kepadatan × luas.

**Kolinearitas (multikolinearitas).** Kondisi ketika dua atau lebih variabel penjelas saling berkorelasi tinggi, sehingga pengaruh masing-masing sulit dipisahkan. Contoh: PDRB dan jumlah UMKM sama-sama naik seiring waktu.

**Kovariat / prediktor / regresor.** Variabel penjelas yang dimasukkan ke dalam model untuk menjelaskan variabel yang diramal. Pilar 3 tidak memakai kovariat.

**Kriteria benefit dan cost.** Pada MCDA, kriteria benefit meningkatkan skor ketika nilainya naik; kriteria cost menurunkan skor ketika nilainya naik.

**Label / ground truth.** Nilai target yang benar untuk setiap data pelatihan pada pembelajaran terawasi (misalnya "berhasil" atau "gagal"). Tidak tersedia pada proyek ini.

**Laravel.** Kerangka kerja (*framework*) pengembangan web berbahasa PHP. Direncanakan untuk situs final.

**Latensi.** Selang waktu antara permintaan dan jawaban sistem.

**Latitude dan longitude (lintang dan bujur).** Koordinat geografis. Proyek memakai sistem WGS84 (sistem koordinat standar yang juga digunakan GPS dan OSM). Lintang DIY bernilai negatif karena berada di selatan khatulistiwa.

**Leave-one-out.** Teknik uji ketahanan dengan menghitung ulang model sebanyak jumlah data, masing-masing dengan membuang satu data. Bila hasil stabil, model dinilai tahan; bila berayun, rapuh. Belum diimplementasikan pada proyek ini (Bagian 3.3.7).

**MAPE (*Mean Absolute Percentage Error*).** Rata-rata persentase selisih mutlak antara nilai model dan data. **RMSE (*Root Mean Squared Error*)** adalah akar dari rata-rata kuadrat selisih, dalam satuan data aslinya. **R² (koefisien determinasi)** adalah proporsi variasi data yang dijelaskan model (0 sampai 1).

**MCDA (*Multi-Criteria Decision Analysis*).** Kerangka penilaian alternatif berdasarkan banyak kriteria. Lihat Bagian 3.1.

**Mirror (server cermin).** Salinan layanan yang sama pada alamat berbeda. Dipakai sebagai cadangan.

**Min-max (normalisasi).** Penskalaan nilai ke rentang 0 sampai 1 dengan `(x − min) ÷ (maks − min)`.

**Node, way, dan relation (OSM).** Tiga tipe objek dasar OSM: *node* adalah titik tunggal, *way* adalah garis atau poligon (misalnya bangunan), dan *relation* menghubungkan beberapa objek (misalnya batas administratif). Proyek mengambil *node* dan *way*.

**Noise (derau).** Fluktuasi acak pada data yang bukan pola sebenarnya. Model yang terlalu fleksibel ikut mempelajari derau.

**OLS (*Ordinary Least Squares*, kuadrat terkecil biasa).** Metode penaksiran parameter regresi dengan meminimalkan jumlah kuadrat selisih antara data dan garis model.

**OpenStreetMap (OSM).** Basis data peta dunia yang dibangun secara sukarela oleh komunitas dan terbuka. Kelengkapan datanya bergantung pada kontributor.

**Overfitting dan underfitting.** *Overfitting* adalah kondisi model terlalu menyesuaikan diri pada data pelatihan sehingga buruk pada data baru; *underfitting* adalah kondisi model terlalu sederhana sehingga melewatkan pola nyata.

**Overpass API dan Overpass QL.** Overpass API adalah layanan kueri untuk membaca data OSM. Overpass QL adalah bahasa kueri yang dipakai. Contoh kueri proyek: memilih objek bertag `amenity=cafe` dalam area bernama "Sleman" dengan `admin_level=5`, lalu mengeluarkan koordinatnya (`out center`).

**PCA (*Principal Component Analysis*).** Teknik reduksi dimensi yang membentuk sumbu baru (komponen utama) sebagai kombinasi linear variabel asli untuk menangkap variasi sebanyak mungkin. *Variansi terjelaskan* adalah proporsi variasi total yang ditangkap komponen tertentu.

**PDRB (Produk Domestik Regional Bruto).** Total nilai tambah barang dan jasa yang dihasilkan suatu wilayah dalam periode tertentu. *PDRB per kapita* adalah PDRB dibagi jumlah penduduk, dipakai sebagai penanda skala dan kemakmuran ekonomi.

**Pengeluaran per kapita.** Rata-rata belanja penduduk per orang per bulan (makanan dan bukan makanan). Penanda daya beli.

**Pipeline.** Rangkaian tahap pemrosesan data yang berurutan dan dapat dijalankan ulang secara otomatis.

**POI (*Point of Interest*).** Titik lokasi yang bermakna pada peta, seperti restoran atau toko.

**Prophet.** Pustaka peramalan deret waktu yang dikembangkan Meta (Facebook), dirancang untuk deret dengan pola musiman. Direncanakan untuk diuji pada tahap lanjutan.

**Rasio per 1.000 penduduk.** Ukuran yang menyetarakan jumlah entitas terhadap besar penduduk agar wilayah berbeda ukuran dapat dibandingkan. Contoh: rasio kafe per 1.000 penduduk, rasio UMKM per 1.000 penduduk.

**Rate limiting dan backoff.** *Rate limiting* adalah pembatasan frekuensi permintaan oleh server. *Backoff* adalah strategi memperpanjang jeda setelah kegagalan. Pada kode proyek jeda ditambah secara bertahap (10 detik × nomor percobaan).

**Regresi linear.** Model yang menyatakan hubungan antara variabel dengan garis lurus. *Kemiringan (slope)* adalah perubahan nilai per satuan waktu; *intersep* adalah titik potong garis pada sumbu nilai; *residual* adalah selisih antara data dan nilai pada garis.

**Rule-based system (sistem berbasis aturan).** Sistem yang mengambil keputusan menggunakan aturan eksplisit (jika–maka) dan pencarian tabel, tanpa belajar dari data. Pilar 4 adalah sistem berbasis aturan.

**Seasonality (musiman).** Pola berulang dalam satu periode tetap, misalnya pola bulanan atau tahunan akibat liburan atau Ramadan. Tidak dapat dimodelkan dengan data tahunan.

**SiBakul.** Basis data UMKM Pemerintah Daerah DIY di bawah Dinas Koperasi dan UKM, sumber jumlah UMKM terdaftar.

**Stateless.** Sifat sistem yang memproses setiap permintaan secara independen tanpa menyimpan keadaan dari permintaan sebelumnya.

**Streamlit.** Kerangka kerja Python untuk membangun aplikasi web data secara cepat. Direncanakan untuk prototipe.

**Supervised dan unsupervised learning.** Pembelajaran terawasi memakai data berlabel untuk memprediksi target; pembelajaran tak terawasi mencari struktur pada data tanpa label (misalnya pengelompokan).

**Tag OSM.** Pasangan kunci=nilai yang mendeskripsikan objek pada OSM (misalnya `amenity=cafe`, `shop=laundry`).

**Time series (deret waktu).** Rangkaian pengamatan yang diurutkan menurut waktu.

**Tren.** Arah umum perubahan jangka panjang sebuah deret waktu, naik, turun, atau mendatar.

**UMKM (Usaha Mikro, Kecil, dan Menengah).** Kategori usaha berdasarkan kriteria modal usaha atau hasil penjualan tahunan yang diatur dalam UU No. 20 Tahun 2008 dan diperbarui melalui PP No. 7 Tahun 2021.

**Variansi dan simpangan baku.** Ukuran sebaran data di sekitar rata-ratanya. Simpangan baku adalah akar kuadrat dari variansi, dalam satuan data.

**Weighted Linear Combination (WLC).** Penjumlahan terbobot nilai kriteria untuk memperoleh skor akhir.

**YoY (*Year-over-Year*).** Perbandingan nilai suatu tahun dengan tahun sebelumnya: `(nilai_t − nilai_(t−1)) ÷ nilai_(t−1) × 100%`.

**Z-score (standardisasi).** Penskalaan nilai menjadi jumlah simpangan baku dari rata-rata: `(x − rata-rata) ÷ simpangan baku`. Hasilnya berrata-rata 0 dan simpangan baku 1.

---

## Lampiran B. Kamus Data

Berkas B.1 sampai B.4 berada di `data/cleaned/`. Berkas B.5 sampai B.7 (hasil analisis) berada di `outputs/hasil/`.

### B.1 `kompetitor_per_wilayah.csv` (2.796 baris)
| Kolom | Tipe | Keterangan | Contoh |
|---|---|---|---|
| `nama_tempat` | teks | Nama usaha; "Tanpa Nama" bila tidak tersedia | MARKO milk & coffee |
| `lat` | desimal | Lintang (WGS84) | −7,8012501 |
| `lon` | desimal | Bujur (WGS84) | 110,3441265 |
| `kategori` | teks | `restaurant`, `convenience`, `cafe`, `laundry`, `grocery` | cafe |
| `wilayah` | teks | `kota_yogyakarta`, `sleman`, `bantul`, `kulon_progo`, `gunungkidul` | bantul |

### B.2 `kondisi_ekonomi_wilayah.csv` (5 baris)
| Kolom | Keterangan | Satuan |
|---|---|---|
| `kabupaten_kota` | Nama wilayah (ejaan "Gunung Kidul") | teks |
| `pdrb_per_kapita` | PDRB per kapita ADHB 2024 | ribu rupiah |
| `kepadatan_penduduk` | Kepadatan 2024 | jiwa/km² |
| `luas_km2` | Luas wilayah | km² |
| `pengeluaran_per_kapita` | Pengeluaran sebulan per kapita 2024 | rupiah |
| `jumlah_umkm_2025` | UMKM terdaftar | unit |
| `rasio_umkm_per_1000_penduduk` | Rasio terhadap estimasi penduduk | per 1.000 jiwa |

### B.3 `biaya_operasional.csv` (5 baris)
Kolom: `wilayah`, `wilayah_label`, `harga_sewa_per_m2_tahun` (rupiah/m²/tahun), `kategori_biaya` (Tinggi, Menengah, Terjangkau), `sumber`, `tahun` (2024).

### B.4 `tren_sektor.csv` (125 baris)
Kolom: `wilayah`, `wilayah_label`, `sektor_usaha`, `kbli`, `tahun` (2019–2023), `jumlah_usaha` (unit), `pertumbuhan_tahunan_unit`, `pertumbuhan_tahunan_pct`, `google_trends_score` (skala 0–100; terisi 2021–2023).

### B.5 `hasil_skoring_sektor.csv` (25 baris)
Kolom: `sektor`, `sektor_label`, `wilayah`, `wilayah_label`, `jumlah_kompetitor`, `rasio_kompetitor_per_1000`, `pdrb_per_kapita`, `pengeluaran_per_kapita`, `harga_sewa_per_m2_tahun`, `rasio_umkm_total_per_1000`, `skor` (0–100), `kategori`.

### B.6 `hasil_clustering_wilayah.csv` (5 baris)
Kolom: `wilayah`, `wilayah_label`, `cluster_id`, `cluster_label`, `cluster_deskripsi`, `pca_x`, `pca_y`, serta enam variabel masukan pengelompokan.

### B.7 `hasil_forecasting_sektor.csv` (40 baris: 5 sektor × 8 tahun)
Kolom: `sektor`, `sektor_label`, `tahun` (2019–2026), `jumlah_usaha`, `lower_ci`, `upper_ci`, `arah_tren`, `laju_pertumbuhan_pct`, `status_data` (Historis atau Proyeksi). Untuk baris historis, batas bawah dan atas sama dengan nilai data.

---

## Lampiran C. Tabel Hasil Lengkap

### C.1 Skor kelayakan (skala 0–100)
| Wilayah | Kafe | Minimarket | Kelontong | Laundry | Restoran |
|---|---|---|---|---|---|
| Kota Yogyakarta | 71,00 (Layak) | 81,50 (Layak) | 81,50 (Layak) | 81,50 (Layak) | 81,50 (Layak) |
| Sleman | 56,70 (Cukup) | 52,22 (Cukup) | 51,81 (Cukup) | 51,81 (Cukup) | 51,81 (Cukup) |
| Bantul | 55,59 (Cukup) | 54,66 (Cukup) | 55,59 (Cukup) | 46,14 (Kurang) | 54,30 (Cukup) |
| Kulon Progo | 45,89 (Kurang) | 48,59 (Kurang) | 48,66 (Kurang) | 48,66 (Kurang) | 42,97 (Kurang) |
| Gunungkidul | 49,65 (Kurang) | 39,68 (Kurang) | 50,18 (Cukup) | 50,18 (Cukup) | 41,55 (Kurang) |

Rekapitulasi: Layak 5; Cukup Layak 11; Kurang Layak 9. Skor rata-rata sekitar 55,7.

### C.2 Rasio kompetitor per 1.000 penduduk
| Wilayah | Kafe | Minimarket | Kelontong | Laundry | Restoran |
|---|---|---|---|---|---|
| Kota Yogyakarta | 0,2919 | 0,0297 | 0,0000 | 0,0000 | 0,1054 |
| Sleman | 0,1695 | 0,2475 | 0,0008 | 0,0390 | 0,7238 |
| Bantul | 0,0292 | 0,0497 | 0,0000 | 0,0351 | 0,1813 |
| Kulon Progo | 0,0984 | 0,0313 | 0,0000 | 0,0000 | 0,4406 |
| Gunungkidul | 0,0425 | 0,2563 | 0,0000 | 0,0000 | 0,6136 |

### C.3 Proyeksi jumlah usaha se-DIY
| Sektor | 2024 | 2025 | 2026 |
|---|---|---|---|
| Kafe | 2.657 | 2.820 | 2.983 |
| Restoran | 7.170 | 7.400 | 7.630 |
| Minimarket | 1.975 | 2.031 | 2.088 |
| Laundry | 1.589 | 1.648 | 1.707 |
| Kelontong | 11.635 | 11.562 | 11.489 |

---

## Lampiran D. Peta Berkas Proyek

| Lokasi | Isi |
|---|---|
| `scripts/dataset1_osm/` | Pengambilan (Overpass API), pembagian grid, pembersihan dan deduplikasi OSM |
| `scripts/dataset2_ekonomi/` | Pembersihan data BPS dan SiBakul |
| `scripts/dataset3_sewa/` | Penyusunan dan penyeragaman indeks sewa |
| `scripts/dataset4_tren/` | Penguraian tabel BPS, pengambilan Google Trends, penggabungan tren |
| `scripts/run_all_pipelines.py` | Menjalankan pembersihan seluruh dataset |
| `scripts/generate_visualizations.py` | Membuat gambar hasil pada folder `outputs/` |
| `models/01_skoring.py` sampai `04_rekomendasi.py` | Implementasi empat pilar |
| `models/run_all_models.py` | Menjalankan Pilar 1–3 dan menguji Pilar 4 |
| `models/saved/` | Scaler, K-Means, dan PCA terserialisasi (`.joblib`) |
| `data/raw/` | Data mentah (JSON OSM, CSV BPS, sewa, Google Trends, SiBakul) |
| `data/interim/` | Data perantara (`bps_cleaned.csv`) |
| `data/cleaned/` | Data bersih hasil pipeline (7 CSV, masukan pemodelan) |
| `outputs/hasil/` | Hasil Pilar 1–3 (`hasil_skoring_sektor.csv`, `hasil_clustering_wilayah.csv`, `hasil_forecasting_sektor.csv`) |
| `notebooks/data_cleaning/` | Lima notebook dokumentasi pembersihan data |
| `notebooks/analisis/` | Empat notebook dokumentasi analisis pilar |
| `outputs/` | Gambar hasil (skoring, peta klaster, sebaran PCA, proyeksi tren), subfolder `hasil/` (CSV hasil), dan `logs/` |
| `milestones/` | Laporan Milestone 4 dan 5, panduan proposal, panduan slide, dokumen ini, dan script presentasi |
| `file/` | Berkas presentasi (PDF) dan proposal |
| `prototype/` | Direncanakan untuk prototipe Streamlit (masih kosong) |
| `media/` | Direncanakan untuk situs final Laravel (masih kosong) |
