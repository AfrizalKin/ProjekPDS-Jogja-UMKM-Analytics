"""Pemuat mesin rekomendasi (Pilar 4) dari models/04_rekomendasi.py."""

import importlib

import streamlit as st

from config import BERKAS
from core.data import DataHilangError


@st.cache_resource(show_spinner=False)
def _buat(mtimes: tuple):
    # Nama berkas diawali angka, jadi dimuat lewat importlib (seperti run_all_models.py)
    modul = importlib.import_module("models.04_rekomendasi")
    return modul.UMKMRecommender()


def mesin():
    mtimes = []
    for kunci in ("skoring", "cluster", "forecast"):
        p = BERKAS[kunci]
        if not p.exists():
            raise DataHilangError(str(p))
        mtimes.append(p.stat().st_mtime)
    return _buat(tuple(mtimes))
