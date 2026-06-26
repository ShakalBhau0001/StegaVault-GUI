# 🗝️ StegaVault-GUI  

### Unified Encryption & Steganography Toolkit (GUI Edition)

**StegaVault-GUI** is a modern, password-based **encryption and steganography desktop application** built entirely in **Python (3.12.x compatible)** using **CustomTkinter**.
It allows **end users (non-technical)** to securely:
- Encrypt & decrypt files
- Hide encrypted messages inside images
- Hide encrypted messages inside audio files

All operations are performed locally with **no network usage**, ensuring full user privacy.

---

## 🔄 Also Available as a CLI Tool

Prefer terminal-based workflows or scripting?

👉 **StegaVault-CLI** is the command-line version of this project, designed for developers and power users.

> 🔗 CLI Repository: **[StegaVault-CLI](https://github.com/ShakalBhau0001/StegaVault-CLI)**

---

## ✨ Key Philosophy

StegaVault is designed with three core goals:

1. **Security-first** – modern cryptography only  
2. **End-user friendly** – clean GUI, minimal clicks  
3. **Modular architecture** – logic separated from UI  

This is **not a toy project**. Every module works independently and follows consistent cryptographic rules.

---

## 🧩 Included Modules

### 🔐 File Encryption

Encrypt *any* file using a password.

**Features**

- Supports all file types
- Encrypted output: `.enc`
- Original filename restored on decryption
- Password-based key derivation (PBKDF2)

**Use-case**
> Secure documents, archives, videos, backups

---

### 🖼️ Image Steganography (PNG)

Hide encrypted text inside PNG images using LSB steganography.

**Features**

- Password-protected payload
- MAGIC header integrity check
- Lossless PNG output enforced
- Detects wrong password / corrupted images

**Use-case**
> Invisible message transfer, stego research

---

### 🔊 Audio Steganography (WAV)

Hide encrypted text inside 16‑bit PCM WAV files.

**Features**

- Works only on uncompressed WAV
- Password-based encryption
- Payload integrity validation
- Clean extraction with error handling

**Use-case**
> Audio-based covert communication experiments

---

## 📁 Project Structure

```bash
StegaVault-GUI/
│
├── core/
│   ├── __init__.py    
│   ├── file_crypto.py      
│   ├── image_stego.py       
│   └── audio_stego.py       
│
├── gui/
│   ├── __init__.py
│   ├── app.py              
│   ├── sidebar.py          
│   ├── file_tab.py
│   ├── image_tab.py
│   └── audio_tab.py
│
├── main.py
├── requirements.txt
└── README.md
```

> ✔ Logic and GUI are **strictly separated** for maintainability.

---

## 🔐 Cryptography Details

| Component | Implementation |
|---------|----------------|
| Encryption | Fernet (AES‑128 + HMAC) |
| Key Derivation | PBKDF2‑HMAC‑SHA256 |
| Iterations | 390,000 |
| Salt | Random per operation |
| Integrity | MAGIC header validation |

> ⚠️ Lossy formats (JPEG, MP3) are avoided for output to prevent corruption.

---

## 🖥️ GUI Design

- Built with **CustomTkinter**
- Sidebar navigation
- Separate tabs per module
- Clear error messages
- Designed for **non‑technical users**

Fully tested on:

- **Python 3.12.10**
- Windows 10 / 11

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone https://github.com/ShakalBhau0001/StegaVault-GUI.git
cd StegaVault-GUI
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Run Application

```bash
python main.py
```

---

## 📦 requirements.txt

```txt
cryptography
pillow
customtkinter
```

_No hidden or unnecessary dependencies._

---

## ⚠️ Security Disclaimer

This project is intended for **educational and research purposes**.

While it uses modern cryptographic primitives, it has **not undergone formal security audits**.  
Do not use it for protecting high‑value or life‑critical data.

---

## 🛣️ Roadmap

- Drag‑and‑drop support
- Large payload progress indicator
- Linux & macOS packaging
- PyInstaller standalone builds

---

## 📸 Preview

![Rich CLI Preview](assets/Stega.png)

---

## 🪪 Author

> Developer: **Shakal Bhau**

> GitHub: **[ShakalBhau0001](https://github.com/ShakalBhau0001)**

---

> “Security should be powerful — but never complicated for the user.”

---

## ⭐ Support

If you like this project, consider giving it a ⭐ on GitHub!

---
