# 🔐 Password Manager GUI (Python, Tkinter)

A sleek, secure password manager built with Python and Tkinter.  
Features full encryption, master password login, clipboard copy, and multi-account support — all in a clean, modern UI.

---

## 🧠 Features

- 🔐 **Master Password Login** — Secure login screen before accessing the app  
- 🔁 **Master Password Reset** — Update your login securely  
- ✨ **Modern UI with `ttk`** — Clean and professional interface  
- 👁️ **Show/Hide Password Toggle**  
- 🔍 **Search by Website** — Autofill matching credentials  
- 👥 **Multi-Account Support** — Save multiple logins per site  
- 🗑️ **Delete Saved Credentials**  
- 🔑 **Random Password Generator**  
- 📋 **Clipboard Copy** — One-click copy to clipboard  
- 🧊 **Encrypted Storage** — Data stored securely using Fernet (symmetric encryption)

---

## ⚙️ How to Run

### 1. Clone the repo:

```bash
git clone https://github.com/Cyber-Security-Tech/password-manager-gui.git
cd password-manager-gui
```

### 2. Install dependencies:

```bash
pip install cryptography werkzeug
```

### 3. Set your master password:

```bash
python -c "from werkzeug.security import generate_password_hash; print(generate_password_hash('your_password'))"
```

Copy the output and paste it into `config.json` like this:

```json
{
  "master_password": "PASTE_HASH_HERE"
}
```

### 4. Run the app:

```bash
python ui.py
```

---

## 🗂️ File Structure

```
password-manager-gui/
├── ui.py                  # Main GUI
├── password_logic.py      # Logic layer
├── data_manager.py        # Save/load/delete JSON entries
├── encryption.py          # Handles Fernet encryption
├── save.py                # (Legacy)
├── password_generator.py  # Random password gen
├── login.py               # Master password login screen
├── config.json            # Stores hashed master password
└── data/
    └── passwords.json     # Encrypted saved entries
```

---

## 📦 Dependencies

- `tkinter` (built-in)
- `cryptography`
- `werkzeug`

---

## 📄 License

MIT License 
