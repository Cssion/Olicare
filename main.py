# main.py
# FUNGSI : Pintu masuk program. Jalankan dengan: python main.py
# ISI    : Menyiapkan storage, membuat semua service, lalu membuka MainMenu.
# CATATAN: Jaga file ini tetap pendek. Logika tidak ditulis di sini.

from menus.akun import login, registrasi
from Utilitas.Judul import Judul

def main():
	Judul("OILCARE v1.0")
	while True:
		print("Silahkan Login / registrasi Terlebih Dulu")
		print("1. Login")
		print("2. Registrasi")
		print("3. Keluar")
		userInput = int(input("Masukan Pilihan Anda 1/2/3 (Default: 3) : "))


		if userInput == 1:
			login()
			break;
		elif userInput == 2:
			registrasi()
			break;
		elif userInput == 3:
			print("Terima Kasih Sudah Menggunakan OliCare")
			break






	








if __name__ == "__main__":
	main()
