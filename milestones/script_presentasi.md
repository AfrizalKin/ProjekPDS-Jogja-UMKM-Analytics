# Script Presentasi: UMKM Recommender (15 menit, 6 presenter)

Acuan utama: `file/PPT Projek Pengantar Data Sains.pdf` (15 halaman: judul, anggota, 12 slide isi bernomor 02–13, terima kasih).

Setiap slide punya empat bagian: **Outline**, **Materi** (bekal pemahaman presenter), **Hal yang perlu / tidak perlu disampaikan**, dan **Script general** (kalimat lisan, boleh diparafrase).

**Pembagian presenter** (2 slide isi per orang). Tentukan sendiri siapa mengambil nomor berapa: Afrizal, Andhika, Oka, Theo, Gen, Marcellino.

| Presenter | Slide | Total waktu |
|---|---|---|
| 1 | 02, 03 | 150 detik |
| 2 | 04, 05 | 165 detik |
| 3 | 06, 07 | 150 detik |
| 4 | 08, 09 | 130 detik |
| 5 | 10, 11 | 165 detik |
| 6 | 12, 13 | 140 detik |

Kecepatan bicara acuan: sekitar 2,2 kata per detik. Script bersifat general, jadi tidak perlu dihafal kata per kata. Yang penting urutan gagasannya.

---

## Slide 2: Latar Belakang, Tujuan, dan Sistematika Arsitektur Sistem — Presenter 1 — Target: 80 detik

**Outline**
- Pembuka singkat dan nama projek.
- Peran penting UMKM dan masalah umum: salah memilih lokasi dan sektor.
- Tiga dampak: mortalitas bisnis, kanibalisasi pasar, beban sewa.
- Tujuan dan gambaran arsitektur (5 dataset, 4 pilar, kartu rekomendasi).

**Materi**
- UMKM berkontribusi sekitar 61,07% PDB nasional dan menyerap sekitar 97% tenaga kerja (Kemenkop UKM, 2023). Di DIY ada sekitar 347.744 UMKM aktif (SiBakul Diskop UKM DIY, 2025).
- Akar masalah menurut slide: pemilihan lokasi dan sektor didasarkan pada intuisi, coba-coba, atau tren sesaat di media sosial, tanpa data kondisi ekonomi wilayah.
- Tiga dampak yang dikutip dari literatur:
  - Mortalitas bisnis: sekitar 5 dari 10 UMKM baru tidak bertahan pada 3–5 tahun pertama (U.S. SBA, 2022; Zimmerer & Scarborough, 2008).
  - Kanibalisasi dan perang harga: usaha sejenis menumpuk, misalnya kafe di sekitar kampus (Tjiptono, 2019).
  - Beban sewa: rata-rata sewa komersial pusat kota sampai Rp850.000 per m² per tahun menggerus modal sebelum balik modal (BPS DIY, 2024; Bank Indonesia, 2024).
- Tujuan: mengubah keputusan berbasis intuisi menjadi Sistem Pendukung Keputusan berbasis data sains.
- Arsitektur: 5 dataset → Pilar 1 (MCDA, skor 0–100) → Pilar 2 (K-Means + PCA, klaster wilayah) → Pilar 3 (regresi linear, tren 2024–2026) → Pilar 4 (mesin rekomendasi berbasis aturan) → Pilar 5 (kartu rekomendasi di web, Streamlit/Laravel).

**Hal yang perlu disampaikan**
- Masalahnya konkret: pilih lokasi dengan intuisi.
- Tiga dampak, singkat satu kalimat per dampak.
- Tujuan: dari intuisi ke data.
- Sebut sekilas "lima dataset, empat pilar" sebagai jembatan ke slide berikutnya.

**Hal yang tidak perlu disampaikan**
- Rumus atau detail metode (itu giliran presenter lain).
- Angka literatur secara terlalu rinci. Cukup "sekitar separuh".
- Jangan menyatakan "50% bangkrut" sebagai temuan kami. Itu kutipan literatur.
- Jangan menjanjikan sistem pasti membuat usaha berhasil.

**Script general**
"Selamat pagi semuanya. Kami dari kelompok UMKM Recommender, dan kami akan memaparkan sistem rekomendasi kelayakan sektor usaha UMKM di Yogyakarta berbasis data. Kita mulai dari masalahnya. UMKM itu tulang punggung ekonomi. Menurut Kemenkop UKM, kontribusinya ke PDB nasional sekitar 61 persen dan menyerap sekitar 97 persen tenaga kerja. Di DIY sendiri ada sekitar 348 ribu UMKM. Tapi menurut literatur yang kami kutip, sekitar separuh UMKM baru tidak bertahan sampai tiga sampai lima tahun, salah satunya karena salah memilih lokasi. Akar masalahnya, banyak orang memilih lokasi dan sektor usaha hanya berdasarkan intuisi atau tren media sosial. Dampaknya ada tiga. Pertama, usaha sejenis menumpuk di satu kawasan, misalnya kafe di sekitar kampus, sehingga terjadi perang harga. Kedua, daya beli sekitar tidak cocok dengan produk yang dijual. Ketiga, sewa di pusat kota yang tinggi menggerus modal sebelum balik modal. Karena itu tujuan kami, mengubah keputusan berbasis intuisi menjadi keputusan berbasis data. Caranya, lima dataset kami olah lewat empat pilar analitik, lalu hasilnya kami sajikan sebagai kartu rekomendasi di web. Teman-teman berikutnya akan menjelaskan satu per satu."

---

## Slide 3: Data Requirements — Kebutuhan 5 Dataset Multi-Domain — Presenter 1 — Target: 70 detik

**Outline**
- Lima dataset dari lima domain berbeda.
- Untuk tiap dataset: sumber, isi, dan fungsinya dalam sistem.
- Alasan SiBakul ditambahkan (melengkapi OSM).

**Materi**
1. **Kompetitor usaha (OpenStreetMap, Overpass API):** 2.796 titik usaha (restoran, kafe, minimarket/convenience, laundry, kelontong). Fungsi: menghitung kepadatan pesaing per sektor, jadi penalti di Pilar 1 dan bagian dari profil di Pilar 2.
2. **Kondisi makroekonomi (BPS DIY, 2024):** PDRB per kapita, pengeluaran bulanan per kapita, luas wilayah, kepadatan penduduk. Fungsi: daya beli dan ukuran pasar.
3. **Biaya sewa komersial (Bank Indonesia dan riset pasar properti, 2024):** tarif sewa kios/ruko dalam Rp per m² per tahun untuk 5 kabupaten/kota. Fungsi: beban modal awal (Pilar 1) dan cek kecukupan budget (Pilar 4). Grafik di slide menunjukkan Kota Yogyakarta paling mahal, Kulon Progo dan Gunungkidul paling murah.
4. **Tren sektor usaha (BPS DIY 2019–2023 dan Google Trends):** jumlah unit usaha per tahun dan indeks minat pencarian. Fungsi: basis proyeksi Pilar 3.
5. **SiBakul (Diskop UKM DIY, 2025):** jumlah UMKM resmi per wilayah. Fungsi: menghitung rasio UMKM per 1.000 penduduk sebagai ukuran kepadatan struktural, dipakai di Pilar 1 dan 2.
- Mengapa SiBakul: OpenStreetMap kurang mencatat usaha kecil informal (contoh: toko kelontong hanya 1 titik di OSM). SiBakul memberi gambaran kepadatan usaha yang lebih lengkap di tingkat wilayah.

**Hal yang perlu disampaikan**
- Lima sumber berbeda, satu kalimat fungsi masing-masing.
- Alasan SiBakul sebagai pelengkap OSM. Ini poin kejujuran data yang bagus.
- Bahwa sewa hanya satu angka per kabupaten/kota.

**Hal yang tidak perlu disampaikan**
- Cara teknis pengambilan data (grid sampling, retry, dan lain-lain). Itu di slide 4.
- Rincian jumlah titik per kategori OSM.
- Total jumlah UMKM di slide ini. Cukup fungsi SiBakul-nya.

**Script general**
"Sistem ini membutuhkan lima dataset dari lima domain yang berbeda. Pertama, kompetitor usaha dari OpenStreetMap: ada 2.796 titik usaha, yaitu restoran, kafe, minimarket, laundry, dan toko kelontong. Ini untuk mengukur seberapa padat pesaing. Kedua, kondisi makroekonomi dari BPS tahun 2024: PDRB per kapita, pengeluaran, luas wilayah, dan kepadatan penduduk, untuk mengukur daya beli dan ukuran pasar. Ketiga, biaya sewa komersial per meter persegi per tahun dari Bank Indonesia dan riset properti. Di grafik terlihat Kota Yogyakarta paling mahal dan Kulon Progo serta Gunungkidul paling murah. Ini gambaran beban modal awal. Keempat, tren sektor usaha: jumlah unit usaha BPS tahun 2019 sampai 2023 ditambah Google Trends, untuk melihat sektor yang sedang naik atau melambat. Kelima, data SiBakul dari Diskop UKM DIY, yaitu jumlah UMKM resmi, yang kami pakai untuk menghitung kepadatan usaha per seribu penduduk. Kenapa perlu SiBakul? Karena OpenStreetMap kurang mencatat usaha kecil informal, jadi SiBakul melengkapinya."

---

## Slide 4: Data Overview — Metode Pengambilan, Pengolahan, dan Integrasi Data — Presenter 2 — Target: 80 detik

**Outline**
- Empat tahap pipeline: cleaning, validation, transformation, integration.
- Contoh konkret dari projek pada setiap tahap.
- Hasil akhir: dataset terintegrasi dan siap masuk empat pilar.

**Materi**
- **Cleaning:** hapus duplikat. Titik OSM yang berada di batas antar-kotak terunduh dua kali, karena wilayah padat dipecah menjadi kotak-kotak (grid sampling) supaya server tidak timeout. Duplikat dibuang berdasarkan ID OSM dan koordinat.
- **Validation:** koordinat dicek harus berada dalam batas wilayah DIY. Nama wilayah dicek terhadap referensi resmi.
- **Transformation:** nama wilayah diseragamkan memakai kamus manual (misalnya "Gunung Kidul" dan "Gunungkidul" jadi satu ID). Tarif sewa diseragamkan menjadi Rp per m² per tahun (tarif bulanan dikali 12).
- **Integration:** kelima dataset digabung lewat kunci wilayah, sektor, dan tahun.
- Temuan data yang menarik: tabel BPS menyisipkan baris total "D.I. Yogyakarta" di antara kabupaten. Kalau tidak dibuang, baris itu terhitung sebagai wilayah keenam.
- Audit kualitas data (Milestone 5): skor tiap dataset berkisar 97,6% sampai 100% pada empat dimensi (completeness, consistency, uniqueness, validity).

**Hal yang perlu disampaikan**
- Empat tahap dengan satu contoh nyata per tahap.
- Temuan baris agregat provinsi, sebagai bukti pemeriksaan data yang teliti.
- Hasil akhir: dataset bersih dan terintegrasi untuk empat pilar.

**Hal yang tidak perlu disampaikan**
- Penanganan missing value dengan mean/median/modus, batas "drop jika > 30%", dan deteksi outlier IQR/Z-score. Itu tertulis di slide, tetapi **belum diterapkan di kode projek**. Jangan diklaim sudah dilakukan. Kalau ditanya, katakan itu bagian dari rancangan tahap cleaning dan belum jadi bagian pipeline.
- Total UMKM "342.463" di kotak kiri bawah. Tidak perlu disebut.
- "Proses otomatisasi 100%" sebagai klaim. Sebagian data (misalnya BPS dan sewa) dimasukkan manual.

**Script general**
"Dari lima data mentah tadi, kami jalankan pipeline empat tahap. Tahap pertama, cleaning. Contohnya titik OpenStreetMap yang terunduh dua kali, karena wilayah padat kami pecah jadi kotak-kotak kecil supaya server tidak timeout. Titik kembar itu dibuang berdasarkan ID dan koordinatnya. Tahap kedua, validasi. Setiap koordinat kami cek harus berada di dalam batas wilayah DIY, dan nama wilayah dicocokkan dengan referensi resmi. Tahap ketiga, transformasi. Nama wilayah diseragamkan, misalnya Gunung Kidul dan Gunungkidul jadi satu, dan satuan sewa disamakan menjadi rupiah per meter persegi per tahun. Tahap keempat, integrasi, yaitu menggabungkan kelima dataset lewat kunci wilayah, sektor, dan tahun. Satu temuan menarik: tabel BPS menyertakan baris total provinsi di antara data kabupaten. Kalau tidak dibuang, baris itu terhitung sebagai wilayah keenam. Dari audit kualitas yang kami lakukan, skor semua dataset ada di atas 95 persen. Hasil akhirnya adalah dataset yang bersih, konsisten, dan siap masuk ke empat pilar analitik."

---

## Slide 5: Analytical Framework — 4 Pilar Analitik untuk Rekomendasi Lokasi UMKM — Presenter 2 — Target: 85 detik

**Outline**
- Peta besar: 5 dataset → preprocessing → 4 pilar → rekomendasi.
- Fungsi satu kalimat untuk tiap pilar.
- Pilar 1–3 dihitung sekali (batch), Pilar 4 yang interaktif.

**Materi**
- **Pilar 1, MCDA:** skor kelayakan 0–100 untuk setiap kombinasi wilayah × sektor (25 kombinasi), dari faktor benefit (daya beli, kepadatan) dan cost (sewa, kompetitor, kejenuhan UMKM). Metode: normalisasi, weighted linear combination, klasifikasi.
- **Pilar 2, K-Means + PCA 2D:** mengelompokkan 5 kabupaten/kota menjadi 3 klaster. Tahapan: z-score, K-Means, PCA 2D. Dua sumbu PCA menyimpan 94,09% informasi.
- **Pilar 3, Time Series Forecasting:** regresi linear (OLS) dari data 2019–2023 untuk proyeksi 2024–2026 dengan interval kepercayaan. Ada kotak "Limitasi": variabilitas, faktor lain, data terbatas.
- **Pilar 4, Rule-Based Recommendation Engine:** menerima input pengguna, membaca hasil tiga pilar, lalu mengeluarkan peringkat lokasi.
- Tiga pilar pertama dihitung sekali di belakang layar dan hasilnya disimpan (CSV dan model terserialisasi). Pilar 4 hanya membaca hasil itu, jadi cepat dan terlacak.
- Hasil akhir: Sistem Pendukung Keputusan lokasi UMKM yang berbasis data, objektif (metode jelas), dan real-time.

**Hal yang perlu disampaikan**
- Alur dari data sampai rekomendasi.
- Satu kalimat peran tiap pilar.
- Perbedaan batch (Pilar 1–3) dan interaktif (Pilar 4).
- Bahwa Pilar 3 punya keterbatasan data yang akan dijelaskan.

**Hal yang tidak perlu disampaikan**
- Angka detail di dalam kotak (persentase bobot, R², MAPE). Semuanya dibahas di slide pilar masing-masing.
- Ilustrasi grafik "Cluster 1/2/3 (High/Medium/Low Potential)" dan grafik tren contoh. Itu gambaran bentuk, bukan hasil.
- Aturan Pilar 4 yang tertulis di kotak kanan secara satu per satu. Cukup konsepnya.

**Script general**
"Slide ini peta besar dari analisis kami. Lima dataset masuk ke preprocessing, lalu mengalir ke empat pilar. Pilar satu, MCDA, memberi skor kelayakan nol sampai seratus untuk setiap kombinasi wilayah dan sektor, dengan menggabungkan faktor yang menarik seperti daya beli dan faktor beban seperti sewa dan jumlah pesaing. Pilar dua, K-Means ditambah PCA, mengelompokkan lima kabupaten dan kota menjadi tiga klaster karakter pasar, dan PCA membantu menggambarkannya dalam dua dimensi dengan informasi sekitar 94 persen tetap terjaga. Pilar tiga, time series forecasting, memakai regresi linear dari data 2019 sampai 2023 untuk memproyeksikan jumlah usaha 2024 sampai 2026 beserta rentang ketidakpastiannya, dan di bagian ini kami cantumkan keterbatasan datanya. Pilar empat, mesin rekomendasi berbasis aturan, yang menerima input pengguna lalu membaca hasil tiga pilar sebelumnya untuk menyusun peringkat lokasi. Satu hal penting: tiga pilar pertama dihitung sekali di belakang layar. Hanya pilar empat yang bekerja saat pengguna memakai sistem, sehingga responsnya cepat dan jejak metodenya jelas."

---

## Slide 6: Pilar 1 — MCDA (Multi-Criteria Decision Analysis) — Presenter 3 — Target: 85 detik

**Outline**
- Tujuan Pilar 1 dan alasan memilih MCDA.
- Empat langkah: normalisasi → pembobotan → perhitungan skor → peringkat.
- Rumus skor dan kriteria benefit vs cost.
- Ambang kategori kelayakan.

**Materi**
- **Mengapa MCDA, bukan machine learning terlatih:** tidak ada data berlabel "usaha berhasil/gagal" dari sumber publik. Kalau label dibuat sendiri, hasilnya hanya memantulkan asumsi kami. MCDA transparan: setiap bobot bisa dijelaskan.
- **Normalisasi min-max:** rupiah dan rasio tidak bisa dijumlahkan langsung, jadi tiap kriteria diubah ke skala 0–1 (terkecil 0, terbesar 1).
- **Rumus (kotak "Metode Analisis"):** Skor = 50 + 70 × (Daya Tarik − Beban Biaya), dibatasi 0–100.
  - Daya tarik (benefit): 0,25 PDRB + 0,25 pengeluaran + 0,15 kepadatan.
  - Beban biaya (cost): 0,15 kompetitor + 0,10 sewa + 0,10 kejenuhan UMKM (SiBakul).
- **Kategori:** ≥ 70 Layak, 50–69 Cukup Layak, < 50 Kurang Layak.
- **Contoh hitung (opsional, jika ditanya):** Kota Yogyakarta untuk kafe: daya tarik 0,65, beban 0,35, selisih 0,30, skor 50 + 70 × 0,30 = 71,0. Gunungkidul untuk kafe: daya tarik sangat kecil dan beban kecil, skor sekitar 49,65.
- **Keterbatasan:** bobot ditentukan tim berdasarkan penalaran (daya beli dianggap faktor utama, total 50%), bukan dipelajari dari data. Uji sensitivitas bobot belum dilakukan.

**Hal yang perlu disampaikan**
- Alasan MCDA: tidak ada label berhasil/gagal.
- Empat langkah, dan rumus di kotak Metode Analisis.
- Pembagian benefit dan cost dengan bobotnya.
- Ambang tiga kategori.
- Satu kalimat jujur: bobot ditetapkan tim.

**Hal yang tidak perlu disampaikan**
- Daftar persentase di kotak "Kriteria dan Bobot" (kiri-tengah bawah) dan jumlah kombinasi "14 / 9 / 2" di kotak kanan. Rujuk rumus di tengah dan lanjutkan ke slide 7 untuk jumlah per kategori.
- Penjelasan matematis min-max secara rinci.
- Jangan klaim bobot "optimal" atau "terbukti".

**Script general**
"Kita masuk ke Pilar 1. Tujuannya memberi skor dan peringkat lokasi UMKM dengan Multi-Criteria Decision Analysis. Kenapa MCDA dan bukan machine learning terlatih? Karena data publik tidak punya label usaha berhasil atau gagal, jadi model terlatih tidak bisa divalidasi. MCDA lebih transparan, setiap bobotnya bisa dijelaskan. Prosesnya empat langkah. Pertama, normalisasi, supaya rupiah dan rasio bisa dijumlahkan, semuanya diubah ke skala nol sampai satu. Kedua, pembobotan. Kedua kelompok kriteria punya bobot sendiri. Faktor yang menarik pasar adalah PDRB per kapita dan pengeluaran, masing-masing 25 persen, serta kepadatan penduduk 15 persen. Faktor beban adalah rasio kompetitor 15 persen, sewa 10 persen, dan kejenuhan UMKM 10 persen. Ketiga, skor dihitung dengan rumus 50 ditambah 70 kali selisih daya tarik dan beban, dibatasi nol sampai seratus. Keempat, hasilnya diurutkan jadi peringkat. Kategorinya: skor 70 ke atas Layak, 50 sampai 69 Cukup Layak, dan di bawah 50 Kurang Layak. Satu catatan: bobot ini kami tetapkan berdasarkan penalaran, bukan hasil belajar dari data."

---

## Slide 7: Pilar 1 — Sebaran Skor, Uji Sensitivitas & Pipeline — Presenter 3 — Target: 65 detik

**Outline**
- Ringkasan sebaran 25 kombinasi.
- Pola per kelompok wilayah (tiga kotak di kanan).
- Catatan keterbatasan: skor lebih mencerminkan karakter wilayah, dan data OSM yang jarang memengaruhi sektor tertentu.

**Materi**
- **Ringkasan di grafik:** skor 39,7–81,5, rata-rata 55,7 (simpangan baku 12,9). 5 kombinasi Layak (20%), 11 Cukup Layak (44%), 9 Kurang Layak (36%).
- **Sleman dan Bantul:** hampir semua sektor Cukup Layak (sekitar 52–57). Kafe tertinggi di kedua wilayah (Sleman 56,7; Bantul 55,6). Pengecualian: laundry Bantul 46,1 (Kurang Layak).
- **Kota Yogyakarta:** daya beli tertinggi (PDRB Rp131,4 juta, pengeluaran Rp2,25 juta). Empat sektor mencapai 81,5 sedangkan kafe 71,0 (terendah di kota itu) karena sewa Rp850.000/m² dan kafe paling padat (108 titik OSM). Sektor tanpa titik di OSM ikut menaikkan skor.
- **Kulon Progo dan Gunungkidul:** sewa terendah (Rp220.000–275.000/m²) tetapi daya beli terendah. Skor 39,7–50,2; 8 dari 10 kombinasi Kurang Layak. Hanya laundry dan kelontong Gunungkidul Cukup Layak (50,2), karena OSM mencatat nol pesaing.
- **Mengapa skor antar sektor di satu wilayah mirip:** hanya jumlah kompetitor yang berbeda antar sektor (kriteria lain sama untuk satu wilayah). Dengan bobot kompetitor 15%, selisih antar sektor paling besar sekitar 10 poin. Skor lebih mencerminkan kekuatan wilayah.
- Kata "uji sensitivitas" di subjudul slide: **belum dikerjakan**.

**Hal yang perlu disampaikan**
- Rentang, rata-rata, dan jumlah per kategori.
- Pola tiga kelompok wilayah, singkat.
- Catatan: nol titik di OSM membuat skor sektor tertentu terlalu tinggi.
- Bahwa skor lebih dibedakan oleh wilayah daripada sektor.

**Hal yang tidak perlu disampaikan**
- Jangan menyatakan Kota Yogyakarta "paling layak untuk usaha apa saja" tanpa catatan OSM.
- Jangan klaim sudah melakukan uji sensitivitas. Kalau ditanya: belum, itu langkah lanjutan.
- Tidak perlu membacakan semua angka per sektor. Pilih dua atau tiga yang mewakili.

**Script general**
"Ini hasilnya untuk 25 kombinasi wilayah dan sektor. Skor berkisar dari 39,7 sampai 81,5, dengan rata-rata 55,7. Lima kombinasi masuk Layak, sebelas Cukup Layak, dan sembilan Kurang Layak. Polanya begini. Sleman dan Bantul hampir semuanya Cukup Layak, dengan kafe sebagai sektor tertinggi di keduanya. Kota Yogyakarta unggul karena daya beli dan pengeluarannya tertinggi, tapi untuk kafe skornya paling rendah di kota itu, karena sewa paling mahal dan kafe di sana paling padat. Kulon Progo dan Gunungkidul punya sewa paling murah, tapi daya belinya paling rendah, sehingga sebagian besar kombinasinya Kurang Layak. Ada catatan jujur dari kami. Antar sektor di satu wilayah, hanya jumlah kompetitor yang berbeda, jadi skor lebih banyak mencerminkan karakter wilayah daripada sektornya. Dan untuk sektor yang titiknya nol di OpenStreetMap, skornya terdorong naik karena dianggap tanpa pesaing, jadi perlu dibaca hati-hati."

---

## Slide 8: Pilar 2 — Clustering: Segmentasi Karakteristik Wilayah (Metodologi) — Presenter 4 — Target: 60 detik

**Outline**
- Tujuan: mengenali kemiripan karakter lingkungan bisnis antar wilayah.
- Variabel yang dipakai dan alur: standardisasi → K-Means → PCA.
- Posisi hasil: pengelompokan deskriptif (n = 5).

**Materi**
- **Variabel:** PDRB per kapita, pengeluaran per kapita, kepadatan penduduk, harga sewa, rasio kompetitor per 1.000 penduduk, dan rasio UMKM per 1.000 penduduk (enam variabel tingkat wilayah).
- **Standardisasi (z-score):** menyetarakan skala. Kepadatan Kota Yogyakarta lebih dari 11.000 jiwa/km², sedangkan rasio kompetitor di bawah 2. Tanpa standardisasi, angka besar mendominasi jarak antar wilayah.
- **K-Means (K = 3):** mengelompokkan wilayah yang profilnya mirip. Seperti membagi anak-anak ke tiga kelompok bermain berdasarkan kemiripan, dengan pusat kelompok yang digeser sampai stabil.
- **PCA 2D:** merangkum enam variabel menjadi dua sumbu supaya bisa digambar. Hanya untuk visualisasi. K-Means tetap dihitung dari enam variabel.
- **Keterbatasan:** hanya 5 wilayah. Data ekonomi dan sewa tersedia per kabupaten/kota, bukan per kecamatan. Jadi hasil ini pengelompokan deskriptif, bukan penemuan pola tersembunyi. K = 3 dipilih supaya menghasilkan tiga profil yang mudah ditafsirkan.

**Hal yang perlu disampaikan**
- Tujuan, enam variabel, tiga langkah.
- Alasan standardisasi dengan contoh kepadatan Kota Yogyakarta.
- Pernyataan jujur bahwa n = 5 sehingga ini deskriptif.

**Hal yang tidak perlu disampaikan**
- Kotak "Evaluasi Cluster" (inertia, silhouette, elbow). Tidak ada perhitungan itu di kode. Jangan klaim sudah dihitung.
- Frasa "6 input (5 variabel kriteria + hasil MCDA)" di bar bawah. Sebut saja enam variabel wilayah. Hasil MCDA tidak dipakai sebagai input clustering.
- Matematika algoritma (iterasi, eigenvalue).

**Script general**
"Pilar 2 menjawab pertanyaan: seperti apa karakter lingkungan bisnis di tiap kabupaten dan kota. Kami pakai enam variabel wilayah: PDRB, pengeluaran, kepadatan penduduk, sewa, rasio kompetitor, dan rasio UMKM per seribu penduduk. Langkahnya tiga. Pertama, standardisasi, supaya skala tiap variabel sebanding. Kepadatan Kota Yogyakarta yang lebih dari sebelas ribu jiwa per kilometer persegi jadi tidak menenggelamkan variabel lain. Kedua, K-Means dengan tiga klaster, yaitu mengelompokkan wilayah yang profilnya mirip. Ketiga, PCA, yang merangkum enam variabel menjadi dua sumbu supaya bisa digambar di peta dua dimensi. Perlu kami sampaikan, datanya hanya lima wilayah, karena data ekonomi memang hanya tersedia per kabupaten dan kota. Jadi hasil ini kami posisikan sebagai pengelompokan deskriptif, bukan penemuan pola tersembunyi."

---

## Slide 9: Pilar 2 — Peta Klasterisasi dan Scatter PCA 2D — Presenter 4 — Target: 70 detik

**Outline**
- Tiga klaster dan wilayah anggotanya.
- Membaca scatter PCA dan arti 94,09%.
- Catatan: pengaruh data OSM terhadap posisi Sleman.

**Materi**
- **Klaster Kota Yogyakarta (Urban Padat, Jenuh & Biaya Tinggi):** kepadatan sekitar 11 ribu jiwa/km², PDRB tertinggi, sewa termahal Rp850.000/m².
- **Klaster Sleman (Pasar Berkembang & Biaya Menengah):** kepadatan sekitar 2.000 jiwa/km², pengeluaran tinggi, sewa Rp725.000/m², rasio kompetitor tertinggi.
- **Klaster Bantul, Kulon Progo, Gunungkidul (Pasar Perintis & Biaya Terjangkau):** daya beli lebih rendah dan sewa lebih terjangkau (Rp220.000–450.000/m²).
- **Scatter PCA:** Kota Yogyakarta jauh di kanan, Sleman di atas, tiga wilayah lain mengelompok di kiri-bawah. Dua sumbu menyimpan 94,09% informasi asli (kehilangan 5,91%), jadi gambar dua dimensi tidak menyesatkan.
- **Catatan:** Sleman terpisah antara lain karena jumlah titik OSM-nya paling banyak (1.393 titik). Itu bisa mencerminkan pemetaan OSM yang lebih lengkap, bukan hanya persaingan lebih ketat.
- Nama klaster adalah label tafsiran manusia dari urutan rata-rata PDRB, bukan keluaran algoritma.

**Hal yang perlu disampaikan**
- Tiga klaster dan anggotanya, dengan ciri pembeda.
- Cara membaca scatter: jarak berdekatan berarti profil mirip.
- Total variansi 94,09%, artinya gambar dua dimensi cukup setia.
- Caveat OSM terhadap posisi Sleman.

**Hal yang tidak perlu disampaikan**
- Angka rinci di tiga kotak teks klaster (PDRB "Rp 126,8 juta", rentang sewa "220.000–275.000" untuk klaster 2, "rasio omzet vs biaya terbaik"). Cukup deskripsi umum seperti di Script general.
- Pembagian PC1 dan PC2 secara rinci. Cukup total 94,09%.
- Jangan menyebut klaster ini "terbukti valid secara statistik". Datanya lima wilayah.

**Script general**
"Hasilnya tiga klaster. Kota Yogyakarta berdiri sendiri sebagai pasar padat dengan biaya tinggi: kepadatan sekitar sebelas ribu jiwa per kilometer persegi, PDRB tertinggi, dan sewa Rp850 ribu per meter persegi. Sleman membentuk klaster sendiri sebagai pasar berkembang dengan biaya menengah. Lalu Bantul, Kulon Progo, dan Gunungkidul bersama-sama membentuk klaster perintis dengan biaya terjangkau. Di scatter plot sebelah kiri bawah terlihat ketiga wilayah itu mengelompok, Kota Yogyakarta jauh di kanan, dan Sleman di atas. Kalau dua titik berdekatan, artinya profil ekonominya mirip. Dua sumbu ini menyimpan 94,09 persen informasi asli, jadi gambar dua dimensinya tidak menyesatkan. Satu catatan: Sleman terpisah antara lain karena jumlah titik kompetitor OpenStreetMap-nya paling banyak, dan itu bisa juga mencerminkan pemetaan yang lebih lengkap di sana, bukan hanya persaingan yang lebih ketat."

---

## Slide 10: Pilar 3 — Forecasting: Model dan Metode — Presenter 5 — Target: 85 detik

**Outline**
- Pertanyaan yang dijawab dan data yang dipakai.
- Regresi linear OLS dalam bahasa sederhana, dan arti kemiringan tren.
- Interval ketidakpastian 95% dan klasifikasi arah tren.
- Alasan memilih model sederhana (rasio parameter terhadap data).

**Materi**
- **Data:** jumlah unit usaha per sektor tahun 2019–2023 dari BPS, dijumlahkan se-DIY. Hanya 5 titik per sektor.
- **OLS trend:** tarik satu garis lurus yang paling dekat ke lima titik, lalu perpanjang ke 2024–2026. Rumus: prediksi = β₀ + β₁ × tahun. β₁ adalah kemiringan, yaitu berapa unit usaha bertambah per tahun.
- **Contoh nyata (kafe):** 1.970, 1.910, 2.070, 2.300, 2.590 unit. Kemiringan sekitar +163 unit per tahun, proyeksi 2026 sekitar 2.983 unit, R² 0,855.
- **Interval 95%:** rentang ketidakpastian yang melebar semakin jauh tahun yang diramal.
- **Klasifikasi arah:** tiga kelas (Naik/Ekspansif, Stabil/Moderat, Menurun/Stagnan) berdasarkan laju pertumbuhan.
- **Mengapa OLS, bukan ARIMA/SARIMA:** ARIMA butuh puluhan titik untuk menaksir parameternya. Dengan 5 titik ia cenderung menghafal naik-turun yang kebetulan. OLS hanya menaksir 2 angka. Data tahunan juga tidak bisa menunjukkan pola musiman. Hasil disebut baseline.
- **Mengapa tidak menambah prediktor (PDRB, pertumbuhan UMKM, dan lain-lain):** setiap prediktor menambah satu parameter. Sekarang 2 parameter untuk 5 titik (sisa 3 derajat kebebasan). Dengan 3 prediktor tambahan jadi 5 parameter untuk 5 titik, sehingga model bisa melewati semua titik dengan sempurna, yaitu menghafal, bukan belajar. Selain itu prediktornya ikut naik seiring waktu (tidak bisa dibedakan pengaruhnya), dan untuk meramal 2024–2026 prediktornya harus diramal dulu, jadi kesalahan menumpuk.
- Data eksternal dipakai sebagai konteks pendukung di kesimpulan, bukan masukan model. Contoh: total UMKM DIY naik dari 337.060 (2021) ke 347.744 (2025), sekitar 3,2% dalam 4 tahun. Itu narasi, bukan bukti.

**Hal yang perlu disampaikan**
- Pertanyaan yang dijawab Pilar 3 dan datanya (5 titik).
- Garis lurus dan arti kemiringan, dengan satu contoh angka.
- Interval 95% melebar semakin jauh.
- Mengapa model sederhana dan sebutan "baseline".

**Hal yang tidak perlu disampaikan**
- Rumus estimasi β₁ dan β₀ secara rinci. Cukup konsepnya.
- Notasi "t, n − 2 = 5" dan ambang CAGR 6,8% / 0,6% di kotak bawah. Cukup sebut "tiga kelas berdasarkan laju pertumbuhan".
- Jangan klaim model akurat atau pasti. Jangan klaim uji leave-one-out sudah dilakukan (belum).
- Bias-variance secara teori panjang. Cukup rasio parameter terhadap data, bila ditanya.

**Script general**
"Pilar 3 menjawab pertanyaan: sektor mana yang sedang naik atau melambat. Datanya jumlah unit usaha per sektor tahun 2019 sampai 2023 dari BPS, dijumlahkan se-DIY. Metodenya regresi linear OLS. Gampangnya, kami tarik satu garis lurus yang paling dekat ke lima titik data, lalu garis itu diperpanjang ke tahun 2024 sampai 2026. Rumusnya sederhana: prediksi sama dengan beta nol ditambah beta satu kali tahun, dan beta satu itu kemiringan tren, yaitu berapa unit usaha bertambah per tahun. Contohnya kafe: kemiringannya sekitar 163 unit per tahun. Karena ramalan tidak pernah pasti, kami tambahkan interval ketidakpastian 95 persen, yang makin lebar semakin jauh tahun yang diramal. Lalu arah tren kami klasifikasikan jadi tiga: naik, stabil, dan menurun, berdasarkan laju pertumbuhannya. Kenapa model sesederhana ini? Karena per sektor hanya ada lima titik data. Garis lurus hanya punya dua angka yang ditaksir, jadi jauh lebih aman dari menghafal pola kebetulan. Itu sebabnya kami menyebut hasilnya baseline."

---

## Slide 11: Pilar 3 — Forecasting: Proyeksi Tren Pertumbuhan Sektor (2019–2026) — Presenter 5 — Target: 80 detik

**Outline**
- Membaca grafik proyeksi per sektor (pola, arah, pita ketidakpastian).
- Tabel R², MAPE, RMSE dan cara membacanya.
- Posisi hasil: sinyal arah, bukan angka pasti.

**Materi**
- **Pola per sektor:**
  - Kafe dan restoran: turun sedikit di 2020 (pandemi), lalu naik tajam sampai 2023, proyeksi terus naik sampai 2026. Pita ketidakpastian paling lebar di kafe dan restoran karena datanya paling berfluktuasi.
  - Minimarket: naik stabil dan konsisten.
  - Laundry: turun di 2020 lalu naik moderat.
  - Toko kelontong tradisional: menurun perlahan dari tahun ke tahun (sekitar −73 unit per tahun, atau sekitar −0,6% per tahun).
- **Tabel evaluasi (R²):** kelontong 0,999; minimarket 0,966; kafe 0,855; restoran 0,776; laundry 0,726. R² artinya seberapa besar naik-turun data yang dijelaskan garis lurus.
- **Cara membaca R² dan MAPE dengan benar:** keduanya dihitung pada data yang sama dengan yang dipakai membuat garis (in-sample). Garis yang disesuaikan ke 5 titik memang terlihat bagus. Ukuran ini menunjukkan kecocokan masa lalu, bukan akurasi masa depan.
- **Kekokohan tren:** secara manual, kemiringan kafe tetap positif bila satu tahun dibuang bergantian (kisaran +115 sampai +227 per tahun). Jadi arah naik cukup kokoh, besaran kecepatannya kurang pasti. Uji leave-one-out ini belum diimplementasikan di kode (hanya hitungan manual).
- **Catatan kanan bawah slide:** proyeksi adalah indikator arah, model linear baseline rentan overfitting karena n = 5, perbaikan algoritma dan variabel eksternal menjadi fokus selanjutnya.

**Hal yang perlu disampaikan**
- Pola utama tiap sektor, satu kalimat.
- Arti pita warna (rentang 95%).
- Dua atau tiga angka R² sebagai contoh, dengan peringatan in-sample.
- "Sinyal arah, bukan angka prediksi pasti."

**Hal yang tidak perlu disampaikan**
- Angka "+8,4% per tahun" dan "+3,5% per tahun" di kotak teks kanan.
- Judul kotak "Kota Yogyakarta: Pasar Padat & Risiko Tinggi" di slide ini. Tidak relevan dengan forecasting.
- Menyebut laundry "stabil". Grafiknya menunjukkan tren naik moderat.
- Jangan menyatakan R² tinggi berarti ramalan akurat. Jangan membacakan semua angka MAPE dan RMSE.

**Script general**
"Ini hasil proyeksinya untuk lima sektor. Kafe dan restoran turun sedikit di 2020 saat pandemi, lalu naik tajam sampai 2023, dan proyeksinya terus naik sampai 2026. Minimarket naik stabil, dan laundry naik lebih moderat. Toko kelontong tradisional justru menurun perlahan dari tahun ke tahun. Pita berwarna di grafik adalah rentang ketidakpastian 95 persen, dan terlihat paling lebar di kafe dan restoran, karena datanya paling berfluktuasi. Di tabel, R kuadrat kafe 0,855 dan kelontong 0,999, artinya garis lurus cukup cocok dengan data historis. Tapi kami ingin jujur: ukuran kecocokan ini dihitung pada data yang sama dengan yang dipakai membuat garis, dan datanya hanya lima titik. Jadi kami membacanya sebagai sinyal arah, bukan angka prediksi yang pasti. Itu juga yang tertulis di catatan kanan bawah, bahwa model ini rentan terhadap keterbatasan data, dan perbaikan algoritma jadi fokus berikutnya."

---

## Slide 12: Pilar 4 — Mesin Rekomendasi — Presenter 6 — Target: 70 detik

**Outline**
- Tiga input pengguna.
- Lima tahap inferensi.
- Output berupa kartu rekomendasi.
- Sifat sistem: hanya membaca hasil pilar sebelumnya.

**Materi**
- **Input:** sektor usaha (wajib), modal sewa tahunan, dan preferensi wilayah (opsional).
- **Lima tahap:**
  1. Lookup Pilar 1: ambil skor dan kategori kelayakan untuk sektor dan wilayah yang dipilih.
  2. Cluster Pilar 2: tambahkan profil klaster wilayah.
  3. Trend Pilar 3: tambahkan arah tren sektor (tingkat se-DIY, satu label per sektor).
  4. BFR Check (Budget Feasibility): bandingkan modal sewa pengguna dengan estimasi sewa wilayah itu. Patokan: ruko sekitar 30 m². Contoh: Sleman 725.000 × 30 = Rp21.750.000 per tahun.
  5. Multi-Region Checking: bila pengguna tidak memilih wilayah, semua wilayah diperingkat dan tiga teratas ditampilkan.
- **Output:** kartu rekomendasi (skor, kategori, luas kios yang terjangkau, rekomendasi mitigasi seperti peringatan budget atau kejenuhan kompetitor).
- **Mengapa berbasis aturan, bukan model baru:** semua perhitungan berat sudah selesai di Pilar 1–3. Pilar 4 hanya menggabungkan hasil, sehingga ringan, stabil, dan tidak mengarang angka.
- Patokan 30 m² adalah asumsi ukuran ruko UMKM standar yang kami tetapkan sendiri.

**Hal yang perlu disampaikan**
- Tiga input, lima tahap secara berurutan.
- Pilar ini hanya membaca hasil, tidak menghitung ulang dari data mentah.
- Isi kartu rekomendasi.
- Patokan 30 m² sebagai asumsi.

**Hal yang tidak perlu disampaikan**
- Angka "0 execution error" dan "< 25 ms" di kotak Validasi Sistem. Tidak ada kode pengujian yang membuktikannya di repo. Cukup katakan sistem ringan karena hanya membaca tabel hasil, dan setiap permintaan dihitung terpisah (stateless).
- Isi gambar kartu (skor 72,5, luas 24 m²). Itu ilustrasi tampilan, bukan hasil sistem.
- Detail kode atau struktur kelasnya.

**Script general**
"Pilar 4 adalah satu-satunya bagian yang berinteraksi langsung dengan pengguna. Inputnya tiga: sektor usaha, modal sewa tahunan, dan preferensi wilayah yang sifatnya opsional. Sistem lalu menjalankan lima tahap. Satu, mencari skor kelayakan dari hasil Pilar 1. Dua, menambahkan profil klaster wilayah dari Pilar 2. Tiga, menambahkan arah tren sektor dari Pilar 3. Empat, mengecek apakah modal cukup untuk sewa di wilayah itu, dengan patokan ruko sekitar 30 meter persegi. Lima, kalau pengguna belum menentukan wilayah, sistem membandingkan semua wilayah dan menampilkan tiga yang terbaik. Keluarannya berupa kartu rekomendasi berisi skor, kategori, luas kios yang terjangkau, dan rekomendasi mitigasi. Yang penting, pilar ini tidak menghitung ulang dari data mentah. Ia hanya membaca hasil pilar sebelumnya, sehingga ringan dan responsnya cepat."

---

## Slide 13: Simulasi Engine Rekomendasi — Studi Kasus Personal — Presenter 6 — Target: 70 detik

**Outline**
- Skenario 1: wilayah spesifik dengan budget.
- Skenario 2: wilayah terbuka, tiga teratas.
- Penutup: keterbatasan dan langkah berikutnya.

**Materi**
- **Skenario 1 (kafe, Sleman, Rp30 juta per tahun):**
  - Skor 56,7, kategori Cukup Layak.
  - Profil wilayah: pasar berkembang dengan biaya menengah.
  - Tren sektor kafe: naik (ekspansif).
  - Validasi anggaran: tarif Rp725.000 per m², jadi Rp30 juta cukup untuk sekitar 41 m², di atas patokan 30 m². Status memadai.
- **Skenario 2 (laundry, semua wilayah):** sistem memperingkat kelima wilayah dan menampilkan tiga teratas dengan skor, kategori, dan profil pasar singkat. Dengan data saat ini, urutan teratas untuk laundry adalah Kota Yogyakarta (81,5), Sleman (51,8), Gunungkidul (50,2). Kota Yogyakarta unggul sebagian karena OpenStreetMap mencatat nol laundry di sana, padahal BPS mencatat ratusan unit.
- **Keterbatasan utama sistem:** bobot skor ditetapkan tim; data ekonomi dan sewa hanya tingkat kabupaten/kota; OSM tidak lengkap untuk usaha informal; peramalan hanya 5 titik data; tidak ada validasi terhadap keberhasilan usaha riil.
- **Langkah berikutnya:** prototipe web dengan Streamlit, lalu website final dengan Laravel.

**Hal yang perlu disampaikan**
- Dua skenario sebagai gambaran cara pakai: input, lalu keluaran berupa skor, kategori, profil, tren, dan cek budget.
- Skenario 1: skor, kategori, cek budget.
- Skenario 2: bentuk keluaran (peringkat tiga wilayah beserta alasannya).
- Penutup: alat bantu pertimbangan, bukan jaminan keberhasilan. Langkah berikutnya: Streamlit dan Laravel.

**Hal yang tidak perlu disampaikan**
- Angka skor dan urutan wilayah di skenario 2 pada slide (86,8 / 79,4 / 71,2 dan urutan Sleman, Bantul, Kota). Jelaskan format hasilnya saja, bukan angkanya.
- "+8,4% per tahun" dan "Klaster 1 (Semi-Urban Bertumbuh / Sweet Spot)" di skenario 1. Cukup "tren naik" dan "pasar berkembang".
- Tulisan "LAYAK" di baris Status skenario 1. Yang benar kategorinya Cukup Layak (skor 56,7).
- Jangan menjanjikan hasil bisnis tertentu.

**Script general**
"Terakhir, dua simulasi. Skenario pertama, calon pengusaha ingin membuka kafe di Sleman dengan budget sewa Rp30 juta per tahun. Sistem memberi skor 56,7, kategori Cukup Layak. Wilayahnya berprofil pasar berkembang dengan biaya menengah, dan tren sektor kafe naik. Dengan tarif Rp725 ribu per meter persegi, modal Rp30 juta cukup untuk lebih dari patokan 30 meter persegi, jadi budgetnya memadai. Skenario kedua, calon pengusaha laundry yang terbuka ke semua wilayah. Sistem memperingkat seluruh wilayah dan menampilkan tiga teratas, lengkap dengan skor, kategori, dan profil pasarnya, sehingga pengguna bisa membandingkan pilihan lokasi sekaligus. Satu catatan jujur: untuk sektor yang titiknya sedikit di OpenStreetMap, seperti laundry, hasilnya perlu dibaca bersama keterbatasan data. Sebagai penutup, sistem ini alat bantu pertimbangan, bukan jaminan keberhasilan usaha. Langkah berikutnya, kami membangun prototipe web dengan Streamlit dan website final dengan Laravel. Terima kasih."

---

## Sesi Q&A — Persiapan

Jawab singkat dan jujur. Untuk hal yang belum dikerjakan, katakan terus terang: "belum kami lakukan, dan itu langkah lanjutan".

### Data dan cakupan
**1. (Presenter 1) Kenapa hanya 5 sektor dan 5 wilayah?**
Lima wilayah itu seluruh kabupaten/kota di DIY. Lima sektor dipilih karena bisa dipadankan di OpenStreetMap, tabel unit usaha BPS, dan klasifikasi usaha. Sektor lain belum punya data yang sebanding dari sumber yang sama.

**2. (Presenter 2) Data OpenStreetMap tidak lengkap, apakah hasilnya bias?**
Ya, dan itu temuan kami. Toko kelontong hanya 1 titik di OSM padahal BPS mencatat sekitar 11 ribu unit. Warung rumahan jarang mendaftar di peta digital. Laundry di Kota Yogyakarta juga nol di OSM padahal BPS mencatat ratusan. Mitigasinya, kami menambahkan data resmi SiBakul sebagai pembanding kepadatan usaha dan menandai sektor yang titiknya sedikit sebagai hasil yang perlu dibaca hati-hati.

### Pilar 1: MCDA
**3. (Presenter 3) Kenapa MCDA, bukan machine learning?**
Machine learning terlatih butuh label usaha berhasil atau gagal, dan data publik tidak punya itu. Kalau label kami buat sendiri, hasilnya hanya memantulkan asumsi kami. MCDA transparan, tiap bobot terlihat dan bisa dibahas.

**4. (Presenter 3) Siapa yang menentukan bobot? Sudah diuji sensitivitasnya?**
Bobot ditetapkan tim berdasarkan penalaran: daya beli dianggap faktor utama, jadi totalnya 50 persen. Bobot tidak dipelajari dari data. Uji sensitivitas bobot belum kami lakukan. Itu langkah lanjutan.

**5. (Presenter 3) Kenapa skor antar sektor mirip, dan kenapa Kota Yogyakarta hampir selalu tinggi?**
Hanya jumlah kompetitor yang berbeda antar sektor. Kriteria lain sama untuk satu wilayah. Dengan bobot kompetitor 15 persen, selisih antar sektor di satu wilayah paling besar sekitar 10 poin. Kota Yogyakarta tinggi karena daya beli dan pengeluarannya tertinggi, dan keduanya berbobot 50 persen. Sebagian skornya juga terdorong oleh nol titik di OSM.

### Pilar 2: Clustering
**6. (Presenter 4) K-Means dengan hanya 5 data, apakah valid? Kenapa K = 3?**
Secara statistik lemah, dan kami mengakuinya. Data ekonomi hanya tersedia per kabupaten/kota, jadi tidak bisa dipecah ke kecamatan. Kami memposisikannya sebagai pengelompokan deskriptif. K = 3 dipilih supaya menghasilkan tiga profil yang mudah ditafsirkan, bukan hasil optimasi. Hasilnya masuk akal: Kota Yogyakarta yang padat dan mahal berdiri sendiri, dan tiga wilayah dengan sewa terjangkau berkelompok.

**7. (Presenter 4) Apa fungsi PCA dan apa arti 94,09 persen?**
Wilayah punya enam ukuran, jadi tidak bisa digambar. PCA merangkumnya menjadi dua sumbu untuk visualisasi. 94,09 persen artinya dua sumbu itu menyimpan sekitar 94 persen variasi antar wilayah, jadi gambarnya tidak menyesatkan. Pengelompokan K-Means sendiri tetap dihitung dari enam variabel, bukan dari dua sumbu itu.

### Pilar 3: Forecasting
**8. (Presenter 5) Kenapa regresi linear OLS, bukan ARIMA atau SARIMA?**
Per sektor kami hanya punya lima titik tahunan. ARIMA dan SARIMA butuh puluhan titik untuk menaksir parameternya, dan dengan lima titik model itu cenderung menghafal naik-turun yang kebetulan. Regresi linear hanya menaksir dua angka, jadi jauh lebih aman. Data tahunan juga tidak menunjukkan pola musiman, jadi musiman sengaja tidak dimodelkan. Kami menyebut hasilnya baseline, dan model lanjutan akan diuji bila data lebih panjang.

**9. (Presenter 5) Kenapa tidak menambah variabel seperti PDRB atau pertumbuhan UMKM supaya lebih akurat, padahal datanya ada?**
Karena setiap variabel tambahan menambah satu parameter yang harus ditaksir, sementara datanya cuma lima titik. Sekarang model punya dua parameter untuk lima titik, jadi masih ada sisa data untuk menguji. Dengan tiga variabel tambahan, parameternya jadi lima untuk lima titik, dan model bisa melewati semua titik dengan sempurna. Itu kelihatan akurat, tapi sebenarnya menghafal, dan pada tahun baru bisa lebih buruk. Ada dua masalah lain. Variabel seperti PDRB dan jumlah UMKM ikut naik seiring waktu, sehingga pengaruhnya tidak bisa dipisahkan dari tren waktu itu sendiri. Dan untuk meramal 2024 sampai 2026, kita harus meramal dulu variabel itu, sehingga kesalahan menumpuk. Karena itu data tersebut kami pakai sebagai konteks pendukung di kesimpulan, bukan masukan model. Kalau data lebih panjang, kovariat bisa diuji dengan validasi yang layak.

**10. (Presenter 5) R² tinggi berarti ramalannya akurat? Bagaimana tahu tren itu kokoh?**
Tidak otomatis. R² dihitung pada data yang sama dengan yang dipakai membuat garis, jadi garis yang disesuaikan ke lima titik memang terlihat bagus. Itu kecocokan masa lalu, bukan akurasi masa depan. Untuk menguji kekokohan, idealnya dilakukan uji leave-one-out: hitung ulang kemiringan sambil membuang satu tahun bergantian. Uji itu belum kami implementasikan. Pemeriksaan manual pada kafe menunjukkan kemiringan tetap positif di setiap pembuangan, jadi arahnya cukup kokoh, tetapi besarannya tidak pasti. Karena itu kami menyajikan ramalan sebagai sinyal arah.

### Pilar 4 dan keterbatasan
**11. (Presenter 6) Bagaimana rekomendasi dihasilkan, dan dari mana patokan 30 meter persegi?**
Mesin hanya membaca tabel hasil Pilar 1 sampai 3, jadi tidak menghitung ulang dari data mentah. Patokan 30 meter persegi adalah asumsi ukuran ruko standar UMKM yang kami tetapkan sendiri, untuk membandingkan budget pengguna dengan estimasi sewa tahunan di wilayah itu.

**12. (Presenter 6) Apakah sistem menjamin usaha berhasil? Apa keterbatasan terbesarnya?**
Tidak. Ini alat bantu pertimbangan. Keterbatasan utama: bobot skor ditentukan tim dan bukan dipelajari dari data; data ekonomi dan sewa hanya tingkat kabupaten/kota sehingga lokasi di dalam satu wilayah tidak dibedakan; OpenStreetMap tidak lengkap untuk usaha informal; peramalan hanya memakai lima titik data; dan tidak ada validasi terhadap keberhasilan usaha sebenarnya karena datanya tidak tersedia.

---

## Pengecekan total waktu

| Slide | Presenter | Detik |
|---|---|---|
| 02 | 1 | 80 |
| 03 | 1 | 70 |
| 04 | 2 | 80 |
| 05 | 2 | 85 |
| 06 | 3 | 85 |
| 07 | 3 | 65 |
| 08 | 4 | 60 |
| 09 | 4 | 70 |
| 10 | 5 | 85 |
| 11 | 5 | 80 |
| 12 | 6 | 70 |
| 13 | 6 | 70 |
| **Total** | | **900 detik = 15 menit** |

- Salam pembuka ada di awal slide 02 dan salam penutup di akhir slide 13, jadi sudah termasuk hitungan di atas. Slide judul, anggota, dan "Thank You" tidak diberi waktu terpisah.
- **Q&A tidak termasuk dalam 15 menit.** Siapkan sebagai cadangan sesuai ketentuan.
- Latihan sekali dengan stopwatch. Kalau melebihi target lebih dari 10 detik, potong contoh, bukan inti.
- Slide 10 dan 11 paling padat. Kalau Presenter 5 kehabisan waktu, potong kalimat tentang rumus di slide 10.
