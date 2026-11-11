# Utilitas/Helper_Riwayat.py
# Fungsi-fungsi kecil yang dipakai oleh fitur Riwayat Penggantian Oli.

import csv
import os
from datetime import datetime


def baca_csv(nama_file):
    """Membaca file CSV dan mengembalikan list berisi dictionary (satu per baris)."""
    # Kalau file belum ada, kembalikan list kosong
    if not os.path.exists(nama_file):
        return []

    data = []
    with open(nama_file, newline="", encoding="utf-8") as file:
        pembaca = csv.DictReader(file)
        for baris in pembaca:
            data.append(baris)
    return data


def ke_angka(teks):
    """Mengubah teks menjadi angka bulat. Kalau gagal, hasilnya None."""
    try:
        return int(teks)
    except (ValueError, TypeError):
        return None


def ke_tanggal(teks):
    """Mengubah teks 'TTTT-BB-HH' (contoh: 2026-09-01) menjadi tanggal. Kalau gagal, hasilnya None."""
    try:
        return datetime.strptime(teks, "%Y-%m-%d")
    except (ValueError, TypeError):
        return None


def format_rupiah(angka):
    """Contoh: 65000 -> Rp65.000"""
    if angka is None:
        return "-"
    return "Rp" + format(angka, ",").replace(",", ".")


def format_km(angka):
    """Contoh: 14000 -> 14.000 km"""
    if angka is None:
        return "-"
    return format(angka, ",").replace(",", ".") + " km"