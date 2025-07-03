import tkinter as tk
from tkinter import messagebox, scrolledtext
import textwrap
import io
import contextlib

class ConstructorRoom:
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
            "🛠️ Tantangan Konstruktor (__init__):\n\n"
            "Konstruktor adalah method spesial yang dijalankan saat sebuah objek dibuat.\n\n"
            "Tugas Anda:\n"
            "1. Buat class `Player`.\n"
            "2. Buat method `__init__(self, name, level)` di dalamnya.\n"
            "3. Di dalam `__init__`, simpan `name` dan `level` sebagai atribut objek (misal: `self.name = name`).\n"
            "4. Buat method `status()` yang mencetak (print) string dalam format: 'Nama: [name], Level: [level]'."
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
            # Tulis class Player Anda di sini
            

            # --- Kode Pengujian (Jangan Diubah) ---
            try:
                # Membuat objek dengan nama 'Ryu' dan level 99
                player1 = Player("Ryu", 99)
                player1.status()
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
        
        self.output_writer("--- Selamat Datang di Ruangan Konstruktor ---\n")

    def evaluate(self):
        """Mengevaluasi pemahaman pengguna tentang __init__ dan atribut."""
        self.attempts += 1 # Tambahkan baris ini
        user_code = self.text_area.get("1.0", "end")
        code_output_io = io.StringIO()

        try:
            # Jalankan kode dan tangkap outputnya
            with contextlib.redirect_stdout(code_output_io):
                exec(user_code, {})
            
            actual_output = code_output_io.getvalue().strip()
            
            # Tampilkan output ke pengguna
            self.output_writer(f"Output Kode Anda:\n---\n{actual_output}\n---\n")

            # Periksa apakah hasilnya sesuai harapan
            expected_output = "Nama: Ryu, Level: 99"
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
                messagebox.showerror("❌ Salah", f"Output tidak sesuai harapan.\n\nDiharapkan: '{expected_output}'\nDiterima: '{actual_output}'\n\nPeriksa kembali method status() dan __init__ Anda.")

        except Exception as e:
            error_message = f"Terjadi Error: {type(e).__name__}: {e}"
            messagebox.showerror("Error pada Kode", error_message)
            self.output_writer(f"{error_message}\n")