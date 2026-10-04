"""Titik masuk prototipe UMKM Recommender.

Jalankan dari root repo:  streamlit run prototype/app.py
"""

import streamlit as st

from config import MENU, NAMA_APLIKASI
from components import ui

st.set_page_config(page_title=NAMA_APLIKASI, layout="wide", initial_sidebar_state="expanded")

ui.muat_css()

halaman = [
    st.Page(berkas, title=judul, url_path=kunci, default=(kunci == "beranda"))
    for kunci, judul, berkas, _ in MENU
]
nav = st.navigation(halaman, position="hidden")
ui.sidebar(halaman)
nav.run()
