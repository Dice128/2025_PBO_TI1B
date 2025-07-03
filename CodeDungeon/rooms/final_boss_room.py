import tkinter as tk
from tkinter import messagebox, scrolledtext # Tambahkan messagebox
import textwrap
import io
import contextlib

class FinalBossRoom:
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
            "💀 FINAL BOSS ROOM 💀\n\n"
            "Gabungkan semua konsep! Buatlah struktur kelas berikut:\n\n"
            "1. **Class `Character`** (Enkapsulasi):\n"
            "   - `__init__(self, name)` yang menyimpan nama ke atribut **privat** `__name`.\n"
            "   - Method `get_name()` yang mengembalikan (return) nama tersebut.\n\n"
            "2. **Class `Hero`** (Pewarisan):\n"
            "   - Mewarisi (inherits) dari `Character`.\n"
            "   - Method `speak()` yang mengembalikan (return) string 'I will save the world!'.\n\n"
            "3. **Class `Villain`** (Polimorfisme):\n"
            "   - Juga mewarisi dari `Character`.\n"
            "   - Method `speak()` yang mengembalikan (return) string 'I will destroy it!'."
        )

        label = tk.Label(self.frame, text=soal_teks, anchor="w", justify="left", wraplength=550, font=("Arial", 11))
        label.pack(pady=10, padx=10, fill="x")

        template_code = textwrap.dedent("""
            # Tulis semua class di sini: Character, Hero, dan Villain
            

            # --- Kode Pengujian (Jangan Diubah) ---
            # Kode ini akan memeriksa semua konsep OOP yang kamu buat
            try:
                # Test Hero
                hero = Hero('Ray')
                print(f"{hero.get_name()} says: {hero.speak()}")
                
                # Test Villain
                villain = Villain('Zorg')
                print(f"{villain.get_name()} says: {villain.speak()}")

            except Exception as e:
                print(f"Error pada kode pengujian: {e}")
        """)

        self.text_area = scrolledtext.ScrolledText(self.frame, height=18, font=("Courier New", 10), relief="solid", bd=1)
        self.text_area.insert("1.0", template_code)
        self.text_area.pack(padx=10, pady=5, fill="both", expand=True)

        run_button = tk.Button(
            self.frame,
            text="⚔ Kalahkan Final Boss ⚔",
            command=self.evaluate,
            bg="#d9534f",
            fg="white",
            font=("Arial", 10, "bold")
        )
        run_button.pack(pady=10)

        self.output_writer("--- Ini adalah tantangan terakhir! Buktikan kamu adalah Master OOP! ---\n")

    def evaluate(self):
        self.attempts += 1 # Tambahkan baris ini
        """Mengevaluasi semua konsep OOP: Enkapsulasi, Pewarisan, dan Polimorfisme."""
        user_code = self.text_area.get("1.0", "end")
        local_scope = {}

        try:
            # Langkah 1: Jalankan kode untuk mendefinisikan class
            exec(user_code, {}, local_scope)

            # Langkah 2: Validasi keberadaan semua class
            required_classes = ["Character", "Hero", "Villain"]
            for cls_name in required_classes:
                if cls_name not in local_scope:
                    messagebox.showerror("❌ Class Kurang", f"Class '{cls_name}' tidak ditemukan. Pastikan semua class sudah dibuat.")
                    return

            Character, Hero, Villain = local_scope['Character'], local_scope['Hero'], local_scope['Villain']

            # Langkah 3: Validasi Enkapsulasi di Character
            try:
                char_instance = Character("test")
                if not hasattr(char_instance, '_Character__name'):
                    messagebox.showerror("❌ Enkapsulasi Gagal", "Atribut 'name' di class Character belum privat. Gunakan __name.")
                    return
            except TypeError:
                 messagebox.showerror("❌ Init Error", "Pastikan __init__ di class Character menerima parameter 'name'.")
                 return


            # Langkah 4: Validasi Pewarisan
            if not issubclass(Hero, Character):
                messagebox.showerror("❌ Pewarisan Gagal", "Class 'Hero' belum mewarisi dari class 'Character'.")
                return
            if not issubclass(Villain, Character):
                messagebox.showerror("❌ Pewarisan Gagal", "Class 'Villain' belum mewarisi dari class 'Character'.")
                return

            # Langkah 5: Jika semua validasi dasar lolos, uji output akhir (Polimorfisme)
            code_output_io = io.StringIO()
            with contextlib.redirect_stdout(code_output_io):
                exec(user_code, {}) # Eksekusi ulang untuk menangkap print

            output_lines = code_output_io.getvalue().strip().splitlines()
            actual_output_text = "\n".join(output_lines)
            self.output_writer(f"Output Kode Anda:\n---\n{actual_output_text}\n---\n")

            expected_output = [
                "Ray says: I will save the world!",
                "Zorg says: I will destroy it!"
            ]

            if output_lines == expected_output:
                messagebox.showinfo("")
                self.on_success(score=3)
                 # --- PERUBAHAN 3: Hitung skor berdasarkan jumlah percobaan ---
                score = 0
                if self.attempts == 1:
                    score = 3
                elif self.attempts <= 3:
                    score = 2
                else:
                    score = 1
                
                bintang_str = "⭐" * score
                messagebox.showinfo("🏆 SELAMAT!", f"Kamu telah mengalahkan Final Boss dan membuktikan penguasaanmu atas OOP! dengan bintang {bintang_str}!")
                self.on_success(score=score) # Kirim skor yang dihitung ke main.py
            else:
                messagebox.showerror("❌ Sedikit Lagi!", f"Struktur class sudah benar, tapi output akhir salah.\n\nDiharapkan:\n{'\n'.join(expected_output)}\n\nDiterima:\n{actual_output_text}")

        except Exception as e:
            error_message = f"Terjadi Error: {type(e).__name__}: {e}"
            messagebox.showerror("Error pada Kode", error_message)
            self.output_writer(f"{error_message}\n")

    # HAPUS: Metode ini tidak lagi diperlukan
    # def finish(self, score):
    #     self.on_success(score)