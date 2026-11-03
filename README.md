# OliCare

Sistem Pengingat Penggantian Oli Kendaraan berbasis Command-Line Interface (CLI).

OliCare membantu pengguna kendaraan memantau jadwal penggantian oli, mencatat kilometer, menyimpan riwayat perawatan, dan mendapatkan rekomendasi jenis oli melalui terminal.

Proyek mata kuliah Rekayasa Perangkat Lunak, Program Studi RPL, Universitas Pendidikan Indonesia Kampus Cibiru. Dokumen acuan: SKPL-OLICARE (Spesifikasi Kebutuhan Perangkat Lunak).

## Fitur Utama

- **Pengelolaan Data Kendaraan**: menambah dan menampilkan data kendaraan yang tersimpan.
- **Pencatatan Kilometer**: mencatat dan memperbarui kilometer kendaraan untuk memantau jarak tempuh.
- **Pengecekan Jadwal Penggantian Oli**: menampilkan status jadwal dan pengingat berdasarkan kilometer, waktu, dan interval penggantian.
- **Pencatatan Penggantian Oli**: menyimpan catatan penggantian oli (tanggal, kilometer, oli, bengkel, biaya, catatan).
- **Riwayat Penggantian Oli**: menampilkan kembali catatan penggantian oli per kendaraan.
- **Rekomendasi Jenis Oli**: memberi rekomendasi oli yang cocok berdasarkan data kendaraan dan katalog produk.

## Alur Penggunaan

1. Masukkan data kendaraan.
2. Perbarui kilometer kendaraan.
3. Cek status jadwal ganti oli. Sistem menampilkan jadwal berikutnya, atau pengingat jika sudah jatuh tempo.
4. Setelah ganti oli, catat penggantiannya. Jadwal berikutnya diperbarui otomatis.
5. Lihat riwayat atau minta rekomendasi oli kapan saja.

## Pengguna Sistem

- **Pengguna Kendaraan**: mengelola kendaraan, mencatat kilometer, mengecek jadwal, mencatat dan melihat riwayat penggantian oli, serta melihat rekomendasi oli.
- **Admin OliCare**: mengelola data pendukung seperti data produk oli dan katalog untuk rekomendasi.

## Teknologi

- Bahasa: Python
- Antarmuka: Command-Line Interface (menu berbasis teks, berbahasa Indonesia)
- Arsitektur: aplikasi mandiri tanpa integrasi layanan eksternal
- Penyimpanan: penyimpanan permanen lokal agar data tetap ada saat program dijalankan ulang

## Prasyarat

- Python 3.x
- Terminal atau Command Prompt (target utama: Windows)

## Instalasi dan Menjalankan

Sesuaikan nama folder dan file berikut dengan struktur repositori yang sebenarnya.

```bash
# Clone repositori
git clone <url-repositori>
cd olicare

# (Opsional) Buat virtual environment
python -m venv venv
venv\Scripts\activate

# (Jika ada) Pasang dependensi
pip install -r requirements.txt

# Jalankan program
python main.py
```

## Struktur Data

Data utama yang dikelola sistem (detail lengkap ada di Kamus Data pada dokumen SKPL):

- **Pengguna**: username, nama_lengkap, telepon, role, salt, password_hash, iterasi, aktif, dibuat_pada, wajib_ganti_password
- **Kendaraan**: id, username, pemilik, merek, tipe, jenis, tahun, nomor_polisi, km, km_ganti_terakhir, tanggal_ganti_terakhir, oli_terakhir, interval_km, interval_hari, id_katalog, km_diperbarui
- **Kilometer**: id, km, km_diperbarui
- **Jadwal Oli**: interval_km, interval_hari, target_km, sisa_km, target_tanggal, sisa_hari
- **Pengingat Oli**: level, status, jenis, alasan, interval_km, target_km, sisa_km, level_km, interval_hari, target_tanggal, sisa_hari, level_tanggal
- **Produk Oli**: id, nama, merek, jenis, viskositas, spesifikasi, volume_kemasan, harga, catatan
- **Katalog Kendaraan**: id, merek, model, tahun, kategori, kapasitas_oli, catatan
- **Rekomendasi Oli**: id, id_katalog, id_produk, nama_produk, merek, viskositas, standar, kecocokan, volume_penggantian, terverifikasi, catatan
- **Penggantian Oli**: id, id_kendaraan, username, tanggal, km, oli, bengkel, harga, catatan
- **Riwayat Penggantian Oli**: id, nama_kendaraan, id_kendaraan, username, tanggal, km, oli, bengkel, harga, catatan
- **Pengaturan Pengingat**: interval_km, interval_hari, ambang_km, ambang_hari

Status pengingat ditentukan dari dua sisi, yaitu jarak tempuh (kilometer) dan waktu (hari). Keduanya dibandingkan dengan interval dan ambang batas pada Pengaturan Pengingat.

## Ruang Lingkup dan Batasan

Termasuk dalam proyek: enam fitur utama di atas dalam bentuk aplikasi CLI berbasis Python.

Tidak termasuk dalam proyek:

- Aplikasi mobile (iOS/Android) dan web
- Pelacakan lokasi GPS dan pembacaan kilometer otomatis dari kendaraan
- Pemesanan produk oli, pembayaran daring, dan pemesanan layanan bengkel
- Integrasi dengan sistem atau layanan pihak ketiga

## Kebutuhan Nonfungsional

- **Kinerja**: respons wajar pada perangkat yang mampu menjalankan Python, tanpa server khusus.
- **Kemudahan penggunaan**: menu terstruktur, petunjuk jelas, pesan kesalahan mudah dipahami, dan seluruh antarmuka berbahasa Indonesia.
- **Keamanan**: validasi masukan, perlindungan dan keutuhan data, serta penanganan kesalahan agar data tidak rusak.
- **Kompatibilitas**: berjalan di terminal pada sistem operasi yang mendukung Python, misalnya Windows.
- **Ketersediaan**: data yang tersimpan tetap tersedia setelah program ditutup dan dibuka kembali.

## Metodologi dan Jadwal

Pengembangan memakai Agile dengan kerangka kerja Scrum (acuan: The Scrum Guide oleh Schwaber dan Sutherland).

Jadwal pengerjaan:

1. Analisis kebutuhan dan perancangan sistem: minggu 1 sampai 7
2. Persiapan pengembangan dan implementasi: minggu 8 sampai 9
3. Pengujian sistem: minggu 10 sampai 12
4. Evaluasi dan perbaikan: minggu 13
5. Penyelesaian dokumentasi: minggu 14 sampai 15

## Tim Pengembang

Kelompok 7:

- Moch Mahreza Jusufi Gunardi (Project Manager) - 2607484
- Siti Patimah Ajahra - 2603050
- Safa Sopian Ali Basya - 2601686
- Sabilal Rasya - 2611204

## Dokumentasi

Dokumentasi lengkap (kebutuhan fungsional, flowmap, DFD, dan kamus data) ada pada dokumen SKPL_KELOMPOK_7.docx.
