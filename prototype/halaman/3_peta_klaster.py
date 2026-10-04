from html import escape

import streamlit as st

from components import charts, ui
from core import data
from core.format import angka

# Kolom profil wilayah pada hasil_clustering_wilayah.csv: (kolom, label, pemformat)
PROFIL = [
    ("pdrb_per_kapita", "PDRB per kapita", lambda v: f"Rp {angka(v)} ribu"),
    ("pengeluaran_per_kapita", "Pengeluaran per kapita / bulan", lambda v: f"Rp {angka(v)}"),
    ("kepadatan_penduduk", "Kepadatan penduduk", lambda v: f"{angka(v)} jiwa/km²"),
    ("harga_sewa_per_m2_tahun", "Sewa komersial", lambda v: f"Rp {angka(v)}/m²/tahun"),
    ("avg_rasio_kompetitor_per_1000", "Rasio kompetitor (semua sektor)", lambda v: f"{angka(v, 2)} per 1.000 jiwa"),
    ("rasio_umkm_total_per_1000", "Rasio UMKM terdaftar", lambda v: f"{angka(v, 2)} per 1.000 jiwa"),
]


def _tab_peta(kompetitor, skoring, cluster):
    label_sektor = skoring.drop_duplicates("sektor").set_index("sektor")["sektor_label"].to_dict()
    label_wilayah = cluster.set_index("wilayah")["wilayah_label"].to_dict()

    pilih = st.multiselect(
        "Wilayah", list(label_wilayah.values()), placeholder="Semua wilayah", key="peta_w"
    )
    df = kompetitor
    if pilih:
        ids = [k for k, v in label_wilayah.items() if v in pilih]
        df = df[df["wilayah"].isin(ids)]
    if df.empty:
        st.warning("Tidak ada titik pesaing untuk filter ini.")
        return

    c1, c2 = st.columns(2)
    with c1:
        ui.kartu_angka("Titik pesaing ditampilkan", angka(len(df)), f"dari {angka(len(kompetitor))} titik")
    with c2:
        ui.kartu_angka("Jumlah sektor pada peta", angka(df["kategori"].nunique()), "Warna titik menurut sektor")
    st.plotly_chart(charts.peta_pesaing(df, label_sektor), width="stretch")
    st.caption(
        "Klik nama sektor pada legenda untuk menampilkan atau menyembunyikan titiknya. "
        "Data peta terbuka kurang lengkap untuk usaha informal, sehingga jumlah titik tidak sama dengan jumlah usaha sebenarnya."
    )


def _tab_klaster(cluster):
    warna = charts.warna_klaster(cluster["cluster_label"])
    ui.judul_bagian("Klaster wilayah")
    grup = cluster.groupby("cluster_label", sort=False)
    kolom = st.columns(len(grup))
    for kol, (label, g) in zip(kolom, grup):
        with kol:
            ui.kartu_hasil(
                f"{angka(len(g))} wilayah",
                f'<span class="kecil" style="color:{warna[label]}">{escape(label)}</span>',
                f'{escape(g["cluster_deskripsi"].iloc[0])}<br><b>{escape(", ".join(g["wilayah_label"]))}</b>',
                tinggi=210,
            )

    ui.judul_bagian("Sebaran wilayah (PCA 2 dimensi)")
    st.plotly_chart(charts.sebar_pca(cluster), width="stretch")
    st.caption("Wilayah yang berdekatan memiliki profil ekonomi yang mirip. PCA hanya dipakai untuk visualisasi.")

    ui.judul_bagian("Profil wilayah")
    pilih = st.selectbox(
        "Pilih wilayah", cluster["wilayah"].tolist(),
        format_func=lambda w: cluster.set_index("wilayah").loc[w, "wilayah_label"],
    )
    r = cluster.set_index("wilayah").loc[pilih]
    ui.kotak_info(f"{r['wilayah_label']}: klaster {r['cluster_label']}. {r['cluster_deskripsi']}")
    for baris in (PROFIL[:3], PROFIL[3:]):
        for kol, (kunci, label, fmt) in zip(st.columns(3), baris):
            with kol:
                ui.kartu_angka(label, fmt(r[kunci]))


def main():
    cluster = data.cluster()
    ui.kop_halaman(
        "Peta dan Klaster Wilayah",
        "Sebaran titik pesaing per sektor dan pengelompokan wilayah berdasarkan karakter ekonominya.",
        "peta_klaster",
    )
    tab1, tab2 = st.tabs(["Peta Pesaing", "Klaster Wilayah"])
    with tab1:
        _tab_peta(data.kompetitor(), data.skoring(), cluster)
    with tab2:
        _tab_klaster(cluster)


with ui.tangkap_data_hilang():
    main()
