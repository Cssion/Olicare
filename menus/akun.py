
# menus/akun.py
# FUNGSI : Mengelola proses login dan registrasi akun.
# TUGAS  : Memvalidasi akun berdasarkan data pada file CSV.
# CATATAN: Akun baru otomatis mendapatkan role 'user'.

import csv
import os
from getpass import getpass
from Utilitas.Judul import Judul
from Utilitas.Rapihkan_Text import text


direktori_sekarang = os.path.dirname(__file__)
CSV_FILE = os.path.join(direktori_sekarang, '..', 'data', 'akun.csv')


def login():
    max_percobaan = 3

    while max_percobaan > 0:
        Judul("Login Page")

        username = text(input("Masukkan Username: "))
        password = getpass("Masukkan Password: ")

        if not username or not password:
            max_percobaan -= 1
            print("Username dan password tidak boleh kosong!")
            continue

        with open(CSV_FILE, 'r', newline='', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, skipinitialspace=True)

            for user in reader:
                if (
                    user['username'].strip().lower() == username.strip().lower()
                    and user['password'].strip() == password.strip()
                ):
                    print("Login berhasil!")
                    return user

        max_percobaan -= 1
        print(f"Username atau password salah! Sisa percobaan: {max_percobaan}")

    print("Anda tidak bisa melakukan login lagi.")
    return None


def registrasi():
    Judul("Registrasi")

    print("Silakan buat username dan password baru.")

    nama = text(input("Masukkan Nama: "))
    username = input("Masukkan Username: ").strip()
    password = getpass("Masukkan Password: ").strip()

    if not nama or not username or not password:
        print("Field tidak boleh ada yang kosong!")
        return False

    with open(CSV_FILE, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        data = list(reader)

    for user in data:
        if user['username'].strip().lower() == username.lower():
            print("Username sudah terdaftar! Silakan gunakan username lain.")
            return False

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([nama, username, password, 'user'])

    print("Akun Anda berhasil dibuat. Silakan login.")
    return True
