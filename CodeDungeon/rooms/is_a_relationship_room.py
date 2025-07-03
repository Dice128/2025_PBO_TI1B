import tkinter as tk
from tkinter import messagebox, scrolledtext
import textwrap
import io
import contextlib

class CompositionRoom:
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
            "🧱 Tantangan Komposisi (Composition):\n\n"
            "Membangun objek kompleks dari objek-objek yang lebih sederhana.\n\n"
            "Tugas Anda:\n"
            "1. Buat class `Computer`.\n"
            "2. `__init__` dari `Computer` harus menerima dua **objek**: `cpu_object` dan `ram_object`.\n"
            "   Simpan kedua objek ini sebagai atribut (misal: `self.cpu = cpu_object`).\n"
            "3. Buat method `display_specs()`.\n"
            "   Method ini harus memanggil method `get_specs()` dari setiap komponennya\n"
            "   untuk menampilkan spesifikasi lengkap komputer."
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
            # Class Komponen (JANGAN DIUBAH)
            class CPU:
                def __init__(self, model, cores):
                    self.model = model
                    self.cores = cores
                
                def get_specs(self):
                    return f"CPU: {self.model} ({self.cores} cores)"

            class RAM:
                def __init__(self, size_gb):
                    self.size_gb = size_gb
                
                def get_specs(self):
                    return f"RAM: {self.size_gb}GB"

            # TODO: Buat class Computer yang MENGGUNAKAN class di atas
            

            # --- Kode Pengujian (Jangan Diubah) ---
            try:
                # 1. Buat objek-objek komponennya dulu
                cpu_intel = CPU("Intel i9", 16)
                ram_corsair = RAM(32)

                # 2. "Rakit" komputer dengan memberikan objek komponen
                my_pc = Computer(cpu_intel, ram_corsair)
                my_pc.display_specs()
            except Exception as e:
                print(f"Error pada kode pengujian: {e}")
        """)

        self.text_area = scrolledtext.ScrolledText(self.frame, height=18, font=("Courier New", 10), relief="solid", bd=1)
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
        
        self.output_writer("--- Selamat Datang di Ruangan Composition ---\n")

    def evaluate(self):
        self.attempts += 1 # Tambahkan baris ini
        """Mengevaluasi pemahaman pengguna tentang komposisi objek."""
        user_code = self.text_area.get("1.0", "end")
        code_output_io = io.StringIO()

        try:
            with contextlib.redirect_stdout(code_output_io):
                exec(user_code, {})
            
            output_lines = code_output_io.getvalue().strip().splitlines()
            actual_output_text = "\n".join(output_lines)
            
            self.output_writer(f"Output Kode Anda:\n---\n{actual_output_text}\n---\n")

            expected_output = [
                "Computer Specifications:",
                "- CPU: Intel i9 (16 cores)",
                "- RAM: 32GB"
            ]

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
                messagebox.showerror("❌ Salah", f"Output tidak sesuai harapan.\n\nDiharapkan:\n{'\n'.join(expected_output)}\n\nDiterima:\n{actual_output_text}\n\nPastikan Anda memanggil method get_specs() dari komponen.")

        except Exception as e:
            error_message = f"Terjadi Error: {type(e).__name__}: {e}"
            messagebox.showerror("Error pada Kode", error_message)
            self.output_writer(f"{error_message}\n")