# MaxTechFix Software Protector — How To Use Guide

**Developer:** Zulfiqar Ali  
**Website:** [www.maxtechfix.com](https://www.maxtechfix.com)  
**Version:** 1.0.0

---

## What is Software Protector?

MaxTechFix Software Protector is an **all-in-one** tool that lets you add a professional
**trial + license system** to any software you build — without writing a single line of
protection code yourself.

- Wrap any **.py**, **.exe**, or **other file** with one click.  
- Customers get a **15-day free trial** (configurable).  
- After the trial expires, a license key is required.  
- License keys are **hardware-bound** — one key, one PC.

---

## Quick Start

```bash
# 1. Install Python 3.8+
# 2. Clone / download this repository
# 3. Run the application
python main.py
```

---

## Step-by-Step Guide

### Step 1 — Launch the Application

```
python main.py
```

The main window opens. The sidebar on the left has six sections:
Dashboard · Protect File · Key Generator · Activate License · How to Use · About

---

### Step 2 — Protect Your File  *(Developer)*

1. Click **Protect File** in the sidebar.  
2. Click the file-browser area and select the file you want to protect.  
   - `.py` files → a `protected_<name>.py` is created with the protection block injected.  
   - `.exe` files → a `launch_<name>.py` launcher wrapper is created.  
   - Any other file → the file is encrypted as `<name>.spdata` and a `launch_<name>.py` launcher is created.  
3. Enter the **Application Name** (shown to customers in trial dialogs).  
4. Choose an **Output Directory**.  
5. Set **Trial Days** (default: 15).  
6. Click **🛡️ Protect File**.  
7. Distribute the protected file(s) to your customers.

> **Tip:** To ship as a standalone `.exe`, install PyInstaller and run:  
> `pyinstaller --onefile protected_yourapp.py`

---

### Step 3 — Generate a License Key  *(Developer)*

1. Click **Key Generator** in the sidebar.  
2. Enter the **developer password** (set in `_DEV_PASSWORD` inside `protector/app.py` — change it before distributing your tool).  
3. Ask your customer for their **Hardware ID**  
   (they see it in the protected app, or in Software Protector → Activate License).  
4. Enter the customer's **email address** and **Hardware ID**.  
5. Click **🔑 Generate Key**.  
6. Copy the key and send it to the customer.

---

### Step 4 — Activate a License  *(Customer)*

1. Open the protected application (or Software Protector itself).  
2. Go to **Activate License**.  
3. Copy the **Hardware ID** shown and send it to the developer/reseller.  
4. Once you receive your license key, enter your **email** and **license key**.  
5. Click **✅ Activate License**.  
6. Done — the software is permanently unlocked on this PC.

---

### Step 5 — Distribute Your Software

| File type  | Protected output            | Next step                                  |
|------------|-----------------------------|--------------------------------------------|
| `.py`      | `protected_app.py`          | `pyinstaller --onefile protected_app.py`   |
| `.exe`     | `launch_app.py`             | `pyinstaller --onefile launch_app.py`      |
| Other      | `<name>.spdata` + `launch_<stem>.py` | Distribute both files together   |

---

## Security Architecture

| Layer            | Mechanism                                          |
|------------------|----------------------------------------------------|
| Trial storage    | XOR-encrypted JSON written to `~/.sp_data/`        |
| License storage  | Same encryption, separate file per app             |
| Key algorithm    | HMAC-SHA256(secret, email + hardware_id)           |
| Hardware binding | SHA-256 of MAC address → 16-char hex fingerprint   |
| Tamper protection| Corrupt/missing files reset to a new trial         |

---

## FAQ

**Q: Can a customer use one license on two PCs?**  
A: No. The key is bound to the Hardware ID of one specific machine.

**Q: What happens when the trial expires?**  
A: A dialog appears asking for a license key. The software does not run until a valid key is entered.

**Q: How do I change the developer password?**  
A: Edit `_DEV_PASSWORD` in `protector/app.py`. Use a strong, unique password before distributing your tool.

**Q: Can I change the trial period?**  
A: Yes — set the Trial Days value in the Protect File form (each protected app has its own timer).

**Q: Does the customer need Python installed?**  
A: Only if you distribute the `.py` directly. Compile with PyInstaller to ship a standalone `.exe`.

---

## Requirements

- Python 3.8+
- tkinter (included with Python; install `python3-tk` on Linux)

No external packages required for core functionality.

---

## Contact & Support

**Zulfiqar Ali**  
MaxTechFix  
🌐 [www.maxtechfix.com](https://www.maxtechfix.com)

---

*© 2024 MaxTechFix · All rights reserved.*
