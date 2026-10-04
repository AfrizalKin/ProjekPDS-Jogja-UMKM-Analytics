from html import escape

import pandas as pd
import streamlit as st

from components import charts, ui
from core import data
from core.format import angka

HIST, PROY = "Historis", "Proyeksi"


def _ringkasan(fc: pd.DataFrame) -> dict:
    hist = fc[fc["status_data"] == HIST].sort_values("tahun")
    proy = fc[fc["status_data"] == PROY].sort_values("tahun")
    return {
        "arah": fc["arah_tren"].iloc[0],
        "hist": hist.iloc[-1] if not hist.empty else None,
        "proy": proy.iloc[-1] if not proy.empty else None,
    }


def main():
    df = data.forecast()
    ui.kop_halaman(
        "Forecasting Tren",
        "Data historis jumlah unit usaha per sektor di D.I. Yogyakarta dan proyeksi tahun-tahun berikutnya.",
        "forecasting",
    )
    ui.kotak_info(
        "Proyeksi adalah sinyal arah, bukan angka pasti: dihitung dengan regresi tren linear dari "
        "lima titik data tahunan, dan interval 95% bersifat indikatif."
    )

    sektor = df.drop_duplicates("sektor").set_index("sektor")["sektor_label"].to_dict()
    pilih = st.selectbox("Sektor usaha", list(sektor), format_func=sektor.get)
    fc = df[df["sektor"] == pilih]
    r = _ringkasan(fc)

    c1, c2, c3 = st.columns(3)
    with c1:
        ui.kartu_hasil("Arah tren", f'<span class="kecil">{escape(r["arah"])}</span>', "Berdasarkan hasil pemodelan tren", 125)
    with c2:
        if r["hist"] is not None:
            ui.kartu_angka(
                f"Data historis terakhir ({int(r['hist']['tahun'])})",
                angka(r["hist"]["jumlah_usaha"]), "unit usaha se-DIY",
            )
    with c3:
        if r["proy"] is not None:
            p = r["proy"]
            ui.kartu_angka(
                f"Proyeksi {int(p['tahun'])}", angka(p["jumlah_usaha"]),
                f"Rentang 95%: {angka(p['lower_ci'])} – {angka(p['upper_ci'])}",
            )

    ui.judul_bagian(f"Historis dan proyeksi: {sektor[pilih]}")
    st.plotly_chart(charts.garis_forecast(fc, sektor[pilih]), width="stretch")
    st.caption("Garis biru utuh: data historis. Garis hijau putus-putus: proyeksi. Area berwarna: interval 95%.")

    ui.judul_bagian("Ringkasan semua sektor")
    baris = []
    for sid, nama in sektor.items():
        rr = _ringkasan(df[df["sektor"] == sid])
        baris.append({
            "Sektor": nama,
            "Arah Tren": rr["arah"],
            f"Historis {int(rr['hist']['tahun'])}": rr["hist"]["jumlah_usaha"],
            f"Proyeksi {int(rr['proy']['tahun'])}": rr["proy"]["jumlah_usaha"],
            "Batas Bawah 95%": rr["proy"]["lower_ci"],
            "Batas Atas 95%": rr["proy"]["upper_ci"],
        })
    tabel = pd.DataFrame(baris)
    angka_kol = [k for k in tabel.columns if k not in ("Sektor", "Arah Tren")]
    st.dataframe(
        tabel.style.format({k: (lambda v: angka(v)) for k in angka_kol}),
        width="stretch", hide_index=True,
    )


with ui.tangkap_data_hilang():
    main()
