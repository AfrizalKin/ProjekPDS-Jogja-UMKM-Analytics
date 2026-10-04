"""Grafik Plotly bertema gelap."""

import pandas as pd
import plotly.graph_objects as go

from config import AMBANG_CUKUP, AMBANG_LAYAK, WARNA_SEKTOR

TEKS = "#5B6B76"
GARIS = "#E1E7EB"


def tema(fig: go.Figure, tinggi: int = 420) -> go.Figure:
    fig.update_layout(
        template="plotly_white",
        separators=",.",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color=TEKS, size=13),
        height=tinggi,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(orientation="h", y=-0.2, title_text=""),
    )
    fig.update_xaxes(gridcolor=GARIS, zerolinecolor=GARIS)
    fig.update_yaxes(gridcolor=GARIS, zerolinecolor=GARIS)
    return fig


def batang_skor(df, kelompok: str = "wilayah_label") -> go.Figure:
    """Batang skor per wilayah, berwarna per sektor, dengan garis ambang."""
    fig = go.Figure()
    for sektor_id, g in df.groupby("sektor", sort=False):
        fig.add_bar(
            x=g[kelompok],
            y=g["skor"],
            name=g["sektor_label"].iloc[0],
            marker_color=WARNA_SEKTOR.get(sektor_id),
            hovertemplate="%{x}<br>" + g["sektor_label"].iloc[0] + ": %{y}<extra></extra>",
        )
    for nilai, nama, warna in (
        (AMBANG_LAYAK, "Layak", "#1E8E5A"),
        (AMBANG_CUKUP, "Cukup Layak", "#966B00"),
    ):
        fig.add_hline(y=nilai, line_dash="dash", line_color=warna)
        fig.add_annotation(
            xref="paper", x=1.0, xanchor="left", y=nilai, yanchor="middle", showarrow=False,
            text=f"{nama} ({nilai})", font=dict(color=warna, size=12),
        )
    tema(fig)
    fig.update_layout(barmode="group", yaxis=dict(range=[0, 100], title="Skor kelayakan"), margin=dict(l=10, r=120, t=30, b=10))
    return fig


def warna_klaster(labels) -> dict:
    """Peta cluster_label -> warna; label tak dikenal memakai warna cadangan."""
    from config import WARNA_KLASTER, WARNA_KLASTER_CADANGAN

    hasil, cadangan = {}, iter(WARNA_KLASTER_CADANGAN)
    for lb in sorted(set(labels)):
        hasil[lb] = WARNA_KLASTER.get(lb) or next(cadangan, "#5B6B76")
    return hasil


def peta_pesaing(df, label_sektor: dict) -> go.Figure:
    """Peta titik pesaing berwarna per sektor. df: kompetitor (lat, lon, kategori, nama_tempat)."""
    fig = go.Figure()
    for sektor_id, g in df.groupby("kategori", sort=False):
        nama = label_sektor.get(sektor_id, sektor_id)
        fig.add_trace(
            go.Scattermap(
                lat=g["lat"], lon=g["lon"], mode="markers", name=f"{nama} ({len(g):,})".replace(",", "."),
                marker=dict(size=7, color=WARNA_SEKTOR.get(sektor_id), opacity=0.8),
                text=g["nama_tempat"], hovertemplate="%{text}<br>" + nama + "<extra></extra>",
            )
        )
    fig.update_layout(
        map=dict(
            style="carto-positron",
            center=dict(lat=df["lat"].mean(), lon=df["lon"].mean()),
            zoom=8.6,
        ),
        height=560, margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#1B2A33"),
        legend=dict(bgcolor="rgba(255,255,255,.92)", bordercolor=GARIS, borderwidth=1, x=0.01, y=0.99),
    )
    return fig


def sebar_pca(df) -> go.Figure:
    """Diagram sebar PCA 2D untuk wilayah, berwarna menurut cluster_label."""
    warna = warna_klaster(df["cluster_label"])
    fig = go.Figure()
    for lb, g in df.groupby("cluster_label", sort=False):
        fig.add_trace(
            go.Scatter(
                x=g["pca_x"], y=g["pca_y"], mode="markers+text", name=lb,
                text=g["wilayah_label"], textposition="top center", textfont=dict(color="#1B2A33"),
                marker=dict(size=16, color=warna[lb], line=dict(color="#FFFFFF", width=2)),
                hovertemplate="%{text}<br>PC1 %{x:.2f}, PC2 %{y:.2f}<extra></extra>",
            )
        )
    tema(fig, 440)
    fig.update_xaxes(title="Komponen utama 1", range=[df["pca_x"].min() - 1.2, df["pca_x"].max() + 1.2])
    fig.update_yaxes(title="Komponen utama 2")
    return fig


def garis_forecast(df, nama_sektor: str) -> go.Figure:
    """Historis (garis utuh) dan proyeksi (putus-putus) dengan pita interval 95%."""
    df = df.sort_values("tahun")
    hist = df[df["status_data"] == "Historis"]
    proy = df[df["status_data"] == "Proyeksi"]
    fig = go.Figure()
    if not proy.empty:
        sambung = pd.concat([hist.tail(1), proy])
        fig.add_trace(go.Scatter(
            x=list(sambung["tahun"]) + list(sambung["tahun"])[::-1],
            y=list(sambung["upper_ci"]) + list(sambung["lower_ci"])[::-1],
            fill="toself", fillcolor="rgba(14,124,134,0.14)", line=dict(width=0), mode="lines",
            name="Interval 95%", hoverinfo="skip",
        ))
        fig.add_trace(go.Scatter(
            x=sambung["tahun"], y=sambung["jumlah_usaha"], mode="lines+markers",
            name="Proyeksi", line=dict(color="#0E7C86", dash="dash", width=3),
            marker=dict(size=9, symbol="diamond-open", line=dict(width=2)),
        ))
    fig.add_trace(go.Scatter(
        x=hist["tahun"], y=hist["jumlah_usaha"], mode="lines+markers",
        name="Data historis", line=dict(color="#1D4ED8", width=3), marker=dict(size=9),
    ))
    tema(fig, 440)
    fig.update_xaxes(dtick=1, tickformat="d")
    fig.update_yaxes(title=f"Jumlah unit usaha ({nama_sektor})", tickformat=",d")
    return fig
