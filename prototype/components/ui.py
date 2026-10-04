"""Komponen UI bersama: CSS, sidebar, kop halaman, kartu, lencana, kotak info."""

from contextlib import contextmanager
from html import escape

import streamlit as st

from config import (
    CSS_PATH,
    KATEGORI_STYLE,
    MENU,
    NAMA_APLIKASI,
    PERINGATAN,
    SUBJUDUL_APLIKASI,
)
from core import data


def muat_css():
    try:
        css = CSS_PATH.read_text(encoding="utf-8")
    except OSError:
        return
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def sidebar(halaman):
    with st.sidebar:
        st.markdown(
            f"""<div class="brand"><div class="brand-nama">{escape(NAMA_APLIKASI)}</div>
            <div class="brand-sub">{escape(SUBJUDUL_APLIKASI)}</div></div>
            <div class="nav-label">Navigasi Analisis</div>""",
            unsafe_allow_html=True,
        )
        for pg, (_, judul, _, ikon) in zip(halaman, MENU):
            st.page_link(pg, label=judul, icon=ikon)


@contextmanager
def tangkap_data_hilang():
    """Tampilkan pesan jelas (bukan galat teknis) bila berkas data tidak ada."""
    try:
        yield
    except data.DataHilangError as e:
        st.error(
            f"Berkas data tidak ditemukan: {e}. "
            "Pastikan hasil analisis sudah dibuat (jalankan models/run_all_models.py)."
        )
        st.stop()


def kop_halaman(judul: str, deskripsi: str, halaman: str):
    st.markdown(
        f"""<h1 class="judul-halaman">{escape(judul)}</h1>
        <div class="data-per">{escape(data.keterangan_periode(halaman))}</div>
        <p class="deskripsi">{escape(deskripsi)}</p>""",
        unsafe_allow_html=True,
    )


def kotak_info(teks: str):
    st.markdown(
        f'<div class="kotak kotak-info"><span class="ikon">ⓘ</span>{escape(teks)}</div>',
        unsafe_allow_html=True,
    )


def kotak_peringatan(teks: str = PERINGATAN):
    st.markdown(
        f'<div class="kotak kotak-peringatan"><span class="ikon">⚠</span>{escape(teks)}</div>',
        unsafe_allow_html=True,
    )


def lencana(kategori: str) -> str:
    st_ = KATEGORI_STYLE.get(kategori)
    if not st_:
        return f'<span class="lencana">{escape(str(kategori))}</span>'
    return (
        f'<span class="lencana" style="color:{st_["warna"]};background:{st_["bg"]};'
        f'border-color:{st_["border"]}">{st_["ikon"]} {escape(kategori)}</span>'
    )


def kartu_angka(label: str, nilai: str, keterangan: str = ""):
    st.markdown(
        f"""<div class="kartu-angka"><div class="kartu-label">{escape(label)}</div>
        <div class="kartu-nilai">{escape(nilai)}</div>
        <div class="kartu-ket">{escape(keterangan)}</div></div>""",
        unsafe_allow_html=True,
    )


def kartu_hasil(label: str, isi_html: str, ket_html: str = "", tinggi: int = 150):
    """Kartu hasil dengan isi HTML (isi dan keterangan harus sudah di-escape pemanggil)."""
    st.markdown(
        f"""<div class="kartu-angka" style="height:{tinggi}px"><div class="kartu-label">{escape(label)}</div>
        <div class="kartu-nilai">{isi_html}</div>
        <div class="kartu-ket">{ket_html}</div></div>""",
        unsafe_allow_html=True,
    )


def judul_bagian(teks: str):
    st.markdown(f'<h2 class="judul-bagian">{escape(teks)}</h2>', unsafe_allow_html=True)
