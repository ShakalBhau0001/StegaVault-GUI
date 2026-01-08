import customtkinter as ctk
from gui.sidebar import Sidebar
from gui.file_tab import FileTab
from gui.image_tab import ImageTab
from gui.audio_tab import AudioTab

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class StegaVaultApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("StegaVault")
        self.geometry("1100x650")
        self.resizable(False, False)

        # layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # sidebar
        self.sidebar = Sidebar(self, self.switch_tab)
        self.sidebar.grid(row=0, column=0, sticky="ns")

        # content frames
        self.frames = {
            "file": FileTab(self),
            "image": ImageTab(self),
            "audio": AudioTab(self),
        }

        for frame in self.frames.values():
            frame.grid(row=0, column=1, sticky="nsew")

        self.switch_tab("file")

    def switch_tab(self, name: str):
        for frame in self.frames.values():
            frame.grid_remove()

        self.frames[name].grid()
