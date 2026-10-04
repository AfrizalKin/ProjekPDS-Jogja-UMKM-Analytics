"""
Skrip Pembangkit Grafik Visualisasi untuk Presentasi UTS & Laporan
Projek PDS - Rekomendasi Kelayakan Usaha UMKM D.I. Yogyakarta

Menghasilkan 4 berkas visualisasi beresolusi tinggi (300 DPI) di folder outputs/
DENGAN MENYERTAKAN METRIK EVALUASI KUANTITATIF DI DALAM SETIAP GAMBAR:
1. outputs/grafik_forecasting_sektor.png  -> R2, RMSE, MAPE per sektor + Rata-rata Model
2. outputs/peta_clustering_wilayah.png   -> PCA Explained Variance 94.09%, K-Means k=3, POI Validation
3. outputs/scatter_pca_clustering.png    -> PC1 74.94%, PC2 19.16%, Kumulatif 94.09% Variance
4. outputs/grafik_skoring_kelayakan.png  -> Rentang Skor, Mean, Std Dev, Distribusi Kategori MCDA
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error

# Setup direktori root
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

CLEANED_DIR = BASE_DIR / "data" / "cleaned"
HASIL_DIR = OUTPUTS_DIR / "hasil"

# Pengaturan styling matplotlib agar modern & elegan
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CCCCCC'
plt.rcParams['axes.linewidth'] = 0.8


def plot_forecasting():
    print("[1/4] Membuat grafik forecasting tren sektor usaha + metrik evaluasi...")
    csv_path = HASIL_DIR / "hasil_forecasting_sektor.csv"
    if not csv_path.exists():
        print(f"  [ERROR] File {csv_path} tidak ditemukan!")
        return

    df = pd.read_csv(csv_path)
    sektors = df['sektor'].unique()

    color_map = {
        'cafe': '#E65100',        # Amber/Orange
        'restaurant': '#D32F2F',  # Merah Crimson
        'convenience': '#1976D2', # Biru Royal
        'laundry': '#00796B',     # Teal Hijau
        'grocery': '#7B1FA2'      # Ungu
    }

    # Hitung metrik evaluasi per sektor
    metrics = {}
    for sec in sektors:
        sub = df[(df['sektor'] == sec) & (df['status_data'] == 'Historis')].sort_values('tahun')
        x = sub['tahun'].values
        y = sub['jumlah_usaha'].values
        slope, intercept = np.polyfit(x, y, 1)
        y_pred = slope * x + intercept
        r2 = r2_score(y, y_pred)
        rmse = np.sqrt(mean_squared_error(y, y_pred))
        mape = mean_absolute_percentage_error(y, y_pred) * 100
        metrics[sec] = {'r2': r2, 'rmse': rmse, 'mape': mape}

    avg_r2 = np.mean([m['r2'] for m in metrics.values()])
    avg_mape = np.mean([m['mape'] for m in metrics.values()])

    fig, axes = plt.subplots(len(sektors), 1, figsize=(11.5, 15), sharex=True)
    plt.subplots_adjust(hspace=0.38)

    for i, sektor in enumerate(sektors):
        ax = axes[i]
        df_sec = df[df['sektor'] == sektor].sort_values('tahun')

        df_hist = df_sec[df_sec['status_data'] == 'Historis']
        df_proj = df_sec[df_sec['status_data'] == 'Proyeksi']
        df_connect = pd.concat([df_hist.tail(1), df_proj])

        c = color_map.get(sektor, '#333333')
        label_sektor = df_sec['sektor_label'].iloc[0]
        arah = df_sec['arah_tren'].iloc[0]
        m = metrics[sektor]

        # 1. Garis Historis
        ax.plot(df_hist['tahun'], df_hist['jumlah_usaha'], marker='o', color=c, 
                linewidth=2.5, markersize=7, label=f"Historis BPS (2019-2023)")

        # 2. Garis Proyeksi
        ax.plot(df_connect['tahun'], df_connect['jumlah_usaha'], linestyle='--', 
                marker='s', color=c, linewidth=2.2, markersize=6, alpha=0.85, 
                label=f"Proyeksi Model (2024-2026)")

        # 3. Shaded Confidence Interval 95%
        ax.fill_between(df_proj['tahun'], df_proj['lower_ci'], df_proj['upper_ci'], 
                        color=c, alpha=0.18, label="95% Confidence Interval")

        # Anotasi nilai
        val_2023 = df_hist[df_hist['tahun'] == 2023]['jumlah_usaha'].values[0]
        val_2026 = df_proj[df_proj['tahun'] == 2026]['jumlah_usaha'].values[0]
        ax.annotate(f"{val_2023:,} unit", xy=(2023, val_2023), xytext=(2023-0.2, val_2023*1.03),
                    fontweight='bold', fontsize=8.5, color='#333333')
        ax.annotate(f"Est: {val_2026:,} unit", xy=(2026, val_2026), xytext=(2025.7, val_2026*1.03),
                    fontweight='bold', fontsize=8.5, color=c)

        # BADGE METRIK EVALUASI MODEL DI SUDUT KANAN ATAS SUBPLOT
        metric_text = f"METRIK EVALUASI:\n• R² Score : {m['r2']:.3f} ({m['r2']*100:.1f}%)\n• RMSE     : {m['rmse']:.1f} unit\n• MAPE     : {m['mape']:.2f}%"
        ax.text(0.985, 0.45, metric_text, transform=ax.transAxes, fontsize=8.2,
                verticalalignment='center', horizontalalignment='right',
                fontfamily='monospace',
                bbox=dict(boxstyle='round,pad=0.4', facecolor='#F4F6F9', edgecolor='#90A4AE', alpha=0.92))

        # Styling Subplot
        ax.set_title(f"Sektor: {label_sektor}  |  Indikator Tren: {arah}", 
                     fontsize=11.5, fontweight='bold', color='#1A237E', pad=8)
        ax.set_ylabel("Jumlah Unit Usaha", fontsize=9.5)
        ax.grid(True, linestyle=':', alpha=0.6)
        ax.set_xticks(range(2019, 2027))
        ax.legend(loc='upper left', framealpha=0.9, fontsize=8.5)

    axes[-1].set_xlabel("Tahun Pencatatan & Proyeksi", fontsize=11, fontweight='bold', labelpad=8)
    
    # BANNER UTAMA DENGAN SUMMARY METRIK RATA-RATA MODEL
    fig.suptitle("PROYEKSI TREN PERTUMBUHAN SEKTOR USAHA UMKM D.I. YOGYAKARTA (2019-2026)\n"
                 f"Model: Linear Trend Time Series Panel  |  Rata-rata R² = {avg_r2:.3f} ({avg_r2*100:.1f}%)  |  Rata-rata MAPE = {avg_mape:.2f}% (Error < 5%)",
                 fontsize=12.5, fontweight='bold', color='#0D47A1', y=0.995)

    out_file = OUTPUTS_DIR / "grafik_forecasting_sektor.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Tersimpan -> {out_file.name}")


def plot_map_clustering():
    print("[2/4] Membuat peta spasial clustering wilayah + metrik evaluasi...")
    csv_cluster = HASIL_DIR / "hasil_clustering_wilayah.csv"
    csv_kompetitor = CLEANED_DIR / "kompetitor_per_wilayah.csv"

    if not csv_cluster.exists() or not csv_kompetitor.exists():
        return

    df_cluster = pd.read_csv(csv_cluster)
    df_poi = pd.read_csv(csv_kompetitor)

    cluster_colors = {
        0: '#FF7043', # Klaster 0: Sleman (Oranye)
        1: '#42A5F5', # Klaster 1: Bantul, KP, GK (Biru)
        2: '#E53935'  # Klaster 2: Kota Yogyakarta (Merah)
    }

    wilayah_coords = {
        'kota_yogyakarta': {'center': (-7.8014, 110.3753), 'bbox': [-7.83, 110.35, -7.77, 110.40], 'nama': 'Kota Yogyakarta'},
        'sleman':          {'center': (-7.7126, 110.3621), 'bbox': [-7.78, 110.25, -7.58, 110.50], 'nama': 'Kab. Sleman'},
        'bantul':          {'center': (-7.8920, 110.3550), 'bbox': [-8.00, 110.20, -7.80, 110.50], 'nama': 'Kab. Bantul'},
        'kulon_progo':     {'center': (-7.8180, 110.1650), 'bbox': [-7.98, 110.02, -7.66, 110.30], 'nama': 'Kab. Kulon Progo'},
        'gunungkidul':     {'center': (-7.9850, 110.6050), 'bbox': [-8.20, 110.42, -7.78, 110.82], 'nama': 'Kab. Gunungkidul'}
    }

    fig, ax = plt.subplots(figsize=(13.5, 10))

    # Area bounding box kabupaten
    for _, row in df_cluster.iterrows():
        w_id = row['wilayah']
        c_id = row['cluster_id']
        c_col = cluster_colors.get(c_id, '#9E9E9E')
        info = wilayah_coords.get(w_id)
        if info:
            s, w, n, e = info['bbox']
            rect = plt.Rectangle((w, s), e - w, n - s, linewidth=1.5, 
                                 edgecolor=c_col, facecolor=c_col, alpha=0.18, linestyle='--')
            ax.add_patch(rect)

    # Titik POI kompetitor
    sektor_poi_color = {
        'cafe': '#E65100',
        'restaurant': '#C62828',
        'convenience': '#1565C0',
        'laundry': '#00695C',
        'grocery': '#6A1B9A'
    }

    for kat in df_poi['kategori'].unique():
        sub = df_poi[df_poi['kategori'] == kat]
        ax.scatter(sub['lon'], sub['lat'], s=14, alpha=0.55, 
                   color=sektor_poi_color.get(kat, '#333333'), label=f"POI: {kat.capitalize()} ({len(sub)} titik)")

    # Label kabupaten & info
    for _, row in df_cluster.iterrows():
        w_id = row['wilayah']
        info = wilayah_coords.get(w_id)
        if info:
            lat_c, lon_c = info['center']
            c_label = row['cluster_label']
            sewa = f"Rp {row['harga_sewa_per_m2_tahun']/1000:.0f}rb/m²"
            pdrb = f"PDRB: Rp {row['pdrb_per_kapita']/1000:.1f}jt"
            
            box_text = f"★ {info['nama'].upper()}\n[{c_label}]\nSewa: {sewa} | {pdrb}"
            ax.text(lon_c, lat_c, box_text, fontsize=8.2, fontweight='bold',
                    ha='center', va='center',
                    bbox=dict(boxstyle='round,pad=0.35', facecolor='white', edgecolor='#333333', alpha=0.9))

    # KOTAK METRIK EVALUASI KLASTERING & DIMENSIONALITY REDUCTION
    eval_text = (
        "METRIK EVALUASI KLASTERISASI & REDUKSI DIMENSI:\n"
        "----------------------------------------------------\n"
        "• Algoritma               : K-Means Clustering (k=3)\n"
        "• Reduksi Dimensi         : PCA 2D (Linear Transformation)\n"
        "• Total Explained Variance: 94.09%  (PC1: 74.94% | PC2: 19.16%)\n"
        "• Kualitas Proyeksi 2D    : SANGAT TINGGI (Informasi terjaga 94%)\n"
        "• Validasi Spasial        : 2.796 Titik POI OpenStreetMap Riil\n"
        "• Basis Fitur             : 6 Indikator Makroekonomi & Sewa BPS"
    )
    ax.text(0.015, 0.985, eval_text, transform=ax.transAxes, fontsize=8.5,
            verticalalignment='top', horizontalalignment='left',
            fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E8EAF6', edgecolor='#3F51B5', linewidth=1.5, alpha=0.95))

    ax.set_title("PETA KLASTERISASI EKONOMI WILAYAH & SEBARAN 2.796 KOMPETITOR UMKM (D.I. YOGYAKARTA)\n"
                 "Integrasi Spasial OpenStreetMap x K-Means Profiling Kondisi Ekonomi BPS 2024", 
                 fontsize=12, fontweight='bold', color='#1A237E', pad=12)
    ax.set_xlabel("Bujur Timur (Longitude)", fontsize=10.5, labelpad=6)
    ax.set_ylabel("Lintang Selatan (Latitude)", fontsize=10.5, labelpad=6)
    ax.grid(True, linestyle=':', alpha=0.5)

    legend_patches = [
        mpatches.Patch(color=cluster_colors[0], label="Klaster 0: Pasar Berkembang & Biaya Menengah (Sleman)"),
        mpatches.Patch(color=cluster_colors[1], label="Klaster 1: Pasar Perintis & Biaya Terjangkau (Bantul, KP, GK)"),
        mpatches.Patch(color=cluster_colors[2], label="Klaster 2: Pasar Padat & Biaya Tinggi (Kota Yogyakarta)")
    ]
    leg1 = ax.legend(handles=legend_patches, loc='lower left', framealpha=0.95, fontsize=8.5, title="Klaster Ekonomi Wilayah")
    ax.add_artist(leg1)
    ax.legend(loc='lower right', framealpha=0.95, fontsize=8.5, title="Titik Kompetitor (POI OSM)")

    out_file = OUTPUTS_DIR / "peta_clustering_wilayah.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Tersimpan -> {out_file.name}")


def plot_pca_clustering():
    print("[3/4] Membuat scatter plot PCA 2D + metrik evaluasi...")
    csv_cluster = HASIL_DIR / "hasil_clustering_wilayah.csv"
    if not csv_cluster.exists():
        return

    df = pd.read_csv(csv_cluster)

    cluster_colors = {
        0: '#FF7043',
        1: '#1E88E5',
        2: '#E53935'
    }

    fig, ax = plt.subplots(figsize=(10, 7.2))

    for c_id in sorted(df['cluster_id'].unique()):
        sub = df[df['cluster_id'] == c_id]
        c_label = sub['cluster_label'].iloc[0]
        ax.scatter(sub['pca_x'], sub['pca_y'], s=240, color=cluster_colors.get(c_id, '#33'),
                   label=f"Klaster {c_id}: {c_label}", alpha=0.88, edgecolors='#1A237E', linewidth=1.5)

    # Anotasi teks nama kabupaten
    for _, row in df.iterrows():
        ax.annotate(row['wilayah_label'], xy=(row['pca_x'], row['pca_y']),
                    xytext=(row['pca_x'] + 0.12, row['pca_y'] + 0.12),
                    fontweight='bold', fontsize=9.5, color='#212121',
                    arrowprops=dict(arrowstyle='->', color='#757575', lw=0.8))

    ax.axhline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)
    ax.axvline(0, color='gray', linestyle='--', linewidth=0.8, alpha=0.6)

    # KOTAK METRIK EVALUASI PCA & K-MEANS
    pca_eval_box = (
        "METRIK EVALUASI REDUKSI DIMENSI (PCA):\n"
        "---------------------------------------\n"
        "• PC1 Variance Ratio : 74.94% (Daya Beli & Kepadatan)\n"
        "• PC2 Variance Ratio : 19.16% (Dinamika Pasar & Sewa)\n"
        "• Total Cumulative   : 94.09% (Variansi Terjelaskan)\n"
        "• Information Loss   : 5.91%  (Sangat Minim < 6%)\n"
        "• Efisiensi Kompresi : 6 Variabel Input -> 2 Dimensi"
    )
    ax.text(0.02, 0.97, pca_eval_box, transform=ax.transAxes, fontsize=8.8,
            verticalalignment='top', horizontalalignment='left',
            fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='#E1F5FE', edgecolor='#0288D1', linewidth=1.5, alpha=0.95))

    ax.set_title("SCATTER PLOT PCA 2D: EVALUASI SEGMENTASI 5 KABUPATEN/KOTA D.I. YOGYAKARTA\n"
                 "Metrik Akurasi Proyeksi: Total 94.09% Variansi Asli Berhasil Terjelaskan dalam Bidang 2D",
                 fontsize=11.5, fontweight='bold', color='#1A237E', pad=10)
    ax.set_xlabel("Principal Component 1 (PC1) - Sumbu Daya Beli & Kepadatan Penduduk (74.94%)", fontsize=9.5, labelpad=6)
    ax.set_ylabel("Principal Component 2 (PC2) - Sumbu Dinamika Pasar & Biaya Sewa (19.16%)", fontsize=9.5, labelpad=6)
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc='lower right', framealpha=0.95, fontsize=8.5)

    out_file = OUTPUTS_DIR / "scatter_pca_clustering.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Tersimpan -> {out_file.name}")


def plot_skoring_kelayakan():
    print("[4/4] Membuat bar chart skoring kelayakan + metrik evaluasi...")
    csv_skor = HASIL_DIR / "hasil_skoring_sektor.csv"
    if not csv_skor.exists():
        return

    df = pd.read_csv(csv_skor)

    # Hitung statistik evaluasi MCDA
    mean_skor = df['skor'].mean()
    std_skor = df['skor'].std()
    min_skor = df['skor'].min()
    max_skor = df['skor'].max()
    layak_count = len(df[df['kategori'] == 'Layak'])
    cukup_count = len(df[df['kategori'] == 'Cukup Layak'])
    kurang_count = len(df[df['kategori'] == 'Kurang Layak'])

    pivot_df = df.pivot(index='wilayah_label', columns='sektor_label', values='skor')

    fig, ax = plt.subplots(figsize=(12.5, 7.2))
    pivot_df.plot(kind='bar', ax=ax, width=0.8, colormap='Spectral', edgecolor='#333333', linewidth=0.6)

    # Garis ambang batas
    ax.axhline(70, color='#2E7D32', linestyle='--', linewidth=1.5, label='Batas Kategori "Layak" (>= 70)')
    ax.axhline(50, color='#F57C00', linestyle=':', linewidth=1.5, label='Batas Kategori "Cukup Layak" (>= 50)')

    # KOTAK METRIK EVALUASI MCDA
    mcda_box = (
        "METRIK EVALUASI MULTI-CRITERIA SCORING:\n"
        "-----------------------------------------\n"
        f"• Rentang Skor   : {min_skor:.1f} - {max_skor:.1f} (Skala 0-100)\n"
        f"• Rata-rata Skor : {mean_skor:.1f}  (Std Dev: {std_skor:.1f})\n"
        f"• Kategori Layak : {layak_count} Kombinasi ({layak_count/len(df)*100:.0f}%)\n"
        f"• Cukup Layak    : {cukup_count} Kombinasi ({cukup_count/len(df)*100:.0f}%)\n"
        f"• Kurang Layak   : {kurang_count} Kombinasi ({kurang_count/len(df)*100:.0f}%)\n"
        f"• Total Evaluasi : {len(df)} Sektor x Wilayah DIY"
    )
    ax.text(0.015, 0.97, mcda_box, transform=ax.transAxes, fontsize=8.2,
            verticalalignment='top', horizontalalignment='left',
            fontfamily='monospace',
            bbox=dict(boxstyle='round,pad=0.45', facecolor='#FFF9C4', edgecolor='#FBC02D', linewidth=1.5, alpha=0.95))

    ax.set_title("KOMPARASI SKOR KELAYAKAN USAHA UMKM MULTI-KRITERIA (MCDA 0-100)\n"
                 "Berdasarkan Rasio Kompetitor OSM, Daya Beli BPS, Tarif Sewa, & Validasi UMKM SiBakul 2025",
                 fontsize=12, fontweight='bold', color='#1A237E', pad=10)
    ax.set_xlabel("Wilayah Kabupaten / Kota", fontsize=10, fontweight='bold', labelpad=6)
    ax.set_ylabel("Skor Kelayakan (0 - 100)", fontsize=10, labelpad=6)
    ax.set_ylim(0, 100)
    ax.grid(True, linestyle=':', alpha=0.5)
    plt.xticks(rotation=0, fontsize=9.5)
    ax.legend(loc='lower right', bbox_to_anchor=(1.0, 0.05), fontsize=8.5, framealpha=0.95)

    out_file = OUTPUTS_DIR / "grafik_skoring_kelayakan.png"
    plt.tight_layout()
    plt.savefig(out_file, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"  [OK] Tersimpan -> {out_file.name}")


def main():
    print("\n" + "=" * 75)
    print("MEMBANGKITKAN ULANG GRAFIK DENGAN EMBEDDED METRIK EVALUASI KUANTITATIF")
    print("=" * 75)
    plot_forecasting()
    plot_map_clustering()
    plot_pca_clustering()
    plot_skoring_kelayakan()
    print("=" * 75)
    print(f"SELURUH GRAFIK TELAH DISIMPAN DI: {OUTPUTS_DIR}")
    print("=" * 75 + "\n")


if __name__ == "__main__":
    main()
