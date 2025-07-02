import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os
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

        # Interface
        self._build_main_interface()

    def _build_main_interface(self):
        title_label = ctk.CTkLabel(self.app, text="Bienvenue", font=ctk.CTkFont(size=24, weight="bold"))
        title_label.pack(pady=30)

        # Username input field
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


    def open_pattern_window(self):

        pattern_window = ctk.CTkToplevel(self.app)
        pattern_window.title("Tracer le motif")
        pattern_window.geometry("1200x800")

        label = ctk.CTkLabel(pattern_window, text=f"Bienvenue {self.username_entry.get().strip()} ! Ici vous tracerez le motif avec l'eye tracker",
                            font=ctk.CTkFont(size=16))
        label.pack(pady=20)

        canvas_frame = tk.Frame(pattern_window, bg="white", width=1000, height=600, bd=2, relief="solid")
        canvas_frame.pack(pady=10)

        canvas = tk.Canvas(canvas_frame, width=1000, height=600, bg="white", highlightthickness=0)
        canvas.pack()

        base_path = os.path.dirname(os.path.abspath(__file__))
        img_path = os.path.join(base_path, "..", "assets", "fond.png")  

        pil_image = Image.open(img_path).resize((1000, 600))
        self.image = ImageTk.PhotoImage(pil_image) 

        canvas.create_image(0, 0, image=self.image, anchor="nw") 

        tracker = EyeTracker('localhost', 50020)
        tracker.subscribe('surfaces')
        gaze_list = tracker.collectData("Surface 1")

        user = self.username_entry.get().strip()

        if gaze_list:
            gaze_positions = GazePosition(gaze_list)
            gaze_positions.preprocess()

            user_gaze_position = Crypt.decrypt(user)
            Crypt.encrypt(user)

            comparator = Comparator(gaze_positions, user_gaze_position)
            if comparator.compare():
                self.open_success_window()
            else:
                result_label = ctk.CTkLabel(pattern_window, text="Motif non reconnu !", font=ctk.CTkFont(size=16, weight="bold"), text_color="red")
                result_label.pack(pady=20)


    def run(self):
        self.app.mainloop()




