# menus/user_menu.py
# KELAS  : UserMenu
# FUNGSI : Menu untuk pengguna kendaraan.
# PILIHAN: Data kendaraan, catat kilometer, cek jadwal ganti oli,
#          catat penggantian oli, riwayat, rekomendasi oli, logout.
# CATATAN: Hanya menampilkan menu dan menerima input. Perhitungan ada di services/.


from Utilitas.Judul import Judul
from Utilitas.Rapihkan_Text import text


def menu_user():
    print("1. Catat Ganti Oli")
    print("2. Cek Jadwal Ganti Oli")
    print("3. Catat Kilometer")
    print("4. Rekomendasi Oli")
    print("5. Riwayat Ganti Oli")
    userChoose = text(input("Pilih Operasi Yang Ingin Dilakukan: "))


    while True:
        if( userChoose == 1):
            catatGantiOli()
            break
        elif(userChoose == 2):
            cekJadwalGantiOli()
            break
        elif(userChoose == 3):
            catatKilometer()
            break
        elif(userChoose == 4):
            rekomendasiOli()
            break
        elif(userChoose == 5):
            riwayatGantiOli()
            break
        else:
            print("Input tidak valid")
            break
