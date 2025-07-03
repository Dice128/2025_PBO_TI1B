import tkinter as tk
from tkinter import messagebox, scrolledtext
import textwrap
import io
import contextlib

class AdvancedInheritanceRoom:
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
            "🚀 Pewarisan Lanjutan (super()):\n\n"
            "Terkadang, kita tidak ingin mengganti total method parent, tapi hanya ingin **menambahkannya**.\n"
            "Gunakan `super()` untuk memanggil method dari parent class.\n\n"
            "Tugas Anda:\n"
            "1. Buat class `Manager` yang mewarisi `Employee`.\n"
            "2. Di `__init__` `Manager`, terima `name`, `salary`, dan `department`.\n"
            "   - Panggil `super().__init__(name, salary)` untuk menyerahkan tugas ke parent.\n"
            "   - Atur `self.department` secara manual.\n"
            "3. Override method `display()`:\n"
            "   - Panggil `super().display()` untuk mencetak info nama dan gaji.\n"
            "   - Kemudian, `print()` informasi department secara terpisah."
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
            # Class Parent (JANGAN DIUBAH)
            class Employee:
                def __init__(self, name, salary):
                    self.name = name
                    self.salary = salary

                def display(self):
                    print(f"Name: {self.name}, Salary: {self.salary}")

            # TODO: Buat class Manager yang mewarisi Employee di sini
            

            # --- Kode Pengujian (Jangan Diubah) ---
            try:
                manager1 = Manager("Cynthia", 90000, "Engineering")
                manager1.display()
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
        
        self.output_writer("--- Selamat Datang di Ruangan Advanced Inheritance ---\n")

    def evaluate(self):
        """Mengevaluasi penggunaan super() dalam inheritance."""
        self.attempts += 1 # Tambahkan baris ini
        user_code = self.text_area.get("1.0", "end")
        code_output_io = io.StringIO()

        try:
            with contextlib.redirect_stdout(code_output_io):
                exec(user_code, {})
            
            output_lines = code_output_io.getvalue().strip().splitlines()
            actual_output_text = "\n".join(output_lines)
            
            self.output_writer(f"Output Kode Anda:\n---\n{actual_output_text}\n---\n")

            expected_output = [
                "Name: Cynthia, Salary: 90000",
                "Department: Engineering"
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
                messagebox.showerror("❌ Salah", f"Output tidak sesuai harapan.\n\nDiharapkan:\n{'\n'.join(expected_output)}\n\nDiterima:\n{actual_output_text}\n\nPastikan Anda memanggil super() di __init__ dan display().")

        except Exception as e:
            error_message = f"Terjadi Error: {type(e).__name__}: {e}"
            messagebox.showerror("Error pada Kode", error_message)
            self.output_writer(f"{error_message}\n")