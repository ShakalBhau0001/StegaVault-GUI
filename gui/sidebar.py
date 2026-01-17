import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, switch_callback):
        super().__init__(master, width=200, corner_radius=0)
        self.switch_callback = switch_callback

        self.grid_rowconfigure(5, weight=1)

        ctk.CTkLabel(
            self,
            text="🔐 StegaVault",
            font=ctk.CTkFont(size=18, weight="bold"),
        ).grid(row=0, column=0, pady=20)

        self._btn("File Encryption", "file", 1)
        self._btn("Image Steganography", "image", 2)
        self._btn("Audio Steganography", "audio", 3)

    def _btn(self, text, name, row):
        ctk.CTkButton(
            self,
            text=text,
            command=lambda: self.switch_callback(name),
            width=160,
        ).grid(row=row, column=0, pady=10, padx=20)
