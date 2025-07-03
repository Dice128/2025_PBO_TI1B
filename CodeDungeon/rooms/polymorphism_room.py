import tkinter as tk
from tkinter import messagebox, scrolledtext # Tambahkan messagebox
import textwrap
import io
import contextlib

class PolymorphismRoom:
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
            "🎭 Tantangan Polimorfisme (Polymorphism):\n\n"
            "Objek yang berbeda dapat merespons satu perintah yang sama dengan cara yang berbeda.\n\n"
            "1. Buat dua class: `Cat` dan `Dog`.\n"
            "2. Keduanya harus memiliki method `speak()`.\n"
            "3. Method `speak()` pada `Cat` harus mencetak (print) string **'Meow'**.\n"
            "4. Method `speak()` pada `Dog` harus mencetak (print) string **'Woof'**."
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
            # Tulis class Cat di sini
            
            
            # Tulis class Dog di sini
            

            # --- Kode Pengujian (Jangan Diubah) ---
            # Kode ini akan memeriksa jawabanmu
            try:
                animals = [Cat(), Dog()]
                for animal in animals:
                    animal.speak()
            except NameError:
                print("Pastikan class 'Cat' dan 'Dog' sudah dibuat.")
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
        
        self.output_writer("--- Selamat Datang di Ruangan Polimorfisme ---\n")

    def evaluate(self):
        """
        Mengevaluasi kode pengguna, memeriksa polimorfisme, dan menampilkan popup.
        """
        self.attempts += 1 # Tambahkan baris ini
        user_code = self.text_area.get("1.0", "end")
        code_output_io = io.StringIO()

        try:
            # Jalankan kode lengkap dengan pengujian dan tangkap outputnya
            with contextlib.redirect_stdout(code_output_io):
                exec(user_code, {})
            
            # Ambil hasil output dan pisahkan per baris
            # .strip() menghapus spasi/baris kosong di awal/akhir
            # .splitlines() memecah string menjadi list berdasarkan baris baru
            output_lines = code_output_io.getvalue().strip().splitlines()
            
            # Gabungkan kembali untuk ditampilkan di output box
            actual_output_text = "\n".join(output_lines)
            self.output_writer(f"Output Kode Anda:\n---\n{actual_output_text}\n---\n")

            # Periksa apakah hasilnya sesuai harapan
            expected_output = ['Meow', 'Woof']
            if output_lines == expected_output:
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
                messagebox.showerror("❌ Salah", f"Output tidak sesuai harapan.\n\nDiharapkan:\nMeow\nWoof\n\nDiterima:\n{actual_output_text}")

        except Exception as e:
            # Jika terjadi error saat eksekusi (misal: SyntaxError)
            error_message = f"Terjadi Error: {type(e).__name__}: {e}"
            messagebox.showerror("Error pada Kode", error_message)
            self.output_writer(f"{error_message}\n")

    # HAPUS: Metode ini tidak lagi diperlukan karena logikanya sudah pindah ke evaluate()
    # def finish(self, score):
    #     self.on_success(score)