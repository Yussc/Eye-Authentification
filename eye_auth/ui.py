import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
from concurrent.futures import ThreadPoolExecutor

from eye_auth.tracker import EyeTracker
from eye_auth.gaze_position import GazePosition
from eye_auth.crypt import Crypt
from eye_auth.comparator import Comparator


class UI:

    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.app = ctk.CTk()
        self.app.title("Login par Motif - Eye Tracker")
        self.app.geometry("400x300")

        self.executor = ThreadPoolExecutor(max_workers=1)
        self.future = None
        self.pattern_window = None

        self._build_main_interface()

    def _build_main_interface(self):
        title_label = ctk.CTkLabel(self.app, text="Bienvenue", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=30)

        username_label = ctk.CTkLabel(self.app, text="Nom d'utilisateur:", font=ctk.CTkFont(size=14))
        username_label.pack(pady=(0, 5))

        self.username_entry = ctk.CTkEntry(self.app, width=200)
        self.username_entry.pack(pady=(0, 10))

        login_button = ctk.CTkButton(self.app, text="Login", command=self.open_pattern_window)
        login_button.pack(pady=20)

    def open_success_window(self):
        success_window = ctk.CTkToplevel(self.app)
        success_window.title("Succès")
        success_window.geometry("300x200")

        label = ctk.CTkLabel(success_window, text="Connexion réussie !", font=ctk.CTkFont(size=16))
        label.pack(pady=20)

        close_button = ctk.CTkButton(success_window, text="Fermer", command=success_window.destroy)
        close_button.pack(pady=10)

    def collect_gaze_data(self):
        tracker = EyeTracker('131.206.224.19', 50020)
        tracker.connect()
        tracker.subscribe('surfaces')
        tracker.subscribe('blinks')
        gaze_list = tracker.collectData("Surface 1")
        print(gaze_list)
        return gaze_list

    def open_pattern_window(self):
        self.pattern_window = ctk.CTkToplevel(self.app)
        self.pattern_window.title("Tracer le motif")
        self.pattern_window.geometry("1200x800")

        label = ctk.CTkLabel(self.pattern_window, text=f"Bienvenue {self.username_entry.get().strip()} ! Ici vous tracerez le motif avec l'eye tracker",
                             font=ctk.CTkFont(size=16))
        label.pack(pady=20)

        canvas_frame = tk.Frame(self.pattern_window, bg="white", width=1000, height=600, bd=2, relief="solid")
        canvas_frame.pack(pady=10)

        canvas = tk.Canvas(canvas_frame, width=1000, height=600, bg="white", highlightthickness=0)
        canvas.pack()

        base_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_path, "..", "assets", "fond.png")

        pil_image = Image.open(img_path).resize((1000, 600))
        self.image = ImageTk.PhotoImage(pil_image)

        canvas.create_image(0, 0, image=self.image, anchor="nw")

        # Lancer la collecte dans un thread
        self.future = self.executor.submit(self.collect_gaze_data)

        # Afficher un message pendant l'attente
        self.status_label = ctk.CTkLabel(self.pattern_window, text="Collecte des données en cours...", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=10)

        # Vérifier toutes les 500ms si la collecte est terminée
        self.app.after(500, self.check_gaze_data)

    def check_gaze_data(self):
        if self.future.done():
            try:
                gaze_list = self.future.result()
            except Exception as e:
                self.status_label.configure(text=f"Erreur : {e}", text_color="red")
                return

            user = self.username_entry.get().strip()

            if gaze_list:
                gaze_positions = GazePosition(gaze_list)
                print(len(gaze_positions.gaze_positions))
                gaze_positions.preprocess()
                print(len(gaze_positions.gaze_positions))
                gaze_positions.save_image(os.path.join(os.path.dirname(__file__), "..", "assets", f"{user}_gaze_pattern.png"))

                user_gaze_position = Crypt.decrypt(user)
                Crypt.encrypt(user)

                comparator = Comparator(gaze_positions.gaze_positions, user_gaze_position)
                print(comparator.compare())
                if comparator.compare():
                    self.pattern_window.destroy()
                    self.open_success_window()
                else:
                    self.status_label.configure(text="Motif non reconnu !", text_color="red")
            else:
                self.status_label.configure(text="Aucune donnée captée.", text_color="red")
        else:
            # Re-vérifie dans 500ms
            self.app.after(500, self.check_gaze_data)

    def run(self):
        self.app.mainloop()


if __name__ == "__main__":
    ui = UI()
    ui.run()
