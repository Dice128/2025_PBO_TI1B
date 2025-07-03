# setup_db_pengeluaran.py

import sqlite3
import os

from konfigurasi import DB_PATH 

def setup_database():
    print(f"Memeriksa/membuat database di: {DB_PATH}")
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        sql_create_table = """
            CREATE TABLE pengeluaran (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                kategori TEXT,
                jumlah REAL,
                keterangan TEXT
            );"""
        print(" Membuat tabel 'transaksi' (jika belum ada)...")
        cursor.execute(sql_create_table)
        conn.commit(); print(" -> Tabel 'ttransaksi' siap.")
        return True
    except sqlite3.Error as e:
        print(f" -> Error SQLite saat setup: {e}");
        return False
    finally:
        if conn:
            conn.close();
            print(" -> Koneksi DB setup ditutup.")

if __name__ == "__main__":
    print("--- Memulai Setup Database Pengeluaran ---")
    if setup_database():
        print(f"\nSetup database '{os.path.basename(DB_PATH)}' selesai'")
    else:
        print(f"\nSetup database GAGAL.")
    print("--- Selesai Setup Database Pengeluaran ---")