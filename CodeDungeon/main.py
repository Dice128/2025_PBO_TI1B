import tkinter as tk
from tkinter import messagebox, scrolledtext
import os
import json
from PIL import Image, ImageTk

# (Impor ruangan Anda tetap sama)
from rooms.inheritance_room import InheritanceRoom
from rooms.encapsulation_room import EncapsulationRoom
from rooms.polymorphism_room import PolymorphismRoom
from rooms.constructor_room import ConstructorRoom
from rooms.advanced_inheritance_room import AdvancedInheritanceRoom
from rooms.is_a_relationship_room import CompositionRoom
from rooms.final_boss_room import FinalBossRoom

DATA_FILE = "data/progress.json"
ASSET_DIR = "assets"

class CodeDungeonApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Code Dungeon: Learn OOP Adventure")
        self.master.state("zoomed")
        self.master.configure(bg="#2C3E50")

        self.room_status = {
            "Inheritance": {"status": "unlocked", "score": 0},
            "Encapsulation": {"status": "locked", "score": 0},
            "Polymorphism": {"status": "locked", "score": 0},
            "Constructor": {"status": "locked", "score": 0},
            "Advanced Inheritance": {"status": "locked", "score": 0},
            "Composition": {"status": "locked", "score": 0},
            "Final Boss": {"status": "locked", "score": 0},
        }

        self.room_icons = {}
        self.title_icon_ref = None

        os.makedirs("data", exist_ok=True)
        os.makedirs("assets", exist_ok=True)
        self.load_progress()
        self.create_widgets()

    def load_icon(self, name, size=(50, 50)):
        try:
            path = os.path.join(ASSET_DIR, name)
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except Exception as e:
            print(f"Error loading icon {name}: {e}")
            return None

    def create_widgets(self):
        for widget in self.master.winfo_children():
            widget.destroy()

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(1, weight=1)

        self.left_frame = tk.Frame(self.master, bg="#34495E", bd=5, relief="raised")
        self.left_frame.grid(row=0, column=0, padx=15, pady=15, sticky="ns")

        self.right_frame = tk.Frame(self.master, bg="#ECF0F1", bd=5, relief="sunken")
        self.right_frame.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        title_frame = tk.Frame(self.left_frame, bg="#34495E")
        title_frame.pack(pady=20, fill="x")
        self.title_icon_ref = self.load_icon("dungeon_map.png", size=(70, 70))
        if self.title_icon_ref:
            tk.Label(title_frame, image=self.title_icon_ref, bg="#34495E").pack(side="left", padx=5)
        tk.Label(title_frame, text="Code Dungeon Map", font=("Impact", 18, "bold"), fg="#ECF0F1", bg="#34495E").pack(side="left", padx=10)

        self.room_button_font = ("Impact", 11, "bold")
        
        map_container = tk.Frame(self.left_frame, bg="#34495E")
        map_container.pack(fill="both", expand=True)

        canvas = tk.Canvas(map_container, bg="#34495E", highlightthickness=0)
        scrollbar = tk.Scrollbar(map_container, orient="vertical", command=canvas.yview)
        
        scrollable_frame = tk.Frame(canvas, bg="#34495E")

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        def _on_mousewheel(event):
            if event.num == 5 or event.delta == -120:
                canvas.yview_scroll(1, "units")
            if event.num == 4 or event.delta == 120:
                canvas.yview_scroll(-1, "units")

        self.master.bind_all("<MouseWheel>", _on_mousewheel)
        self.master.bind_all("<Button-4>", _on_mousewheel)
        self.master.bind_all("<Button-5>", _on_mousewheel)

        room_defs = [
            ("Inheritance", self.load_inheritance_room, "inheritance_icon.png"),
            ("Encapsulation", self.load_encapsulation_room, "encapsulation_icon.png"),
            ("Polymorphism", self.load_polymorphism_room, "polymorphism_icon.png"),
            ("Constructor", self.load_constructor_room, "constructor_icon.png"),
            ("Advanced Inheritance", self.load_advanced_inheritance_room, "super_icon.png"),
            ("Composition", self.load_composition_room, "composition_icon.png"),
            ("Final Boss", self.load_final_boss_room, "boss_icon.png")
        ]
        
        normal_rooms = [room for room in room_defs if room[0] != "Final Boss"]
        boss_room_data = next((room for room in room_defs if room[0] == "Final Boss"), None)

        scrollable_frame.grid_columnconfigure(0, weight=1)
        scrollable_frame.grid_columnconfigure(1, weight=1)

        for i, (room_name, action, icon_name) in enumerate(normal_rooms):
            row = i // 2
            col = i % 2
            
            if room_name in self.room_status:
                status = self.room_status[room_name]["status"]
                score = self.room_status[room_name]["score"]
                stars = "⭐" * score + "☆" * (3 - score)

                room_icon = self.load_icon(icon_name, size=(40, 40))
                self.room_icons[room_name] = room_icon

                btn = tk.Button(
                    scrollable_frame,
                    text=f"{room_name}\n{stars}",
                    image=self.room_icons[room_name],
                    compound="top", width=150, height=100,
                    state=tk.NORMAL if status != "locked" else tk.DISABLED,
                    bg="#28A745" if status == "cleared" else ("#FFC107" if status == "unlocked" else "#6C757D"),
                    fg="white", font=self.room_button_font,
                    command=action if status != "locked" else lambda rn=room_name: self.locked_message(rn),
                    bd=3, relief="raised"
                )
                btn.grid(row=row, column=col, padx=10, pady=8, sticky="ew")

        if boss_room_data:
            room_name, action, icon_name = boss_room_data
            boss_row = (len(normal_rooms) + 1) // 2
            
            if room_name in self.room_status:
                status = self.room_status[room_name]["status"]
                score = self.room_status[room_name]["score"]
                stars = "⭐" * score + "☆" * (3 - score)

                room_icon = self.load_icon(icon_name, size=(40, 40))
                self.room_icons[room_name] = room_icon
                
                btn_boss = tk.Button(
                    scrollable_frame,
                    text=f"{room_name}\n{stars}",
                    image=self.room_icons[room_name],
                    compound="top", width=320, height=100,
                    state=tk.NORMAL if status != "locked" else tk.DISABLED,
                    bg="#d9534f" if status != "cleared" else "#28A745",
                    fg="white", font=self.room_button_font,
                    command=action if status != "locked" else lambda rn=room_name: self.locked_message(rn),
                    bd=3, relief="raised"
                )
                btn_boss.grid(row=boss_row, column=0, columnspan=2, padx=10, pady=15)

        self.output_box = scrolledtext.ScrolledText(self.master, height=8, state="disabled", bg="#1C2833", fg="#EAECEE", font=("Consolas", 10), bd=3, relief="sunken")
        self.output_box.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="we")
        self.master.grid_rowconfigure(1, weight=0)
        self.write_to_output("Welcome to Code Dungeon! Select a room to start your adventure.\n")
    
    # --- PERUBAHAN 1: Buat fungsi baru untuk membersihkan output ---
    def clear_output_box(self):
        """Membersihkan semua teks dari output box."""
        self.output_box.config(state="normal")
        self.output_box.delete("1.0", tk.END)
        self.output_box.config(state="disabled")

    def write_to_output(self, message):
        self.output_box.config(state="normal")
        self.output_box.insert(tk.END, message)
        self.output_box.see(tk.END)
        self.output_box.config(state="disabled")

    def clear_right_frame(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()

    def locked_message(self, room_name):
        messagebox.showwarning("Dungeon Locked!", f"The '{room_name}' dungeon is still locked! You must clear the previous rooms first.")
        self.write_to_output(f"Attempted to enter locked room: {room_name}\n")

    # --- PERUBAHAN 2: Panggil clear_output_box() di setiap fungsi load ---
    def load_inheritance_room(self):
        self.clear_output_box() # Hapus output lama
        self.clear_right_frame()
        room = InheritanceRoom(self.right_frame, self.write_to_output, lambda score: self.on_success("Inheritance", score))
        room.start()
        self.write_to_output("\n--- Entering Inheritance Room ---\n")

    def load_encapsulation_room(self):
        self.clear_output_box() # Hapus output lama
        self.clear_right_frame()
        room = EncapsulationRoom(self.right_frame, self.write_to_output, lambda score: self.on_success("Encapsulation", score))
        room.start()
        self.write_to_output("\n--- Entering Encapsulation Room ---\n")

    def load_polymorphism_room(self):
        self.clear_output_box() # Hapus output lama
        self.clear_right_frame()
        room = PolymorphismRoom(self.right_frame, self.write_to_output, lambda score: self.on_success("Polymorphism", score))
        room.start()
        self.write_to_output("\n--- Entering Polymorphism Room ---\n")
    
    def load_constructor_room(self):
        self.clear_output_box() # Hapus output lama
        self.clear_right_frame()
        room = ConstructorRoom(self.right_frame, self.write_to_output, lambda score: self.on_success("Constructor", score))
        room.start()
        self.write_to_output("\n--- Entering Constructor Room ---\n")

    def load_advanced_inheritance_room(self):
        self.clear_output_box() # Hapus output lama
        self.clear_right_frame()
        room = AdvancedInheritanceRoom(self.right_frame, self.write_to_output, lambda score: self.on_success("Advanced Inheritance", score))
        room.start()
        self.write_to_output("\n--- Entering Advanced Inheritance Room ---\n")

    def load_composition_room(self):
        self.clear_output_box() # Hapus output lama
        self.clear_right_frame()
        room = CompositionRoom(self.right_frame, self.write_to_output, lambda score: self.on_success("Composition", score))
        room.start()
        self.write_to_output("\n--- Entering Composition Room ---\n")

    def load_final_boss_room(self):
        self.clear_output_box() # Hapus output lama
        self.clear_right_frame()
        room = FinalBossRoom(self.right_frame, self.write_to_output, lambda score: self.on_success("Final Boss", score))
        room.start()
        self.write_to_output("\n--- Entering Final Boss Room ---\n")

    def on_success(self, room_name, score):
        if room_name not in self.room_status: return

        prev_score = self.room_status[room_name]["score"]
        self.room_status[room_name]["status"] = "cleared"
        self.room_status[room_name]["score"] = max(prev_score, score)

        if room_name == "Inheritance":
            self.room_status["Encapsulation"]["status"] = "unlocked"
        elif room_name == "Encapsulation":
            self.room_status["Polymorphism"]["status"] = "unlocked"
        elif room_name == "Polymorphism":
            self.room_status["Constructor"]["status"] = "unlocked"
        elif room_name == "Constructor":
            self.room_status["Advanced Inheritance"]["status"] = "unlocked"
        elif room_name == "Advanced Inheritance":
            self.room_status["Composition"]["status"] = "unlocked"
        elif room_name == "Composition":
            self.room_status["Final Boss"]["status"] = "unlocked"

        self.save_progress()
        self.create_widgets()
        
        self.write_to_output(f"\n--- Dungeon Cleared! You've conquered {room_name} with {score} stars! ---\n")
        messagebox.showinfo("Dungeon Cleared!", f"Congratulations! You've cleared the {room_name} dungeon with {score} stars!")

    def save_progress(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.room_status, f, indent=4)

    def load_progress(self):
        if not os.path.exists(DATA_FILE): return
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                for key, value in data.items():
                    if key in self.room_status:
                        self.room_status[key].update(value)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading progress file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeDungeonApp(root)
    root.mainloop()