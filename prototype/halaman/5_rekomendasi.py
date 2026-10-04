from html import escape

import pandas as pd
import streamlit as st

from components import ui
from config import KATEGORI_STYLE
from core import data
from core.format import angka, lokal, rupiah, skor as f_skor
from core.recommender import mesin

SEMUA = "Semua wilayah"
STATUS_KURANG = "Kurang"
STATUS_MENCUKUPI = "Mencukupi"


def _lencana_anggaran(status: str) -> str:
    kunci = "Tidak terjangkau" if status == STATUS_KURANG else status
    st_ = KATEGORI_STYLE.get(kunci)
    if not st_:
        return f'<span class="lencana lencana-netral">{escape(status)}</span>'
    return (
        f'<span class="lencana" style="color:{st_["warna"]};background:{st_["bg"]};'
        f'border-color:{st_["border"]}">{st_["ikon"]} {escape(kunci)}</span>'
    )


def _proyeksi(sektor_id: str) -> str:
    fc = data.forecast()
    fc = fc[(fc["sektor"] == sektor_id) & (fc["status_data"] == "Proyeksi")]
    if fc.empty:
        return ""
    r = fc.sort_values("tahun").iloc[-1]
    return f"Proyeksi {int(r['tahun'])}: {angka(r['jumlah_usaha'])} unit usaha (se-DIY)"


def _hasil_spesifik(rec: dict):
    ui.judul_bagian(f"{rec['sektor_label']} di {rec['wilayah_label']}")
    c1, c2 = st.columns([1, 2])
    with c1:
        ui.kartu_hasil(
            "Skor kelayakan",
            f'{f_skor(rec["skor"])} <span style="font-size:15px;color:#5B6B76">/ 100</span>'
            f'<br>{ui.lencana(rec["kategori"])}',
            tinggi=170,
        )
    with c2:
        ui.kartu_hasil(
            "Klaster wilayah",
            f'<span class="kecil">{escape(rec["cluster_label"])}</span>',
            escape(rec["cluster_deskripsi"]),
            tinggi=170,
        )
    c3, c4, c5 = st.columns(3)
    with c3:
        ui.kartu_hasil(
            "Tren sektor",
            f'<span class="kecil">{escape(rec["arah_tren_sektor"])}</span>',
            escape(_proyeksi(rec["sektor"])),
            tinggi=170,
        )
    with c4:
        ui.kartu_hasil(
            "Estimasi sewa per tahun",
            f'<span class="kecil">{rupiah(rec["estimasi_sewa_tahunan_30m2"])}</span>',
            f'Asumsi luas ruko {angka(rec["luas_asumsi_m2"])} m²',
            tinggi=170,
        )
    with c5:
        ui.kartu_hasil(
            "Status anggaran",
            _lencana_anggaran(rec["budget_status"]),
            escape(lokal(rec["budget_catatan"])) if rec["budget_catatan"] else "Isi anggaran sewa untuk membandingkan.",
            tinggi=170,
        )
    if rec["kejenuhan_warning"]:
        ui.kotak_peringatan(lokal(rec["kejenuhan_warning"]))
    ui.kotak_info(lokal(rec["narasi_rekomendasi"]))


def _hasil_semua(rec: dict, anggaran):
    ui.judul_bagian(f"Peringkat wilayah untuk {rec['sektor_label']}")
    if rec["pesan_tanpa_layak"]:
        ui.kotak_peringatan(lokal(rec["pesan_tanpa_layak"]))

    semua = rec["semua_wilayah"]
    if rec["anggaran_dievaluasi"]:
        ok = [r["wilayah_label"] for r in semua if r["is_affordable"]]
        if ok:
            ui.kotak_info(
                f"Dengan anggaran {rupiah(anggaran)} per tahun, wilayah yang terjangkau: {', '.join(ok)}."
            )
        else:
            ui.kotak_peringatan(
                f"Tidak ada wilayah yang terjangkau dengan anggaran {rupiah(anggaran)} per tahun."
            )

    for kolom, r in zip(st.columns(3), rec["ranking_wilayah"]):
        with kolom:
            ui.kartu_hasil(
                f"Peringkat {r['rank']}",
                f'<span class="kecil">{escape(r["wilayah_label"])}</span>'
                f'{f_skor(r["skor"])} {ui.lencana(r["kategori"])}',
                f'{escape(r["cluster_label"])}<br>Sewa {rupiah(r["estimasi_sewa_tahunan"])}/tahun<br>'
                f'{_lencana_anggaran(r["budget_status"])}',
                tinggi=200,
            )

    ui.judul_bagian("Semua wilayah")
    tabel = pd.DataFrame(
        [
            {
                "Peringkat": r["rank"],
                "Wilayah": r["wilayah_label"],
                "Skor": r["skor"],
                "Kategori": r["kategori"],
                "Klaster": r["cluster_label"],
                "Estimasi Sewa (Rp/tahun)": r["estimasi_sewa_tahunan"],
                "Anggaran": "Tidak terjangkau" if r["budget_status"] == STATUS_KURANG else r["budget_status"],
            }
            for r in semua
        ]
    )

    def warna(v):
        st_ = KATEGORI_STYLE.get(v)
        return f"color:{st_['warna']};font-weight:600" if st_ else ""

    sty = tabel.style.map(warna, subset=["Kategori", "Anggaran"]).format(
        {"Skor": f_skor, "Estimasi Sewa (Rp/tahun)": lambda v: angka(v)}
    )
    st.dataframe(sty, width="stretch", hide_index=True)


def main():
    df = data.skoring()
    ui.kop_halaman(
        "Rekomendasi",
        "Pilih sektor usaha dan wilayah, lalu isi anggaran sewa bila ingin memeriksa kecukupannya. "
        "Hasil langsung diperbarui.",
        "rekomendasi",
    )

    sektor = df.drop_duplicates("sektor").set_index("sektor")["sektor_label"].to_dict()
    wilayah = df.drop_duplicates("wilayah").set_index("wilayah")["wilayah_label"].to_dict()

    with st.container(key="panel_param"):
        a, b, c = st.columns(3)
        with a:
            pilih_s = st.selectbox("Sektor usaha", list(sektor), format_func=sektor.get)
        with b:
            pilih_w = st.selectbox(
                "Wilayah", [None, *wilayah], format_func=lambda x: SEMUA if x is None else wilayah[x]
            )
        with c:
            anggaran = st.number_input(
                "Anggaran sewa tahunan (Rp), opsional",
                value=None, step=1_000_000, format="%d",
                placeholder="Kosongkan bila tidak dievaluasi",
            )

    try:
        rec = mesin().recommend(pilih_s, pilih_w, anggaran)
    except ValueError as e:
        st.error(str(e))
        return

    if rec["mode"] == "spesifik":
        _hasil_spesifik(rec)
    else:
        _hasil_semua(rec, anggaran)

    st.caption(
        f"Estimasi sewa = tarif sewa per m² per tahun × {angka(rec['luas_asumsi_m2'])} m² "
        "(asumsi luas ruko standar untuk semua sektor)."
    )
    ui.kotak_peringatan()


with ui.tangkap_data_hilang():
    main()
