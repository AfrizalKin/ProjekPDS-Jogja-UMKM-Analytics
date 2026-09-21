"""
Pilar 3: Forecasting Tren Pertumbuhan Sektor Usaha UMKM
Projek PDS - Rekomendasi Kelayakan Usaha UMKM D.I. Yogyakarta

Sifat:
- Batch process (offline, tanpa input user).
- Level analisis: Sektor usaha (Kafe, Restoran, Minimarket, Laundry, Toko Kelontong).
- Memproyeksikan estimasi jumlah usaha untuk 1-3 tahun ke depan (2024 - 2026).
- Menghitung Confidence Interval 95% dan menentukan arah tren (Naik / Stabil / Turun).
- Output disimpan ke: data/processed/hasil_forecasting_sektor.csv
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

# Menambahkan root project ke sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.append(str(BASE_DIR))

TREN_SEKTOR_CSV = BASE_DIR / "data" / "processed" / "tren_sektor.csv"
OUTPUT_FORECAST_CSV = BASE_DIR / "data" / "processed" / "hasil_forecasting_sektor.csv"

SEKTOR_LABELS = {
    "cafe": "Kafe / Kedai Kopi",
    "restaurant": "Restoran / Warung Makan",
    "convenience": "Minimarket / Toko Modern",
    "laundry": "Jasa Pencucian / Laundry",
    "grocery": "Toko Kelontong Tradisional"
}


def run_pilar3_forecasting(forecast_years: list[int] = [2024, 2025, 2026]) -> pd.DataFrame:
    print("=" * 75)
    print("MEMULAI PILAR 3: FORECASTING TREN PERTUMBUHAN SEKTOR USAHA (BATCH PROCESS)")
    print("=" * 75)

    if not TREN_SEKTOR_CSV.exists():
        raise FileNotFoundError(f"Berkas tidak ditemukan: {TREN_SEKTOR_CSV}")

    df_tren = pd.read_csv(TREN_SEKTOR_CSV)

    # Agregasi total jumlah usaha per (sektor, tahun) di tingkat provinsi D.I. Yogyakarta
    agg_df = (
        df_tren.groupby(["sektor_usaha", "tahun"])["jumlah_usaha"]
        .sum()
        .reset_index()
        .sort_values(by=["sektor_usaha", "tahun"])
    )

    all_results = []

    for sektor_id, group in agg_df.groupby("sektor_usaha"):
        sektor_label = SEKTOR_LABELS.get(sektor_id, sektor_id.capitalize())
        group = group.sort_values(by="tahun").reset_index(drop=True)

        years_hist = group["tahun"].values.astype(float)
        units_hist = group["jumlah_usaha"].values.astype(float)
        n = len(years_hist)

        # Regresi Linier Tren: y = slope * x + intercept
        slope, intercept = np.polyfit(years_hist, units_hist, 1)

        # Hitung Standard Error of Estimate (Residual Variance)
        fitted_hist = slope * years_hist + intercept
        residuals = units_hist - fitted_hist
        dof = max(1, n - 2)
        s_err = np.sqrt(np.sum(residuals ** 2) / dof)

        # Nilai t-kritis (pendekatan 95% CI dua sisi, t ~ 2.57 untuk dof=3)
        t_crit = 2.57 if dof <= 3 else 2.0

        # Rata-rata laju pertumbuhan tahunan historis (%)
        growth_rates = np.diff(units_hist) / units_hist[:-1] * 100.0
        avg_growth_pct = np.mean(growth_rates)

        # Klasifikasi arah tren:
        # Naik jika slope > 0 dan rata-rata pertumbuhan > 1%
        # Turun jika slope < 0 dan rata-rata pertumbuhan < -1%
        # Stabil jika perubahan di sekitar 0%
        if avg_growth_pct > 1.0 and slope > 0:
            arah_tren = "Naik (Ekspansif)"
        elif avg_growth_pct < -1.0 and slope < 0:
            arah_tren = "Turun (Kontraksi)"
        else:
            arah_tren = "Stabil"

        # 1. Simpan baris data historis (2019 - 2023)
        for i, yr in enumerate(years_hist):
            val = units_hist[i]
            prev_val = units_hist[i - 1] if i > 0 else val
            pct_change = ((val - prev_val) / prev_val * 100.0) if i > 0 else 0.0

            all_results.append({
                "sektor": sektor_id,
                "sektor_label": sektor_label,
                "tahun": int(yr),
                "jumlah_usaha": int(round(val)),
                "lower_ci": int(round(val)),
                "upper_ci": int(round(val)),
                "arah_tren": arah_tren,
                "laju_pertumbuhan_pct": round(pct_change, 2),
                "status_data": "Historis"
            })

        # 2. Proyeksikan 1-3 tahun ke depan (2024, 2025, 2026)
        x_mean = np.mean(years_hist)
        ss_x = np.sum((years_hist - x_mean) ** 2)
        prev_proj = units_hist[-1]

        for f_yr in forecast_years:
            pred_y = slope * f_yr + intercept
            # Prediction standard error untuk x masa depan
            margin_err = t_crit * s_err * np.sqrt(1 + (1.0 / n) + ((f_yr - x_mean) ** 2) / ss_x)

            pred_y_clipped = max(10.0, pred_y)
            lower_bound = max(0.0, pred_y_clipped - margin_err)
            upper_bound = pred_y_clipped + margin_err

            f_pct_change = ((pred_y_clipped - prev_proj) / prev_proj) * 100.0
            prev_proj = pred_y_clipped

            all_results.append({
                "sektor": sektor_id,
                "sektor_label": sektor_label,
                "tahun": int(f_yr),
                "jumlah_usaha": int(round(pred_y_clipped)),
                "lower_ci": int(round(lower_bound)),
                "upper_ci": int(round(upper_bound)),
                "arah_tren": arah_tren,
                "laju_pertumbuhan_pct": round(f_pct_change, 2),
                "status_data": "Proyeksi"
            })

    df_forecast = pd.DataFrame(all_results)

    # Simpan hasil ke data/processed/hasil_forecasting_sektor.csv
    OUTPUT_FORECAST_CSV.parent.mkdir(parents=True, exist_ok=True)
    df_forecast.to_csv(OUTPUT_FORECAST_CSV, index=False)

    print(f"\n[SUKSES] Hasil Forecasting Tren Sektor berhasil disimpan ke:\n  -> {OUTPUT_FORECAST_CSV}")
    print(f"Total Sektor Teranalisis : {agg_df['sektor_usaha'].nunique()}")
    print(f"Rentang Waktu            : 2019 - 2026 (Historis + Proyeksi)")

    # Tampilkan ikhtisar arah tren
    print("\n--- IKHTISAR ARAH TREN & PROYEKSI PER SEKTOR (SE-DIY) ---")
    summary = (
        df_forecast[df_forecast["tahun"].isin([2023, 2026])]
        .pivot(index=["sektor", "sektor_label", "arah_tren"], columns="tahun", values="jumlah_usaha")
        .reset_index()
    )
    summary.columns = ["sektor", "sektor_label", "arah_tren", "unit_2023_historis", "unit_2026_proyeksi"]
    print(summary.to_string(index=False))
    print("=" * 75 + "\n")

    return df_forecast


if __name__ == "__main__":
    run_pilar3_forecasting()
