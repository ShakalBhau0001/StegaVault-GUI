import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.file_crypto import encrypt_file, decrypt_file


class FileTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.file_path = ctk.StringVar()
        self.password = ctk.StringVar()

        ctk.CTkLabel(
            self,
            text="🔐 File Encryption / Decryption",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=20)

        ctk.CTkEntry(
            self,
            textvariable=self.file_path,
            width=420,
            placeholder_text="Select file...",
        ).pack(pady=8)

        ctk.CTkButton(
            self,
            text="Browse File",
            command=self.browse_file,
        ).pack(pady=5)

        ctk.CTkEntry(
            self,
            textvariable=self.password,
            show="*",
            width=240,
            placeholder_text="Password",
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Encrypt File",
            command=self.encrypt,
            fg_color="#2e7d32",
        ).pack(pady=6)

        ctk.CTkButton(
            self,
            text="Decrypt File",
            command=self.decrypt,
            fg_color="#1565c0",
        ).pack(pady=6)

    def browse_file(self):
        path = filedialog.askopenfilename()
        if path:
            self.file_path.set(path)

    def encrypt(self):
        try:
            out = encrypt_file(self.file_path.get(), self.password.get())
            messagebox.showinfo("Success", f"Encrypted:\n{out}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decrypt(self):
        try:
            out = decrypt_file(self.file_path.get(), self.password.get())
            messagebox.showinfo("Success", f"Decrypted:\n{out}")
        except Exception:
            messagebox.showerror("Error", "Wrong password or corrupted file")
