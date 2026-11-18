import csv
import os
from datetime import date

FILE_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'kendaraan.csv')

def baca_data():
    if not os.path.exists(FILE_CSV):
        return [], []

    with open(FILE_CSV, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        kolom = reader.fieldnames
        baris = list(reader)

    if kolom is None:
        kolom = []
    return kolom, baris


def simpan_data(kolom, data):
    with open(FILE_CSV, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=kolom)
        writer.writeheader()
        writer.writerows(data)

def garis():
    print("-" * 60)


def ke_angka(teks):
    teks = str(teks).strip()
    if teks.isdigit():
        return int(teks)  
    return None


def nama_kendaraan(k):
    return f"{k['merek']} {k['tipe']} ({k['nomor_polisi']})"


def kendaraan_milik(data, username):
    hasil = []
    for k in data:
        if k['username'].strip().lower() == username.strip().lower():
            hasil.append(k)
    return hasil


def pilih_kendaraan(daftar):
    if len(daftar) == 0:
        print("Kamu belum punya kendaraan. Tambahkan dulu di menu Data Kendaraan.")
        return None

    print("\nPilih kendaraan:")
    nomor = 1
    for k in daftar:
        print(f"{nomor}. {nama_kendaraan(k)}")
        nomor += 1
    print("0. Batal")

    pilihan = input("Nomor kendaraan: ")

    if not pilihan.strip().isdigit():
        print("Input harus berupa angka!")
        return None

    pilihan = int(pilihan)

    if pilihan == 0:
        return None
    if pilihan < 1 or pilihan > len(daftar):
        print("Nomor kendaraan tidak ada!")
        return None

    return daftar[pilihan - 1]

# BAGIAN 3: FITUR USER

def ubah_km(username, koreksi):
    if koreksi:
        print("\n=== KOREKSI KILOMETER (SALAH KETIK) ===")
    else:
        print("\n=== PERBARUI KILOMETER ===")

    kolom, data = baca_data()
    kendaraan = pilih_kendaraan(kendaraan_milik(data, username))
    if kendaraan is None:
        return

    km_lama = ke_angka(kendaraan['km'])
    if km_lama is None:
        print(f"{nama_kendaraan(kendaraan)}: kilometer belum terisi.")
    else:
        print(f"{nama_kendaraan(kendaraan)}: kilometer sekarang {km_lama} km.")

    if koreksi:
        km_input = input("Kilometer yang BENAR: ")
    else:
        km_input = input("Kilometer odometer saat ini: ")

    # Validasi: harus angka
    km_baru = ke_angka(km_input)
    if km_baru is None:
        print("Input harus berupa angka bulat!")
        return

    # Validasi: odometer tidak boleh mundur (kecuali mode koreksi)
    if not koreksi and km_lama is not None and km_baru < km_lama:
        print(f"Kilometer tidak boleh lebih kecil dari {km_lama} km.")
        print("Kalau tadi salah ketik, pakai menu Koreksi kilometer.")
        return

    # Konfirmasi sebelum nyimpen
    print(f"\nKilometer {nama_kendaraan(kendaraan)}: {km_lama} -> {km_baru} km")
    yakin = input("Simpan perubahan? (y/n): ")

    if yakin.lower() != "y":
        print("Perubahan dibatalkan.")
        return

    kendaraan['km'] = str(km_baru)
    if 'km_diperbarui' in kolom:
        kendaraan['km_diperbarui'] = date.today().isoformat()  # format YYYY-MM-DD

    simpan_data(kolom, data)
    print("Kilometer berhasil disimpan!")


def perbarui_kilometer(username):
    ubah_km(username, False)


def koreksi_kilometer(username):
    ubah_km(username, True)


def cek_kilometer_saya(username):
    print("\n=== CEK KILOMETER ===")

    kolom, data = baca_data()
    kendaraan = pilih_kendaraan(kendaraan_milik(data, username))
    if kendaraan is None:
        return

    km = ke_angka(kendaraan['km'])
    diperbarui = kendaraan.get('km_diperbarui', '').strip()

    print(f"\nKendaraan       : {nama_kendaraan(kendaraan)}")
    if km is None:
        print("Kilometer       : belum terisi")
    else:
        print("Kilometer       :", km, "km")

    if diperbarui == "":
        print("Terakhir diubah : belum pernah diperbarui")
    else:
        print("Terakhir diubah :", diperbarui)


# FITUR ADMIN 

def tampilkan_tabel(daftar):
    garis()
    print(f"{'Username':<12}{'Kendaraan':<30}{'Km':>8}  {'Diperbarui'}")
    garis()
    for k in daftar:
        km = ke_angka(k['km'])
        teks_km = "-" if km is None else str(km)
        diperbarui = k.get('km_diperbarui', '').strip()
        if diperbarui == "":
            diperbarui = "-"
        print(f"{k['username']:<12}{nama_kendaraan(k):<30}{teks_km:>8}  {diperbarui}")
    garis()


def cek_semua_kilometer():
    print("\n=== KILOMETER SEMUA KENDARAAN ===")

    kolom, data = baca_data()
    if len(data) == 0:
        print("Belum ada data kendaraan.")
        return

    tampilkan_tabel(data)


def cek_kilometer_user():
    username = input("Masukkan username yang ingin dicek: ")

    kolom, data = baca_data()
    daftar = kendaraan_milik(data, username)

    if len(daftar) == 0:
        print("Data kendaraan user tersebut tidak ditemukan.")
        return

    print(f"\n=== KILOMETER {username.upper()} ===")
    tampilkan_tabel(daftar)



#MENU UTAMA (dipanggil dari Menu_User / Menu_Admin)

def menu_kilometer(username, role):
    """
    username : username yang sedang login
    role     : "admin" atau "user"
    """
    role = str(role).strip().lower()

    # Pengaman: role selain admin/user tidak boleh masuk
    if role not in ("admin", "user"):
        print("Role tidak dikenali, akses ditolak.")
        return

    while True:
        print("\n=== MENU KILOMETER ===")

        if role == "admin":
            print("1. Lihat kilometer semua kendaraan")
            print("2. Lihat kilometer kendaraan milik user")
            print("0. Kembali")
            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                cek_semua_kilometer()
            elif pilihan == "2":
                cek_kilometer_user()
            elif pilihan == "0":
                break
            else:
                print("Pilihan tidak valid!")

        else:  # role user
            print("1. Perbarui kilometer")
            print("2. Cek kilometer")
            print("3. Koreksi kilometer (salah ketik)")
            print("0. Kembali")
            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                perbarui_kilometer(username)
            elif pilihan == "2":
                cek_kilometer_saya(username)
            elif pilihan == "3":
                koreksi_kilometer(username)
            elif pilihan == "0":
                break
            else:
                print("Pilihan tidak valid!")
                
