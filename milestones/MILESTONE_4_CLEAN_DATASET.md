# 📄 LAPORAN TUGAS MILESTONE 4: CLEAN DATASET & DATA PREPARATION
**Mata Kuliah:** Pengantar Data Sains (Pertemuan 5)  
**Judul Projek:** Pemodelan Kelayakan Sektor Usaha UMKM Menggunakan Pendekatan Machine Learning dan Time Series untuk Rekomendasi Lokasi Berbasis Data di D.I. Yogyakarta  
**Cakupan Wilayah:** 5 Kabupaten/Kota (Kulon Progo, Bantul, Gunung Kidul, Sleman, Kota Yogyakarta)  

---

## 1. Ringkasan Pembersihan Data (Data Cleaning Summary)

Pembersihan data dilakukan terhadap 5 sumber dataset independen untuk mengatasi isu **missing values**, **duplikasi spasial/ID**, dan **inkonsistensi penamaan/format**:

| Sumber / Dataset | Isu Awal yang Ditemukan | Teknik Pembersihan yang Dilakukan | Hasil Bersih |
| :--- | :--- | :--- | :--- |
| **Dataset 1: OpenStreetMap (POI Kompetitor)** | • 773 duplikasi ID node/way akibat *grid sampling* overlapping.<br>• 3 duplikasi spasial (koordinat berimpit radius < 5 meter).<br>• Karakter khusus pada string nama toko. | • Deduplikasi 2 lapis (`drop_duplicates(subset=['id'])` dan pembulatan koordinat).<br>• Standardisasi sektor UMKM: Kafe, Restoran, Minimarket, Laundry, Kelontong.<br>• Filter *bounding box* geografis DIY. | **2.796 baris bersih** tanpa nilai kosong (*zero missing values*). Tersimpan di `data/processed/kompetitor_per_wilayah.csv`. |
| **Dataset 2: BPS Kondisi Ekonomi 2024** | • Format tabel multi-header (baris 1–4 metadata BPS).<br>• Baris agregat provinsi ("D.I. Yogyakarta") mencampur level kabupaten.<br>• Inkonsistensi ejaan ("Kulonprogo" & "Gunungkidul" tanpa spasi). | • Parsing dinamis dengan `skiprows=4` dan *encoding* `utf-8-sig`.<br>• Filter eksklusi baris agregat provinsi.<br>• *Explicit dictionary mapping* untuk standarisasi nama kabupaten berspasi. | **5 baris data murni** tingkat kabupaten/kota. Tersimpan di `data/processed/kondisi_ekonomi_wilayah.csv`. |
| **Dataset 3: Biaya Sewa Operasional** | • Satuan waktu sewa bercampur antara tarif bulanan dan tahunan.<br>• Variasi nama wilayah ("Kab. Sleman", "Kota Jogja"). | • Normalisasi satuan waktu: tarif bulanan dikonversi menjadi `Rp/m²/tahun` ($\text{tarif} \times 12$).<br>• Klasifikasi ordinal biaya operasional (*Tinggi, Menengah, Terjangkau*). | **5 baris data sewa** standar tahunan. Tersimpan di `data/processed/biaya_operasional.csv`. |
| **Dataset 4: Tren Sektor Usaha (BPS & Google Trends)** | • Multi-line header dan catatan kaki (*footnotes*) pada tabel statistik usaha.<br>• Sinyal Google Trends memiliki frekuensi mingguan terpisah. | • Ekstraksi baris data time-series (2019–2023).<br>• Standardisasi nama wilayah & sektor KBLI.<br>• Agregasi rata-rata tahunan skor Google Trends dan penggabungan via *Left Join*. | **125 baris data panel** (5 wilayah x 5 sektor x 5 tahun). Tersimpan di `data/processed/tren_sektor.csv`. |
| **Dataset 5: UMKM Terdaftar (SiBakul Jogja)** | • Variasi kolom wilayah & perbedaan format angka ribuan. | • Standardisasi nama 5 kabupaten/kota.<br>• Konversi tipe data numerik integer.<br>• Integrasi ke kondisi ekonomi untuk menghitung rasio UMKM. | **5 baris data kabupaten/kota** + 2 tabel rujukan provinsi. Tersimpan di `data/processed/umkm_sibakul.csv`. |

---

## 2. Transformasi Data yang Dilakukan (Data Transformations)

Transformasi data dilakukan secara sistematis guna mempersiapkan fitur-fitur pemodelan analitik:

1. **Standardisasi Identitas Wilayah (Uniform Primary Key)**:
   Menerapkan *explicit mapping dictionary* 100% deterministik untuk menjamin kecocokan *inner join*:
   $$\text{Raw Name} \in \{\text{'kulonprogo'}, \text{'kab. kulon progo'}\} \xrightarrow{\text{mapping}} \text{"Kulon Progo"}$$
   
2. **Normalisasi Satuan Finansial Biaya Sewa Properti**:
   Menyeragamkan seluruh biaya sewa menjadi biaya sewa tahunan per meter persegi:
   $$\text{Harga Sewa (Rp/m}^2\text{/tahun)} = \begin{cases} \text{harga} \times 12, & \text{jika satuan bulan} \\ \text{harga}, & \text{jika satuan tahun} \end{cases}$$

3. **Kalkulasi Laju Pertumbuhan Usaha Tahunan (YoY Growth Rate)**:
   Menghitung pertambahan unit dan persentase pertumbuhan dinamis tahunan per sektor:
   $$\Delta \text{Unit}_{t} = \text{Unit}_{t} - \text{Unit}_{t-1}$$
   $$\text{Pertumbuhan YoY (\%)} = \left(\frac{\text{Unit}_{t} - \text{Unit}_{t-1}}{\text{Unit}_{t-1}}\right) \times 100\%$$

4. **Kalkulasi Rasio Kejenuhan UMKM terhadap Populasi Penduduk**:
   Mengestimasi jumlah penduduk ($\text{Kepadatan} \times \text{Luas}$) dan menghitung rasio kepadatan unit usaha:
   $$\text{Rasio UMKM per 1.000 Penduduk} = \left(\frac{\text{Jumlah UMKM 2025}}{\text{Kepadatan Penduduk} \times \text{Luas Wilayah}}\right) \times 1.000$$

---

## 3. Ringkasan Langkah-Langkah Pembersihan & Eksekusi Pipeline

Pembersihan dapat direproduksi secara instan (*reproducible pipeline*) melalui perintah:
```bash
python scripts/run_all_pipelines.py
```

### Tahapan Eksekusi Otomatis:
```text
[Langkah 1: OSM Parser] ──► Parse 25 JSON ──► Dedup ID & Radius ──► 2.796 Titik Usaha
[Langkah 2: BPS Parser] ──► Skiprows 4 ──► Exclude Agregat DIY ──► Standarisasi Ejaan
[Langkah 3: Sewa Parser] ──► Normalisasi Rp/m2/tahun ──► Klasifikasi Biaya
[Langkah 4: Tren Parser] ──► Reshape Wide-to-Long ──► Hitung YoY Growth & Merge Trends
[Langkah 5: SiBakul Join] ──► Inner Join BPS + SiBakul ──► Hitung Rasio per 1.000 Penduduk
```

### Tabel Perbandingan Sebelum vs Sesudah Pembersihan:
| Dataset | Jumlah Baris Mentah | Jumlah Baris Bersih | Kondisi Missing Values | Status Validasi |
| :--- | :---: | :---: | :---: | :---: |
| **1. Kompetitor (OSM)** | 3.572 elemen | **2.796 baris** | 0% missing | 100% di BBox DIY |
| **2. Ekonomi (BPS)** | 27 baris | **5 baris** | 0% missing | Agregat provinsi tereliminasi |
| **3. Sewa Properti** | 5 baris | **5 baris** | 0% missing | 100% standar tahunan |
| **4. Tren Pertumbuhan** | Beragam (unstructured) | **125 baris** | 0% missing | Time-series 2019–2023 |
| **5. SiBakul UMKM** | 5 baris | **5 baris** | 0% missing | Sinkron dengan BPS 2024 |

---

## 4. Pembaruan Kamus Data Resmi (Updated Data Dictionary)

Berikut adalah struktur kolom baku yang tersimpan di direktori `data/processed/`:

### A. Berkas `kondisi_ekonomi_wilayah.csv` (Dataset 2 & 5)
| Nama Kolom | Tipe Data | Deskripsi | Satuan | Contoh Nilai |
| :--- | :--- | :--- | :--- | :--- |
| `kabupaten_kota` | String | Nama resmi kabupaten/kota di D.I. Yogyakarta | - | `"Sleman"`, `"Bantul"` |
| `pdrb_per_kapita` | Float | PDRB per kapita atas dasar harga berlaku 2024 | Ribu Rupiah | `54501.31` (= Rp 54,5 jt) |
| `kepadatan_penduduk` | Integer | Kepadatan penduduk per kilometer persegi (2024) | Jiwa / km² | `2052` |
| `luas_km2` | Float | Luas wilayah administratif resmi | km² | `575.0` |
| `pengeluaran_per_kapita`| Integer | Rata-rata pengeluaran bulanan per kapita (2024) | Rupiah / bulan | `2181883` |
| `jumlah_umkm_2025` | Integer | Total UMKM terdaftar resmi (SiBakul Jogja) | Unit usaha | `113691` |
| `rasio_umkm_per_1000_penduduk` | Float | Jumlah unit UMKM per 1.000 jiwa penduduk | Rasio | `96.36` |

### B. Berkas `kompetitor_per_wilayah.csv` (Dataset 1)
| Nama Kolom | Tipe Data | Deskripsi | Contoh Nilai |
| :--- | :--- | :--- | :--- |
| `nama_tempat` | String | Nama toko / restoran / kafe | `"MARKO milk & coffee"` |
| `lat` | Float | Titik lintang spasial (Latitude WGS84) | `-7.801250` |
| `lon` | Float | Titik bujur spasial (Longitude WGS84) | `110.344126` |
| `kategori` | String | Kategori UMKM (`restaurant`, `convenience`, `cafe`, `laundry`, `grocery`) | `"cafe"` |
| `wilayah` | String | ID wilayah administratif baku | `"bantul"` |

### C. Berkas `biaya_operasional.csv` (Dataset 3)
| Nama Kolom | Tipe Data | Deskripsi | Satuan |
| :--- | :--- | :--- | :--- |
| `wilayah` | String | ID wilayah baku | `"sleman"` |
| `wilayah_label` | String | Nama formal kabupaten/kota | `"Kabupaten Sleman"` |
| `harga_sewa_per_m2_tahun`| Float | Standarisasi harga sewa ruko/kios komersial | Rp / m² / tahun |
| `kategori_biaya` | String | Kategori tingkat biaya (`Tinggi`, `Menengah`, `Terjangkau`) | `"Tinggi"` |
| `sumber` | String | Publikasi acuan data | `"Bank Indonesia & Property Index"` |
| `tahun` | Integer | Tahun rujukan data | `2024` |

### D. Berkas `tren_sektor.csv` (Dataset 4)
| Nama Kolom | Tipe Data | Deskripsi | Satuan / Skala |
| :--- | :--- | :--- | :--- |
| `wilayah` | String | ID wilayah administratif | `"bantul"` |
| `sektor_usaha` | String | Sektor UMKM target | `"cafe"`, `"restaurant"` |
| `tahun` | Integer | Tahun pencatatan data (2019 s/d 2023) | Tahun |
| `jumlah_usaha` | Float | Jumlah unit usaha aktif tercatat di BPS | Unit usaha |
| `pertumbuhan_tahunan_unit` | Float | Pertambahan unit usaha dibandingkan tahun lalu | Unit |
| `pertumbuhan_tahunan_pct` | Float | Persentase laju pertumbuhan tahunan (YoY) | Persen (%) |
| `google_trends_score` | Float | Rata-rata indeks minat pencarian pasar tahunan | Skala 0 - 100 |
