# services/reminder_service.py
# FUNGSI : Fitur Pengecekan Jadwal Penggantian Oli dan Pengingat.
# TUGAS  : Hitung target km dan tanggal ganti oli berikutnya, hitung sisa
#          km/hari, tentukan status (aman / mendekati / jatuh tempo).



"""
services/riwayatGantiOli.py

Logika fitur Riwayat Penggantian Oli (SKPL 3.1.5, Flowmap 4.2, DFD 3.2).
Seluruh logika dijadikan satu fungsi: riwayat_ganti_oli(username).
Tidak ada print/input; tampilan ada di menus/Menu_Riwayat_Oli.py.

Pemakaian (misalnya di main.py):
    from services.riwayatGantiOli import riwayat_ganti_oli
    hasil = riwayat_ganti_oli(username)

Struktur data mengikuti Kamus Data SKPL:
    kendaraan.csv:
        id, username, pemilik, merek, tipe, jenis, tahun, nomor_polisi, km,
        km_ganti_terakhir, tanggal_ganti_terakhir, oli_terakhir,
        interval_km, interval_hari, id_katalog, km_diperbarui
    penggantian_oli.csv:
        id, id_kendaraan, username, tanggal, km, oli, bengkel, harga, catatan
"""

import os
from datetime import datetime, timedelta

from Utilitas.Helper_Riwayat import baca_csv, ke_int, ke_tanggal

# data/ berada satu level di atas folder services/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
FILE_KENDARAAN = os.path.join(DATA_DIR, "kendaraan.csv")
FILE_PENGGANTIAN = os.path.join(DATA_DIR, "penggantian_oli.csv")


def riwayat_ganti_oli(username, id_kendaraan=None):
    """
    Ambil riwayat penggantian oli milik pengguna beserta jadwal berikutnya.

    Parameter:
        username      : pengguna yang sedang login.
        id_kendaraan  : (opsional) batasi hasil ke satu kendaraan.

    Kembalian: list of dict, satu dict per kendaraan milik pengguna
    (list kosong bila pengguna belum punya kendaraan):
        {
            "kendaraan"    : dict data kendaraan,
            "riwayat"      : list catatan penggantian (terbaru ke terlama),
            "jumlah"       : jumlah penggantian,
            "total_biaya"  : jumlah seluruh biaya,
            "jadwal"       : {"target_km", "sisa_km",
                              "target_tanggal" (datetime), "sisa_hari"}
                             (nilai None bila data tidak cukup),
        }
    """
    semua_penggantian = baca_csv(FILE_PENGGANTIAN)
    hasil = []

    for kendaraan in baca_csv(FILE_KENDARAAN):
        if kendaraan.get("username") != username:
            continue
        if id_kendaraan is not None and str(kendaraan.get("id")) != str(id_kendaraan):
            continue

        # Catatan penggantian milik kendaraan ini, terbaru ke terlama
        riwayat = [
            r
            for r in semua_penggantian
            if str(r.get("id_kendaraan")) == str(kendaraan.get("id"))
            and r.get("username") == username
        ]
        riwayat.sort(
            key=lambda r: (ke_tanggal(r.get("tanggal")) or datetime.min, ke_int(r.get("km"), 0)),
            reverse=True,
        )

        total_biaya = sum(ke_int(r.get("harga"), 0) for r in riwayat)

        # Jadwal berikutnya: basis penggantian terakhir, fallback data kendaraan
        interval_km = ke_int(kendaraan.get("interval_km"))
        interval_hari = ke_int(kendaraan.get("interval_hari"))
        km_sekarang = ke_int(kendaraan.get("km"))

        terakhir = riwayat[0] if riwayat else {}
        km_terakhir = ke_int(terakhir.get("km"), ke_int(kendaraan.get("km_ganti_terakhir")))
        tgl_terakhir = ke_tanggal(terakhir.get("tanggal")) or ke_tanggal(
            kendaraan.get("tanggal_ganti_terakhir")
        )

        jadwal = {"target_km": None, "sisa_km": None, "target_tanggal": None, "sisa_hari": None}

        if interval_km is not None and km_terakhir is not None:
            jadwal["target_km"] = km_terakhir + interval_km
            if km_sekarang is not None:
                jadwal["sisa_km"] = jadwal["target_km"] - km_sekarang

        if interval_hari is not None and tgl_terakhir is not None:
            jadwal["target_tanggal"] = tgl_terakhir + timedelta(days=interval_hari)
            jadwal["sisa_hari"] = (jadwal["target_tanggal"].date() - datetime.now().date()).days

        hasil.append(
            {
                "kendaraan": kendaraan,
                "riwayat": riwayat,
                "jumlah": len(riwayat),
                "total_biaya": total_biaya,
                "jadwal": jadwal,
            }
        )

    return hasil