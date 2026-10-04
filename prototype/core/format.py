"""Pemformat angka berformat Indonesia (titik ribuan, koma desimal)."""


def angka(x, desimal: int = 0) -> str:
    s = f"{x:,.{desimal}f}"
    return s.replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def skor(x) -> str:
    """Skor tanpa nol di belakang: 56,7 / 54,66 / 81,5."""
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return s.replace(".", ",")


def rupiah(x) -> str:
    return "Rp " + angka(x, 0)


def lokal(teks: str) -> str:
    """Ubah angka berformat Inggris dalam teks (1,234.5) ke format Indonesia (1.234,5)."""
    import re

    return re.sub(
        r"\d[\d.,]*\d|\d",
        lambda m: m.group(0).translate(str.maketrans(",.", ".,")),
        teks,
    )
