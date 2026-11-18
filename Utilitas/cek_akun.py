import os
import csv

direktori_sekarang = os.path.dirname(__file__)
file_csv = os.path.join(direktori_sekarang, '..', 'data', 'akun.csv')


def cek_akun(username):
    with open(file_csv, 'r', newline='', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file, skipinitialspace=True)

        for user in reader:
            if user['username'].strip().lower() == username.strip().lower():
                user['password'] = user['password'].strip()
                return user

    return None