"""
Utilitas/Helper_Riwayat.py

Kumpulan fungsi bantu (helper) untuk fitur Riwayat Penggantian Oli.
Hanya berisi alat umum: baca CSV, konversi angka/tanggal, dan format teks.
Tidak berisi logika fitur maupun tampilan menu.
"""

import csv
import os
from datetime import datetime

FORMAT_TANGGAL = ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y")


def baca_csv(path):
    """Baca file CSV menjadi list of dict. Kembalikan [] bila file belum ada."""
    if not os.path.exists(path):
        return []
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ke_int(nilai, default=None):
    """Ubah nilai ke integer. Kembalikan default bila gagal."""
    try:
        return int(float(str(nilai).strip()))
    except (ValueError, TypeError):
        return default


def ke_tanggal(teks):
    """Ubah teks tanggal ke datetime. Kembalikan None bila format tidak dikenal."""
    teks = (teks or "").strip()
    for fmt in FORMAT_TANGGAL:
        try:
            return datetime.strptime(teks, fmt)
        except ValueError:
            continue
    return None


def format_tanggal(teks):
    """Tanggal ditampilkan sebagai DD-MM-YYYY."""
    tgl = ke_tanggal(teks)
    return tgl.strftime("%d-%m-%Y") if tgl else (teks or "-")


def format_rupiah(nilai):
    angka = ke_int(nilai)
    if angka is None:
        return "-"
    return "Rp{:,}".format(angka).replace(",", ".")


def format_km(nilai):
    angka = ke_int(nilai)
    if angka is None:
        return "-"
    return "{:,} km".format(angka).replace(",", ".")