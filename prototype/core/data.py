"""Pemuat data hanya-baca dengan cache. Pembaruan hasil cukup mengganti berkas CSV."""

import json

import pandas as pd
import streamlit as st

from config import BERKAS


class DataHilangError(Exception):
    """Berkas data yang dibutuhkan tidak ditemukan."""


def _cek(path):
    if not path.exists():
        raise DataHilangError(str(path))
    return path


@st.cache_data(show_spinner=False)
def _csv(path_str: str, mtime: float) -> pd.DataFrame:
    # mtime ikut menjadi kunci cache agar CSV yang diganti terbaca ulang
    return pd.read_csv(path_str)


@st.cache_data(show_spinner=False)
def _json(path_str: str, mtime: float) -> dict:
    with open(path_str, encoding="utf-8") as f:
        return json.load(f)


def _muat_csv(kunci: str) -> pd.DataFrame:
    p = _cek(BERKAS[kunci])
    return _csv(str(p), p.stat().st_mtime).copy()


def skoring() -> pd.DataFrame:
    return _muat_csv("skoring")


def cluster() -> pd.DataFrame:
    return _muat_csv("cluster")


def forecast() -> pd.DataFrame:
    return _muat_csv("forecast")


def kompetitor() -> pd.DataFrame:
    return _muat_csv("kompetitor")


def ekonomi() -> pd.DataFrame:
    return _muat_csv("ekonomi")


def sewa() -> pd.DataFrame:
    return _muat_csv("sewa")


def umkm() -> pd.DataFrame:
    return _muat_csv("umkm")


def metadata() -> dict:
    p = _cek(BERKAS["metadata"])
    return _json(str(p), p.stat().st_mtime)


def keterangan_periode(halaman: str) -> str:
    """Susun satu baris 'Data ... per ...' dari berkas metadata."""
    meta = metadata()
    bagian = []
    for kunci in meta["halaman"][halaman]:
        s = meta[kunci]
        teks = f"{s['ringkas']} {s.get('awalan', '')} {s['periode']}".replace("  ", " ")
        if s.get("keterangan"):
            teks += f" ({s['keterangan']})"
        bagian.append(teks)
    return "Data " + "; ".join(bagian)
