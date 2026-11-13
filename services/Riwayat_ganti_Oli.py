# services/reminder_service.py
# FUNGSI : Fitur Pengecekan Jadwal Penggantian Oli dan Pengingat.
# TUGAS  : Hitung target km dan tanggal ganti oli berikutnya, hitung sisa
#          km/hari, tentukan status (aman / mendekati / jatuh tempo).


import os
from datetime import datetime, timedelta

from Utilitas.Helper_Riwayat_Pergantian import baca_csv, ke_angka, ke_tanggal

# Lokasi file data (folder data/ ada satu tingkat di atas folder services/)
FOLDER_DATA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
FILE_KENDARAAN = os.path.join(FOLDER_DATA, "kendaraan.csv")
FILE_PENGGANTIAN = os.path.join(FOLDER_DATA, "penggantian_oli.csv")


def ambil_tanggal(catatan):
    """Dipakai untuk mengurutkan riwayat berdasarkan tanggal."""
    return catatan["tanggal"]


def riwayat_ganti_oli(username):
    """
    Mengambil riwayat penggantian oli semua kendaraan milik pengguna.

    Hasilnya berupa list. Setiap isinya adalah dictionary dengan kunci:
        kendaraan   : data kendaraan
        riwayat     : list catatan penggantian oli (terbaru di urutan pertama)
        jumlah      : banyaknya penggantian
        total_biaya : jumlah semua biaya
        jadwal      : jadwal penggantian berikutnya (isi None kalau datanya kurang)
    """
    semua_kendaraan = baca_csv(FILE_KENDARAAN)
    semua_catatan = baca_csv(FILE_PENGGANTIAN)
    hasil = []

    for kendaraan in semua_kendaraan:
        # Lewati kendaraan milik pengguna lain
        if kendaraan["username"] != username:
            continue

        # 1. Kumpulkan catatan penggantian oli milik kendaraan ini
        riwayat = []
        for catatan in semua_catatan:
            if catatan["id_kendaraan"] == kendaraan["id"] and catatan["username"] == username:
                riwayat.append(catatan)

        # 2. Urutkan dari tanggal terbaru ke terlama
        riwayat.sort(key=ambil_tanggal, reverse=True)

        # 3. Hitung total biaya
        total_biaya = 0
        for catatan in riwayat:
            biaya = ke_angka(catatan["harga"])
            if biaya is not None:
                total_biaya += biaya

        # 4. Hitung jadwal penggantian berikutnya
        jadwal = {
            "target_km": None,
            "sisa_km": None,
            "target_tanggal": None,
            "sisa_hari": None,
        }

        interval_km = ke_angka(kendaraan["interval_km"])
        interval_hari = ke_angka(kendaraan["interval_hari"])
        km_sekarang = ke_angka(kendaraan["km"])

        # Ambil data penggantian terakhir (dari riwayat, kalau kosong dari data kendaraan)
        if len(riwayat) > 0:
            km_terakhir = ke_angka(riwayat[0]["km"])
            tanggal_terakhir = ke_tanggal(riwayat[0]["tanggal"])
        else:
            km_terakhir = ke_angka(kendaraan["km_ganti_terakhir"])
            tanggal_terakhir = ke_tanggal(kendaraan["tanggal_ganti_terakhir"])

        if interval_km is not None and km_terakhir is not None:
            jadwal["target_km"] = km_terakhir + interval_km
            if km_sekarang is not None:
                jadwal["sisa_km"] = jadwal["target_km"] - km_sekarang

        if interval_hari is not None and tanggal_terakhir is not None:
            jadwal["target_tanggal"] = tanggal_terakhir + timedelta(days=interval_hari)
            selisih = jadwal["target_tanggal"] - datetime.now()
            jadwal["sisa_hari"] = selisih.days + 1

        hasil.append({
            "kendaraan": kendaraan,
            "riwayat": riwayat,
            "jumlah": len(riwayat),
            "total_biaya": total_biaya,
            "jadwal": jadwal,
        })

    return hasil