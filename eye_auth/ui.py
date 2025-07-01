import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk
import os


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

        login_button = ctk.CTkButton(self.app, text="Login", command=self.open_pattern_window)
        login_button.pack(pady=20)

    def open_pattern_window(self):
        pattern_window = ctk.CTkToplevel(self.app)
        pattern_window.title("Tracer le motif")
        pattern_window.geometry("1200x800")

        label = ctk.CTkLabel(pattern_window, text="Ici vous tracerez le motif avec l'eye tracker",
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


    def run(self):
        self.app.mainloop()




