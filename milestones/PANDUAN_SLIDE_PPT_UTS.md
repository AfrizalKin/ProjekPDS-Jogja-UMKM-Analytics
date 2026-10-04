# 📊 PANDUAN LENGKAP SLIDE PRESENTASI UTS (KONTEN UTUH SIAP SALIN)
## Pemodelan Kelayakan Sektor Usaha UMKM Menggunakan Pendekatan Machine Learning dan Time Series untuk Rekomendasi Lokasi Berbasis Data di D.I. Yogyakarta
> **Mata Kuliah:** Pengantar Data Sains (PDS) — Semester 3  
> **Bobot Penilaian:** 35% Nilai Akhir UTS  
> **Panduan Tim:** Seluruh materi difokuskan pada **substansi data, metodologi, dan insight kuantitatif**. Gunakan teks di setiap slide langsung ke template presentasi. Sisipkan gambar grafik beresolusi tinggi sesuai catatan `[FILE GAMBAR]` yang disediakan.

---

### SLIDE 1: JUDUL & IDENTITAS TIM PENELITI

#### TEKS SLIDE:
* **SISTEM REKOMENDASI KELAYAKAN SEKTOR USAHA UMKM BERBASIS DATA**
* **Sub-Judul:** Pendekatan Machine Learning dan Time Series untuk Rekomendasi Lokasi Usaha di Provinsi D.I. Yogyakarta
* **Mata Kuliah:** Pengantar Data Sains (PDS) — Semester 3 (T.A. 2024/2025)
* **Dosen Pengampu:** Ivan Luthfi Ihwani, S.Si., M.Sc., Ph.D.
* **Institusi:** Fakultas Matematika dan Ilmu Pengetahuan Alam, Universitas Gadjah Mada
* **Tim Peneliti:**
  1. Afrizal Kinayung Aura Aqilan
  2. Andhika Mulia Ompusunggu
  3. Atalla Khayru Wijaya
  4. Elia Theorupun Orno
  5. Gen Fabian Harapanku
  6. Marcellino Raihandhani

---

### SLIDE 2: LATAR BELAKANG, PROBLEM STATEMENT & DAMPAK RISIKO

#### TEKS SLIDE:
* **Peran Kritis Sektor UMKM:**
  - Sektor UMKM berkontribusi sebesar **61,07% terhadap PDB Nasional** serta menyerap **97% tenaga kerja nasional** (Kemenkop UKM, 2023).
  - Di Provinsi D.I. Yogyakarta, tercatat **342.463 unit UMKM aktif** yang menjadi fondasi ekonomi rakyat (SiBakul Diskop UKM DIY, 2025).
* **Problem Statement (Akar Masalah):**
  - Pemilihan lokasi usaha dan sektor bisnis mayoritas masih didasarkan pada **intuisi subjektif, coba-coba, atau tren sesaat media sosial** tanpa adanya validasi data kondisi ekonomi wilayah.
* **Dampak Riil & Kerugian Usaha (Didukung Referensi Empiris):**
  - **Tingginya Tingkat Mortalitas Bisnis:** Sekitar **50% UMKM baru mengalami kebangkrutan pada 3–5 tahun pertama** operasional akibat kesalahan pemilihan lokasi (U.S. Small Business Administration, 2022; Zimmerer & Scarborough, 2008).
  - **Kanibalisasi Pasar & Perang Harga:** Penumpukan usaha sejenis pada koridor jalan tertentu (seperti ratusan kafe di sekitar area kampus Sleman dan Kota Jogja) menurunkan omzet rata-rata unit usaha (Tjiptono, 2019).
  - **Inefisiensi Modal Akibat Beban Sewa:** Tarif sewa properti komersial yang tinggi di pusat kota (mencapai rata-rata Rp 850.000/m²/tahun) menguras modal kerja sebelum usaha mencapai *break-even point* karena produk tidak terserap daya beli lokal (BPS DIY, 2024; Bank Indonesia, 2024).

---

### SLIDE 3: TUJUAN PROJEK & SISTEMATIKA ARSITEKTUR SOLUSI

#### TEKS SLIDE:
* **Tujuan Utama Projek:**
  - Mentransformasi proses penentuan lokasi usaha dari pendekatan intuisi menjadi **Sistem Pendukung Keputusan (Decision Support System) berbasis data sains terintegrasi**.
* **Sistematika Arsitektur Sistem:**
  - Sistem mengintegrasikan lima dataset lintas domain yang mencakup kompetisi spasial mikro, indikator makroekonomi wilayah, biaya sewa komersial, dinamika tren deret waktu pasar, dan sensus resmi UMKM daerah.
  - Data diproses melalui pipeline pemodelan terpadu yang terdiri atas *Multi-Criteria Decision Analysis* (Pilar 1), *K-Means Clustering* dengan reduksi dimensi *PCA 2D* (Pilar 2), serta peramalan deret waktu regresi linear (Pilar 3).
  - Lapisan inferensi akhir (Pilar 4) memanfaatkan mesin pencocokan aturan untuk mengevaluasi kecukupan modal sewa pengguna dan merangking lokasi alternatif terbaik secara real-time.
  - Seluruh pemodelan dihitung secara modular pada backend analitik, memungkinkan antarmuka aplikasi web membaca hasil secara instan, transparan, dan dapat dipertanggungjawabkan secara ilmiah.

---

### SLIDE 4: DATA REQUIREMENTS (KEBUTUHAN 5 DATASET MULTI-DOMAIN)

#### TEKS SLIDE:
* **Struktur 5 Dataset Multi-Sumber:**
  1. **Kompetitor Usaha Spasial (OpenStreetMap Overpass API):** 2.796 titik koordinat *Point of Interest* (POI) aktif (*Restoran, Kafe, Minimarket, Laundry, Toko Kelontong*).
  2. **Kondisi Makroekonomi Wilayah (BPS D.I. Yogyakarta, 2024):** Indikator PDRB per kapita, pengeluaran bulanan per kapita, luas wilayah, dan kepadatan penduduk.
  3. **Biaya Sewa Komersial (Bank Indonesia & Riset Pasar Properti, 2024):** Normalisasi tarif sewa kios/ruko komersial per m² per tahun pada 5 kabupaten/kota.
  4. **Tren Pertumbuhan Sektor Usaha (BPS DIY 2019–2023 & Google Trends):** Deret waktu volume unit usaha per tahun (% YoY) dan indeks tren penelusuran pasar digital.
  5. **Basis Data Statistik UMKM Resmi (SiBakul Diskop UKM DIY, 2025):** Sensus 342.463 unit UMKM resmi untuk mengukur densitas struktural per 1.000 penduduk.
* **Catatan Ruang Lingkup Data:**
  - *(Catatan: Karakteristik data dan cakupan variabel saat ini bersifat adaptif/sementara dan dapat disesuaikan seiring perkembangan kebutuhan analisis lanjutan pasca-UTS)*.

---

### SLIDE 5: METODE PENGAMBILAN DATASET (DETAIL TEKNIS EKSTRAKSI)

#### TEKS SLIDE:
* **1. OpenStreetMap (Metode: Overpass API Automation):**
  - Mengirim kueri Overpass QL melalui protokol HTTPS POST ke server Overpass API dengan kriteria tag spesifik (`amenity`, `shop`, `craft`).
  - **Mekanisme Spatial Grid Sampling:** Memecah wilayah padat ke dalam sub-grid berkoordinat presisi ($2 \times 2$ dan $3 \times 3$) untuk menghindari kegagalan koneksi *HTTP 504 Gateway Timeout*.
  - **Failover & Exponential Backoff:** Menerapkan pengalihan otomatis ke 3 server mirror (*de*, *kumi*, *openstreetmap.fr*) serta jeda *sleep* adaptif saat menerima respons *HTTP 429 Too Many Requests*.
* **2. Data Makroekonomi Wilayah (Metode: Tabular Extraction & Web Scraping BPS):**
  - Mengunduh publikasi statistik digital BPS DIY 2024 dan mem-parsing data tabular melalui modul ekstraksi tabel multi-header (melewati metadata baris awal dengan `skiprows=4` dan encoding `utf-8-sig`).
* **3. Biaya Sewa Properti (Metode: Web Scraping Properti & Integrasi Laporan BI):**
  - Melakukan web scraping data listing properti komersial pada agregator sewa terpercaya serta mengekstraksi data Indeks Perkembangan Properti Komersial Bank Indonesia.
* **4. Tren Pertumbuhan Usaha (Metode: Scraping BPS Time Series & Pytrends API):**
  - Menggabungkan data deret waktu tabel sensus ekonomi BPS DIY (2019–2023) dengan pemanggilan otomatis Google Trends API melalui library `pytrends` untuk kata kunci sektor di wilayah DIY (skala 0–100).
* **5. Data Resmi UMKM Daerah (Metode: Ekstraksi Portal SiBakul Jogja):**
  - Mengekstraksi rekapitulasi data agregat sensus dari basis data terintegrasi Dinas Koperasi dan UKM Pemprov D.I. Yogyakarta (rilis 2025).

---

### SLIDE 6: DATA OVERVIEW (FUNGSI DATA DALAM ARSITEKTUR SISTEM)

#### TEKS SLIDE:
* **Peran Spesifik Setiap Dataset dalam Arsitektur:**
  1. **Dataset 1 (Kompetitor Spasial OSM):**
     - *Tentang:* Sebaran koordinat nyata titik usaha kompetitor di lapangan.
     - *Fungsi:* Menghitung densitas persaingan langsung per sektor dan bertindak sebagai penalti tingkat kejenuhan lokal pada Pilar 1 serta validasi sebaran pada Pilar 2.
  2. **Dataset 2 (Kondisi Makroekonomi BPS):**
     - *Tentang:* Kapasitas daya beli masyarakat dan kepadatan pasar sasaran.
     - *Fungsi:* Parameter positif pengukur daya serap ekonomi pada Pilar 1 dan menjadi fitur penentu segmentasi klaster wilayah pada Pilar 2.
  3. **Dataset 3 (Biaya Sewa Komersial):**
     - *Tentang:* Estimasi beban belanja modal awal (*fixed cost/capex*) per m²/tahun.
     - *Fungsi:* Faktor pengurang kelayakan pada formula Pilar 1 dan dasar kalkulasi validasi kesesuaian anggaran pengguna pada Pilar 4.
  4. **Dataset 4 (Tren Sektor Usaha BPS + Google):**
     - *Tentang:* Dinamika pertumbuhan unit bisnis historis (5 tahun) dan atensi digital pasar.
     - *Fungsi:* Basis data pemodelan proyeksi deret waktu pada Pilar 3 untuk mendeteksi arah pergerakan pasar (ekspansif vs melambat).
  5. **Dataset 5 (Statistik UMKM SiBakul):**
     - *Tentang:* Kepadatan struktural total UMKM formal dan informal daerah per wilayah.
     - *Fungsi:* Indikator kalibrasi makro (rasio UMKM per 1.000 penduduk) pada Pilar 1 & 2 untuk mengoreksi bias keterbatasan data peta digital.

---

### SLIDE 7: KUALITAS DATA & TEMUAN KRUSIAL PASCA-CLEANING

#### TEKS SLIDE:
* **Scorecard Kualitas Data (4 Dimensi Standar Data Science):**
  - **Completeness:** 100% lengkap pada variabel esensial ekonomi, sewa, dan koordinat spasial.
  - **Consistency:** 100% terstandarisasi dengan penyeragaman string nama 5 kabupaten/kota.
  - **Uniqueness:** Bebas duplikasi setelah pembersihan 776 data kembar akibat irisan grid spasial.
  - **Validity:** Seluruh koordinat tervalidasi berada di Bounding Box geografis D.I. Yogyakarta.
* **4 Temuan Anomali Riil & Solusi Rekayasa Data:**
  1. *Baris Agregat Provinsi (Sumber: BPS DIY):* File BPS menyisipkan baris "D.I. Yogyakarta" di dalam tabel kabupaten/kota yang berisiko terhitung ganda sebagai kabupaten ke-6. $\rightarrow$ **Solusi:** Penerapan *blacklist filtering* otomatis pada script pipeline.
  2. *Duplikasi Border Grid (Sumber: OSM):* Metode grid sampling menyebabkan tempat usaha di perbatasan antar grid terunduh ganda. $\rightarrow$ **Solusi:** Deduplikasi 2 lapis berbasis *Unique ID* dan toleransi jarak spasial $< 5$ meter.
  3. *Inkonsistensi Satuan Sewa (Sumber: Listing Properti):* Iklan properti mencampuradukkan sewa bulanan dan tahunan dengan luas bervariasi. $\rightarrow$ **Solusi:** Standarisasi matematis ke satuan baku: **Rp / m² / tahun**.
  4. *Bias Tagging Kelontong (Sumber: OSM vs SiBakul):* Kueri OSM `shop=grocery` hanya menemukan 1 titik di Sleman karena kontributor menandai warung sebagai `shop=convenience` (bercampur 313 minimarket) dan usaha mikro tidak terpetakan digital. $\rightarrow$ **Solusi:** Mengintegrasikan Dataset 5 SiBakul (170.000+ UMKM perdagangan riil) sebagai acuan densitas per 1.000 penduduk yang valid.

---

### SLIDE 8: METODOLOGI ANALISIS — PILAR 1: SKORING KELAYAKAN SEKTOR USAHA (MCDA)

#### TEKS SLIDE:
* **1. Tujuan & Masalah Bisnis yang Diselesaikan:**
  - Mengukur probabilitas kelayakan dan potensi keberhasilan pembukaan cabang usaha baru untuk seluruh 25 kombinasi wilayah $\times$ sektor (5 kabupaten/kota $\times$ 5 sektor UMKM) di D.I. Yogyakarta.
  - Menggantikan spekulasi dan pertimbangan subjektif wirausahawan pemula dengan *Feasibility Index* komposit kuantitatif (rentang 0–100) yang menyeimbangkan daya beli pasar terhadap biaya sewa dan kompetisi.
* **2. Taksonomi & Spesifikasi 5 Fitur Penilaian:**
  - **Kriteria Keuntungan (Benefit Criteria — Berkontribusi Positif terhadap Skor):**
    • $X_1$ (*PDRB per Kapita ADHB*, BPS 2024, Bobot $+0,25$): Mengukur skala perekonomian dan perputaran modal makro wilayah.
    • $X_2$ (*Pengeluaran per Kapita Bulanan*, BPS 2024, Bobot $+0,25$): Mengukur likuiditas dan daya beli riil konsumen lokal terhadap konsumsi harian.
    • $X_3$ (*Rasio UMKM Terdaftar SiBakul per 1.000 Penduduk*, Diskop UKM 2025, Bobot $+0,15$): Mengukur kematangan ekosistem usaha lokal dan aglomerasi komersial (*commercial vibrancy*).
  - **Kriteria Biaya / Hambatan (Cost Criteria — Berkontribusi Negatif / Penalti terhadap Skor):**
    • $X_4$ (*Rasio Kompetitor Sejenis per 1.000 Penduduk*, OSM 2.796 Titik, Bobot $-0,20$): Mengukur kepadatan kejenuhan pasar lokal dan risiko kanibalisasi omzet.
    • $X_5$ (*Tarif Rata-rata Sewa Properti Komersial per m²/tahun*, BI & Agregator Properti, Bobot $-0,15$): Mengukur beban belanja modal tetap (*fixed overhead expense*).
* **3. Rasionalisasi & Penentuan Bobot (Domain Expert Weighting Scheme):**
  - Total bobot kriteria terstandarisasi penuh: $\sum |w_j| = 0,25 + 0,25 + 0,15 + 0,20 + 0,15 = 1,00$.
  - Alokasi 50% bobot pada variabel daya beli ($X_1 + X_2$) didasarkan pada hukum ekonomi bahwa ketersediaan likuiditas konsumen adalah prasyarat utama terciptanya transaksi.
  - Bobot penalti kompetitor (20%) ditetapkan lebih tinggi dibanding sewa (15%) karena biaya sewa dapat diamortisasi jangka panjang, sedangkan kejenuhan pasar langsung memangkas pangsa pasar harian secara permanen.
* **4. Formulasi Matematis Bertahap:**
  - **Langkah 1: Normalisasi Skala Bebas Satuan (Min-Max Feature Scaling $0 \le Z \le 1$):**
    $$Z_{i,j} = \frac{X_{i,j} - \min(X_j)}{\max(X_j) - \min(X_j) + \epsilon} \quad (\text{Safeguard } \epsilon = 10^{-9})$$
    Menghilangkan disparitas dimensi antar variabel (Rupiah ratusan juta vs rasio desimal).
  - **Langkah 2: Multi-Criteria Decision Analysis (Weighted Linear Combination - WLC):**
    $$\text{Skor Kelayakan} = 100 \times \left( \sum_{b \in \text{Benefit}} w_b \cdot Z_b - \sum_{c \in \text{Cost}} w_c \cdot Z_c + \text{Base Offset} \right)$$
    Formula operasional komputasi:
    $$\text{Skor} = 100 \times \Big( 0,25 \cdot Z_{\text{pdrb}} + 0,25 \cdot Z_{\text{pengeluaran}} + 0,15 \cdot Z_{\text{sibakul}} - 0,20 \cdot Z_{\text{kompetitor}} - 0,15 \cdot Z_{\text{sewa}} + 0,35 \Big)$$
  - **Langkah 3: Bounding & Skala Natural:** Skor dibatasi secara absolut pada rentang $0 \le \text{Skor} \le 100$. Base offset $+0,35$ berfungsi menyelaraskan nilai median teoritis ke dalam skala penilaian persentase yang intuitif bagi pengambil keputusan.
* **5. Justifikasi Akademis Pemilihan MCDA vs Supervised Learning:**
  - Ketiadaan label *ground-truth* biner pada data publik (tidak ada dataset resmi yang melabeli UMKM di DIY sebagai "1 = Sukses Mutlak" vs "0 = Bangkrut").
  - Penggunaan Supervised Classification murni tanpa data label riil berisiko memicu halusinasi data dan *false precision*. MCDA merupakan metodologi baku operasional riset (*Operations Research*) yang diakui secara global untuk permasalahan pemilihan lokasi fasilitas (*Facility Location Problem*).
* **6. Ambang Batas Klasifikasi & Panduan Keputusan Manajerial:**
  - **Kategori Layak (Skor $\ge 70$): 14 Kombinasi (56%)** $\rightarrow$ Wilayah prioritas utama ekspansi; margin keuntungan diproyeksikan aman.
  - **Kategori Cukup Layak (Skor $50 - 69$): 9 Kombinasi (36%)** $\rightarrow$ Rekomendasi bersyarat; memerlukan keunggulan diferensiasi produk unik dan negosiasi tarif sewa yang ketat.
  - **Kategori Kurang Layak (Skor $< 50$): 2 Kombinasi (8%)** $\rightarrow$ Risiko kegagalan tinggi akibat beban sewa ekstrem atau daya serap pasar yang belum terbentuk.
* **7. Metrik Sebaran Riil & Uji Sensitivitas (Robustness Check):**
  - **Sebaran Skor Riil Data:** Minimum = **26,4** (Kafe di Gunungkidul), Maksimum = **86,8** (Laundry di Sleman), Rata-rata = **68,2**, Deviasi Standar = **13,5**.
  - **Uji Ketahanan Ranking (*Rank Stability*):** Simulasi perturbasi bobot kriteria $\pm 10\%$ membuktikan urutan 5 besar wilayah terbaik tetap stabil tanpa terjadinya pembalikan peringkat (*no rank reversal*).
* **8. Kontrak Data Output & Pipeline Eksekusi End-to-End:**
  - Ekstraksi Fitur Multi-Sumber $\rightarrow$ Sanitasi Nilai Ekstrem $\rightarrow$ Min-Max Transformation $\rightarrow$ Matriks Perkalian Bobot $\rightarrow$ Klasifikasi Kategori $\rightarrow$ Ekspor File Artefak CSV `outputs/hasil/hasil_skoring_sektor.csv` (skema: `wilayah, sektor, skor, kategori, rasio_kompetitor, tarif_sewa`).

---

### SLIDE 9: METODOLOGI ANALISIS — PILAR 2: CLUSTERING KARAKTERISTIK WILAYAH

#### TEKS SLIDE:
* **1. Tujuan & Masalah Bisnis yang Diselesaikan:**
  - Mengidentifikasi tipologi alami dan segmentasi homogenitas 5 kabupaten/kota di D.I. Yogyakarta berdasarkan 6 indikator makroekonomi, demografi, dan biaya operasional tanpa asumsi subjektif.
  - Membantu wirausahawan memahami karakter makro wilayah tempat usahanya beroperasi (kawasan jenuh vs kawasan bertumbuh vs kawasan perintis berbiaya terjangkau).
* **2. Spesifikasi Input 6 Dimensi Makroekonomi:**
  - $X_1$: PDRB per kapita atas dasar harga berlaku (Ribu Rp / tahun)
  - $X_2$: Rata-rata pengeluaran per kapita sebulan (Rp / bulan)
  - $X_3$: Kepadatan penduduk riil (Jiwa / km²)
  - $X_4$: Tarif rata-rata sewa komersial ruko per m²/tahun (Rp)
  - $X_5$: Rata-rata rasio kompetitor POI per 1.000 penduduk
  - $X_6$: Rasio total UMKM terdaftar SiBakul per 1.000 penduduk
* **3. Formulasi Matematis & Landasan Algoritma:**
  - **Tahap 1: Standardisasi Fitur Z-Score (Zero Mean, Unit Variance):**
    $$Z_{i,j} = \frac{X_{i,j} - \mu_j}{\sigma_j}$$
    Wajib dilakukan agar variabel berskala nominal jutaan (PDRB) tidak mendominasi metrik jarak Euclidean terhadap variabel rasio desimal.
  - **Tahap 2: Optimasi K-Means Clustering ($K=3$ - Algoritma Lloyd):**
    Meminimalkan fungsi objektif inersia *Within-Cluster Sum of Squares* (WCSS):
    $$J = \sum_{k=1}^{K} \sum_{\mathbf{z}_i \in C_k} \|\mathbf{z}_i - \boldsymbol{\mu}_k\|^2$$
    Proses iterasi konvergen ketika pergeseran posisi centroid antar iterasi $\|\boldsymbol{\mu}_k^{(t+1)} - \boldsymbol{\mu}_k^{(t)}\| < 10^{-4}$ (toleransi konvergensi) atau mencapai batas maksimum 300 iterasi.
  - **Tahap 3: Reduksi Dimensi Principal Component Analysis (PCA 2D):**
    Menghitung matriks kovariansi fitur ternormalisasi $\mathbf{\Sigma} = \frac{1}{N-1}\mathbf{Z}^T\mathbf{Z}$, menyelesaikan persamaan karakteristik nilai eigen $\mathbf{\Sigma}\mathbf{v}_i = \lambda_i\mathbf{v}_i$, lalu memproyeksikan data 6D ke bidang kartesius 2D ortogonal melalui $\mathbf{Z}_{\text{pca}} = \mathbf{Z} \cdot [\mathbf{v}_1, \mathbf{v}_2]$.
* **4. Justifikasi Ilmiah Pemilihan $K=3$ (Elbow & Domain Tata Ruang DIY):**
  - Evaluasi matematis kurva inersia (metode *Elbow*) dan keselarasan dengan morfologi tata ruang perkotaan DIY membuktikan $K=3$ memisahkan struktur wilayah secara alami tanpa fragmentasi berlebih (*over-segmentation*):
    (1) Kota Inti Padat, (2) Wilayah Penyangga Semi-Urban, dan (3) Wilayah Pesisir/Perbukitan Rural.
* **5. Metrik Evaluasi Kuantitatif Proyeksi:**
  - **PCA Explained Variance Ratio:**
    • Principal Component 1 ($PC_1$): **74,94%** *(Sumbu kapasitas ekonomi makro & kepadatan penduduk)*.
    • Principal Component 2 ($PC_2$): **19,16%** *(Sumbu dinamika persaingan pasar & beban tarif sewa)*.
    • **Total Kumulatif Explained Variance: 94,09%**.
  - **Information Loss:** Hanya **5,91%** $\rightarrow$ Membuktikan bahwa reduksi dari 6 dimensi ke bidang 2D mempertahankan 94% keutuhan informasi data multidimensi asli.
* **6. Profil Tipologi Hasil 3 Klaster Wilayah DIY:**
  - **Klaster 0: Urban Padat, Jenuh & Biaya Tinggi (Kota Yogyakarta):**
    • Kepadatan ekstrem (11.517 jiwa/km²), PDRB tertinggi (Rp 126,8 juta), sewa termahal (Rp 850.000/m²). Pasar matang dengan persaingan sangat ketat.
  - **Klaster 1: Semi-Urban Bertumbuh / Sweet Spot Ekspansi (Kabupaten Sleman & Bantul):**
    • Kepadatan 1.900–2.100 jiwa/km², pengeluaran tinggi, pusat kampus & pemukiman baru. Menawarkan rasio terbaik antara potensi omzet dan biaya operasional.
  - **Klaster 2: Rural Potensial & Biaya Rendah (Kabupaten Kulon Progo & Gunungkidul):**
    • Kepadatan $< 800$ jiwa/km², kompetisi longgar, tarif sewa sangat terjangkau (Rp 220.000–275.000/m²). Peluang pasar kebutuhan pokok dan kuliner wisata.
* **7. Arsitektur Model, Serialisasi & Deployment:**
  - Objek transformer scaler, model K-Means, dan reduksi PCA disimpan secara permanen menggunakan serialisasi joblib: `models/saved/kmeans_wilayah.joblib`, `scaler_clustering.joblib`, dan `pca_wilayah.joblib`. Tabel karakteristik diekspor ke `hasil_clustering_wilayah.csv`.
* **8. Pipeline Eksekusi End-to-End:**
  - Konsolidasi Indikator Regional $\rightarrow$ Z-Score Standardization $\rightarrow$ Fitting Model K-Means ($k=3$) $\rightarrow$ Transformasi PCA 2D $\rightarrow$ Pelabelan Klaster Wilayah $\rightarrow$ Serialisasi Model & Ekspor CSV.

---

### SLIDE 10: METODOLOGI ANALISIS — PILAR 3: FORECASTING TREN PERTUMBUHAN SEKTOR

#### TEKS SLIDE:
* **1. Tujuan & Masalah Bisnis yang Diselesaikan:**
  - Menjawab pertanyaan keberlanjutan bisnis jangka menengah: *"Apakah sektor usaha yang dipilih sedang tumbuh (sunrise) atau terancam jenuh/stagnan (sunset) pada 3 tahun ke depan (2024–2026)?"*.
  - Menghindarkan wirausahawan dari investasi modal pada sektor yang permintaannya mengalami kontraksi struktural.
* **2. Spesifikasi Input Data & Sumber Deret Waktu:**
  - Data historis runtun waktu tahunan jumlah unit usaha aktif BPS DIY (2019–2023) per sektor ($n=5$ titik observasi historis per sektor).
  - Indeks minat pencarian pasar digital Google Trends DIY (2019–2023) via API Pytrends (skala 0–100) sebagai kovariat pembanding dinamika minat konsumen lokal.
* **3. Formulasi Matematis Model Tren Linear (Ordinary Least Squares - OLS):**
  - **Persamaan Garis Tren Linear:**
    $$\hat{Y}_t = \beta_0 + \beta_1(t)$$
  - **Estimator Koefisien Parameter (Metode Kuadrat Terkecil):**
    $$\beta_1 = \frac{\sum_{t=1}^n (t - \bar{t})(Y_t - \bar{Y})}{\sum_{t=1}^n (t - \bar{t})^2}, \qquad \beta_0 = \bar{Y} - \beta_1 \bar{t}$$
    dengan $n=5$, titik tengah historis $\bar{t} = 2021$, dan $\bar{Y}$ adalah rata-rata volume unit usaha historis.
  - **Ekstrapolasi Proyeksi Horizon Masa Depan (2024–2026):**
    $$\hat{Y}_{2024} = \beta_0 + \beta_1(2024), \quad \hat{Y}_{2025} = \beta_0 + \beta_1(2025), \quad \hat{Y}_{2026} = \beta_0 + \beta_1(2026)$$
* **4. Formulasi Interval Ketidakpastian (95% Confidence Interval):**
  - Menggunakan distribusi probabilitas Student's $t$ dengan derajat kebebasan $df = n - 2 = 3$:
    $$\text{CI}_{95\%} = \hat{Y}_t \pm t_{3, \, 0.025} \times \text{SE}_{\text{regresi}} \sqrt{1 + \frac{1}{n} + \frac{(t - \bar{t})^2}{\sum_{i=1}^n (t_i - \bar{t})^2}}$$
    di mana $t_{3, \, 0.025} \approx 3,182$ dan Standard Error of Regression: $\text{SE}_{\text{regresi}} = \sqrt{\frac{\sum (Y_i - \hat{Y}_i)^2}{n-2}}$.
  - Pita ketidakpastian secara realistis melebar membentuk kurva hiperbolik seiring pertambahan horizon waktu proyeksi ($t \to 2026$).
* **5. Kaidah Klasifikasi Arah Tren Bisnis (Directional Signal):**
  - Dihitung menggunakan laju pertumbuhan tahunan majemuk proyeksi (*Projected CAGR*):
    $$\text{CAGR}_{\text{proj}} = \left( \frac{\hat{Y}_{2026}}{\hat{Y}_{2023}} \right)^{\frac{1}{3}} - 1$$
  - • *Naik (Ekspansif):* $\text{CAGR} \ge +3,0\%$ per tahun (Kafe, Restoran, Minimarket) $\rightarrow$ Permintaan konsumen terus mengembang.
  - • *Stabil / Bertumbuh Moderat:* $0,0\% \le \text{CAGR} < +3,0\%$ per tahun (Laundry) $\rightarrow$ Permintaan defensif dan elastisitas stabil.
  - • *Cenderung Melambat / Stagnan:* $\text{CAGR} < 0,0\%$ per tahun (Toko Kelontong Murni) $\rightarrow$ Tekanan kompetisi dari ritel modern.
* **6. Metrik Evaluasi Kuantitatif Lengkap:**
  - **Rata-rata Koefisien Determinasi ($R^2$):** **0,864 (86,4%)** $\rightarrow$ Model menangkap 86% variasi tren historis.
  - **Rata-rata Kesalahan Relatif (MAPE):** **2,18%** $\rightarrow$ Kategori *Highly Accurate* ($\text{MAPE} < 10\%$).
  - **Rincian Metrik per Sektor Usaha:**
    • *Convenience Store / Minimarket:* $R^2 = 0,966$ | $\text{MAPE} = 0,78\%$ | $\text{RMSE} = 34,2$
    • *Toko Kelontong:* $R^2 = 0,999$ | $\text{MAPE} = 0,02\%$ | $\text{RMSE} = 0,4$
    • *Kafe:* $R^2 = 0,855$ | $\text{MAPE} = 4,25\%$ | $\text{RMSE} = 58,1$
    • *Restoran:* $R^2 = 0,776$ | $\text{MAPE} = 2,51\%$ | $\text{RMSE} = 142,6$
    • *Laundry:* $R^2 = 0,726$ | $\text{MAPE} = 3,35\%$ | $\text{RMSE} = 12,8$
* **7. Status Kritis & Limitasi Model (Preliminary Baseline):**
  - Model peramalan deret waktu saat ini berstatus **eksplorasi baseline awal** dan belum bersifat final.
  - Keterbatasan data historis tahunan dari publikasi resmi BPS ($n=5$ titik tahun) menyebabkan model regresi tren linear rentan terhadap *overfitting* atau simplifikasi yang belum menangkap fluktuasi riil ekonomi pasca-pandemi secara non-linear.
  - **Rencana Peningkatan Pasca-UTS:** Eksplorasi algoritma lanjutan (ARIMA/SARIMA, Prophet Facebook) serta penambahan prediktor makroekonomi/digital eksternal (inflasi, mobilitas wisata) guna meningkatkan keandalan proyeksi.
* **8. Pipeline Eksekusi End-to-End:**
  - Parsing Data Deret Waktu BPS $\rightarrow$ Transformasi Struktur Waktu $\rightarrow$ Estimasi Parameter OLS $\rightarrow$ Ekstrapolasi Proyeksi 2024–2026 $\rightarrow$ Perhitungan Margin CI 95% $\rightarrow$ Pelabelan Sinyal Arah Tren $\rightarrow$ Ekspor File `hasil_forecasting_sektor.csv`.

---

### SLIDE 11: METODOLOGI ANALISIS — PILAR 4: MESIN REKOMENDASI PERSONAL

#### TEKS SLIDE:
* **1. Tujuan & Masalah Bisnis yang Diselesaikan:**
  - Menyediakan sistem inferensi interaktif yang menerjemahkan hasil komputasi analitik (Pilar 1, 2, 3) menjadi panduan keputusan lokasi yang personal dan operasional secara *real-time*.
  - Menjawab kebutuhan praktis calon pengusaha: *"Berapa skor kelayakan di lokasi yang saya tuju, apakah modal sewa saya cukup untuk mendapatkan ruko yang layak, dan apa rekomendasi alternatif wilayah terbaik jika modal terbatas?"*.
* **2. Spesifikasi Input Pengguna (User Interface Contract):**
  - $U_1$ (*Sektor Usaha*): Pilihan kategori tunggal (*Kafe, Restoran, Minimarket, Laundry, Toko Kelontong*).
  - $U_2$ (*Modal Sewa Tahunan*): Input numerik anggaran sewa dalam Rupiah (opsional, cth: Rp 30.000.000).
  - $U_3$ (*Preferensi Wilayah*): Pilihan wilayah spesifik (5 kabupaten/kota) ATAU opsi fleksibel *"Semua Wilayah"*.
* **3. Formulasi Algoritma 5 Tahap Inferensi & Validasi Biaya:**
  - **Tahap 1: Multi-Criteria Matrix Lookup (Pilar 1):**
    Mengambil data skor kelayakan komposit ($0-100$), kategori status, rasio kompetitor lokal, dan tarif sewa dasar dari tabel `hasil_skoring_sektor.csv`.
  - **Tahap 2: Contextual Cluster Enrichment (Pilar 2):**
    Menggabungkan label tipologi ekonomi makro wilayah (Urban Jenuh, Sweet Spot, Rural Potensial) dan ringkasan kondisi pasar dari `hasil_clustering_wilayah.csv`.
  - **Tahap 3: Market Growth Sizing (Pilar 3):**
    Menyematkan status proyeksi arah tren sektor (Ekspansif, Stabil, Melambat) dan rentang pertumbuhan dari `hasil_forecasting_sektor.csv`.
  - **Tahap 4: Cost-to-Area Feasibility Check (Validasi Luas Usaha Efektif):**
    Menghitung estimasi luas lantai tempat usaha yang dapat disewa:
    $$\text{Estimasi Luas Kios Tercover (m}^2) = \frac{\text{Budget Sewa Pengguna } (U_2)}{\text{Tarif Sewa Rata-rata Wilayah (Rp/m}^2/\text{tahun)}}$$
    Mengevaluasi rasio kecukupan anggaran (*Budget Feasibility Ratio* - $\text{BFR}$) terhadap standar minimum operasional ruko/kios UMKM ($30\text{ m}^2$):
    $$\text{BFR} = \frac{U_2}{\text{Tarif Sewa} \times 30\text{ m}^2}$$
    • *Status MEMADAI ($\text{BFR} \ge 1,0$ / Luas $\ge 30\text{ m}^2$):* Anggaran mencukupi standar ruko komersial mandiri.
    • *Status MARGINAL ($0,70 \le \text{BFR} < 1,0$ / Luas $21 - 29\text{ m}^2$):* Anggaran terbatas, disarankan konsep kios kompak / booth ritel.
    • *Status KURANG MEMADAI ($\text{BFR} < 0,70$ / Luas $< 21\text{ m}^2$):* Sistem membunyikan *Budget Warning* dan menyarankan negosiasi sewa atau migrasi ke klaster wilayah bertarif lebih rendah.
  - **Tahap 5: Multi-Region Ranking (Skenario Wilayah Terbuka):**
    Jika $U_3 = \text{"Semua Wilayah"}$, sistem mengurutkan seluruh 5 kandidat kabupaten/kota secara menurun (*descending*) berdasarkan Skor Kelayakan dan BFR:
    $$\text{Rank} = \text{ArgSort}(\text{Skor Kelayakan DESC}, \text{BFR DESC})$$
    dan menyajikan ringkasan **Top 3 Wilayah Rekomendasi Terpilih**.
* **4. Metrik & Karakteristik Kinerja Sistem Rekomendasi:**
  - **Latensi Eksekusi Runtime:** **$< 25$ milidetik** per transaksi inferensi (respon seketika tanpa komputasi berat saat diakses pengguna).
  - **Throughput & Concurrency:** Mampu melayani ratusan akses simultan secara stabil karena logika bersifat *stateless*.
  - **Konsistensi Inferensi:** Logika validasi terpusat pada modul Python `UMKMRecommender` mencegah perbedaan interpretasi di berbagai platform antarmuka.
* **5. Arsitektur Pemodelan Decoupled Pre-computed Inference:**
  - Memisahkan secara tegas antara proses komputasi analitik berat (*batch offline pipeline*) dengan mesin inferensi ringan (*online query service*).
  - Menghilangkan *runtime training overhead*, menjamin *zero crash* saat diintegrasikan ke antarmuka aplikasi Streamlit maupun Laravel PHP.
* **6. Kontrak Data Output & Pipeline Eksekusi End-to-End:**
  - Validasi Input Pengguna $\rightarrow$ Matrix Lookup Pilar 1 $\rightarrow$ Cluster Merging Pilar 2 $\rightarrow$ Trend Merging Pilar 3 $\rightarrow$ Evaluasi Finansial BFR $\rightarrow$ Multi-Region Ranking $\rightarrow$ Penyusunan Objek Kartu Rekomendasi Terstruktur (Skor, Kategori, Luas Kios, Rekomendasi Mitigasi).

---

### SLIDE 12: HASIL SEMENTARA — PILAR 1: SKORING KELAYAKAN SEKTOR

#### TEKS SLIDE:
* **Catatan Penyisipan Visual:**
  - `[FILE GAMBAR: outputs/grafik_skoring_kelayakan.png]`
* **Temuan & Insight Komparasi Kelayakan Wilayah:**
  - **Kabupaten Sleman & Bantul (Sentra Pertumbuhan Usaha):**
    • Meraih skor tertinggi untuk sektor **Kafe (Skor: 83,2)** dan **Laundry (Skor: 86,8)** karena didukung oleh konsentrasi mahasiswa, populasi usia produktif, dan daya beli pengeluaran tinggi.
  - **Kota Yogyakarta (Pasar Padat & Risiko Tinggi bagi Usaha Baru):**
    • Memiliki daya beli tertinggi (PDRB Rp 126,8 juta), namun skor kafe baru tertekan ke kategori *Cukup Layak* (Skor: 69,1) akibat tingginya beban sewa (Rp 850.000/m²) dan kejenuhan kompetitor aktif (651 titik).
  - **Kulon Progo & Gunungkidul (Peluang Pasar Perintis):**
    • Menjadi wilayah paling prospektif untuk **Minimarket/Ritel Kebutuhan Harian (Skor: 72,1)** dan **Kuliner Wisata (Skor: 70,3)** berkat biaya sewa yang sangat terjangkau (Rp 220.000–275.000/m²) dan persaingan modern yang masih longgar.

---

### SLIDE 13: HASIL SEMENTARA — PILAR 2: KLASTERING KARAKTERISTIK WILAYAH

#### TEKS SLIDE:
* **Catatan Penyisipan Visual:**
  - `[FILE GAMBAR: outputs/peta_clustering_wilayah.png]` (Peta Spasial DIY)
  - `[FILE GAMBAR: outputs/scatter_pca_clustering.png]` (Scatter Plot PCA 2D)
* **Temuan & Karakteristik 3 Klaster Wilayah DIY:**
  - **Klaster 0: Urban Padat, Jenuh & Biaya Tinggi (Kota Yogyakarta)**
    • Kepadatan ekstrem (11.517 jiwa/km²), PDRB per kapita tertinggi (Rp 126,8 juta), sewa termahal (Rp 850.000/m²). Pasar matang dengan persaingan sangat ketat.
  - **Klaster 1: Semi-Urban Bertumbuh / Sweet Spot Ekspansi (Sleman & Bantul)**
    • Kepadatan 1.900–2.100 jiwa/km², pengeluaran tinggi, kawasan penyangga pemukiman & kampus. Menawarkan rasio terbaik antara potensi omzet dan biaya operasional.
  - **Klaster 2: Rural Potensial & Biaya Rendah (Kulon Progo & Gunungkidul)**
    • Kepadatan rendah ($< 800$ jiwa/km²), biaya sewa paling ekonomis (Rp 220.000–275.000/m²), kompetisi modern minim. Sangat potensial untuk model bisnis perintis dan pariwisata.

---

### SLIDE 14: HASIL SEMENTARA — PILAR 3: PROYEKSI TREN PERTUMBUHAN SEKTOR

#### TEKS SLIDE:
* **Catatan Penyisipan Visual:**
  - `[FILE GAMBAR: outputs/grafik_forecasting_sektor.png]`
* **Temuan Dinamika Deret Waktu Sektor (2019–2026):**
  - **Sektor F&B (Kafe & Restoran):** Menunjukkan kurva *V-shaped rebound* yang agresif pasca-pandemi, diproyeksikan **Naik Signifikan (+8,4% per tahun)** didorong oleh gaya hidup mahasiswa dan pariwisata.
  - **Sektor Jasa Laundry:** Menunjukkan pola **Stabil Bertumbuh Moderat (+3,5% per tahun)** dengan volatilitas rendah.
  - **Sektor Minimarket Modern:** Bertumbuh konsisten sejalan dengan ekspansi ritel ke kawasan suburban.
  - **Sektor Toko Kelontong Tradisional:** Cenderung **Stagnan / Melambat**, memperlihatkan tekanan struktural dari gerai modern.
* **Refleksi Akademis & Limitasi Model (Penting):**
  - Hasil proyeksi saat ini berfungsi sebagai **indikator arah tren (*directional signal*)**, bukan angka prediksi absolut di masa depan.
  - Model linear baseline ini diakui masih rentan terhadap *overfitting* karena keterbatasan data deret waktu tahunan yang minim ($n=5$).
  - Perbaikan pemilihan algoritma dan penambahan variabel input eksternal akan menjadi fokus optimasi utama pada tahap pasca-UTS.

---

### SLIDE 15: HASIL SEMENTARA — PILAR 4: UJI VALIDASI SISTEM REKOMENDASI

#### TEKS SLIDE:
* **Hasil Evaluasi Validasi Mesin Rekomendasi:**
  - Modul inferensi berhasil diuji pada seluruh variasi skenario pengguna tanpa terjadi kegagalan logika sistem (*zero execution error*).
  - Sistem mampu menyinkronkan skor kelayakan mikro per sektor dengan konteks klaster ekonomi makro wilayah secara koheren.
  - Pengujian sensitivitas membuktikan bahwa batasan anggaran sewa efektif menyaring lokasi yang berisiko membebani arus kas usaha pengguna.
  - Waktu respons komputasi inferensi tercatat stabil di bawah **25 milidetik**, membuktikan efisiensi tinggi arsitektur sistem berbasis pra-komputasi (*pre-computed analytical tables*).

---

### SLIDE 16: SIMULASI ENGINE REKOMENDASI (STUDI KASUS PERSONAL)

#### TEKS SLIDE:
* **Skenario 1: Evaluasi Target Wilayah Spesifik**
  - **Input Pengguna:** Sektor: *"Kafe / Kedai Kopi"* | Wilayah: *"Kabupaten Sleman"* | Anggaran Sewa: *"Rp 30.000.000 / Tahun"*
  - **Output Sistem:**
    • Status Evaluasi: **LAYAK (Skor: 83,2 / 100)**
    • Profil Wilayah: **Klaster 1 (Semi-Urban Bertumbuh / Sweet Spot)**
    • Proyeksi Sektor: **Tren Naik Signifikan (+8,4% per tahun)**
    • Validasi Anggaran: **MEMADAI** (Estimasi tarif sewa Rp 725.000/m² mencukupi untuk ruko seluas 35–40 m²).
* **Skenario 2: Rekomendasi Wilayah Terbuka (Peringkat Top 3 Alternatif)**
  - **Input Pengguna:** Sektor: *"Jasa Laundry"* | Opsi Lokasi: *"Terbuka ke Semua Wilayah"*
  - **Output Sistem:**
    1. **Peringkat 1 — Kabupaten Sleman:** Skor **86,8 / 100** *(Layak | Densitas Mahasiswa Tinggi | Tren Stabil)*
    2. **Peringkat 2 — Kabupaten Bantul:** Skor **79,4 / 100** *(Layak | Sewa Moderat Rp 450k/m² | Buffer Pemukiman)*
    3. **Peringkat 3 — Kota Yogyakarta:** Skor **71,2 / 100** *(Layak | Pasar Padat | Biaya Sewa Tinggi Rp 850k/m²)*
* **Kotak Logika Algoritma Rekomendasi:**
  ```text
  [Input User] ──► [Matrix Lookup Pilar 1] ──► [Cluster Context Pilar 2] ──► [Growth Factor Pilar 3] ──► [Budget Feasibility Check] ──► [Kartu Rekomendasi]
  ```

---

### SLIDE 17: KESIMPULAN INTEGRASI UTS & ROADMAP TAHAP IMPLEMENTASI WEB

#### TEKS SLIDE:
* **Kesimpulan Capaian Tahap UTS (Integrasi Pertemuan 1–8):**
  1. Berhasil mengintegrasikan 5 dataset multi-domain untuk 5 kabupaten/kota DIY secara otomatis melalui data pipeline terstandarisasi.
  2. Membuktikan secara matematis segmentasi pasar lewat 3 klaster ekonomi K-Means dengan keandalan proyeksi PCA sebesar **94,09%**.
  3. Memvalidasi arah pergerakan pasar melalui peramalan regresi deret waktu dengan akurasi sangat tinggi (Rata-rata MAPE **2,18%**).
  4. Menghasilkan sistem penilaian kelayakan multi-kriteria objektif sebagai pengganti intuisi subjektif wirausaha.
* **Roadmap Tahap Pasca-UTS (Fase 3: Web Application Development):**
  - **Tahap 1 (Penyempurnaan Algoritma Peramalan Pilar 3):** Eksplorasi model deret waktu lanjutan (seperti ARIMA/SARIMA, Prophet, atau penambahan variabel input makro) untuk mengatasi limitasi *overfitting* data historis minim sebelum implementasi penuh.
  - **Tahap 2 (Rapid Prototyping & Visualisasi Interaktif):** Pembangunan aplikasi web dashboard menggunakan **Streamlit** (pada folder `app/`) untuk menguji interaktivitas peta spasial, grafik tren, dan form simulasi rekomendasi langsung.
  - **Tahap 3 (Finalisasi Platform Web Produksi):** Pengembangan platform web skala penuh berstandar industri menggunakan framework **Laravel (PHP)** dengan basis data relasional, desain antarmuka responsif modern, serta API rekomendasi terstruktur untuk digunakan oleh publik dan pelaku UMKM di D.I. Yogyakarta.

---

### SLIDE 18: PENUTUP & SESI TANYA JAWAB

#### TEKS SLIDE:
* **TERIMA KASIH**
* **Sistem Rekomendasi Kelayakan Sektor Usaha UMKM Berbasis Data (D.I. Yogyakarta)**
* *Projek Mata Kuliah Pengantar Data Sains (PDS) — Semester 3*
* **Repositori Projek:** `https://github.com/AfrizalKin/ProjekPDS-Jogja-UMKM-Analytics`
* **SESI TANYA JAWAB (Q&A) DIPERSILAKAN**
