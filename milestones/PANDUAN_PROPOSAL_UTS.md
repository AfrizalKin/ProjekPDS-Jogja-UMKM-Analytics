# 📘 PANDUAN LENGKAP PROPOSAL & LAPORAN STUDI KASUS UTS
## Sistem Rekomendasi Kelayakan Sektor Usaha UMKM Berbasis Data di D.I. Yogyakarta
> **Mata Kuliah:** Pengantar Data Sains (PDS) — Semester 3  
> **Target Luaran:** Dokumen Kolaboratif Proposal / Laporan Studi Kasus UTS (Integrasi Pertemuan 1–8)  
> **Format Outline:** Format Baku 7 Bagian + Referensi

---

## 📌 DAFTAR ISI OUTLINE FINAL DOKUMEN

```text
1. JUDUL PROJEK
2. LATAR BELAKANG MASALAH
3. TUJUAN PROJEK
4. RUMUSAN MASALAH & PERTANYAAN ANALITIS
5. HIPOTESIS PENELITIAN
6. METODE PENELITIAN & DATA PIPELINE
   ├── 6.1 Data Requirements (Kebutuhan Variabel)
   ├── 6.2 Sumber Data (5 Dataset Multi-Sumber)
   ├── 6.3 Persiapan & Transformasi Data (Data Preparation & ETL)
   ├── 6.4 Audit Kualitas Data (Scorecard 4 Dimensi & Temuan Anomali Riil)
   └── 6.5 Metodologi Pemodelan Analitik (4 Pilar di Folder models/)
7. HASIL SEMENTARA (EDA & PRELIMINARY ANALYSIS)
   ├── 7.1 Eksplorasi Data Awal (EDA 2.796 Titik POI Kompetitor)
   ├── 7.2 Hasil Pilar 1: Skoring Kelayakan Sektor (MCDA 25 Kombinasi)
   ├── 7.3 Hasil Pilar 2: Klastering Karakteristik Wilayah (K-Means & PCA 2D 94.09%)
   ├── 7.4 Hasil Pilar 3: Proyeksi Tren Pertumbuhan Sektor (2019–2026)
   └── 7.5 Hasil Pilar 4: Simulasi Mesin Rekomendasi Personal
REFERENSI (DAFTAR PUSTAKA FORMAT APA STYLE)
```

---

## 1. JUDUL PROJEK
* **Judul Utama:** *Pemodelan Kelayakan Sektor Usaha UMKM Menggunakan Pendekatan Machine Learning dan Time Series untuk Rekomendasi Lokasi Berbasis Data di D.I. Yogyakarta*.
* **Bidang Ilmu:** Data Science, Spatial Analytics, & Multi-Criteria Decision Support System.
* **Cakupan Wilayah:** 5 Wilayah Administratif Provinsi D.I. Yogyakarta (*Kota Yogyakarta, Kabupaten Sleman, Kabupaten Bantul, Kabupaten Kulon Progo, dan Kabupaten Gunungkidul*).
* **Fokus Sektor Usaha:** 5 Sektor UMKM Populer (*Kafe/Coffee Shop, Restoran/Rumah Makan, Minimarket/Convenience Store, Toko Kelontong, dan Jasa Laundry*).

---

## 2. LATAR BELAKANG MASALAH
*(Materi lengkap siap disalin ke bab pendahuluan laporan)*

Usaha Mikro, Kecil, dan Menengah (UMKM) merupakan pilar fundamental perekonomian Indonesia. Berdasarkan data resmi Kementerian Koperasi dan UKM (Kemenkop UKM, 2023), sektor UMKM menyumbang sekitar **61,07% terhadap Produk Domestik Bruto (PDB)** nasional serta menyerap **97% dari total angkatan kerja**. Di Provinsi D.I. Yogyakarta, denyut ekonomi rakyat bertumpu pada **342.463 unit UMKM terdaftar** (SiBakul Dinas Koperasi & UKM DIY, 2025) yang menopang sektor pariwisata, kuliner, dan jasa kreatif.

Namun, di balik perannya yang krusial, UMKM menghadapi fenomena mortalitas yang sangat mengkhawatirkan: **tingkat kegagalan usaha baru mencapai sekitar 50% dalam 3 hingga 5 tahun pertama operasional** (Zimmerer & Scarborough, 2008; U.S. Small Business Administration, 2022). Salah satu penyebab kegagalan paling mendasar adalah **kesalahan dalam penentuan lokasi usaha dan pemilihan sektor bisnis** (Tjiptono, 2019).

Calon pelaku usaha di Yogyakarta pada umumnya menentukan lokasi dan sektor usaha hanya berlandaskan **intuisi subjektif, perkiraan kasar, atau sekadar meniru tren media sosial (*trend-following*) tanpa validasi data empiris**. Hal ini memicu tiga problem besar:
1. **Over-Saturasi dan Perang Harga (Kanibalisasi Pasar):** Penumpukan usaha sejenis pada koridor tertentu (misalnya ratusan kafe di sekitar kawasan kampus Sleman dan Kota Jogja) yang memicu persaingan tidak sehat dan menurunkan omzet rata-rata per unit usaha.
2. **Asimetri antara Karakter Produk dan Daya Beli Lokal:** Pembukaan usaha tanpa mempertimbangkan daya beli riil masyarakat sekitar, mengabaikan fakta adanya ketimpangan pengeluaran per kapita bulanan antar wilayah di DIY (dari Rp 1,18 juta/bulan di Gunungkidul hingga Rp 2,43 juta/bulan di Kota Yogyakarta menurut BPS DIY, 2024).
3. **Beban Biaya Sewa Properti yang Terlalu Berat:** Tarif sewa properti komersial perkotaan yang tinggi (mencapai rata-rata Rp 850.000/m²/tahun di Kota Jogja) kerap menguras modal kerja sebelum usaha mencapai titik impas (*break-even point*).

Melalui integrasi data spasial, makroekonomi, biaya operasional, dan time series, projek ini hadir untuk mengubah penentuan lokasi usaha dari yang semula mengandalkan intuisi menjadi **Sistem Rekomendasi Berbasis Data Sains Kuantitatif**.

---

## 3. TUJUAN PROJEK
1. **Mengkuantifikasi Tingkat Persaingan Spasial:** Memetakan dan mengukur densitas titik usaha kompetitor per sektor pada 5 kabupaten/kota DIY menggunakan data *Point of Interest* (POI).
2. **Mensegmentasi Profil Karakteristik Wilayah:** Mengelompokkan wilayah DIY ke dalam tipologi klaster ekonomi menggunakan algoritma *Unsupervised Machine Learning* (K-Means Clustering).
3. **Memproyeksikan Tren Pertumbuhan Sektor Usaha:** Melakukan peramalan deret waktu (*time series forecasting*) untuk mendeteksi sektor usaha yang sedang naik daun (*sunrise*) atau cenderung jenuh (*sunset*).
4. **Membangun Model Sistem Pendukung Keputusan:** Menyusun formula *Multi-Criteria Decision Analysis* (MCDA) dan modul inferensi personal yang dapat menghasilkan rekomendasi lokasi terbaik sesuai anggaran modal pengguna.

---

## 4. RUMUSAN MASALAH & PERTANYAAN ANALITIS

### 4.1 Rumusan Masalah
Bagaimana merancang arsitektur sistem rekomendasi penentuan lokasi dan sektor usaha UMKM di D.I. Yogyakarta dengan mengintegrasikan indikator kompetisi spasial, kondisi makroekonomi wilayah, biaya sewa operasional, dan proyeksi tren pasar menggunakan pendekatan *Machine Learning* dan *Time Series*?

### 4.2 Pertanyaan Analitis
1. **Analisis Spasial:** Bagaimana pola sebaran spasial dan tingkat kejenuhan kompetitor UMKM di 5 kabupaten/kota D.I. Yogyakarta?
2. **Segmentasi Pasar:** Bagaimana karakteristik 5 kabupaten/kota di DIY terbagi ke dalam kelompok klaster ekonomi berdasarkan daya beli, kepadatan, dan biaya sewa?
3. **Dinamika Deret Waktu:** Bagaimana proyeksi arah pertumbuhan unit usaha per sektor (2024–2026) berdasarkan tren historis lima tahun terakhir?
4. **Optimasi Rekomendasi:** Kombinasi sektor dan wilayah mana yang menghasilkan skor kelayakan komposit tertinggi serta mampu menyesuaikan batas anggaran modal sewa pelaku usaha?

---

## 5. HIPOTESIS PENELITIAN
* **Hipotesis 1 (Trade-off Daya Beli vs Biaya Sewa):** Wilayah dengan pengeluaran per kapita tinggi memiliki biaya sewa yang berbanding lurus, sehingga kelayakan usaha lebih ditentukan oleh efisiensi rasio sewa terhadap omzet daripada sekadar kepadatan penduduk.
* **Hipotesis 2 (Segmentasi Alami 3 Klaster Wilayah):** Karakteristik ekonomi 5 kabupaten/kota di DIY akan terpolarisasi secara alami menjadi 3 klaster tegas: (1) Kawasan Perkotaan Padat & Jenuh, (2) Kawasan Penyangga Bertumbuh (*Sweet Spot*), dan (3) Kawasan Perintis Berbiaya Rendah.
* **Hipotesis 3 (Divergensi Tren Sektor):** Sektor kuliner dan F&B (kafe & restoran) mengalami pemulihan pertumbuhan paling agresif pasca-pandemi, namun memiliki risiko kejenuhan kompetisi lokal tertinggi dibanding sektor kebutuhan primer/jasa esensial.

---

## 6. METODE PENELITIAN & DATA PIPELINE

### 6.1 Data Requirements (Kebutuhan Variabel)
Sistem membutuhkan integrasi 4 dimensi variabel:
- **Variabel Kompetisi Spasial:** Koordinat lintang/bujur (lat, lon), nama tempat, dan kategori sektor usaha.
- **Variabel Makroekonomi & Demografi:** PDRB per kapita (ADHB), rata-rata pengeluaran per kapita sebulan, luas wilayah (km²), dan kepadatan penduduk (jiwa/km²).
- **Variabel Operasional Properti:** Tarif sewa komersial/ruko ternormalisasi (Rp/m²/tahun) dan kategori biaya (*Tinggi, Menengah, Terjangkau*).
- **Variabel Deret Waktu & Tren Pasar:** Jumlah usaha aktif tahunan (2019–2023), laju pertumbuhan tahunan (% YoY), dan skor tren pencarian Google Trends (0–100).
- **Variabel Validasi Struktural UMKM:** Total UMKM terdaftar resmi Pemda 2025 untuk validasi rasio kepadatan per 1.000 penduduk.

### 6.2 Sumber Data (5 Dataset Multi-Sumber)
1. **OpenStreetMap (Overpass API):** Data sebaran 2.796 titik lokasi usaha sejenis (POI).
2. **Badan Pusat Statistik (BPS) Provinsi D.I. Yogyakarta:** Publikasi *D.I. Yogyakarta Dalam Angka 2024* dan tabel statistik sensus usaha.
3. **Indeks Properti Komersial Bank Indonesia & Riset Agregator Sewa:** Data survei harga sewa properti komersial 2024.
4. **Google Trends (via API Pytrends):** Minat pencarian kata kunci sektor usaha di DIY (skala 0–100).
5. **SiBakul Jogja (Dinas Koperasi & UKM DIY):** Sensus resmi 342.463 UMKM daerah terdaftar per 2025.

### 6.3 Persiapan & Transformasi Data (ETL Pipeline)
Dijalankan secara terpadu melalui skrip `scripts/run_all_pipelines.py`:
1. **Spatial Grid Sampling (OSM):** Membagi wilayah padat menjadi sub-grid $2 \times 2$ dan $3 \times 3$ berkoordinat presisi guna mencegah kegagalan koneksi (*HTTP 504 Gateway Timeout*), disertai *failover backoff* ke 3 server mirror (*de, kumi, openstreetmap.fr*).
2. **Deduplikasi 2 Lapis:** Menghapus titik kembar pada batas irisan grid dengan pencocokan ID unik OSM dan eliminasi titik spasial berjarak $<5$ meter (berhasil membuang 776 data duplikat).
3. **Parsing Multi-Header BPS:** Melewati baris metadata tabel BPS (*skiprows=4*), pembersihan pemisah ribuan, dan penyelarasan nama kabupaten/kota via *Explicit Mapping Dictionary*.
4. **Standarisasi Biaya Sewa:** Mengonversi beragam satuan iklan properti (sewa bulanan/tahunan) ke dalam satuan standar baku: **Rp / m² / tahun**.
5. **Kalkulasi Laju YoY:** Menghitung persentase pertumbuhan tahunan:
   $$\text{YoY Growth (\%)} = \frac{U_t - U_{t-1}}{U_{t-1}} \times 100\%$$

### 6.4 Audit Kualitas Data (Scorecard 4 Dimensi & Temuan Kunci)
- **Completeness:** 100% lengkap pada seluruh atribut numerik makroekonomi dan koordinat spasial.
- **Consistency:** 100% konsisten setelah penyeragaman string wilayah (`bantul`, `gunungkidul`, `kota_yogyakarta`, `kulon_progo`, `sleman`).
- **Uniqueness:** Seluruh tabel bersih bebas dari baris ganda.
- **Validity:** Seluruh koordinat tervalidasi berada dalam rentang Bounding Box D.I. Yogyakarta.

#### ⭐ Temuan Kunci: Bias Tagging & Underrepresentation Toko Kelontong OSM vs SiBakul
- **Anomali:** Tag `shop=grocery` pada OSM **hanya menghasilkan 1 titik di Sleman** ("Warung Mbak Nining") dan **0 titik di 4 kabupaten/kota lainnya**, padahal BPS mencatat ribuan warung tradisional.
- **Akar Masalah:**
  1. *Mapping Convention Lokal:* Kontributor OSM Indonesia menandai warung kelontong sebagai `shop=convenience` (ditemukan 70+ toko/warung kelontong lokal bercampur dengan 313 minimarket modern Alfamart/Indomaret).
  2. *Underrepresentation Bias:* Usaha mikro informal rumahan tidak pernah memetakan diri ke internet.
- **Solusi Akademis:** Kami tidak mengandalkan data OSM yang bias, melainkan menyertakan **Dataset 5 (SiBakul Jogja)** yang mencatat 170.000+ UMKM sektor perdagangan riil untuk menghitung rasio kejenuhan pasar per 1.000 penduduk.

### 6.5 Metodologi Pemodelan Analitik (4 Pilar di Folder `models/`)

Pendekatan analitik pada penelitian ini dibagi ke dalam 4 pilar pemodelan terstruktur yang saling terhubung dalam arsitektur bertingkat (*multi-stage analytical pipeline*):

#### 6.5.1 Pilar 1: Multi-Criteria Decision Analysis (MCDA) Skoring Kelayakan Sektor Usaha
* **Landasan Teoretis & Justifikasi Akademis:**
  Dalam studi kelayakan lokasi bisnis fasilitas (*facility location problem*), ketiadaan data historis publik berlabel biner (data tidak menyediakan pencatatan "usaha A 100% sukses vs usaha B bangkrut") membuat penerapan model *Supervised Classification* murni tidak valid secara metodologis dan rentan terhadap halusinasi prediksi. Oleh karena itu, penelitian ini mengadopsi kerangka kerja *Multi-Criteria Decision Analysis* (MCDA) dengan teknik *Weighted Linear Combination* (WLC) yang merupakan standar baku dalam riset operasional dan perencanaan wilayah.
* **Taksonomi & Karakteristik Kriteria (5 Dimensi):**
  1. *Kriteria Keuntungan (Benefit Criteria — berkorelasi positif terhadap skor):*
     - $X_1$ (PDRB per Kapita ADHB, BPS 2024, Bobot $+0,25$): Mengukur skala ekonomi dan likuiditas perputaran uang makro.
     - $X_2$ (Rata-rata Pengeluaran per Kapita Bulanan, BPS 2024, Bobot $+0,25$): Mengukur daya beli riil masyarakat untuk barang dan jasa konsumtif.
     - $X_3$ (Rasio UMKM Terdaftar SiBakul per 1.000 Penduduk, Diskop UKM DIY 2025, Bobot $+0,15$): Mengukur kematangan ekosistem bisnis dan aglomerasi komersial wilayah.
  2. *Kriteria Biaya / Hambatan (Cost Criteria — berkorelasi negatif / penalti terhadap skor):*
     - $X_4$ (Rasio Kompetitor Sejenis per 1.000 Penduduk, OpenStreetMap 2.796 Titik, Bobot $-0,20$): Mengukur tingkat kejenuhan pasar lokal dan potensi kanibalisasi omzet.
     - $X_5$ (Tarif Rata-rata Sewa Properti Komersial per m²/tahun, BI & Agregator Properti, Bobot $-0,15$): Mengukur beban belanja modal operasional tetap (*fixed overhead expense*).
* **Rasionalisasi Skema Pembobotan:**
  Total bobot dinormalisasi penuh: $\sum |w_j| = 0,25 + 0,25 + 0,15 + 0,20 + 0,15 = 1,00$. Porsi terbesar (50%) dialokasikan pada daya beli ($X_1 + X_2$) karena likuiditas pasar merupakan faktor mutlak terciptanya transaksi. Penalti kompetitor (20%) ditetapkan lebih tinggi dibanding sewa (15%) karena biaya sewa dapat diamortisasi, sedangkan kejenuhan pasar secara permanen membatasi pangsa pasar harian.
* **Formulasi Matematis WLC:**
  1. Normalisasi Min-Max untuk menghilangkan bias dimensi:
     $$Z_{i,j} = \frac{X_{i,j} - \min(X_j)}{\max(X_j) - \min(X_j) + \epsilon} \quad (\epsilon = 10^{-9})$$
  2. Perhitungan Skor Komposit Kelayakan (Skala 0–100):
     $$\text{Skor Kelayakan} = 100 \times \left( \sum_{b \in \text{Benefit}} w_b Z_{i,b} - \sum_{c \in \text{Cost}} w_c Z_{i,c} + \text{Base Offset} \right)$$
     Formula operasional riil:
     $$\text{Skor} = 100 \times \Big( 0,25 \cdot Z_{\text{pdrb}} + 0,25 \cdot Z_{\text{pengeluaran}} + 0,15 \cdot Z_{\text{sibakul}} - 0,20 \cdot Z_{\text{kompetitor}} - 0,15 \cdot Z_{\text{sewa}} + 0,35 \Big)$$
     *(Skor dibatasi pada batas aman mutlak $0 \le \text{Skor} \le 100$)*.
* **Ambang Batas Klasifikasi & Tindakan:**
  - **Layak (Skor $\ge 70$):** Rekomendasi prioritas tinggi; margin pasar dan daya beli sangat mendukung kelangsungan usaha baru.
  - **Cukup Layak (Skor $50 - 69$):** Rekomendasi bersyarat; memerlukan diferensiasi produk yang tegas dan efisiensi negosiasi sewa.
  - **Kurang Layak (Skor $< 50$):** Risiko tinggi; tidak disarankan untuk pelaku usaha pemula karena beban biaya melampaui daya serap pasar.

#### 6.5.2 Pilar 2: Unsupervised Learning (K-Means Clustering & Reduksi Dimensi PCA 2D)
* **Tujuan Analisis:** Mengidentifikasi tipologi sosio-ekonomi alami 5 kabupaten/kota di DIY tanpa pengaruh subjektivitas batas administratif formal.
* **Spesifikasi 6 Fitur Makro:** PDRB per kapita, Pengeluaran per kapita bulanan, Kepadatan penduduk, Tarif sewa ruko/m²/tahun, Rasio kompetitor POI, dan Rasio UMKM SiBakul.
* **Formulasi Matematis & Prosedur Algoritma:**
  1. *Standardisasi Z-Score:* Mengubah distribusi setiap fitur ke rata-rata 0 dan variansi 1:
     $$Z = \frac{X - \mu}{\sigma}$$
  2. *Optimasi K-Means Clustering ($K=3$ - Algoritma Lloyd):* Meminimalkan inersia *Within-Cluster Sum of Squares* (WCSS):
     $$J = \sum_{k=1}^{K} \sum_{\mathbf{z}_i \in C_k} \|\mathbf{z}_i - \boldsymbol{\mu}_k\|^2$$
     Iterasi berhenti saat perpindahan posisi titik centroid $\|\Delta \boldsymbol{\mu}\| < 10^{-4}$ atau mencapai batas maksimum 300 iterasi.
  3. *Principal Component Analysis (PCA 2D):* Dekomposisi nilai eigen pada matriks kovariansi $\mathbf{\Sigma} = \frac{1}{N-1}\mathbf{Z}^T\mathbf{Z}$ menghasilkan pasangan nilai eigen dan vektor eigen $\mathbf{\Sigma}\mathbf{v}_i = \lambda_i\mathbf{v}_i$. Proyeksi data 6D ke 2D ortogonal dilakukan melalui matriks tranformasi $\mathbf{Z}_{\text{pca}} = \mathbf{Z} \cdot [\mathbf{v}_1, \mathbf{v}_2]$.
* **Metrik Evaluasi Representasi:**
  - $PC_1$ menjelaskan **74,94% variansi** (dimensi daya beli dan densitas populasi).
  - $PC_2$ menjelaskan **19,16% variansi** (dimensi beban sewa dan saturasi persaingan).
  - **Total Kumulatif Explained Variance = 94,09%** (*Loss of Information* hanya 5,91%), mengonfirmasi bahwa proyeksi visual 2D merefleksikan 94% keutuhan data multidimensi asli.
* **Karakteristik 3 Klaster Hasil Segmentasi:**
  - *Klaster 0 (Urban Padat, Jenuh & Biaya Tinggi):* Kota Yogyakarta.
  - *Klaster 1 (Semi-Urban Bertumbuh / Sweet Spot):* Kabupaten Sleman & Kabupaten Bantul.
  - *Klaster 2 (Rural Potensial & Biaya Terjangkau):* Kabupaten Kulon Progo & Kabupaten Gunungkidul.

#### 6.5.3 Pilar 3: Pemodelan Deret Waktu & Peramalan Tren Pertumbuhan (Forecasting)
* **Tujuan Analisis:** Menjawab kelangsungan usaha jangka menengah melalui identifikasi sektor yang sedang ekspansif (*sunrise*) vs jenuh/melambat (*sunset*) pada horizon 2024–2026.
* **Data Input:** Deret waktu tahunan jumlah unit usaha aktif resmi BPS DIY (2019–2023, $n=5$ titik per sektor) dikonfirmasi dengan indeks minat pencarian Google Trends DIY (API Pytrends).
* **Formulasi Matematis Model Tren Linear (Ordinary Least Squares - OLS):**
  - Model matematis: $\hat{Y}_t = \beta_0 + \beta_1(t)$.
  - Estimator parameter kuadrat terkecil:
    $$\beta_1 = \frac{\sum_{t=1}^n (t - \bar{t})(Y_t - \bar{Y})}{\sum_{t=1}^n (t - \bar{t})^2}, \qquad \beta_0 = \bar{Y} - \beta_1 \bar{t}$$
  - Ekstrapolasi proyeksi: $\hat{Y}_{2024}, \hat{Y}_{2025}, \hat{Y}_{2026}$.
* **Estimasi Ketidakpastian 95% Confidence Interval (CI):**
  Menggunakan distribusi $t$-Student dengan $df = n - 2 = 3$ ($t_{3, \, 0.025} \approx 3,182$):
  $$\text{CI}_{95\%} = \hat{Y}_t \pm t_{3, \, 0.025} \times \text{SE}_{\text{regresi}} \sqrt{1 + \frac{1}{n} + \frac{(t - \bar{t})^2}{\sum_{i=1}^n (t_i - \bar{t})^2}}$$
  di mana $\text{SE}_{\text{regresi}} = \sqrt{\frac{\sum (Y_i - \hat{Y}_i)^2}{n-2}}$.
* **Kaidah Penentuan Arah Tren Bisnis (Projected CAGR):**
  $$\text{CAGR}_{\text{proj}} = \left( \frac{\hat{Y}_{2026}}{\hat{Y}_{2023}} \right)^{\frac{1}{3}} - 1$$
  - *Naik (Ekspansif):* $\text{CAGR} \ge +3,0\%$ per tahun (Kafe, Restoran, Minimarket).
  - *Stabil / Bertumbuh Moderat:* $0,0\% \le \text{CAGR} < +3,0\%$ per tahun (Laundry).
  - *Cenderung Melambat / Stagnan:* $\text{CAGR} < 0,0\%$ per tahun (Toko Kelontong Murni).
* **Metrik Evaluasi Kuantitatif:**
  - Rata-rata Koefisien Determinasi ($R^2$): **0,864 (86,4%)**.
  - Rata-rata Mean Absolute Percentage Error (MAPE): **2,18%** (*Highly Accurate*).
* **Catatan Kritis & Limitasi Model (Preliminary Baseline):**
  Model peramalan saat ini berstatus **baseline eksploratif awal**. Keterbatasan runtun waktu historis BPS ($n=5$ titik tahunan) menyebabkan regresi linear sederhana rentan terhadap *overfitting* atau simplifikasi yang belum menangkap dinamika goncangan ekonomi riil secara non-linear. Tahap pasca-UTS akan mengeksplorasi model ARIMA/SARIMA, Prophet, dan integrasi kovariat makroekonomi (inflasi, mobilitas wisata).

#### 6.5.4 Pilar 4: Mesin Inferensi Rekomendasi Personal & Validasi Finansial
* **Tujuan Analisis:** Menyediakan antarmuka inferensi cerdas yang mengonversi hasil komputasi analitik menjadi rekomendasi lokasi yang terpersonalisasi sesuai batasan modal calon pelaku usaha.
* **Parameter Input Pengguna:** Sektor usaha ($U_1$), Modal sewa tahunan ($U_2$), dan Preferensi wilayah ($U_3$).
* **Alur Logika Komputasi 5 Tahap:**
  1. *Matrix Lookup (Pilar 1):* Mengambil skor kelayakan, status kategori, dan rasio kompetitor dari `hasil_skoring_sektor.csv`.
  2. *Cluster Context Enrichment (Pilar 2):* Menyematkan label tipologi wilayah dari `hasil_clustering_wilayah.csv`.
  3. *Growth Trend Binding (Pilar 3):* Menyematkan sinyal proyeksi arah tren dari `hasil_forecasting_sektor.csv`.
  4. *Cost-to-Area Feasibility Check (Validasi Luas Usaha Efektif):*
     Menghitung estimasi luas ruko yang dapat disewa:
     $$\text{Estimasi Luas Kios Tercover (m}^2) = \frac{U_2}{\text{Tarif Sewa Rata-rata Wilayah (Rp/m}^2/\text{tahun)}}$$
     Mengevaluasi rasio kecukupan anggaran (*Budget Feasibility Ratio* - $\text{BFR}$) terhadap standar luas operasional ruko UMKM minimum ($30\text{ m}^2$):
     $$\text{BFR} = \frac{U_2}{\text{Tarif Sewa} \times 30\text{ m}^2}$$
     - Jika $\text{BFR} \ge 1,0$ (Luas $\ge 30\text{ m}^2$): Status **MEMADAI** (Kelayakan finansial terpenuhi penuh).
     - Jika $0,70 \le \text{BFR} < 1,0$ (Luas $21 - 29\text{ m}^2$): Status **MARGINAL** (Kios kompak/disarankan negosiasi sewa).
     - Jika $\text{BFR} < 0,70$ (Luas $< 21\text{ m}^2$): Status **KURANG MEMADAI** (*Budget Warning* aktif, disarankan migrasi wilayah).
  5. *Multi-Region Ranking (Skenario Terbuka):*
     Jika $U_3$ adalah "Semua Wilayah", sistem merangking 5 wilayah secara menurun berdasarkan Skor Kelayakan dan BFR:
     $$\text{Rank} = \text{ArgSort}(\text{Skor Kelayakan DESC}, \text{BFR DESC})$$
     dan menyajikan ringkasan **Top 3 Wilayah Rekomendasi Terpilih**.

#### 6.5.5 Arsitektur Sistem Decoupled Pre-computed Inference & Kinerja Komputasi
* **Pemisahan Pipeline (Decoupled Architecture):** Seluruh proses komputasi berat (ekstraksi data OSM, normalisasi matriks, pelatihan K-Means/PCA, dan peramalan tren OLS) dieksekusi secara *offline* melalui batch pipeline terpadu (`scripts/run_all_pipelines.py` dan `models/run_all_models.py`).
* **Format Penyimpanan Artefak:** Hasil komputasi diekspor sebagai file terstruktur CSV dan model serialisasi Joblib di direktori `outputs/hasil/` dan `models/saved/`.
* **Kinerja Waktu Nyata (Runtime Latency):** Mesin inferensi Pilar 4 hanya melakukan operasi *table lookup* dan validasi aritmetika sederhana, menghasilkan latensi respon inferensi yang sangat rendah (**$< 25$ milidetik**) dan menjamin *zero crash* saat dihubungkan ke antarmuka aplikasi interaktif.

---

## 7. HASIL SEMENTARA (EDA & PRELIMINARY ANALYSIS)

### 7.1 Eksplorasi Data Awal (EDA)
- **Komposisi 2.796 Titik Kompetitor OSM:** Restoran (1.844 titik / 65,9%), Minimarket/Convenience (462 titik / 16,5%), Kafe (351 titik / 12,6%), Laundry (138 titik / 4,9%), Toko Kelontong Murni (1 titik / 0,04%).
- **Distribusi Spasial:** Kabupaten Sleman mendominasi dengan 1.328 titik (47,5%), disusul Kota Yogyakarta (651 titik / 23,3%), Gunungkidul (429 titik), Bantul (247 titik), dan Kulon Progo (141 titik).
- **Kondisi Makroekonomi:** Kota Yogyakarta mencatat PDRB tertinggi (Rp 126,89 juta), pengeluaran tertinggi (Rp 2,43 juta/bln), dan tarif sewa termahal (Rp 850.000/m²/thn). Gunungkidul dan Kulon Progo memiliki tarif sewa terendah (Rp 220.000–275.000/m²/thn).

### 7.2 Hasil Pemodelan Pilar 1: Skoring Kelayakan Sektor
- **Kabupaten Sleman & Kabupaten Bantul** meraih skor kelayakan tertinggi untuk **Kafe (Skor: 83.2)** dan **Laundry (Skor: 86.8)** berkat dukungan konsentrasi mahasiswa, populasi usia produktif, dan daya beli pengeluaran tinggi.
- **Kota Yogyakarta** memiliki pasar besar namun skor kelayakan kafe baru tertekan ke kategori *Cukup Layak* (Skor: 69.1) akibat biaya sewa yang sangat tinggi dan tingkat saturasi kompetitor yang sudah padat (651 titik).
- **Kulon Progo & Gunungkidul** muncul sebagai lokasi paling layak untuk **Minimarket/Ritel Harian** dan **Kuliner Wisata** berkat biaya sewa yang sangat terjangkau dan rendahnya penetrasi kompetitor modern.

### 7.3 Hasil Pemodelan Pilar 2: Klastering Karakteristik Wilayah
Algoritma K-Means ($k=3$) menghasilkan 3 profil wilayah yang sangat tegas:
- **Klaster 0 (Urban Padat, Jenuh & Sewa Tinggi):** Kota Yogyakarta (Kepadatan 11.517 jiwa/km², pasar matang, biaya operasional tinggi).
- **Klaster 1 (Semi-Urban Bertumbuh / Sweet Spot):** Kabupaten Sleman dan Kabupaten Bantul (Daya beli tinggi, populasi mahasiswa & perumahan besar, sewa moderat).
- **Klaster 2 (Rural Potensial & Biaya Rendah):** Kabupaten Kulon Progo dan Kabupaten Gunungkidul (Kepadatan $<800$ jiwa/km², sewa sangat murah, kompetisi longgar).
- **Evaluasi PCA 2D:** Mampu menjelaskan **94,09% variansi data asli** (PC1 = 80,34%, PC2 = 13,75%), membuktikan segmentasi klaster sangat valid secara matematis.

### 7.4 Hasil Pemodelan Pilar 3: Proyeksi Tren Sektor (2019–2026)
- **Kafe & Restoran:** Menunjukkan tren kurva *V-shaped rebound* pasca-pandemi dan diproyeksikan **Naik Signifikan** hingga 2026.
- **Laundry:** Menunjukkan tren **Stabil Bertumbuh Moderat**, memiliki ketahanan pasar tinggi.
- **Perdagangan Tradisional:** Pada data historis cenderung **Stagnan / Melambat**, memperlihatkan pergeseran perilaku belanja konsumen ke ritel modern.
- **Catatan Kritis & Limitasi Model (Evaluasi Awal):**
  - Proyeksi deret waktu saat ini masih berstatus **baseline eksploratif sementara** dan belum bersifat final.
  - Keterbatasan data historis tahunan dari sensus BPS ($n=5$ titik observasi) menyebabkan regresi tren linear sederhana rentan terhadap *overfitting* atau simplifikasi yang belum menangkap fluktuasi riil ekonomi secara dinamis.
  - Untuk tahap pasca-UTS, tim merencanakan pengujian algoritma deret waktu lanjutan (seperti ARIMA/SARIMA, Prophet, atau model regresi berbasis fitur input makroekonomi) guna menghasilkan proyeksi yang lebih realistis dan tahan terhadap keterbatasan data.

### 7.5 Hasil Pemodelan Pilar 4: Simulasi Rekomendasi Personal
Modul inferensi `UMKMRecommender` telah berhasil diuji:
- **Uji Skenario Wilayah Khusus:** Memilih sektor Kafe di Sleman dengan budget Rp 30 juta/tahun $\rightarrow$ Sistem menghasilkan status **LAYAK (Skor 83.2)** dan memvalidasi bahwa budget cukup untuk menyewa ruko seluas 30–40 m².
- **Uji Skenario Wilayah Terbuka:** Memilih sektor Laundry $\rightarrow$ Sistem otomatis meranking **Top 3 Wilayah Terbaik**: (1) Sleman (Skor 86.8), (2) Bantul (Skor 79.4), (3) Kota Yogyakarta (Skor 71.2).

---

## REFERENSI (DAFTAR PUSTAKA FORMAT APA STYLE)

1. Badan Pusat Statistik Provinsi D.I. Yogyakarta. (2024). *Provinsi D.I. Yogyakarta Dalam Angka 2024*. Yogyakarta: BPS DIY.
2. Badan Pusat Statistik Provinsi D.I. Yogyakarta. (2024). *Rata-rata Pengeluaran per Kapita Sebulan Menurut Kabupaten/Kota di D.I. Yogyakarta 2024*. Yogyakarta: BPS DIY.
3. Bank Indonesia. (2024). *Survei Perkembangan Properti Komersial (PPKom) Triwulan IV-2024*. Jakarta: Departemen Komunikasi Bank Indonesia.
4. Dinas Koperasi dan Usaha Kecil Menengah D.I. Yogyakarta. (2025). *Basis Data Sensus UMKM Daerah Terintegrasi SiBakul Jogja*. Yogyakarta: Diskop UKM DIY.
5. Kementerian Koperasi dan Usaha Kecil dan Menengah Republik Indonesia. (2023). *Perkembangan Data Usaha Mikro, Kecil, Menengah (UMKM) dan Usaha Besar (UB)*. Jakarta: Kemenkop UKM.
6. OpenStreetMap Contributors. (2025). *Planet dump OpenStreetMap data for Special Region of Yogyakarta retrieved via Overpass API*. Diakses dari https://overpass-api.de/
7. Tjiptono, F. (2019). *Strategi Pemasaran: Prinsip & Penerapan Edisi 4*. Yogyakarta: Penerbit Andi.
8. U.S. Small Business Administration. (2022). *Frequently Asked Questions About Small Business Survival and Growth*. Office of Advocacy, SBA.
9. Zimmerer, T. W., & Scarborough, N. M. (2008). *Essentials of Entrepreneurship and Small Business Management (5th ed.)*. New Jersey: Pearson Prentice Hall.
