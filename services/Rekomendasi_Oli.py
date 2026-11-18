# services/recommendation_service.py
# FUNGSI : Fitur Rekomendasi Jenis Oli dan Pengelolaan Produk Oli (admin).
# TUGAS  : Cocokkan kendaraan dengan katalog dan produk oli, tampilkan
#          rekomendasi; admin menambah/mengubah/melihat produk oli.


import csv
import os

from Utilitas.Judul import Judul
from Utilitas.Rapihkan_Text import text
from services.Pencatatan_Kilometer import (
    baca_data, kendaraan_milik, pilih_kendaraan, nama_kendaraan, ke_angka, garis
)

DIREKTORI = os.path.dirname(__file__)
FILE_PRODUK = os.path.join(DIREKTORI, '..', 'data', 'produk_oli.csv')
FILE_KATALOG = os.path.join(DIREKTORI, '..', 'data', 'katalog_kendaraan.csv')
FILE_REKOMENDASI = os.path.join(DIREKTORI, '..', 'data', 'rekomendasi_oli.csv')

FIELD_PRODUK = [
    'id', 'nama', 'merek', 'jenis', 'viskositas',
    'spesifikasi', 'volume_kemasan', 'harga', 'catatan'
]


# ============================================================
# BAGIAN 1: FUNGSI BANTU
# ============================================================

def baca_csv(nama_file):
    """Membaca file CSV menjadi list. Kalau file belum ada, hasilnya list kosong."""
    if not os.path.exists(nama_file):
        return []

    with open(nama_file, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, skipinitialspace=True)
        return list(reader)


def format_rupiah(teks):
    """Contoh: '50000' -> Rp50.000"""
    angka = ke_angka(teks)
    if angka is None:
        return "-"
    return "Rp" + format(angka, ",").replace(",", ".")


# ============================================================
# BAGIAN 2: REKOMENDASI OLI (PENGGUNA)
# ============================================================

def cari_katalog(kendaraan, daftar_katalog):
    """
    Mencari data katalog yang cocok dengan kendaraan.
    Hasil: (daftar katalog cocok, keterangan, apakah cocok persis)
    """
    merek = text(kendaraan['merek'])
    tipe = text(kendaraan['tipe'])
    jenis = text(kendaraan['jenis'])
    tahun = kendaraan['tahun'].strip()

    # Cara 1: kendaraan sudah punya id_katalog
    id_katalog = kendaraan['id_katalog'].strip()
    if id_katalog != "":
        for katalog in daftar_katalog:
            if katalog['id'].strip() == id_katalog:
                return [katalog], "sesuai katalog kendaraan", True

    # Cara 2: merek dan model (tipe) sama
    cocok = []
    for katalog in daftar_katalog:
        if text(katalog['merek']) == merek and text(katalog['model']) == tipe:
            cocok.append(katalog)

    if len(cocok) > 0:
        # Kalau ada beberapa tahun, pilih yang tahunnya sama dengan kendaraan
        for katalog in cocok:
            if katalog['tahun'].strip() == tahun:
                return [katalog], "merek, model, dan tahun kendaraan", True
        return [cocok[0]], "merek dan model kendaraan", True

    # Cara 3: tidak ada yang persis, pakai jenis kendaraan (kategori)
    sekategori = []
    for katalog in daftar_katalog:
        if text(katalog['kategori']) == jenis:
            sekategori.append(katalog)

    if len(sekategori) > 0:
        return sekategori, "jenis kendaraan (" + jenis + "), rekomendasi umum", False

    return [], "", False


def urutan_kecocokan(rekomendasi):
    """Dipakai untuk mengurutkan: tinggi dulu, lalu sedang, lalu lainnya."""
    kecocokan = text(rekomendasi['kecocokan'])
    if kecocokan == "tinggi":
        return 0
    if kecocokan == "sedang":
        return 1
    return 2


def cari_rekomendasi(daftar_katalog_cocok):
    """Mengambil rekomendasi oli untuk katalog yang cocok, tanpa produk yang dobel."""
    semua = baca_csv(FILE_REKOMENDASI)
    hasil = []
    produk_sudah_ada = []

    for katalog in daftar_katalog_cocok:
        for r in semua:
            if r['id_katalog'].strip() != katalog['id'].strip():
                continue
            if r['id_produk'].strip() in produk_sudah_ada:
                continue
            hasil.append(r)
            produk_sudah_ada.append(r['id_produk'].strip())

    hasil.sort(key=urutan_kecocokan)
    return hasil


def cari_produk(id_produk, daftar_produk):
    """Mencari satu produk berdasarkan id. Kalau tidak ketemu, hasilnya None."""
    for p in daftar_produk:
        if p['id'].strip() == id_produk.strip():
            return p
    return None


def tampilkan_rekomendasi(kendaraan, katalog, keterangan, persis, daftar_rekomendasi):
    produk = baca_csv(FILE_PRODUK)

    print(f"\nKendaraan        : {nama_kendaraan(kendaraan)}")
    print(f"Dasar pencocokan : {keterangan}")
    if persis:
        print(f"Kapasitas oli    : {katalog[0]['kapasitas_oli']}")

    print("\n=== REKOMENDASI OLI ===")
    nomor = 1
    for r in daftar_rekomendasi:
        garis()
        print(f"{nomor}. {r['nama_produk']} ({r['merek']})")
        print(f"   Viskositas         : {r['viskositas']}")
        print(f"   Standar            : {r['standar']}")
        print(f"   Tingkat kecocokan  : {r['kecocokan']}")
        print(f"   Volume penggantian : {r['volume_penggantian']}")

        p = cari_produk(r['id_produk'], produk)
        if p is not None:
            print(f"   Jenis oli          : {p['jenis']}")
            print(f"   Ukuran kemasan     : {p['volume_kemasan']}")
            print(f"   Harga              : {format_rupiah(p['harga'])}")

        if text(r['terverifikasi']) == "ya":
            print("   Status             : sudah diverifikasi admin")
        else:
            print("   Status             : belum diverifikasi admin")

        if r['catatan'].strip() != "":
            print(f"   Catatan            : {r['catatan']}")
        nomor += 1
    garis()
    print("Pilih oli yang sesuai, lalu catat di menu Catat Ganti Oli setelah penggantian.")


def rekomendasi_oli(username):
    """Fungsi utama rekomendasi oli, dipanggil dari Menu_User."""
    Judul("Rekomendasi Oli")

    kolom, data = baca_data()
    kendaraan = pilih_kendaraan(kendaraan_milik(data, username))
    if kendaraan is None:
        return

    daftar_katalog = baca_csv(FILE_KATALOG)
    if len(daftar_katalog) == 0:
        print("Data katalog kendaraan belum tersedia. Hubungi admin.")
        return

    katalog, keterangan, persis = cari_katalog(kendaraan, daftar_katalog)
    if len(katalog) == 0:
        print(f"\n{nama_kendaraan(kendaraan)} belum ada di katalog.")
        print("Rekomendasi belum tersedia. Silakan hubungi admin.")
        return

    daftar_rekomendasi = cari_rekomendasi(katalog)
    if len(daftar_rekomendasi) == 0:
        print(f"\nBelum ada rekomendasi oli untuk {nama_kendaraan(kendaraan)}.")
        print("Silakan hubungi admin.")
        return

    tampilkan_rekomendasi(kendaraan, katalog, keterangan, persis, daftar_rekomendasi)


# ============================================================
# BAGIAN 3: PENGELOLAAN PRODUK OLI (ADMIN)
# ============================================================

def simpan_produk(data):
    with open(FILE_PRODUK, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=FIELD_PRODUK)
        writer.writeheader()
        writer.writerows(data)


def input_tidak_kosong(pertanyaan):
    """Mengulang pertanyaan sampai pengguna mengisi sesuatu."""
    while True:
        isi = input(pertanyaan).strip()
        if isi != "":
            return isi
        print("Isian tidak boleh kosong!")


def input_harga(pertanyaan):
    """Mengulang pertanyaan sampai harga berupa angka bulat."""
    while True:
        isi = input(pertanyaan).strip()
        if ke_angka(isi) is not None:
            return isi
        print("Harga harus berupa angka bulat (contoh: 50000)!")


def lihat_produk_oli():
    print("\n=== DATA PRODUK OLI ===")

    data = baca_csv(FILE_PRODUK)
    if len(data) == 0:
        print("Belum ada data produk oli.")
        return

    garis()
    print(f"{'ID':<4}{'Nama':<28}{'Merek':<10}{'Visk.':<8}{'Kemasan':<9}{'Harga'}")
    garis()
    for p in data:
        print(
            f"{p['id']:<4}{p['nama']:<28}{p['merek']:<10}"
            f"{p['viskositas']:<8}{p['volume_kemasan']:<9}{format_rupiah(p['harga'])}"
        )
    garis()


def tambah_produk_oli():
    print("\n=== TAMBAH PRODUK OLI ===")

    nama = input_tidak_kosong("Nama produk: ")
    merek = input_tidak_kosong("Merek: ")
    jenis = input_tidak_kosong("Jenis (mineral/semi-sintetik/sintetik): ")
    viskositas = input_tidak_kosong("Viskositas (contoh 10W-30): ")
    spesifikasi = input_tidak_kosong("Spesifikasi (contoh JASO MB): ")
    volume = input_tidak_kosong("Volume kemasan (contoh 0.8 L): ")
    harga = input_harga("Harga (angka saja): ")
    catatan = input("Catatan (boleh kosong): ").strip()

    data = baca_csv(FILE_PRODUK)

    # Cari id terbesar, lalu tambah 1
    id_baru = 1
    for p in data:
        id_lama = ke_angka(p['id'])
        if id_lama is not None and id_lama >= id_baru:
            id_baru = id_lama + 1

    data.append({
        'id': id_baru,
        'nama': nama,
        'merek': merek,
        'jenis': jenis,
        'viskositas': viskositas,
        'spesifikasi': spesifikasi,
        'volume_kemasan': volume,
        'harga': harga,
        'catatan': catatan
    })

    simpan_produk(data)
    print("\nProduk oli berhasil disimpan!")


def ubah_produk_oli():
    print("\n=== UBAH PRODUK OLI ===")

    data = baca_csv(FILE_PRODUK)
    if len(data) == 0:
        print("Belum ada data produk oli.")
        return

    lihat_produk_oli()
    id_dipilih = input("Masukkan ID produk yang ingin diubah: ").strip()

    produk = cari_produk(id_dipilih, data)
    if produk is None:
        print("ID produk tidak ditemukan!")
        return

    # Daftar bagian yang bisa diubah
    bagian = ['nama', 'merek', 'jenis', 'viskositas',
              'spesifikasi', 'volume_kemasan', 'harga', 'catatan']

    print(f"\nProduk: {produk['nama']}")
    nomor = 1
    for b in bagian:
        print(f"{nomor}. {b} (sekarang: {produk[b]})")
        nomor += 1
    print("0. Batal")

    pilihan = input("Bagian yang ingin diubah: ").strip()
    if not pilihan.isdigit():
        print("Input harus berupa angka!")
        return
    pilihan = int(pilihan)

    if pilihan == 0:
        return
    if pilihan < 1 or pilihan > len(bagian):
        print("Pilihan tidak ada!")
        return

    nama_bagian = bagian[pilihan - 1]

    if nama_bagian == 'harga':
        nilai_baru = input_harga("Harga baru (angka saja): ")
    elif nama_bagian == 'catatan':
        nilai_baru = input("Catatan baru: ").strip()
    else:
        nilai_baru = input_tidak_kosong(f"{nama_bagian} baru: ")

    produk[nama_bagian] = nilai_baru
    simpan_produk(data)
    print("\nProduk oli berhasil diubah!")


def menu_produk_oli():
    """Menu admin untuk mengelola produk oli, dipanggil dari Menu_Admin."""
    while True:
        print("\n=== KELOLA PRODUK OLI ===")
        print("1. Lihat produk oli")
        print("2. Tambah produk oli")
        print("3. Ubah produk oli")
        print("0. Kembali")

        pilihan = text(input("Pilih menu: "))

        if pilihan == "1":
            lihat_produk_oli()
        elif pilihan == "2":
            tambah_produk_oli()
        elif pilihan == "3":
            ubah_produk_oli()
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid!")