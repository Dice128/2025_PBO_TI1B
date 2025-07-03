import tkinter as tk
from tkinter import messagebox, scrolledtext # Tambahkan messagebox
import textwrap
import io
import contextlib

class EncapsulationRoom:
    def __init__(self, frame, output_writer, on_success):
        self.frame = frame
        self.output_writer = output_writer
        self.on_success = on_success
        self.attempts = 0 # Tambahkan baris ini

    def start(self):
        """Membangun antarmuka pengguna untuk ruangan."""
        for widget in self.frame.winfo_children():
            widget.destroy()

        soal_teks = (
            "🔐 Tantangan Enkapsulasi (Encapsulation):\n\n"
            "1. Di dalam `__init__`, buat atribut **privat** bernama `__name`.\n"
            "2. Buat method `get_name()` yang mengembalikan (return) nilai `self.__name`.\n"
            "3. Buat method `set_name(new_name)` yang mengubah nilai `self.__name`.\n\n"
            "Tujuannya adalah menyembunyikan data agar tidak bisa diakses langsung."
        )

        label = tk.Label(
            self.frame,
            text=soal_teks,
            anchor="w",
            justify="left",
            wraplength=550,
            font=("Arial", 11)
        )
        label.pack(pady=10, padx=10, fill="x")

        template_code = textwrap.dedent("""
            class Person:
                def __init__(self):
                    # TODO: Buat atribut privat __name di sini
                    self.__name = "Default"

                # TODO: Buat method get_name() di sini
                

                # TODO: Buat method set_name(new_name) di sini
                

            # --- Kode Pengujian (Jangan Diubah) ---
            # Kode ini akan memeriksa jawabanmu
            try:
                p = Person()
                p.set_name('Alice')
                name_output = p.get_name()
                print(name_output)
            except Exception as e:
                print(f"Error pada kode pengujian: {e}")
        """)

        self.text_area = scrolledtext.ScrolledText(self.frame, height=15, font=("Courier New", 10), relief="solid", bd=1)
        self.text_area.insert("1.0", template_code)
        self.text_area.pack(padx=10, pady=5, fill="both", expand=True)

        run_button = tk.Button(
            self.frame,
            text="▶ Jalankan & Periksa Kode",
            command=self.evaluate,
            bg="#28a745",
            fg="white",
            font=("Arial", 10, "bold")
        )
        run_button.pack(pady=10)
        
        self.output_writer("--- Selamat Datang di Ruangan Enkapsulasi ---\n")

    def evaluate(self):
        """
        Mengevaluasi kode pengguna, memeriksa enkapsulasi, dan menampilkan popup.
        """
        self.attempts += 1 # Tambahkan baris ini
        user_code = self.text_area.get("1.0", "end")
        
        local_scope = {}
        try:
            # Langkah 1: Jalankan kode untuk mendapatkan definisi class
            exec(user_code, {}, local_scope)
            
            # Langkah 2: Periksa apakah class 'Person' ada
            if "Person" not in local_scope:
                messagebox.showerror("❌ Salah", "Class 'Person' tidak ditemukan. Pastikan nama class sudah benar.")
                return

            PersonClass = local_scope['Person']
            person_instance = PersonClass()

            # Langkah 3: Periksa apakah atributnya benar-benar privat
            # Atribut __name akan di-"mangle" menjadi _Person__name
            if not hasattr(person_instance, '_Person__name'):
                 messagebox.showerror("❌ Salah", "Atribut 'name' belum dibuat sebagai atribut privat.\nGunakan dua garis bawah di depan: __name.")
                 return

            # Langkah 4: Jalankan kode lengkap dengan pengujian dan tangkap outputnya
            code_output_io = io.StringIO()
            with contextlib.redirect_stdout(code_output_io):
                exec(user_code, {}, local_scope) # Eksekusi ulang untuk menangkap print
            
            actual_output = code_output_io.getvalue().strip()
            
            # Tulis output ke konsol utama
            self.output_writer(f"Output Kode Anda:\n---\n{actual_output}\n---\n")

            # Langkah 5: Bandingkan output
            expected_output = "Alice"
            if actual_output == expected_output:
                # --- PERUBAHAN 3: Hitung skor berdasarkan jumlah percobaan ---
                score = 0
                if self.attempts == 1:
                    score = 3
                elif self.attempts <= 3:
                    score = 2
                else:
                    score = 1
                
                bintang_str = "⭐" * score
                messagebox.showinfo("✅ Berhasil!", f"Kerja bagus! Kamu menyelesaikan ini dalam {self.attempts} percobaan dan meraih {score} bintang {bintang_str}!")
                self.on_success(score=score) # Kirim skor yang dihitung ke main.py
            else:
                messagebox.showerror("❌ Salah", f"Output salah atau method belum benar.\n\nDiharapkan: '{expected_output}'\nDiterima: '{actual_output}'\n\nPastikan get_name() dan set_name() berfungsi.")

        except Exception as e:
            # Jika terjadi error saat eksekusi
            error_message = f"Terjadi Error: {type(e).__name__}: {e}"
            messagebox.showerror("Error pada Kode", error_message)
            self.output_writer(f"{error_message}\n")

    # HAPUS: Metode ini tidak lagi diperlukan
    # def finish(self, score):
    #     self.on_success(score)