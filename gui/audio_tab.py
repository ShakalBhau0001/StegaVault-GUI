import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.audio_stego import embed_audio, extract_audio


class AudioTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.audio_path = ctk.StringVar()
        self.password = ctk.StringVar()
        self.output = ctk.StringVar(value="stego.wav")

        ctk.CTkLabel(
            self,
            text="🔊 Audio Steganography (WAV)",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=15)

        ctk.CTkEntry(
            self,
            textvariable=self.audio_path,
            width=420,
            placeholder_text="Select WAV audio",
        ).pack(pady=6)

        ctk.CTkButton(self, text="Browse WAV", command=self.browse).pack()

        self.msg_box = ctk.CTkTextbox(self, width=420, height=120)
        self.msg_box.pack(pady=10)

        ctk.CTkEntry(
            self,
            textvariable=self.password,
            show="*",
            width=240,
            placeholder_text="Password",
        ).pack(pady=6)

        ctk.CTkEntry(
            self,
            textvariable=self.output,
            width=240,
            placeholder_text="Output WAV name",
        ).pack(pady=6)

        ctk.CTkButton(
            self,
            text="Encrypt & Embed",
            fg_color="#2e7d32",
            command=self.encrypt,
        ).pack(pady=6)

        ctk.CTkButton(
            self,
            text="Extract & Decrypt",
            fg_color="#1565c0",
            command=self.decrypt,
        ).pack(pady=6)

    def browse(self):
        path = filedialog.askopenfilename(filetypes=[("WAV Audio", "*.wav")])
        if path:
            self.audio_path.set(path)

    def encrypt(self):
        if not self.audio_path.get():
            messagebox.showwarning("Missing Audio", "Please select a WAV file.")
            return
        msg = self.msg_box.get("0.0", "end").strip()
        if not msg:
            messagebox.showwarning("Missing Message", "Please type a message to hide.")
            return
        if not self.password.get():
            messagebox.showwarning("Missing Password", "Please enter a password.")
            return
        if not self.output.get():
            self.output.set("stego.wav")
        elif not self.output.get().lower().endswith(".wav"):
            self.output.set(self.output.get() + ".wav")

        try:
            embed_audio(
                self.audio_path.get(),
                msg.encode(),
                self.password.get(),
                self.output.get(),
            )
            messagebox.showinfo(
                "Success", f"Message embedded successfully:\n{self.output.get()}"
            )
        except Exception as e:
            messagebox.showerror("Error", str(e) if str(e) else repr(e))

    def decrypt(self):
        if not self.audio_path.get():
            messagebox.showwarning("Missing Audio", "Please select a WAV file.")
            return
        if not self.password.get():
            messagebox.showwarning("Missing Password", "Please enter a password.")
            return
        try:
            msg = extract_audio(self.audio_path.get(), self.password.get())
            self.msg_box.delete("0.0", "end")
            self.msg_box.insert("0.0", msg.decode())
        except Exception:
            messagebox.showerror("Error", "Wrong password or corrupted audio")
