# menus/main_menu.py
# FUNGSI : Menu awal program: Login, Registrasi, Keluar.
# TUGAS  : Setelah login berhasil, arahkan ke UserMenu atau AdminMenu
#          sesuai role.

#=====NOTE=======
# Setiap user harus memiliki role yang berbeda yaitu User Biasa & admin
# Agar dapat membedakan mana yang masuk ke menu admin dan mana yang masuk ke menu user
# Belum ada nambahin fitur kayak gitu disini
# Baru nambahin validasi akun dan file csv usernya aja


from Utilitas.Judul import Judul
from getpass import getpass
from Utilitas.cek_akun import cek_akun
import csv
import os

direktori_sekarang = os.path.dirname(__file__)
CSV_FILE = os.path.join(direktori_sekarang,'..','data','users.csv')

def login():
    Judul("Login Page")
    username = input("Masukkan Username: ").strip()
    password = getpass("Masukkan Password: ")

    if not username or not password:
        return False, "Username dan password tidak boleh kosong!", None

    user = cek_akun(username)

    if user is None:
        return False, "Akun tidak ditemukan!", None

    if user['password'] == password:
        print(f"Selamat datang, {user['username']}!", user)
        return True

    return False, "Username atau password salah!", None



def registrasi():
    Judul("Registrasi")
    print("Silakan buat username dan password baru.")

    username = input("Masukkan Username: ").strip()
    password = input("Masukkan Password: ").strip()
    if not username or not password:
        return False, "Username dan password tidak boleh kosong!"

    akun = cek_akun(username)
    if akun:
        return False, "Username sudah terdaftar! Silakan gunakan username lain."

    # Pendaftaran umum otomatis diberikan role 'user'

    with open(CSV_FILE, "a", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([username, password])

    return True, "Akun berhasil dibuat! Silakan login."







