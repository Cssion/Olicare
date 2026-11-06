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
    max_percobaan = 3

    while max_percobaan > 0:
        Judul("Login Page")
        username = input("Masukkan Username: ").lower().strip()
        password = getpass("Masukkan Password: ")

        if not username or not password:
            max_percobaan -= 1
            print("Username dan password tidak boleh kosong!")
            continue

        user = cek_akun(username)

        if user is not None and user['password'] == password:
            if user['role'] == 'admin':
                print(f"Selamat datang admin {user['username']}")
            else:
                print(f"Selamat datang, {user['username']}!")
            return user          # kembalikan data user agar bisa dipakai menu lain

        max_percobaan -= 1
        print(f"Username atau password salah! Sisa percobaan: {max_percobaan}")

    print("Anda tidak bisa melakukan login lagi")
    return None

    
    

    



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
        writer.writerow([username, password,'user'])

    return True, "Akun berhasil dibuat! Silakan login."







