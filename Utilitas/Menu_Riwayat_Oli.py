# menus/Menu_Riwayat_Oli.py
# Tampilan fitur Riwayat Penggantian Oli.
# Data diambil dari services/riwayatGantiOli.py.

from services.riwayatGantiOli import riwayat_ganti_oli
from Utilitas.Helper_Riwayat import ke_angka, format_km, format_rupiah


def nama_kendaraan(kendaraan):
    """Contoh hasil: Honda Beat (D1234AB)"""
    return kendaraan["merek"] + " " + kendaraan["tipe"] + " (" + kendaraan["nomor_polisi"] + ")"


def pilih_kendaraan(hasil):
    """Meminta pengguna memilih kendaraan. Mengembalikan datanya, atau None kalau kembali."""
    # Kalau kendaraannya cuma satu, langsung dipakai
    if len(hasil) == 1:
        return hasil[0]

    print("\nPilih kendaraan:")
    nomor = 1
    for data in hasil:
        print(str(nomor) + ". " + nama_kendaraan(data["kendaraan"]))
        nomor += 1
    print("0. Kembali")

    while True:
        pilihan = input("Pilihan: ")
        if pilihan == "0":
            return None
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(hasil):
            return hasil[int(pilihan) - 1]
        print("Pilihan tidak valid, coba lagi.")


def tampilkan_tabel(riwayat):
    """Menampilkan daftar penggantian oli dalam bentuk tabel."""
    print("-" * 78)
    print("No   Tanggal      Kilometer    Oli                  Bengkel          Biaya")
    print("-" * 78)

    nomor = 1
    for catatan in riwayat:
        print(
            str(nomor).ljust(5)
            + catatan["tanggal"].ljust(13)
            + format_km(ke_angka(catatan["km"])).ljust(13)
            + catatan["oli"].ljust(21)
            + catatan["bengkel"].ljust(17)
            + format_rupiah(ke_angka(catatan["harga"]))
        )
        if catatan["catatan"] != "":
            print("     Catatan: " + catatan["catatan"])
        nomor += 1

    print("-" * 78)


def tampilkan_jadwal(jadwal):
    """Menampilkan jadwal penggantian oli berikutnya."""
    print("\nJadwal penggantian berikutnya:")

    if jadwal["target_km"] is None:
        print("  Target kilometer : -")
    else:
        print("  Target kilometer : " + format_km(jadwal["target_km"])
              + " (sisa " + format_km(jadwal["sisa_km"]) + ")")

    if jadwal["target_tanggal"] is None:
        print("  Target tanggal   : -")
    else:
        tanggal = jadwal["target_tanggal"].strftime("%d-%m-%Y")
        if jadwal["sisa_hari"] >= 0:
            keterangan = "sisa " + str(jadwal["sisa_hari"]) + " hari"
        else:
            keterangan = "terlambat " + str(-jadwal["sisa_hari"]) + " hari"
        print("  Target tanggal   : " + tanggal + " (" + keterangan + ")")


def tampilkan_riwayat_oli(username):
    """Fungsi utama yang dipanggil dari menu pengguna."""
    print("=" * 78)
    print("RIWAYAT PENGGANTIAN OLI".center(78))
    print("=" * 78)

    hasil = riwayat_ganti_oli(username)

    if len(hasil) == 0:
        print("\nAnda belum memiliki data kendaraan.")
        input("\nTekan Enter untuk kembali...")
        return

    data = pilih_kendaraan(hasil)
    if data is None:
        return

    kendaraan = data["kendaraan"]
    print("\nKendaraan : " + nama_kendaraan(kendaraan))
    print("Kilometer : " + format_km(ke_angka(kendaraan["km"])) + "\n")

    if data["jumlah"] == 0:
        print("Belum ada catatan penggantian oli untuk kendaraan ini.")
    else:
        tampilkan_tabel(data["riwayat"])
        print("Jumlah penggantian : " + str(data["jumlah"]) + " kali")
        print("Total biaya        : " + format_rupiah(data["total_biaya"]))

    tampilkan_jadwal(data["jadwal"])
    input("\nTekan Enter untuk kembali...")