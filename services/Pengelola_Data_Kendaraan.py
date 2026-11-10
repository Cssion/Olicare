
import csv
import os

DIREKTORI = os.path.dirname(__file__)
FILE_CSV = os.path.join(DIREKTORI, '..', 'data', 'kendaraan.csv')

FIELD = [
    'id', 'username', 'pemilik', 'merek', 'tipe',
    'jenis', 'tahun', 'nomor_polisi', 'km',
    'km_ganti_terakhir', 'tanggal_ganti_terakhir',
    'oli_terakhir', 'interval_km', 'interval_hari',
    'id_katalog', 'km_diperbarui'
]


def baca_data():
    with open(FILE_CSV, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        return list(reader)


def tambah_kendaraan(username):
    print("\n=== TAMBAH DATA KENDARAAN ===")

    pemilik = input("Nama pemilik: ")
    merek = input("Merek kendaraan: ")
    tipe = input("Tipe kendaraan: ")
    jenis = input("Jenis kendaraan: ")
    tahun = input("Tahun kendaraan: ")
    nomor_polisi = input("Nomor polisi: ")
    km = input("Kilometer saat ini: ")

    data = baca_data()

    id_baru = 1

    for kendaraan in data:
        try:
            id_lama = int(kendaraan['id'])
            if id_lama >= id_baru:
                id_baru = id_lama + 1
        except (ValueError, KeyError):
            continue

    kendaraan_baru = {
        'id': id_baru,
        'username': username.strip(),
        'pemilik': pemilik,
        'merek': merek,
        'tipe': tipe,
        'jenis': jenis,
        'tahun': tahun,
        'nomor_polisi': nomor_polisi,
        'km': km,
        'km_ganti_terakhir': '',
        'tanggal_ganti_terakhir': '',
        'oli_terakhir': '',
        'interval_km': '',
        'interval_hari': '',
        'id_katalog': '',
        'km_diperbarui': ''
    }

    data.append(kendaraan_baru)

    with open(FILE_CSV, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELD)
        writer.writeheader()
        writer.writerows(data)

    print("\nData kendaraan berhasil disimpan!")


def lihat_kendaraan(username):
    print("\n=== DATA KENDARAAN SAYA ===")

    data = baca_data()
    ditemukan = False

    for kendaraan in data:
        if kendaraan['username'].strip().lower() == username.strip().lower():
            ditemukan = True

            print("\nID:", kendaraan['id'])
            print("Pemilik:", kendaraan['pemilik'])
            print("Merek:", kendaraan['merek'])
            print("Tipe:", kendaraan['tipe'])
            print("Jenis:", kendaraan['jenis'])
            print("Tahun:", kendaraan['tahun'])
            print("Nomor Polisi:", kendaraan['nomor_polisi'])
            print("Kilometer:", kendaraan['km'])

    if not ditemukan:
        print("Belum ada data kendaraan.")


if __name__ == "__main__":
    username = input("Masukkan username: ")

    print("\n=== MENU PENGELOLAAN KENDARAAN ===")
    print("1. Tambah Kendaraan")
    print("2. Lihat Kendaraan")

    pilihan = input("Pilih menu: ")

    if pilihan == "1":
        tambah_kendaraan(username)
    elif pilihan == "2":
        lihat_kendaraan(username)
    else:
        print("Pilihan tidak valid.")
