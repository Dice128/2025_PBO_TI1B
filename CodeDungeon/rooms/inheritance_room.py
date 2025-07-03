import tkinter as tk
from tkinter import messagebox, scrolledtext
import textwrap
import io
import contextlib

class InheritanceRoom:
    def __init__(self, frame, output_writer, on_success):
        self.frame = frame
        self.output_writer = output_writer
        self.on_success = on_success
        # --- PERUBAHAN 1: Tambahkan penghitung percobaan ---
        self.attempts = 0

    def start(self):
        """Membangun antarmuka pengguna untuk ruangan."""
        for widget in self.frame.winfo_children():
            widget.destroy()

        soal_teks = (
            "🧬 Tantangan Pewarisan (Inheritance):\n\n"
            "1. Buat class `Dog` yang mewarisi (inherits) dari class `Animal`.\n"
            "2. Override (timpa) method `sound()` pada class `Dog`.\n"
            "3. Method `sound()` pada `Dog` harus mencetak (print) string 'Woof!'."
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
            class Animal:
                def sound(self):
                    print("Some generic animal sound")

            # Tulis class `Dog` Anda di bawah ini
            

            # --- Kode Pengujian (Jangan Diubah) ---
            try:
                my_dog = Dog()
                my_dog.sound()
            except NameError:
                print("Class 'Dog' belum didefinisikan.")
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
        run_button.pack(pady=15)
        
        self.output_writer("--- Selamat Datang di Ruangan Pewarisan ---\n")

    def evaluate(self):
        """
        Mengevaluasi kode pengguna, memeriksa hasilnya, dan memberikan skor bintang.
        """
        # --- PERUBAHAN 2: Tambah 1 ke penghitung setiap kali tombol ditekan ---
        self.attempts += 1
        
        user_code = self.text_area.get("1.0", "end")
        code_output_io = io.StringIO()

        try:
            with contextlib.redirect_stdout(code_output_io):
                exec(user_code)
            
            actual_output = code_output_io.getvalue().strip()
            self.output_writer(f"Percobaan #{self.attempts}\nOutput Kode Anda:\n---\n{actual_output}\n---\n")

            if actual_output == "Woof!":
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
                messagebox.showerror("❌ Salah", f"Output salah.\n\nDiharapkan: 'Woof!'\nDiterima: '{actual_output}'\n\nCoba lagi!")

        except Exception as e:
            error_message = f"Terjadi Error: {type(e).__name__}: {e}"
            messagebox.showerror("Error pada Kode", error_message)
            self.output_writer(f"Percobaan #{self.attempts}\n{error_message}\n")