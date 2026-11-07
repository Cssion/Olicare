from Utilitas.Judul import Judul
from Utilitas.Rapihkan_Text import text
import os
import csv

file_sekarang = os.path.dirname(__file__)
CSV_FILE = os.path.join(file_sekarang,'..','data','akun.csv')
FIELD = ['nama','username','password','role']

def readFile():
    with open(CSV_FILE,'r') as file:
        reader = csv.DictReader(file)
        return list(reader)

def writeFile(users):
    rows = [{f: u[f] for f in FIELD} for u in users]
    with open(CSV_FILE,'w',newline='') as file:
        writer = csv.DictWriter(file, fieldnames=FIELD)
        writer.writeheader()
        writer.writerows(users)

        

def lihatUser():
    user = readFile()

    print(f"{' ':<2}{'NAMA':<20}{'USERNAME':<20}{'ROLE':<20}")
    print("-" * 40)
    for u in user:
        print(f"{u['nama']:<20}{u['username']:<20}{u['role']:<20}")

def updateUser(users):
    lihatUser()
    username = text(input("Masukan Username Dari User Untuk Mengupdate Data: "))

    for u in users:
        if u['username'] == username:
            field = text(input("Masukan Field Data Yang Akan Diupdate nama / username / role: "))

            if field == 'nama':
                u['nama'] = text(input("Masukan Nama Dari User: "))

            elif field == 'username':
                new_username = text(input("Masukan username baru user (username harus unique): "))
                if any(x['username'] == new_username for x in users):
                    print("Username sudah dipakai.")
                    return
                u['username'] = new_username

            elif field == 'role':
                u['role'] = text(input("Masukan Role Baru: "))

            else:
                print("Field tidak valid")
                return

            writeFile(users)
            print("User berhasil diubah")
            return

    print("User tidak ditemukan")

def deleteUser(users):
    lihatUser()
    username = text(input("Masukan username dari user yang ingin dihapus: "))

    for u in users:
        if u['username'] == username:
            konfirmasi = text(input(f"Apakah anda yakin ingin menghapus user {u['username']}? y/n: "))
            if konfirmasi != 'y':
                print("Penghapusan Dibatalkan")
                return
            users.remove(u)
            writeFile(users)
            print("User Berhasil Dihapus")
            return
    print("User tidak ditemukan")
    
            




def kelola_user():
    load_users = readFile()
    while True:
        Judul("KELOLA DASAR USER")
        print("1. Lihat Data User")
        print("2. Update Data User")
        print("3. Hapus Data User")
        userChoose = int(input("Silahkan Pilih Operasi Yang Ingin Dilakukan: "))

        if(userChoose == 1):
            lihatUser()
            break
        elif(userChoose == 2):
            updateUser(load_users)
            break
        elif(userChoose == 3):
            deleteUser(load_users)
            break
    