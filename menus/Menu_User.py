
# menus/user_menu.py
# KELAS  : UserMenu
# FUNGSI : Menu untuk pengguna kendaraan.
# PILIHAN: Data kendaraan, catat kilometer, cek jadwal ganti oli,
#          catat penggantian oli, riwayat, rekomendasi oli, logout.
# CATATAN: Hanya menampilkan menu dan menerima input. Perhitungan ada di services/.

from Utilitas.Judul import Judul
from Utilitas.Rapihkan_Text import text
from services.Pengelola_Data_Kendaraan import tambah_kendaraan, lihat_kendaraan
from services.Catat_Ganti_Oli import catat_penggantian_oli


def menu_user(username):
    while True:
        print("\n=== MENU PENGGUNA ===")
        print("1. Pengelolaan Data Kendaraan")
        print("2. Catat Ganti Oli")
        print("3. Cek Jadwal Ganti Oli")
        print("4. Catat Kilometer")
        print("5. Rekomendasi Oli")
        print("6. Riwayat Ganti Oli")
        print("7. Logout")

        userChoose = text(input("Pilih Operasi Yang Ingin Dilakukan: "))

        if userChoose == "1":
            print("\n=== PENGELOLAAN DATA KENDARAAN ===")
            print("1. Tambah Kendaraan")
            print("2. Lihat Kendaraan")

            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                tambah_kendaraan(username)
            elif pilihan == "2":
                lihat_kendaraan(username)
            else:
                print("Input tidak valid")

        elif userChoose == "2":
            catat_penggantian_oli(username)

        elif userChoose == "3":
            print("Fitur Cek Jadwal Ganti Oli belum dihubungkan.")

        elif userChoose == "4":
            print("Fitur Catat Kilometer belum dihubungkan.")

        elif userChoose == "5":
            print("Fitur Rekomendasi Oli belum dihubungkan.")

        elif userChoose == "6":
            print("Fitur Riwayat Ganti Oli belum dihubungkan.")

        elif userChoose == "7":
            print("Berhasil logout.")
            break

        else:
            print("Input tidak valid")
