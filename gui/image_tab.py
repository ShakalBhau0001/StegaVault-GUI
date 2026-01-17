import customtkinter as ctk
from tkinter import filedialog, messagebox
from core.image_stego import embed_message, extract_message


class ImageTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.img_path = ctk.StringVar()
        self.password = ctk.StringVar()
        self.output = ctk.StringVar(value="stego.png")

        ctk.CTkLabel(
            self,
            text="🖼 Image Steganography",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(pady=15)

        ctk.CTkEntry(
            self,
            textvariable=self.img_path,
            width=420,
            placeholder_text="Select PNG image",
        ).pack(pady=6)

        ctk.CTkButton(self, text="Browse Image", command=self.browse).pack()

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
            placeholder_text="Output image name",
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
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png")])
        if path:
            self.img_path.set(path)

    def encrypt(self):
        # Input Validation
        if not self.img_path.get():
            messagebox.showwarning("Missing Image", "Please select an image file.")
            return
        msg = self.msg_box.get("0.0", "end").strip()
        if not msg:
            messagebox.showwarning("Missing Message", "Please type a message to hide.")
            return
        if not self.password.get():
            messagebox.showwarning("Missing Password", "Please enter a password.")
            return
        if not self.output.get():
            self.output.set("stego.png")
        elif not self.output.get().lower().endswith(".png"):
            self.output.set(self.output.get() + ".png")

        # EMBED
        try:
            embed_message(
                self.img_path.get(),
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
        if not self.img_path.get():
            messagebox.showwarning("Missing Image", "Please select an image file.")
            return
        if not self.password.get():
            messagebox.showwarning("Missing Password", "Please enter a password.")
            return
        try:
            msg = extract_message(self.img_path.get(), self.password.get())
            self.msg_box.delete("0.0", "end")
            self.msg_box.insert("0.0", msg.decode())
        except Exception:
            messagebox.showerror("Error", "Wrong password or corrupted image")
