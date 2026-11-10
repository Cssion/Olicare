"""
menus/Menu_Riwayat_Oli.py

Tampilan fitur Riwayat Penggantian Oli (print/input).
Seluruh logika data diambil dari services/riwayatGantiOli.py.

Pemakaian di Menu_User.py:
    from menus.Menu_Riwayat_Oli import tampilkan_riwayat_oli
    tampilkan_riwayat_oli(username)
"""

from services.riwayatGantiOli import riwayat_ganti_oli
from Utilitas.Helper_Riwayat import format_km, format_rupiah, format_tanggal


def garis(panjang=78, simbol="="):
    print(simbol * panjang)


def tampilkan_judul(teks):
    """Pakai Utilitas.Judul bila tersedia; jika tidak, cetak judul sederhana."""
    try:
        from Utilitas import Judul  # type: ignore

        for nama in ("tampilkan_judul", "judul", "Judul", "tampil_judul"):
            fungsi = getattr(Judul, nama, None)
            if callable(fungsi):
                fungsi(teks)
                return
    except Exception:
        pass
    garis()
    print(teks.center(78))
    garis()


def nama_kendaraan(k):
    nama = " ".join(x for x in (k.get("merek"), k.get("tipe")) if x).strip()
    plat = k.get("nomor_polisi")
    return "{} ({})".format(nama or "Kendaraan", plat) if plat else (nama or "Kendaraan")


def pilih_kendaraan(daftar):
    """Minta pengguna memilih kendaraan. Kembalikan dict kendaraan atau None."""
    if len(daftar) == 1:
        return daftar[0]

    print("\nPilih kendaraan:")
    for i, k in enumerate(daftar, start=1):
        print("  {}. {}".format(i, nama_kendaraan(k)))
    print("  0. Kembali")

    while True:
        pilihan = input("Pilihan: ").strip()
        if pilihan == "0":
            return None
        if pilihan.isdigit() and 1 <= int(pilihan) <= len(daftar):
            return daftar[int(pilihan) - 1]
        print("Pilihan tidak valid, coba lagi.")


def tampilkan_tabel(riwayat):
    kolom = "{:<4} {:<12} {:<12} {:<20} {:<16} {:<14}"
    print(kolom.format("No", "Tanggal", "Kilometer", "Oli", "Bengkel", "Biaya"))
    garis(78, "-")
    for i, r in enumerate(riwayat, start=1):
        print(
            kolom.format(
                i,
                format_tanggal(r.get("tanggal")),
                format_km(r.get("km")),
                (r.get("oli") or "-")[:20],
                (r.get("bengkel") or "-")[:16],
                format_rupiah(r.get("harga")),
            )
        )
        catatan = (r.get("catatan") or "").strip()
        if catatan:
            print("     Catatan: {}".format(catatan))
    garis(78, "-")


def tampilkan_jadwal_berikutnya(jadwal):
    print("\nJadwal penggantian berikutnya:")

    if jadwal["target_km"] is not None:
        baris = "  Target kilometer : {}".format(format_km(jadwal["target_km"]))
        if jadwal["sisa_km"] is not None:
            baris += " (sisa {})".format(format_km(jadwal["sisa_km"]))
        print(baris)
    else:
        print("  Target kilometer : -")

    if jadwal["target_tanggal"] is not None:
        sisa = jadwal["sisa_hari"]
        ket = "sisa {} hari".format(sisa) if sisa >= 0 else "terlambat {} hari".format(-sisa)
        print("  Target tanggal   : {} ({})".format(jadwal["target_tanggal"].strftime("%d-%m-%Y"), ket))
    else:
        print("  Target tanggal   : -")


def tampilkan_riwayat_oli(username):
    """Entry point tampilan Riwayat Penggantian Oli untuk pengguna yang login."""
    tampilkan_judul("RIWAYAT PENGGANTIAN OLI")

    hasil = riwayat_ganti_oli(username)
    if not hasil:
        print("\nAnda belum memiliki data kendaraan.")
        print("Tambahkan kendaraan terlebih dahulu melalui menu Kelola Data Kendaraan.")
        input("\nTekan Enter untuk kembali...")
        return

    kendaraan = pilih_kendaraan([h["kendaraan"] for h in hasil])
    if kendaraan is None:
        return
    data = next(h for h in hasil if h["kendaraan"] is kendaraan)

    print("\nKendaraan : {}".format(nama_kendaraan(kendaraan)))
    print("Kilometer : {}\n".format(format_km(kendaraan.get("km"))))

    if not data["riwayat"]:
        print("Belum ada catatan penggantian oli untuk kendaraan ini.")
        print("Catat penggantian oli melalui menu Catat Penggantian Oli.")
    else:
        tampilkan_tabel(data["riwayat"])
        print("Jumlah penggantian : {} kali".format(data["jumlah"]))
        print("Total biaya        : {}".format(format_rupiah(data["total_biaya"])))

    tampilkan_jadwal_berikutnya(data["jadwal"])
    input("\nTekan Enter untuk kembali...")