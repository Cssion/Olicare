
import csv
import os
from datetime import datetime

DIREKTORI = os.path.dirname(__file__)
FILE_CSV = os.path.join(
    DIREKTORI, '..', 'data', 'kendaraan.csv'
)


def catat_penggantian_oli(username):
    with open(FILE_CSV, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        data = list(reader)

    kendaraan_user = []

    for kendaraan in data:
        if kendaraan['username'].strip().lower() == username.strip().lower():
            kendaraan_user.append(kendaraan)

    if not kendaraan_user:
        print("Belum ada kendaraan yang terdaftar.")
        return

    print("\n=== DAFTAR KENDARAAN ===")

    for i, kendaraan in enumerate(kendaraan_user, start=1):
        print(
            f"{i}. {kendaraan['merek']} "
            f"{kendaraan['tipe']} - {kendaraan['nomor_polisi']}"
        )

    try:
        pilihan = int(input("\nPilih kendaraan: "))

        if pilihan < 1 or pilihan > len(kendaraan_user):
            print("Pilihan tidak valid.")
            return

    except ValueError:
        print("Masukkan angka yang benar.")
        return

    kendaraan_dipilih = kendaraan_user[pilihan - 1]

    print("\n=== PENCATATAN PENGGANTIAN OLI ===")

    tanggal = input("Tanggal penggantian (YYYY-MM-DD): ")

    try:
        datetime.strptime(tanggal, "%Y-%m-%d")
    except ValueError:
        print("Format tanggal tidak valid.")
        return

    try:
        kilometer = int(input("Kilometer saat penggantian: "))

        if kilometer < 0:
            print("Kilometer tidak boleh negatif.")
            return

    except ValueError:
        print("Kilometer harus berupa angka.")
        return

    jenis_oli = input("Jenis oli yang digunakan: ").strip()

    if not jenis_oli:
        print("Jenis oli tidak boleh kosong.")
        return

    kendaraan_dipilih['km_ganti_terakhir'] = str(kilometer)
    kendaraan_dipilih['tanggal_ganti_terakhir'] = tanggal
    kendaraan_dipilih['oli_terakhir'] = jenis_oli

    with open(FILE_CSV, 'w', newline='', encoding='utf-8') as file:
        fieldnames = list(data[0].keys())
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print("\nPenggantian oli berhasil dicatat!")
    print("Data penggantian terakhir berhasil diperbarui.")


if __name__ == "__main__":
    username = input("Masukkan username: ")
    catat_penggantian_oli(username)
