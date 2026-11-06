# menus/admin_menu.py
# KELAS  : AdminMenu
# FUNGSI : Menu untuk admin OliCare.
# PILIHAN: Kelola produk oli (tambah, ubah, lihat), logout.

from Utilitas.Judul import Judul
from Utilitas.Kelola_User import kelola_user
from Utilitas.Kelola_Kendaraan import kelola_kendaraan
from Utilitas.Tinjau_Data_Oli import tinjau_oli
def menu_admin():
    Judul("ADMIN DASHBOARD")
    while True:
        print("1. Kelola Data User")
        print("2. Kelola Data Kendaraan")
        print("3. Tinjau Data Produk Oli")
        userChoose = int(input("Pilih Operasi Yang Ingin Dilakukan: "))

        if userChoose == 1:
            kelola_user()
            break
        elif userChoose == 2:
            kelola_kendaraan()
            break
        elif userChoose == 3:
            tinjau_oli()
            break
        else:
            print("Pilihan Invalid")
            break

