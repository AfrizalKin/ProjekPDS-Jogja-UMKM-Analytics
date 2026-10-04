import streamlit as st

from components import ui
from config import MENU
from core import data
from core.format import angka


def main():
    skor = data.skoring()
    n_titik = len(data.kompetitor())
    n_wilayah = skor["wilayah"].nunique()
    n_sektor = skor["sektor"].nunique()

    ui.kop_halaman(
        "Rekomendasi Sektor dan Lokasi Usaha UMKM di D.I. Yogyakarta",
        "Banyak pelaku usaha pemula memilih lokasi dan jenis usaha berdasarkan intuisi atau "
        "kebiasaan, bukan data. UMKM Recommender membantu calon pemilik usaha menilai potensi "
        f"pasar, sebaran pesaing, dan arah tren di {n_wilayah} kabupaten/kota secara terukur.",
        "beranda",
    )
    ui.kotak_info(
        "Gunakan menu di sebelah kiri untuk menelusuri skor kelayakan, peta dan klaster wilayah, "
        "proyeksi tren sektor, atau langsung memperoleh rekomendasi."
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        ui.kartu_angka("Titik pesaing terpetakan", angka(n_titik), "Lokasi usaha di D.I. Yogyakarta")
    with c2:
        ui.kartu_angka("Cakupan wilayah", f"{angka(n_wilayah)} Kab/Kota", "Kota dan kabupaten di D.I. Yogyakarta")
    with c3:
        ui.kartu_angka("Sektor usaha dianalisis", angka(n_sektor), "Dari restoran hingga toko kelontong")

    ui.judul_bagian("Fitur Analitik Utama")
    deskripsi = {
        "skoring": f"Skor kelayakan {angka(len(skor))} kombinasi wilayah dan sektor, lengkap dengan filter dan perbandingan.",
        "peta_klaster": "Sebaran titik pesaing dan klaster karakter ekonomi tiap wilayah.",
        "forecasting": "Data historis dan proyeksi jumlah usaha per sektor beserta arah trennya.",
        "rekomendasi": "Pilih sektor, wilayah, dan anggaran sewa untuk memperoleh rekomendasi.",
    }
    kartu = [m for m in MENU if m[0] != "beranda"]
    for baris in (kartu[:2], kartu[2:]):
        kolom = st.columns(2)
        for kol, (kunci, judul, berkas, ikon) in zip(kolom, baris):
            with kol:
                with st.container(key=f"kartu_{kunci}"):
                    st.markdown(f"#### {judul}")
                    st.caption(deskripsi[kunci])
                    st.page_link(berkas, label=f"Buka {judul}", icon=":material/arrow_forward:")

    st.write("")
    ui.kotak_peringatan()


with ui.tangkap_data_hilang():
    main()
