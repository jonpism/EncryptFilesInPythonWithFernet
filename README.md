# Encrypt and Decrypt Files in Python using Fernet (PyQt6 application)

This is a **PyQt6** desktop application that allows users to **encrypt and decrypt files** using **Fernet encryption** (part of Python's `cryptography` library).  
The application features a GUI with a main menu and separate encryption and decryption screens.

## Features
- **GUI-Based Interface**: Built with PyQt6 for an interactive experience.
- **Fernet Encryption**: Ensures data confidentiality and integrity.
- **File Encryption & Decryption**: Encrypt and decrypt files securely.

---

## Installation

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/encrypt-decrypt-files.git
cd encrypt-decrypt-files
```

### **2. Install dependencies**
```bash
pip install -r requirements.txt
```

### **3. Ensure you have python version >3.6**
```bash
python --version
```

### **4. Install Additional System Dependencies (if required)**
Ubuntu/Debian:
```bash
sudo apt-get install qt6-base-dev
```
macOS:
```bash
brew install qt
```

### **5. Install additional required packages (if needed)**
```bash
pip install pyqt6 cryptography
```

### **6. Run the application**
```bash
python main.py
```

---

## Creating an executable file

### **1. Clone the repository**
```bash
git clone https://github.com/your-username/encrypt-decrypt-files.git
cd encrypt-decrypt-files
```

### **2. Install Pyinstaller**
```bash
pip install pyinstaller
```

### **3. Create the executable**
```bash
pyinstaller --noconsole --onefile --name EncryptAndDecryptFiles main.py
```

### **4. Handle external modules (optional)**
```bash
pyinstaller --noconsole --onefile --name EncryptAndDecryptFiles --add-data "button_style.py;." --add-data "qtextedit_style.py;." --add-data "encryption.py;." --add-data "decryption.py;." main.py
```

### **5. Locate the executable file**
```bash
cd dist/EncryptAndDecryptFiles.exe
```
