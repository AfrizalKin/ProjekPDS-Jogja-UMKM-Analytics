# Evaluasi Kritis Metodologi dan Implementasi (Pilar 1–4)

Evaluasi ini disusun dari pembacaan seluruh notebook, script, dan data proyek. **Tidak ada berkas yang dijalankan atau diubah.** Angka yang dihitung sendiri dari data ditandai "hitungan manual". Temuan tentang notebook didasarkan pada pembacaan kode, bukan eksekusi.

Struktur tiap pilar: status singkat, temuan (gap/risiko → alasan penting → saran perbaikan), dan bug yang dipisahkan dari saran desain.

---

## Pilar 1: Skoring Kelayakan (MCDA)
**Status singkat:** ada gap. Mekanismenya benar dan bisa direproduksi, tetapi dua hal membuat hasilnya kurang bisa diandalkan.

**Temuan**
- **Ukuran kompetitor memakai OSM, padahal ada sumber yang lebih lengkap di proyek ini.**
  - Penyebab: Dataset 4 (tabel BPS) sudah memuat jumlah usaha per sektor × wilayah. Cakupan OSM terhadap BPS 2023 sangat timpang: restoran Kota Yogyakarta 39 vs 1.380 (2,8%), laundry Kota 0 vs 330, minimarket Gunungkidul 193 vs 240 (80%).
  - Dampak: rasio OSM tidak bisa dibandingkan antar wilayah. Dengan rasio BPS, Kota Yogyakarta menjadi wilayah paling jenuh di kelima sektor (restoran 3,73 per 1.000 penduduk vs 1,18–2,08 di wilayah lain). Skor 81,5 Kota untuk empat sektor turun menjadi 71,0 (hitungan manual). Kota tetap peringkat 1, tetapi selisih antar-sektor di Kota hilang.
  - Saran: jadikan unit usaha BPS 2023 ÷ estimasi penduduk × 1.000 sebagai ukuran kompetitor utama. OSM dipertahankan sebagai pembanding atau sensitivitas. Ini juga menyelesaikan masalah kelontong, karena BPS punya angkanya (±11.700 unit).
- **Kriteria benefit dan cost hampir semuanya mengukur hal yang sama, yaitu tingkat "keurbanan".**
  - Penyebab: Kota Yogyakarta tertinggi di PDRB, pengeluaran, kepadatan, sewa, dan rasio UMKM sekaligus.
  - Dampak: skor Kota selalu 50 + 70 × (0,65 − 0,35) = 71 atau lebih. Peringkat ditentukan oleh total bobot benefit vs cost, bukan oleh trade-off ekonomi yang sebenarnya.
  - Saran: tambahkan matriks korelasi kriteria (hitungan sederhana dengan pandas). Ganti sebagian kriteria dengan rasio yang bermakna ekonomi, misalnya permintaan per kompetitor (penduduk × pengeluaran ÷ jumlah usaha sektor) dan beban sewa terhadap pengeluaran.
- **Min-max pada 5 wilayah terdistorsi oleh outlier Kota Yogyakarta.**
  - Dampak: nilai PDRB dan kepadatan empat wilayah lain tertekan mendekati 0 (PDRB 0–0,20; kepadatan ≤ 0,14), sehingga dua kriteria itu nyaris tidak membedakan mereka.
  - Saran: transformasi log atau peringkat sebelum normalisasi, lalu laporkan perubahannya.
- **Normalisasi kompetitor per sektor menghilangkan skala absolut.**
  - Dampak: Sleman dengan 1 titik kelontong mendapat penalti penuh (0,15), sama seperti Sleman dengan 854 restoran. Karena itu skor Sleman identik 51,81 untuk tiga sektor.
  - Saran: gunakan ukuran absolut dari BPS (poin pertama) atau ambang acuan per sektor.
- **Tidak ada uji sensitivitas bobot.**
  - Dampak: bobot ditetapkan peneliti, jadi hasil mudah diserang.
  - Saran: bagian ini cukup sekitar 20 baris. Ubah tiap bobot ±50% lalu normalisasi ulang, tambah skenario bobot sama rata, balik tanda rasio UMKM, lalu laporkan korelasi peringkat Spearman terhadap baseline.
- **Rasio UMKM total sebagai penanda kejenuhan lemah secara konstruk.** Angka itu mencakup semua jenis UMKM termasuk industri, dan arah tandanya (cost) hanyalah asumsi. Saran: nyatakan asumsi itu secara eksplisit dan uji dengan balik tanda di sensitivitas.
- **Perbedaan antar-sektor sangat kecil** (maksimal 10,5 poin dalam satu wilayah). Saran: sektor perlu satu fitur khas, misalnya laju pertumbuhan sektor atau skor Google Trends per sektor, yang sudah ada di Dataset 4.

**Bug**
- Tidak ada bug logika pada `models/01_skoring.py`. Rumusnya cocok dengan CSV (dicek manual pada tiga sel).

---

## Pilar 2: Clustering Wilayah
**Status singkat:** ada gap. Keterbatasan n = 5 sudah diakui, tetapi interpretasi dan ketahanannya belum diperiksa.

**Temuan**
- **Fitur kompetitor bersumber OSM yang bias.** Dampaknya, Sleman (rasio 1,18, tertinggi) terpisah sebagian karena kelengkapan pemetaan OSM, bukan semata persaingan. Saran: ganti dengan rasio BPS (seperti Pilar 1) lalu cek apakah klaster berubah.
- **Hasil dipengaruhi outlier.** Kota Yogyakarta z ≈ +2 pada banyak variabel dan otomatis membentuk klaster sendiri. Saran: ulangi K-Means tanpa Kota dengan K = 2 untuk melihat apakah Sleman vs ketiga lainnya bertahan. Tambahkan satu dendrogram hirarkis (scipy sudah ada di `requirements.txt`).
- **Label klaster kurang akurat untuk Bantul.** Label diambil dari urutan rata-rata PDRB, sedangkan Bantul punya kepadatan 2.024 jiwa/km² (setara Sleman) dan sewa Rp450.000, dua kali Gunungkidul. Deskripsi "biaya sewa sangat ekonomis" kurang tepat untuknya. Saran: cetak tabel centroid dalam satuan asli dan loading PCA, lalu tulis label dari profil centroid atau beri catatan heterogenitas.
- **Angka PCA tidak dihitung dari model.** Persentase 74,94 / 19,16 / 94,09 dan label sumbu "Daya Beli & Kepadatan" diketik langsung di `generate_visualizations.py`, tidak dibaca dari `pca_wilayah.joblib`. Pembagian PC1/PC2 belum terverifikasi dari kode. Dengan 5 titik, data yang dipusatkan berperingkat paling banyak 4 dan PC1 hampir pasti sumbu "Kota". Saran: baca `explained_variance_ratio_` dan loading dari model, lalu tulis ke gambar secara otomatis.
- **Tidak ada validasi klaster atau pembenaran K = 3.** Saran: bandingkan K = 2 dan 3 secara deskriptif lewat tabel inersia, dan nyatakan terus terang bahwa ini kategorisasi deskriptif.

**Bug**
- Legenda dan warna di `generate_visualizations.py` memetakan `cluster_id` 0/1/2 ke nama wilayah secara manual. ID K-Means bersifat arbitrer, jadi bila versi sklearn atau data berubah, legenda bisa salah sementara `cluster_label` di CSV benar. Perbaikan: warnai berdasarkan `cluster_label`.
- Di notebook `02_pilar2...ipynb`, `label_map = {0:..., 1:..., 2:...}` langsung diterapkan pada ID mentah K-Means. Itu tidak benar, karena nomor klaster tidak punya makna tetap. Versi `.py` sudah benar (label dari urutan PDRB).
- Nama kolom `avg_rasio_kompetitor_per_1000` menyesatkan, karena nilainya total rasio semua sektor, bukan rata-rata.

---

## Pilar 3: Forecasting Tren Sektor (OLS)
**Status singkat:** pilihan metodenya (OLS pada 5 titik) dapat dipertanggungjawabkan dan sudah dibahas. Ada **satu bug perhitungan** dan beberapa gap pelaporan dan validasi yang murah diperbaiki.

**Temuan**
- **Tidak ada validasi di luar data pelatihan.**
  - Penyebab: R², MAPE, dan RMSE dihitung pada data yang sama dengan data pembentuk garis (*in-sample*).
  - Dampak: angka tersebut hampir pasti tampak bagus dan tidak mengukur kemampuan meramal. Contoh hitungan manual untuk kafe: garis yang dilatih pada 2019–2021 menaksir 2022 sebesar 2.083 (aktual 2.300, selisih sekitar 9%) dan 2023 sebesar 2.133 (aktual 2.590, selisih sekitar 18%), jauh di atas MAPE in-sample 4,25%. Penyebabnya, pemulihan pasca-pandemi bersifat melengkung dan garis lurus meremehkannya.
  - Saran: tambahkan uji *rolling-origin* sederhana (latih 2019–2021, uji 2022 dan 2023; latih 2019–2022, uji 2023) dan laporkan galat di luar sampel. Cukup beberapa baris dengan data yang sudah ada.
- **Uji leave-one-out belum dilaksanakan.**
  - Dampak: kekokohan kemiringan tren belum teruji. Hitungan manual menunjukkan kemiringan kafe berayun +115 hingga +227 per tahun (arah tetap positif).
  - Saran: implementasikan sebagai satu fungsi yang menghitung ulang kemiringan dengan membuang satu tahun bergantian, lalu laporkan rentangnya per sektor.
- **Guncangan pandemi (2020) mempengaruhi kemiringan dan label tren.**
  - Penyebab: label "Naik" didasarkan pada rata-rata pertumbuhan tahunan historis yang menyertakan penurunan 2020 dan rebound sesudahnya.
  - Dampak: untuk kafe, rata-rata pertumbuhan 7,3% per tahun sebagian merupakan pemulihan sekali jalan, bukan laju yang akan terus berlanjut.
  - Saran: tambahkan analisis sensitivitas yang membandingkan kemiringan 2019–2023 dengan kemiringan 2021–2023, atau menyebutkan secara eksplisit di laporan bahwa proyeksi mengasumsikan pola pemulihan berlanjut.
- **Aturan label tren tidak menangkap penurunan perlahan.** Ambang −1% rata-rata pertumbuhan membuat kelontong (turun sekitar 0,6% per tahun, kemiringan −73 unit per tahun, R² 0,999) berlabel "Stabil". Penurunannya sangat konsisten. Saran: tambahkan kategori "Menurun perlahan" atau gunakan tanda kemiringan beserta signifikansinya, lalu jelaskan di laporan.
- **Peramalan hanya pada tingkat DIY, sementara rekomendasi bersifat per wilayah.** Pilar 4 memakai satu label tren sektor untuk semua wilayah, padahal panel per wilayah × sektor (125 baris) tersedia. Saran: minimal hitung kemiringan per wilayah × sektor sebagai informasi tambahan, dengan catatan bahwa jumlah titiknya tetap lima.
- **Interval 95% adalah interval prediksi dengan asumsi galat normal dan bebas.** Asumsi itu tidak teruji pada lima titik dan galat jelas berpola (melengkung). Saran: tuliskan asumsi itu di laporan dan sebut interval sebagai indikatif.
- **Google Trends dan data UMKM total DIY tidak dipakai sama sekali.** Itu keputusan yang dapat dibenarkan (rasio parameter terhadap data), tetapi perlu diwujudkan sebagai narasi pendukung di kesimpulan agar data tersebut tidak terlihat sia-sia.

**Bug**
- **Nilai kritis t salah untuk derajat kebebasan 3.** Kode memakai `t_crit = 2.57 if dof <= 3 else 2.0`. Untuk 5 titik, derajat kebebasan = 3 dan nilai eksak dua sisi 95% adalah 3,182. Nilai 2,57 sesuai derajat kebebasan 5. Akibatnya interval dalam `hasil_forecasting_sektor.csv` terlalu sempit sekitar 19% (hitungan manual untuk kafe 2026: 2.376–3.590 seharusnya sekitar 2.232–3.734). Perbaikan: `scipy.stats.t.ppf(0.975, dof)`. Setelah itu, jalankan ulang `models/03_forecasting.py` dan gambar.
- Baris 2019 pada keluaran memuat `laju_pertumbuhan_pct = 0.0`, padahal tidak ada pembanding. Nilainya seharusnya kosong (NaN), karena 0,0% terbaca sebagai "tidak tumbuh". Perbaikan kecil di pembuatan kolom.
- Batas bawah proyeksi `max(10.0, ...)` adalah angka sembarang yang tidak berfungsi pada data saat ini. Aman, tetapi sebaiknya dihapus atau didokumentasikan.
- Di notebook `03_pilar3...ipynb`, kolom yang dibaca (`sektor`, `jumlah_unit`) berbeda dari CSV hasil script (`sektor_usaha`, `jumlah_usaha`), dan aturan klasifikasi berbeda (CAGR ≥ 3% vs rata-rata pertumbuhan > 1%). Lihat catatan lintas pilar.

---

## Pilar 4: Mesin Rekomendasi
**Status singkat:** sebagian besar memadai untuk lingkup mata kuliah. Ada beberapa gap logika.

**Temuan**
- **Mode terbuka mengabaikan anggaran dalam peringkat.** `is_affordable` hanya jadi penanda, jadi pengguna dengan Rp10 juta tetap mendapat Kota (Rp25,5 juta) di peringkat 1. Saran: urutkan wilayah terjangkau lebih dulu, dan jika tak ada yang terjangkau, tampilkan pesan khusus.
- **Tidak ada ambang minimal skor.** Bila semua wilayah Kurang Layak (misalnya minimarket: 39,68–54,66), sistem tetap menampilkan "Top 3". Saran: tampilkan "tidak ada wilayah berkategori Layak" bila skor tertinggi < 50.
- **Luas 30 m² ditanam di dalam fungsi.** Restoran dan laundry tidak butuh luas yang sama. Saran: jadikan `luas_m2` parameter opsional dengan default 30.
- **Ambang kejenuhan 0,20 per 1.000 berlaku sama untuk semua sektor dan bersumber OSM.** Restoran selalu terkena peringatan, sedangkan laundry tidak mungkin terkena. Saran: ambang relatif (misalnya di atas median lima wilayah per sektor), atau pakai rasio BPS.
- **Penjelasan "kenapa" minim.** CSV Pilar 1 tidak menyimpan komponen daya tarik dan beban. Saran: simpan kedua kolom itu agar kartu rekomendasi bisa menyebut faktor yang mengangkat atau menekan skor.
- **Arah tren hanya dipakai di narasi.** Kelontong (turun sekitar −73 unit per tahun) berlabel Stabil, sehingga tidak muncul peringatan. Saran: peringatan bila kemiringan negatif.
- **Tidak ada pengujian otomatis.** `run_all_models.py` hanya mencetak satu uji sukses. Saran: beberapa `assert` untuk kasus batas (tanpa anggaran, anggaran 0, wilayah salah).

**Bug**
- Pada wilayah spesifik tanpa anggaran, `budget_status` bernilai default "Sesuai", padahal anggaran tidak dievaluasi. Antarmuka yang menampilkan field ini akan memberi jaminan palsu. Perbaikan: default "Tidak dievaluasi".
- Anggaran bernilai 0 atau negatif diam-diam dianggap tidak diisi.

---

## Bobot Skoring: Dasar, Validasi, dan Pengaturan Manual (Pilar 1)

### Dasar bobot saat ini
Bobot berasal dari penalaran tim, bukan dari data atau literatur. Alasan tertulis hanya ada di panduan proposal: daya beli diberi porsi terbesar karena menentukan terjadinya transaksi, dan kompetitor diberi bobot lebih besar daripada sewa karena sewa bisa diamortisasi. Tidak ada sumber yang dikutip dan belum ada uji sensitivitas.

Nilai bawaan saat ini (`models/01_skoring.py`): PDRB 0,25; pengeluaran 0,25; kepadatan 0,15; kompetitor 0,15; sewa 0,10; rasio UMKM 0,10 (total 1,00). Skor = 50 + 70 × (daya tarik − beban). Ambang kategori: Layak ≥ 70, Cukup Layak ≥ 50.

### Cara membuat bobot lebih dapat dipertanggungjawabkan
Bobot tidak bisa dibuktikan "benar" tanpa data hasil usaha. Yang bisa dilakukan adalah membuatnya terdokumentasi, dibandingkan, dan diuji ketahanannya.

| Cara | Kebutuhan | Manfaat | Catatan |
|---|---|---|---|
| **AHP** (perbandingan berpasangan) | Penilaian tim atau 3–5 pelaku usaha/ahli | Prosedur baku dan rasio konsistensi yang bisa dilaporkan | Tetap subjektif, tetapi terdokumentasi |
| **CRITIC atau entropi** | Data yang sudah ada | Bobot dihitung dari variasi dan korelasi kriteria; CRITIC menurunkan bobot kriteria yang berkorelasi, sesuai dengan kondisi proyek | Dengan 5 wilayah hasilnya tidak stabil; cocok sebagai pembanding, bukan bobot final |
| **Monte Carlo bobot acak** | Data yang sudah ada | Menghasilkan pernyataan seperti "Kota peringkat 1 pada X% skenario bobot" | Bukti ketahanan hasil yang paling kuat |

Kombinasi yang disarankan: AHP sebagai bobot utama, CRITIC sebagai pembanding, Monte Carlo untuk menunjukkan peringkat tidak bergantung pada satu set bobot. Semuanya bisa dibuat dengan pandas dan numpy yang sudah ada.

### Apakah bobot bisa "dilatih" otomatis?
Tidak secara sungguhan. Pelatihan membutuhkan variabel target (omzet, tingkat bertahan, atau status berhasil/gagal) dan proyek ini tidak memilikinya. Jika dipaksakan dengan pertumbuhan jumlah usaha BPS sebagai target pengganti:
- Fitur wilayah hanya punya 5 nilai independen untuk 6 fitur, sehingga regresi pasti menghafal.
- Pertumbuhan jumlah usaha bukan ukuran keuntungan, dan prosesnya memutar (data 2019–2023 dipakai menilai kriteria 2024).
- Yang masih layak adalah **cek kewajaran**, bukan pelatihan: hitung korelasi peringkat (Spearman) antara skor Pilar 1 dan pertumbuhan unit usaha BPS per wilayah × sektor. Korelasi positif memberi dukungan lemah dan harus ditulis dengan catatan keterbatasannya.

### Usulan: bobot dapat diatur manual dengan nilai bawaan tetap
**Prinsip:** pengguna (atau peneliti) boleh mengubah bobot, tetapi tanpa perubahan apa pun sistem berjalan dengan nilai bawaan yang berlaku sekarang. Dengan demikian hasil bawaan tidak berubah dan tetap dapat direproduksi.

**Perubahan yang disarankan**
1. **Pisahkan nilai bawaan sebagai konstanta.** Di `01_skoring.py`, buat satu kamus bobot bawaan (6 kriteria di atas) beserta konstanta 50 dan 70, serta ambang 70 dan 50. Jangan menulis angka bobot langsung di dalam rumus.
2. **Jadikan bobot parameter fungsi.** `run_skoring(bobot=None)`: bila `None`, pakai nilai bawaan. Bila diisi, gabungkan dengan nilai bawaan agar kriteria yang tidak disebut tetap memakai nilai bawaan.
3. **Validasi masukan.** Semua bobot tidak boleh negatif. Normalisasi otomatis agar total 1,0 (atau tolak dengan pesan jelas), dan tolak nama kriteria yang tidak dikenal.
4. **Catat bobot yang dipakai.** Simpan bobot di berkas keluaran (misalnya berkas JSON pendamping atau kolom tambahan), supaya setiap tabel skor dapat ditelusuri. Beri label "bobot kustom" bila berbeda dari nilai bawaan.
5. **Simpan komponen ternormalisasi di CSV.** Tambahkan enam kolom ternormalisasi (`pdrb_norm`, `pengeluaran_norm`, `kepadatan_norm`, `kompetitor_norm`, `sewa_norm`, `umkm_norm`) pada `hasil_skoring_sektor.csv`. Dengan begitu skor dapat dihitung ulang dengan bobot apa pun hanya lewat penjumlahan terbobot, **tanpa menjalankan ulang pipeline dan tanpa melanggar prinsip antarmuka hanya-baca**. Kolom ini juga memungkinkan Pilar 4 menjelaskan faktor yang mengangkat atau menekan skor.
6. **Antarmuka.** Di prototipe Streamlit, sediakan penggeser bobot dengan nilai awal sama dengan bawaan, tombol "Kembalikan ke bawaan", dan normalisasi otomatis. Di situs final Laravel, rumusnya cukup penjumlahan terbobot sehingga mudah direplikasi di PHP.

**Hal yang perlu diperhatikan**
- Mengatur bobot manual **tidak membuat bobot lebih valid**. Ia hanya memberi kebebasan. Tetap laporkan uji sensitivitas agar jelas seberapa besar perubahan bobot mengubah peringkat.
- Karena Kota Yogyakarta ekstrem pada semua kriteria, perubahan bobot sering kali hanya menggeser skor, bukan peringkat. Tampilkan peringkat sebelum dan sesudah perubahan agar pengguna tidak salah menafsirkan.
- Tampilkan selalu bobot yang sedang dipakai di kartu rekomendasi, supaya hasil tidak tampak berasal dari model tetap.

---

## Target Pasar dan Daya Beli Masyarakat (Pilar 1, dengan contoh Bantul)
**Pertanyaan:** apakah skor sudah mempertimbangkan target pemasaran dan tingkat pembelian masyarakat?
**Jawaban singkat:** sebagian. Daya beli sudah masuk secara kasar, tetapi **target pasar belum dipertimbangkan sama sekali**.

**Yang sudah masuk**
- Daya beli: PDRB per kapita (25%) dan pengeluaran per kapita (25%), total 50%.
- Ukuran pasar: kepadatan penduduk (15%) sebagai penanda.

**Yang belum, dengan contoh Bantul**
- **Pengeluaran yang dipakai total, bukan yang relevan untuk sektornya.**
  - Penyebab: berkas BPS sudah memuat pemisahan makanan dan bukan makanan, tetapi kode hanya memakai kolom "Jumlah".
  - Dampak: untuk restoran, kafe, dan kelontong, pengeluaran makanan lebih tepat. Bantul Rp753.850 vs Sleman Rp883.998 dan Kota Rp833.761 (Bantul sekitar 90% dari Kota), sedangkan pada pengeluaran total Bantul hanya sekitar 77% dari Kota.
  - Saran: pakai pengeluaran makanan untuk restoran, kafe, kelontong, dan minimarket, dan pengeluaran bukan makanan untuk laundry. Daya beli menjadi khas per sektor, yang sekaligus menambah pembeda antar sektor.
- **Ukuran pasar agregat tidak dipakai.**
  - Penyebab: skor memakai nilai per kapita dan kepadatan, bukan besarnya populasi dikali belanja.
  - Dampak (hitungan manual): Bantul berpenduduk sekitar 1,03 juta jiwa dengan total belanja sekitar Rp1,78 triliun per bulan, terbesar kedua setelah Sleman (sekitar Rp2,57 triliun) dan dua kali lipat Kota Yogyakarta (sekitar Rp0,83 triliun). Kota tetap berskor tertinggi (71–81,5) walaupun kolam belanjanya kecil.
  - Saran: tambahkan total belanja wilayah (penduduk × pengeluaran) atau permintaan per kompetitor (total belanja ÷ jumlah usaha sektor dari BPS).
- **PDRB per kapita menggambarkan produksi di wilayah, bukan penghasilan warganya.**
  - Dampak: banyak warga Bantul bekerja di Kota atau Sleman, sehingga PDRB Bantul (35,8 juta, skor ternormalisasi 0,004) meremehkan daya beli penghuninya. Pengeluaran lebih mencerminkan sisi permintaan, tetapi bobotnya hanya sama dengan PDRB.
  - Saran: kurangi atau tinjau ulang bobot PDRB, dan laporkan efeknya lewat uji sensitivitas.
- **Kepadatan bukan ukuran pasar.** Bantul dan Sleman berkepadatan hampir sama (2.024 vs 2.052) padahal populasi dan belanja keduanya berbeda jauh. Saran: gunakan total belanja (poin kedua) sebagai pengganti atau pelengkap.
- **Tidak ada segmen konsumen.**
  - Dampak: mahasiswa, wisatawan, pekerja komuter, dan kelompok umur tidak ada di data. Klaim seperti "konsentrasi mahasiswa" pada narasi Sleman tidak didukung data proyek. Di Bantul, potensi wisata pantai pun tidak terukur di mana pun.
  - Saran: tulis sebagai keterbatasan karena datanya tidak tersedia, dan beri label "asumsi kualitatif" pada narasi yang menyebut segmen.
- **Hasil laundry Bantul (46,1, Kurang Layak) kemungkinan artefak.** OSM mencatat laundry di Kota, Kulon Progo, dan Gunungkidul nol, sehingga Bantul tampak sebagai wilayah paling jenuh setelah Sleman. Menurut BPS, kepadatan laundry Bantul (sekitar 0,31 per 1.000 jiwa) justru jauh di bawah Sleman (sekitar 0,60) dan Kota (sekitar 0,89).
- **Pilar 4 belum mengaitkan harga produk dengan daya beli.** Saran: tambahkan masukan opsional berupa harga rata-rata produk dan perkiraan frekuensi belanja, lalu bandingkan dengan pengeluaran per kapita. Itu pendekatan paling dekat dengan "target pasar" yang bisa dibuat tanpa data baru.

---

## Catatan lintas pilar: notebook
Notebook adalah deliverable yang dinilai, dan di sinilah risiko terbesar.
- **Tersimpan tanpa output dan tanpa visualisasi.** Notebook Pilar 1 dan 2 mengimpor matplotlib tetapi tidak membuat grafik.
- **Logikanya berbeda dari `models/*.py`.**
  - Bobot, normalisasi, dan rumus rasio kompetitor berbeda. Di notebook Pilar 1 penyebutnya `kepadatan × 0,1`, yang tidak bermakna sebagai rasio per 1.000 penduduk.
  - Nama kolom dan berkas masukan berbeda: `sektor` vs `kategori`, serta berkas `dataset2_bps_makro_cleaned.csv` dan `sibakul_umkm_bersih.csv` yang tidak ada di `data/cleaned/`.
  - Notebook Pilar 4 bergantung pada akhiran kolom `_x` yang rapuh.
- **Konsekuensi (dari pembacaan, belum dijalankan).** Notebook cleaning menulis ulang `data/cleaned/` dengan skema dan data hardcoded yang berbeda. Menjalankannya berisiko menimpa hasil `scripts/` dan menghasilkan angka yang tidak sama dengan CSV.

---

## Verdict
Proyek ini bisa dikumpulkan sebagai versi UTS atau awal. Pipeline-nya utuh, keterbatasannya diakui, dan kode produksinya konsisten dengan hasil. Namun tiga perbaikan prioritas layak dikerjakan sebelum batas waktu:

1. **Sinkronkan dan jalankan notebook.** Pakai logika `models/*.py`, perbaiki bug label klaster dan penyebut rasio, lalu simpan notebook dengan output dan grafik. Ini yang paling sering menjadi dasar penilaian.
2. **Ganti atau lengkapi ukuran kompetitor dengan unit usaha BPS per 1.000 penduduk.** Data sudah ada. Efeknya terhadap skor Pilar 1 dan klaster Pilar 2 bisa dilaporkan dalam satu tabel perbandingan sebagai temuan.
3. **Tambahkan tabel uji sensitivitas bobot (korelasi peringkat) dan perbaiki dua bug kecil Pilar 4.** Dua bug itu adalah status "Sesuai" yang palsu dan peringkat mode terbuka yang tidak peduli anggaran.

**Catatan pelengkap:** bila waktu memungkinkan, pakai pengeluaran makanan atau bukan makanan menurut sektor dan tambahkan total belanja wilayah (lihat bagian Target Pasar dan Daya Beli). Itu menjawab pertanyaan paling mudah ditanyakan penguji tentang daya beli dan target pasar.

**Perbaikan cepat tambahan (kurang dari 30 menit):** ganti `t_crit` di Pilar 3 dengan `scipy.stats.t.ppf(0.975, dof)` dan jalankan ulang `models/run_all_models.py` serta `scripts/generate_visualizations.py`. Ini satu-satunya kesalahan angka pada keluaran yang sudah ada di slide, dan bisa diperbaiki tanpa mengubah struktur analisis.
