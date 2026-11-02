import os
import csv

direktori_sekarang = os.path.dirname(__file__)
file_csv = os.path.join(direktori_sekarang,'..','data','users.csv')


def cek_akun(username):
	with open(file_csv,'r') as file:
		reader = csv.DictReader(file)
		for user in reader:
			if user['username'] == username:
				return user
	return None
	
