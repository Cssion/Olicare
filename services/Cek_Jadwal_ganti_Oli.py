import csv
import os
from datetime import date

FILE_CSV = os.path.join(os.path.dirname(__file__), '..', 'data', 'kendaraan.csv')


DEFAULT_INTERVAL_KM = 2000
DEFAULT_INTERVAL_HARI = 90


BATAS_KM_MENDEKATI = 500
BATAS_HARI_MENDEKATI = 30


BATAS_HARI_KM_LAMA = 14


HARI_PER_BULAN = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)


# BAGIAN 1: BACA DATA
def baca_data():
    """Mengembalikan list baris kendaraan (tiap baris berupa dictionary)."""
    if not os.path.exists(FILE_CSV):
        return []

    with open(FILE_CSV, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        return list(reader)


# BAGIAN 2: FUNGSI BANTU

def garis():
    print("-" * 78)


def ambil(k, kolom): #ngambil isi kolom sebagai teks bersih, ksng kalau tidak ada
    nilai = k.get(kolom, "")
    if nilai is None:
        return ""
    return str(nilai).strip()


def ke_angka(teks): #ngubah teks jadi angka bulat, mengembalikan none kalu bkn angka
    teks = str(teks).strip()
    if teks.isdigit():
        return int(teks)  # casting string -> integer
    return None


def tahun_kabisat(tahun):
    return (tahun % 4 == 0 and tahun % 100 != 0) or tahun % 400 == 0


def ke_tanggal(teks):
    bagian = str(teks).strip().split("-")

    if len(bagian) != 3:
        return None
    if not (bagian[0].isdigit() and bagian[1].isdigit() and bagian[2].isdigit()):
        return None

    tahun = int(bagian[0])
    bulan = int(bagian[1])
    hari = int(bagian[2])

    if tahun < 1 or tahun > 9999 or bulan < 1 or bulan > 12 or hari < 1:
        return None

    maksimal = HARI_PER_BULAN[bulan - 1]
    if bulan == 2 and tahun_kabisat(tahun):
        maksimal = 29
    if hari > maksimal:
        return None

    return date(tahun, bulan, hari)


def nama_kendaraan(k):
    return f"{k['merek']} {k['tipe']} ({k['nomor_polisi']})"


def kendaraan_milik(data, username):
    #ngambil kendaraan 1 user aja
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


def teks_sisa(nilai, satuan):
    if nilai is None:
        return "-"
    if nilai <= 0:
        return f"terlewat {abs(nilai)} {satuan}"
    return f"{nilai} {satuan} lagi"


# ------------------------------------------------------------
# BAGIAN 3: HITUNG JADWAL

def hitung_jadwal(k):
    """
    Mengembalikan (sisa_km, sisa_hari, status).
    sisa_km / sisa_hari bernilai None kalau datanya belum ada.
    """
    km = ke_angka(ambil(k, 'km'))
    km_ganti = ke_angka(ambil(k, 'km_ganti_terakhir'))
    tgl_ganti = ke_tanggal(ambil(k, 'tanggal_ganti_terakhir'))

    interval_km = ke_angka(ambil(k, 'interval_km'))
    if interval_km is None:
        interval_km = DEFAULT_INTERVAL_KM

    interval_hari = ke_angka(ambil(k, 'interval_hari'))
    if interval_hari is None:
        interval_hari = DEFAULT_INTERVAL_HARI

    # Sisa kilometer sebelum ganti oli
    sisa_km = None
    if km is not None and km_ganti is not None:
        sisa_km = km_ganti + interval_km - km

    # Sisa hari sebelum ganti oli
    sisa_hari = None
    if tgl_ganti is not None:
        hari_berlalu = (date.today() - tgl_ganti).days
        sisa_hari = interval_hari - hari_berlalu

    # Tentukan status
    if sisa_km is None and sisa_hari is None:
        status = "DATA BELUM LENGKAP"
    elif (sisa_km is not None and sisa_km <= 0) or (sisa_hari is not None and sisa_hari <= 0):
        status = "SEGERA GANTI OLI"
    elif (sisa_km is not None and sisa_km <= BATAS_KM_MENDEKATI) or (sisa_hari is not None and sisa_hari <= BATAS_HARI_MENDEKATI):
        status = "MENDEKATI JADWAL"
    else:
        status = "AMAN"

    return sisa_km, sisa_hari, status


def pesan_pengingat(sisa_km, sisa_hari):
    """
    Mengembalikan LIST kalimat pengingat (H-1, H-3, sisa sebulan, dst).
    List kosong kalau jadwal ganti oli masih lama.
    """
    pesan = []

    # Pengingat berdasarkan hari
    if sisa_hari is not None:
        if sisa_hari < 0:
            pesan.append(f"Jadwal ganti oli sudah TERLEWAT {abs(sisa_hari)} hari!")
        elif sisa_hari == 0:
            pesan.append("HARI INI waktunya ganti oli!")
        elif sisa_hari == 1:
            pesan.append("H-1 ganti oli! Besok waktunya ganti oli.")
        elif sisa_hari <= 3:
            pesan.append(f"H-{sisa_hari} ganti oli, tinggal {sisa_hari} hari lagi.")
        elif sisa_hari <= 7:
            pesan.append(f"Tinggal {sisa_hari} hari lagi, kurang dari seminggu menuju ganti oli.")
        elif sisa_hari <= 30:
            pesan.append(f"Sisa {sisa_hari} hari lagi, kurang dari sebulan menuju ganti oli.")

    # Pengingat berdasarkan kilometer
    if sisa_km is not None:
        if sisa_km < 0:
            pesan.append(f"Kilometer sudah melewati jadwal ganti oli sejauh {abs(sisa_km)} km!")
        elif sisa_km == 0:
            pesan.append("Kilometer tepat di jadwal ganti oli!")
        elif sisa_km <= 100:
            pesan.append(f"Tinggal {sisa_km} km lagi menuju ganti oli, segera ke bengkel.")
        elif sisa_km <= BATAS_KM_MENDEKATI:
            pesan.append(f"Sisa {sisa_km} km lagi menuju ganti oli.")

    return pesan



# BAGIAN 4: FITUR USER
def cek_jadwal_saya(username):
    print("\n=== CEK JADWAL GANTI OLI ===")

    data = baca_data()
    kendaraan = pilih_kendaraan(kendaraan_milik(data, username))
    if kendaraan is None:
        return

    sisa_km, sisa_hari, status = hitung_jadwal(kendaraan)

    km = ke_angka(ambil(kendaraan, 'km'))
    oli = ambil(kendaraan, 'oli_terakhir')
    if oli == "":
        oli = "-"

    print(f"\nKendaraan            : {nama_kendaraan(kendaraan)}")
    print("Kilometer sekarang   :", "-" if km is None else f"{km} km")
    print("Oli terakhir         :", oli)
    print("Sisa kilometer       :", teks_sisa(sisa_km, "km"))
    print("Sisa waktu           :", teks_sisa(sisa_hari, "hari"))
    print("STATUS               :", status)

    if status == "DATA BELUM LENGKAP":
        print("\nCatat dulu penggantian oli terakhir di menu Catat Ganti Oli.")
    else:
        pesan = pesan_pengingat(sisa_km, sisa_hari)
        if len(pesan) > 0:
            print("\n!!! PENGINGAT !!!")
            for p in pesan:
                print("-", p)

    # Ingatkan kalau kilometer sudah lama tidak diperbarui
    # (karena sisa kilometer dihitung dari kilometer terakhir yang tercatat)
    tgl_km = ke_tanggal(ambil(kendaraan, 'km_diperbarui'))
    if tgl_km is None:
        print("\nKilometer belum pernah diperbarui di menu Pencatatan Kilometer.")
    else:
        lalu = (date.today() - tgl_km).days
        print(f"\nKilometer terakhir diperbarui: {tgl_km} ({lalu} hari lalu)")
        if lalu > BATAS_HARI_KM_LAMA:
            print("Sudah lama, perbarui dulu di menu Pencatatan Kilometer supaya hasilnya akurat.")


def tampilkan_pengingat(username):
    """
    Menampilkan pengingat ganti oli untuk SEMUA kendaraan milik user.
    Tidak menampilkan apa-apa kalau semua kendaraan masih aman.
    Bisa dipanggil dari Menu_User tepat setelah login.
    """
    data = baca_data()
    ada_pengingat = False

    for k in kendaraan_milik(data, username):
        sisa_km, sisa_hari, status = hitung_jadwal(k)
        pesan = pesan_pengingat(sisa_km, sisa_hari)

        if len(pesan) > 0:
            if not ada_pengingat:
                print("\n=== PENGINGAT GANTI OLI ===")
                ada_pengingat = True
            print(f"{nama_kendaraan(k)}:")
            for p in pesan:
                print("  -", p)

    if not ada_pengingat:
        print("\nTidak ada pengingat ganti oli. Semua kendaraan masih aman.")


# BAGIAN 5: FITUR ADMIN (hanya melihat)
def tampilkan_tabel(daftar):
    garis()
    print(f"{'Username':<10}{'Kendaraan':<28}{'Sisa Km':>16}{'Sisa Hari':>16}  Status")
    garis()
    for k in daftar:
        sisa_km, sisa_hari, status = hitung_jadwal(k)
        kendaraan = nama_kendaraan(k)[:27]
        teks_km = teks_sisa(sisa_km, "km")
        teks_hari = teks_sisa(sisa_hari, "hari")
        print(f"{k['username']:<10}{kendaraan:<28}{teks_km:>16}{teks_hari:>16}  {status}")
    garis()


def cek_semua_jadwal():
    print("\n=== JADWAL GANTI OLI SEMUA KENDARAAN ===")

    data = baca_data()
    if len(data) == 0:
        print("Belum ada data kendaraan.")
        return

    tampilkan_tabel(data)


def cek_perlu_perhatian():
    print("\n=== KENDARAAN YANG PERLU PERHATIAN ===")

    data = baca_data()
    perlu = []
    for k in data:
        sisa_km, sisa_hari, status = hitung_jadwal(k)
        if status in ("SEGERA GANTI OLI", "MENDEKATI JADWAL"):
            perlu.append(k)

    if len(perlu) == 0:
        print("Tidak ada kendaraan yang mendekati jadwal ganti oli.")
        return

    tampilkan_tabel(perlu)

# BAGIAN 6: MENU UTAMA (dipanggil dari Menu_User / Menu_Admin)

def menu_jadwal_oli(username, role):
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
        print("\n=== MENU JADWAL GANTI OLI ===")

        if role == "admin":
            print("1. Lihat jadwal semua kendaraan")
            print("2. Lihat kendaraan yang perlu perhatian")
            print("0. Kembali")
            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                cek_semua_jadwal()
            elif pilihan == "2":
                cek_perlu_perhatian()
            elif pilihan == "0":
                break
            else:
                print("Pilihan tidak valid!")

        else:  # role user
            print("1. Cek jadwal ganti oli")
            print("2. Lihat pengingat semua kendaraan saya")
            print("0. Kembali")
            pilihan = input("Pilih menu: ")

            if pilihan == "1":
                cek_jadwal_saya(username)
            elif pilihan == "2":
                tampilkan_pengingat(username)
            elif pilihan == "0":
                break
            else:
                print("Pilihan tidak valid!")
