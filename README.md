# 🛡️ MaxTechFix Software Protector

**Developer:** Zulfiqar Ali | [www.maxtechfix.com](https://www.maxtechfix.com)

An all-in-one professional tool to protect your software with a **trial system**,
**hardware-bound license keys**, and **file encryption** — all through an easy-to-use GUI.

## Features

- **Protect any file** — `.py`, `.exe`, documents, images, and more
- **15-day trial** with countdown dialog shown to customers on every launch
- **HMAC-SHA256 license keys** bound to customer email + hardware ID
- **Hardware binding** — one license = one PC (MAC address fingerprinting)
- **Encrypted trial/license storage** — tamper-resistant data files
- **Developer Mode** — password-protected Key Generator
- **No command line needed** — professional dark-theme GUI

## Quick Start

```bash
# Requires Python 3.8+ and tkinter
pip install -r requirements.txt   # optional extra deps
python main.py
```

## Usage

See [HOW_TO_USE.md](HOW_TO_USE.md) for the complete step-by-step guide.

### Workflow

**Developer side**
1. Select your file in *Protect File* → click *Protect File*
2. Compile the output with PyInstaller → distribute to customers
3. Use *Key Generator* (developer password required) to create license keys

**Customer side**
1. Run the protected software → 15-day trial starts automatically
2. After trial expires → license dialog appears
3. Customer enters email + license key → software unlocked

## Project Structure

```
software-protector/
├── main.py                       # Entry point
├── requirements.txt
├── HOW_TO_USE.md
├── protector/
│   ├── app.py                    # Main GUI application
│   ├── hardware_id.py            # Hardware fingerprinting
│   ├── encryption.py             # XOR + base64 encryption
│   ├── trial_manager.py          # Trial period tracking
│   ├── license_manager.py        # License key generation & validation
│   └── file_protector.py        # File wrapping logic
└── templates/
    ├── protected_py_template.py  # Injected into .py files
    ├── protected_exe_template.py # Launcher for .exe files
    └── protected_generic_template.py  # Launcher for other files
```

## License

© 2024 Zulfiqar Ali · MaxTechFix · All rights reserved.
