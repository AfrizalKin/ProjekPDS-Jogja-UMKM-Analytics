import streamlit as st

from components import charts, ui
from config import AMBANG_CUKUP, AMBANG_LAYAK, KATEGORI_STYLE
from core import data
from core.format import angka, skor as f_skor


def _gaya_kategori(v):
    s = KATEGORI_STYLE.get(v)
    return f"color:{s['warna']};font-weight:600" if s else ""


def _reset_filter():
    # Callback berjalan sebelum widget dibuat ulang, jadi state boleh diubah di sini
    st.session_state["skor_w"] = []
    st.session_state["skor_s"] = []


def main():
    df = data.skoring()

    ui.kop_halaman(
        "Skoring Kelayakan",
        "Perbandingan skor kelayakan usaha untuk setiap kombinasi wilayah dan sektor, "
        "berdasarkan kriteria daya beli, kepadatan, pesaing, sewa, dan kejenuhan UMKM.",
        "skoring",
    )
    ui.kotak_info(
        f"Kategori: Layak jika skor ≥ {AMBANG_LAYAK}, Cukup Layak ≥ {AMBANG_CUKUP}, "
        f"Kurang Layak < {AMBANG_CUKUP}."
    )

    wilayah_opsi = df.drop_duplicates("wilayah")[["wilayah", "wilayah_label"]]
    sektor_opsi = df.drop_duplicates("sektor")[["sektor", "sektor_label"]]

    f1, f2, f3 = st.columns([2, 2, 1], vertical_alignment="bottom")
    with f1:
        pilih_w = st.multiselect(
            "Wilayah", wilayah_opsi["wilayah_label"].tolist(), placeholder="Semua wilayah", key="skor_w"
        )
    with f2:
        pilih_s = st.multiselect(
            "Sektor", sektor_opsi["sektor_label"].tolist(), placeholder="Semua sektor", key="skor_s"
        )
    with f3:
        st.button("Reset filter", width="stretch", on_click=_reset_filter)

    tampil = df
    if pilih_w:
        tampil = tampil[tampil["wilayah_label"].isin(pilih_w)]
    if pilih_s:
        tampil = tampil[tampil["sektor_label"].isin(pilih_s)]

    if tampil.empty:
        st.warning("Tidak ada kombinasi yang sesuai dengan filter.")
        return

    terbanyak = tampil["kategori"].value_counts()
    c1, c2, c3 = st.columns(3)
    with c1:
        ui.kartu_angka("Kombinasi ditampilkan", f"{angka(len(tampil))} dari {angka(len(df))}")
    with c2:
        ui.kartu_angka("Rata-rata skor", f_skor(tampil["skor"].mean()), "Dari kombinasi yang ditampilkan")
    with c3:
        ui.kartu_angka(
            "Kategori terbanyak", terbanyak.index[0], f"{angka(terbanyak.iloc[0])} kombinasi"
        )

    ui.judul_bagian("Perbandingan Skor")
    st.plotly_chart(charts.batang_skor(tampil), width="stretch")

    ui.judul_bagian("Tabel Skor")
    tabel = tampil.sort_values("skor", ascending=False).rename(
        columns={
            "sektor_label": "Sektor",
            "wilayah_label": "Wilayah",
            "jumlah_kompetitor": "Jumlah Kompetitor",
            "rasio_kompetitor_per_1000": "Rasio Kompetitor /1.000 Jiwa",
            "harga_sewa_per_m2_tahun": "Sewa (Rp/m²/tahun)",
            "skor": "Skor",
            "kategori": "Kategori",
        }
    )[["Sektor", "Wilayah", "Jumlah Kompetitor", "Rasio Kompetitor /1.000 Jiwa",
       "Sewa (Rp/m²/tahun)", "Skor", "Kategori"]]
    styler = (
        tabel.style.map(_gaya_kategori, subset=["Kategori"])
        .format({
            "Jumlah Kompetitor": lambda v: angka(v),
            "Rasio Kompetitor /1.000 Jiwa": lambda v: angka(v, 4),
            "Sewa (Rp/m²/tahun)": lambda v: angka(v),
            "Skor": f_skor,
        })
    )
    st.dataframe(styler, width="stretch", hide_index=True, height=min(740, 38 * (len(tabel) + 1)))
    st.caption("Klik judul kolom untuk mengurutkan.")


with ui.tangkap_data_hilang():
    main()
