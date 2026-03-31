"""
MaxTechFix Software Protector — Main GUI Application
Developer: Zulfiqar Ali  |  www.maxtechfix.com
"""
import os
import sys
import tkinter as tk
import tkinter.font as tkfont
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from pathlib import Path

from .hardware_id import get_hardware_id
from .license_manager import generate_license_key
from .trial_manager import get_trial_info, activate_license
from .file_protector import protect_file

# ── Colour palette ────────────────────────────────────────────────────────────
C = {
    "bg":        "#0f172a",
    "panel":     "#1e293b",
    "border":    "#334155",
    "accent":    "#6366f1",
    "accent_h":  "#818cf8",
    "success":   "#10b981",
    "danger":    "#ef4444",
    "warning":   "#f59e0b",
    "text":      "#f1f5f9",
    "muted":     "#94a3b8",
    "dim":       "#475569",
    "sidebar":   "#0d1526",
    "nav_sel":   "#1e293b",
    "nav_hover": "#162032",
}

NAV_ITEMS = [
    ("🏠", "Dashboard"),
    ("🛡️", "Protect File"),
    ("🔑", "Key Generator"),
    ("✅", "Activate License"),
    ("📖", "How to Use"),
    ("ℹ️",  "About"),
]


# ── Helpers ───────────────────────────────────────────────────────────────────

def _card(parent, **kw):
    """Return a styled card Frame."""
    kw.setdefault("bg", C["panel"])
    kw.setdefault("bd", 0)
    kw.setdefault("relief", "flat")
    return tk.Frame(parent, **kw)


def _label(parent, text="", size=10, weight="normal", color=None, **kw):
    kw["bg"] = kw.get("bg", parent["bg"])
    kw["fg"] = color or C["text"]
    kw["font"] = tkfont.Font(family="Segoe UI", size=size, weight=weight)
    return tk.Label(parent, text=text, **kw)


def _btn(parent, text, command, color=None, hover_color=None, width=None, **kw):
    bg = color or C["accent"]
    hv = hover_color or C["accent_h"]
    kw["bg"] = bg
    kw["fg"] = C["text"]
    kw["font"] = tkfont.Font(family="Segoe UI", size=10, weight="bold")
    kw["relief"] = "flat"
    kw["cursor"] = "hand2"
    kw["activebackground"] = hv
    kw["activeforeground"] = C["text"]
    kw["bd"] = 0
    kw["padx"] = 20
    kw["pady"] = 8
    if width:
        kw["width"] = width
    b = tk.Button(parent, text=text, command=command, **kw)

    def _enter(_):
        b.config(bg=hv)
    def _leave(_):
        b.config(bg=bg)

    b.bind("<Enter>", _enter)
    b.bind("<Leave>", _leave)
    return b


def _entry(parent, textvariable=None, show=None, width=None, **kw):
    kw["bg"] = C["panel"]
    kw["fg"] = C["text"]
    kw["font"] = tkfont.Font(family="Segoe UI", size=10)
    kw["relief"] = "flat"
    kw["bd"] = 0
    kw["insertbackground"] = C["text"]
    kw["highlightbackground"] = C["border"]
    kw["highlightcolor"] = C["accent"]
    kw["highlightthickness"] = 1
    if textvariable:
        kw["textvariable"] = textvariable
    if show:
        kw["show"] = show
    if width:
        kw["width"] = width
    return tk.Entry(parent, **kw)


def _divider(parent):
    return tk.Frame(parent, bg=C["border"], height=1)


# ── Main Application ──────────────────────────────────────────────────────────

class SoftwareProtectorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MaxTechFix Software Protector v1.0")
        self.configure(bg=C["bg"])
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.resizable(True, True)

        self._current_view = tk.StringVar(value="Dashboard")
        self._nav_buttons = {}
        self._content_frames = {}

        self._build_layout()
        self._show_view("Dashboard")

    # ── Layout ────────────────────────────────────────────────────────────────

    def _build_layout(self):
        # Sidebar
        self._sidebar = tk.Frame(self, bg=C["sidebar"], width=210)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)

        # Logo area
        logo_frame = tk.Frame(self._sidebar, bg=C["sidebar"], height=80)
        logo_frame.pack(fill="x", pady=(0, 10))
        logo_frame.pack_propagate(False)
        _label(logo_frame, "🛡️", size=26, bg=C["sidebar"]).pack(pady=(14, 0))
        _label(logo_frame, "Software Protector", size=9, weight="bold",
               color=C["accent"], bg=C["sidebar"]).pack()

        _divider(self._sidebar).pack(fill="x", padx=16, pady=(0, 12))

        # Navigation buttons
        for icon, name in NAV_ITEMS:
            btn_frame = tk.Frame(self._sidebar, bg=C["sidebar"])
            btn_frame.pack(fill="x", padx=8, pady=2)

            btn = tk.Button(
                btn_frame,
                text=f"  {icon}  {name}",
                font=tkfont.Font(family="Segoe UI", size=10),
                bg=C["sidebar"],
                fg=C["muted"],
                relief="flat",
                anchor="w",
                bd=0,
                padx=10,
                pady=10,
                cursor="hand2",
                activebackground=C["nav_hover"],
                activeforeground=C["text"],
                command=lambda n=name: self._show_view(n),
            )
            btn.pack(fill="x")
            self._nav_buttons[name] = btn

            def _enter(e, b=btn): b.config(bg=C["nav_hover"], fg=C["text"])
            def _leave(e, b=btn, n=name):
                sel = self._current_view.get()
                b.config(
                    bg=C["nav_sel"] if n == sel else C["sidebar"],
                    fg=C["text"] if n == sel else C["muted"],
                )
            btn.bind("<Enter>", _enter)
            btn.bind("<Leave>", _leave)

        # Bottom brand
        tk.Frame(self._sidebar, bg=C["sidebar"]).pack(fill="both", expand=True)
        _divider(self._sidebar).pack(fill="x", padx=16, pady=8)
        _label(self._sidebar, "Zulfiqar Ali", size=9, color=C["dim"],
               bg=C["sidebar"]).pack(pady=(0, 2))
        _label(self._sidebar, "www.maxtechfix.com", size=8, color=C["dim"],
               bg=C["sidebar"]).pack(pady=(0, 12))

        # Main content area
        self._main = tk.Frame(self, bg=C["bg"])
        self._main.pack(side="left", fill="both", expand=True)

        # Status bar
        self._status_bar = tk.Frame(self, bg=C["panel"], height=28)
        self._status_bar.pack(side="bottom", fill="x")
        self._status_bar.pack_propagate(False)
        self._status_var = tk.StringVar(value="Ready")
        _label(self._status_bar, textvariable=self._status_var, size=9,
               color=C["muted"], bg=C["panel"]).pack(side="left", padx=12)

        # Build all views
        for _, name in NAV_ITEMS:
            builder = getattr(self, f"_build_{name.lower().replace(' ', '_')}")
            frame = tk.Frame(self._main, bg=C["bg"])
            builder(frame)
            self._content_frames[name] = frame

    def _show_view(self, name: str):
        for n, btn in self._nav_buttons.items():
            btn.config(
                bg=C["nav_sel"] if n == name else C["sidebar"],
                fg=C["text"] if n == name else C["muted"],
            )
        for n, frame in self._content_frames.items():
            if n == name:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()
        self._current_view.set(name)

    def _set_status(self, msg: str):
        self._status_var.set(msg)
        self.update_idletasks()

    # ── View builders ─────────────────────────────────────────────────────────

    # 1. Dashboard ─────────────────────────────────────────────────────────────
    def _build_dashboard(self, parent):
        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=C["bg"])
        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all")),
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        p = scroll_frame

        # Header
        hdr = tk.Frame(p, bg=C["bg"])
        hdr.pack(fill="x", padx=36, pady=(30, 8))
        _label(hdr, "Welcome to Software Protector", size=20, weight="bold",
               color=C["text"]).pack(anchor="w")
        _label(hdr, "Secure your software with trial management, license binding & hardware fingerprinting.",
               size=11, color=C["muted"]).pack(anchor="w", pady=(4, 0))

        _divider(p).pack(fill="x", padx=36, pady=(8, 24))

        # Stats cards
        info = get_trial_info()
        cards_row = tk.Frame(p, bg=C["bg"])
        cards_row.pack(fill="x", padx=36, pady=(0, 24))

        def stat_card(parent, title, value, sub, color):
            c = _card(parent, padx=0, pady=0)
            c.pack(side="left", expand=True, fill="both", padx=(0, 14))
            inner = tk.Frame(c, bg=C["panel"], padx=20, pady=18)
            inner.pack(fill="both", expand=True)
            _label(inner, title, size=9, color=C["muted"]).pack(anchor="w")
            _label(inner, value, size=22, weight="bold", color=color).pack(anchor="w", pady=(2, 0))
            _label(inner, sub,   size=9, color=C["muted"]).pack(anchor="w")

        if info["is_licensed"]:
            stat_card(cards_row, "STATUS",    "LICENSED ✅",  f"Email: {info['email']}",     C["success"])
            stat_card(cards_row, "HARDWARE",  get_hardware_id(), "Your machine fingerprint", C["accent"])
            stat_card(cards_row, "PROTECTION","Active 🔒",   "License is valid",              C["success"])
        else:
            days = info["days_left"] or 0
            color = C["success"] if days > 5 else C["warning"] if days > 0 else C["danger"]
            stat_card(cards_row, "TRIAL STATUS",
                      f"{days} days left",
                      f"Used {info['days_used']} of 15 days", color)
            stat_card(cards_row, "HARDWARE ID",  get_hardware_id(), "Your machine fingerprint", C["accent"])
            stat_card(cards_row, "LICENSE",      "Not Activated ⚠️",
                      "Click 'Activate License' to unlock", C["warning"])

        # Quick actions
        _label(p, "Quick Actions", size=13, weight="bold", color=C["text"]).pack(
            anchor="w", padx=36, pady=(0, 12))
        qa = tk.Frame(p, bg=C["bg"])
        qa.pack(fill="x", padx=36, pady=(0, 24))

        def qa_btn(text, icon, view):
            f = _card(qa, padx=0, pady=0)
            f.pack(side="left", padx=(0, 14))
            inner = tk.Frame(f, bg=C["panel"], padx=22, pady=16, cursor="hand2")
            inner.pack()
            _label(inner, icon, size=22, bg=C["panel"]).pack()
            _label(inner, text, size=10, weight="bold", bg=C["panel"]).pack(pady=(4, 0))
            for w in [f, inner]:
                w.bind("<Button-1>", lambda e, v=view: self._show_view(v))
                w.bind("<Enter>", lambda e, w=inner: w.config(bg=C["nav_hover"]))
                w.bind("<Leave>", lambda e, w=inner: w.config(bg=C["panel"]))
            for lbl in inner.winfo_children():
                lbl.bind("<Button-1>", lambda e, v=view: self._show_view(v))
                lbl.bind("<Enter>", lambda e, w=inner: w.config(bg=C["nav_hover"]))
                lbl.bind("<Leave>", lambda e, w=inner: w.config(bg=C["panel"]))

        qa_btn("Protect a File",        "🛡️", "Protect File")
        qa_btn("Generate License Key",  "🔑", "Key Generator")
        qa_btn("Activate My License",   "✅", "Activate License")
        qa_btn("Read the Guide",        "📖", "How to Use")

        # Feature highlights
        _divider(p).pack(fill="x", padx=36, pady=(8, 20))
        _label(p, "What can this tool do?", size=13, weight="bold").pack(
            anchor="w", padx=36, pady=(0, 12))
        features = [
            ("🛡️ File Protection",   "Wrap any .py, .exe, or other file with a trial & license check."),
            ("⏱️ Trial Manager",     "15-day free trial with a visible countdown on every launch."),
            ("🔑 License Keys",      "HMAC-SHA256 keys bound to customer email + machine hardware ID."),
            ("🖥️ Hardware Binding",  "One license = one PC. Prevents key sharing across machines."),
            ("🔒 Encrypted Storage", "Trial and license data stored encrypted on disk."),
            ("👨‍💻 Developer Mode",   "Password-protected Key Generator to manage customer licenses."),
        ]
        feat_grid = tk.Frame(p, bg=C["bg"])
        feat_grid.pack(fill="x", padx=36, pady=(0, 36))
        for i, (title, desc) in enumerate(features):
            row = i // 2
            col = i % 2
            f = _card(feat_grid)
            f.grid(row=row, column=col, sticky="nsew", padx=(0, 14) if col == 0 else (14, 0),
                   pady=(0, 14))
            inner = tk.Frame(f, bg=C["panel"], padx=16, pady=14)
            inner.pack(fill="both", expand=True)
            _label(inner, title, size=11, weight="bold", bg=C["panel"]).pack(anchor="w")
            _label(inner, desc,  size=9,  color=C["muted"], bg=C["panel"],
                   wraplength=320, justify="left").pack(anchor="w", pady=(4, 0))
        feat_grid.columnconfigure(0, weight=1)
        feat_grid.columnconfigure(1, weight=1)

    # 2. Protect File ──────────────────────────────────────────────────────────
    def _build_protect_file(self, parent):
        p = tk.Frame(parent, bg=C["bg"])
        p.pack(fill="both", expand=True, padx=36, pady=30)

        _label(p, "Protect a File", size=20, weight="bold").pack(anchor="w")
        _label(p, "Wrap any file with a built-in trial/license check system.",
               size=11, color=C["muted"]).pack(anchor="w", pady=(4, 0))
        _divider(p).pack(fill="x", pady=(12, 20))

        # File picker area
        drop_frame = tk.Frame(p, bg=C["panel"], relief="flat", bd=0,
                              highlightbackground=C["accent"],
                              highlightthickness=2,
                              cursor="hand2")
        drop_frame.pack(fill="x", pady=(0, 16))
        inner_drop = tk.Frame(drop_frame, bg=C["panel"], padx=30, pady=28)
        inner_drop.pack(fill="x")
        _label(inner_drop, "📂", size=28, bg=C["panel"]).pack()
        _label(inner_drop, "Click to browse for a file to protect",
               size=12, weight="bold", bg=C["panel"]).pack(pady=(6, 2))
        _label(inner_drop, "Supports .py  ·  .exe  ·  any other file type",
               size=9, color=C["muted"], bg=C["panel"]).pack()

        self._pf_path = tk.StringVar()
        self._pf_path_label = _label(inner_drop, "(no file selected)", size=9,
                                     color=C["accent"], bg=C["panel"])
        self._pf_path_label.pack(pady=(8, 0))

        def browse():
            path = fd.askopenfilename(title="Select file to protect")
            if path:
                self._pf_path.set(path)
                self._pf_path_label.config(text=os.path.basename(path), fg=C["success"])
                self._pf_appname.set(Path(path).stem)
                self._pf_outdir.set(str(Path(path).parent))

        for w in [drop_frame, inner_drop]:
            w.bind("<Button-1>", lambda e: browse())
        for child in inner_drop.winfo_children():
            child.bind("<Button-1>", lambda e: browse())

        # Options form
        form = _card(p)
        form.pack(fill="x", pady=(0, 16))
        form_inner = tk.Frame(form, bg=C["panel"], padx=24, pady=20)
        form_inner.pack(fill="x")

        def form_row(label_text, var, row, placeholder=""):
            tk.Label(form_inner, text=label_text, font=tkfont.Font(family="Segoe UI", size=10),
                     bg=C["panel"], fg=C["muted"], anchor="w", width=18).grid(
                row=row, column=0, sticky="w", pady=6, padx=(0, 12))
            e = _entry(form_inner, textvariable=var)
            e.grid(row=row, column=1, sticky="ew", pady=6, ipady=6)
            return e

        self._pf_appname = tk.StringVar()
        self._pf_outdir  = tk.StringVar()
        self._pf_days    = tk.StringVar(value="15")

        form_row("Application Name:", self._pf_appname, 0)
        form_row("Output Directory:",  self._pf_outdir,  1)
        form_row("Trial Days:",         self._pf_days,    2)
        form_inner.columnconfigure(1, weight=1)

        def browse_outdir():
            d = fd.askdirectory(title="Select output directory")
            if d:
                self._pf_outdir.set(d)

        _btn(form_inner, "Browse…", browse_outdir, width=10).grid(
            row=1, column=2, padx=(8, 0))

        # Action buttons
        btn_row = tk.Frame(p, bg=C["bg"])
        btn_row.pack(fill="x", pady=(0, 16))

        self._pf_status = tk.StringVar()
        status_lbl = _label(p, textvariable=self._pf_status, size=10, color=C["success"])
        status_lbl.pack(anchor="w", pady=(0, 8))

        def do_protect():
            path = self._pf_path.get()
            if not path:
                mb.showerror("No file", "Please select a file to protect first.")
                return
            app_name = self._pf_appname.get().strip() or Path(path).stem
            out_dir  = self._pf_outdir.get().strip()
            if not out_dir:
                mb.showerror("No output", "Please set an output directory.")
                return
            try:
                days = int(self._pf_days.get())
            except ValueError:
                mb.showerror("Invalid days", "Trial days must be a number.")
                return

            self._set_status("Protecting file…")
            result = protect_file(path, out_dir, app_name, days)
            if result["success"]:
                out = result["output_path"]
                self._pf_status.config(fg=C["success"])
                self._pf_status.set(f"✅  Protected file saved to: {out}")
                self._set_status(f"Done → {os.path.basename(out)}")
                mb.showinfo("Success", f"File protected successfully!\n\nOutput:\n{out}")
            else:
                self._pf_status.config(fg=C["danger"])
                self._pf_status.set(f"❌  {result.get('error', 'Unknown error')}")
                self._set_status("Protection failed.")

        _btn(btn_row, "🛡️  Protect File", do_protect,
             color=C["accent"]).pack(side="left")
        _btn(btn_row, "Clear", lambda: [
            self._pf_path.set(""), self._pf_path_label.config(text="(no file selected)", fg=C["accent"]),
            self._pf_appname.set(""), self._pf_outdir.set(""), self._pf_status.set("")
        ], color=C["dim"], hover_color=C["border"]).pack(side="left", padx=(12, 0))

    # 3. Key Generator ─────────────────────────────────────────────────────────
    def _build_key_generator(self, parent):
        p = tk.Frame(parent, bg=C["bg"])
        p.pack(fill="both", expand=True, padx=36, pady=30)

        _label(p, "License Key Generator", size=20, weight="bold").pack(anchor="w")
        _label(p, "Developer mode — generate hardware-bound license keys for customers.",
               size=11, color=C["muted"]).pack(anchor="w", pady=(4, 0))
        _divider(p).pack(fill="x", pady=(12, 20))

        self._kg_main = tk.Frame(p, bg=C["bg"])
        self._kg_main.pack(fill="both", expand=True)

        # Main generator UI
        self._kg_build_main(self._kg_main)

    def _kg_build_main(self, parent):
        _label(parent, "Customer License Details", size=13, weight="bold").pack(
            anchor="w", pady=(0, 12))

        form = _card(parent)
        form.pack(fill="x", pady=(0, 16))
        fi = tk.Frame(form, bg=C["panel"], padx=24, pady=20)
        fi.pack(fill="x")

        self._kg_email = tk.StringVar()
        self._kg_hwid  = tk.StringVar()

        for i, (lbl, var) in enumerate([
            ("Customer Email:", self._kg_email),
            ("Hardware ID:",    self._kg_hwid),
        ]):
            tk.Label(fi, text=lbl, font=tkfont.Font(family="Segoe UI", size=10),
                     bg=C["panel"], fg=C["muted"], anchor="w", width=20).grid(
                row=i, column=0, sticky="w", pady=8, padx=(0, 12))
            _entry(fi, textvariable=var).grid(row=i, column=1, sticky="ew",
                                              pady=8, ipady=6)
        fi.columnconfigure(1, weight=1)

        _label(parent, "💡 Ask the customer to open Software Protector → Activate License to see their Hardware ID.",
               size=9, color=C["muted"]).pack(anchor="w", pady=(0, 16))

        # Result area
        res_frame = _card(parent)
        res_frame.pack(fill="x", pady=(0, 16))
        ri = tk.Frame(res_frame, bg=C["panel"], padx=24, pady=20)
        ri.pack(fill="x")
        _label(ri, "Generated License Key:", size=10, weight="bold",
               bg=C["panel"]).pack(anchor="w", pady=(0, 8))

        self._kg_result = tk.StringVar(value="—")
        key_lbl = tk.Label(ri, textvariable=self._kg_result,
                           font=tkfont.Font(family="Consolas", size=16, weight="bold"),
                           bg=C["panel"], fg=C["accent"], pady=12, padx=16)
        key_lbl.pack(fill="x")

        self._kg_status = tk.StringVar()
        _label(ri, textvariable=self._kg_status, size=9, color=C["success"],
               bg=C["panel"]).pack(anchor="w", pady=(6, 0))

        def generate():
            email = self._kg_email.get().strip()
            hwid  = self._kg_hwid.get().strip()
            if not email or not hwid:
                mb.showerror("Missing Info", "Please enter both email and hardware ID.")
                return
            key = generate_license_key(email, hwid)
            self._kg_result.set(key)
            self._kg_status.set("✅  Key generated successfully!")
            self._set_status(f"Key generated for {email}")

        def copy_key():
            key = self._kg_result.get()
            if key and key != "—":
                self.clipboard_clear()
                self.clipboard_append(key)
                self._kg_status.set("📋  Key copied to clipboard!")

        def copy_all():
            key = self._kg_result.get()
            email = self._kg_email.get().strip()
            hwid = self._kg_hwid.get().strip()
            if key and key != "—":
                text = f"Email: {email}\nHardware ID: {hwid}\nLicense Key: {key}"
                self.clipboard_clear()
                self.clipboard_append(text)
                self._kg_status.set("📋  All details copied to clipboard!")

        btn_row = tk.Frame(parent, bg=C["bg"])
        btn_row.pack(fill="x", pady=(0, 16))
        _btn(btn_row, "🔑  Generate Key", generate).pack(side="left")
        _btn(btn_row, "📋 Copy Key", copy_key, color=C["dim"],
             hover_color=C["border"]).pack(side="left", padx=(10, 0))
        _btn(btn_row, "📋 Copy All Details", copy_all, color=C["dim"],
             hover_color=C["border"]).pack(side="left", padx=(10, 0))

    # 4. Activate License ──────────────────────────────────────────────────────
    def _build_activate_license(self, parent):
        p = tk.Frame(parent, bg=C["bg"])
        p.pack(fill="both", expand=True, padx=36, pady=30)

        _label(p, "Activate License", size=20, weight="bold").pack(anchor="w")
        _label(p, "Enter your email and license key to unlock the full version.",
               size=11, color=C["muted"]).pack(anchor="w", pady=(4, 0))
        _divider(p).pack(fill="x", pady=(12, 20))

        # HW ID display
        hw_card = _card(p)
        hw_card.pack(fill="x", pady=(0, 16))
        hw_inner = tk.Frame(hw_card, bg=C["panel"], padx=24, pady=16)
        hw_inner.pack(fill="x")
        _label(hw_inner, "Your Hardware ID (share this with your developer/reseller):",
               size=10, color=C["muted"], bg=C["panel"]).pack(anchor="w")
        hw_row = tk.Frame(hw_inner, bg=C["panel"])
        hw_row.pack(fill="x", pady=(6, 0))
        hw_id = get_hardware_id()
        hw_var = tk.StringVar(value=hw_id)
        hw_entry = tk.Entry(hw_row,
                            textvariable=hw_var,
                            font=tkfont.Font(family="Consolas", size=13, weight="bold"),
                            bg=C["bg"], fg=C["accent"],
                            relief="flat", bd=0,
                            state="readonly",
                            readonlybackground=C["bg"],
                            width=20)
        hw_entry.pack(side="left", ipady=4)

        def copy_hw():
            self.clipboard_clear()
            self.clipboard_append(hw_id)
            self._al_status.set("📋  Hardware ID copied to clipboard!")

        _btn(hw_row, "📋 Copy", copy_hw, color=C["dim"],
             hover_color=C["border"]).pack(side="left", padx=(14, 0))

        # Form
        form = _card(p)
        form.pack(fill="x", pady=(0, 16))
        fi = tk.Frame(form, bg=C["panel"], padx=24, pady=20)
        fi.pack(fill="x")

        self._al_email = tk.StringVar()
        self._al_key   = tk.StringVar()

        for i, (lbl, var) in enumerate([
            ("Email Address:", self._al_email),
            ("License Key:",   self._al_key),
        ]):
            tk.Label(fi, text=lbl, font=tkfont.Font(family="Segoe UI", size=10),
                     bg=C["panel"], fg=C["muted"], anchor="w", width=16).grid(
                row=i, column=0, sticky="w", pady=8, padx=(0, 12))
            _entry(fi, textvariable=var).grid(row=i, column=1, sticky="ew",
                                              pady=8, ipady=8)
        fi.columnconfigure(1, weight=1)

        self._al_status = tk.StringVar()
        status_lbl = _label(p, textvariable=self._al_status, size=11)
        status_lbl.pack(anchor="w", pady=(0, 12))

        def do_activate():
            email = self._al_email.get().strip()
            key   = self._al_key.get().strip()
            if not email or not key:
                mb.showerror("Missing Info", "Please enter both email and license key.")
                return
            if activate_license(email, key):
                status_lbl.config(fg=C["success"])
                self._al_status.set("✅  License activated successfully! Thank you.")
                self._set_status("License activated.")
                mb.showinfo("Activated", f"🎉 Software Protector is now fully licensed!\n\nEmail: {email}")
            else:
                status_lbl.config(fg=C["danger"])
                self._al_status.set("❌  Invalid license key. Please check and try again.")
                self._set_status("Activation failed.")

        btn_row = tk.Frame(p, bg=C["bg"])
        btn_row.pack(fill="x")
        _btn(btn_row, "✅  Activate License", do_activate).pack(side="left")
        _btn(btn_row, "Clear", lambda: [
            self._al_email.set(""), self._al_key.set(""), self._al_status.set("")
        ], color=C["dim"], hover_color=C["border"]).pack(side="left", padx=(12, 0))

        # Status info
        _divider(p).pack(fill="x", pady=(24, 16))
        info = get_trial_info()
        info_card = _card(p)
        info_card.pack(fill="x")
        ii = tk.Frame(info_card, bg=C["panel"], padx=24, pady=16)
        ii.pack(fill="x")
        _label(ii, "Current Status", size=11, weight="bold", bg=C["panel"]).pack(anchor="w")
        if info["is_licensed"]:
            _label(ii, f"✅  Licensed to: {info['email']}", size=10,
                   color=C["success"], bg=C["panel"]).pack(anchor="w", pady=(6, 0))
        else:
            days = info["days_left"] or 0
            col = C["success"] if days > 5 else C["warning"] if days > 0 else C["danger"]
            _label(ii, f"⏱️  Trial:  {days} days remaining  (of 15)", size=10,
                   color=col, bg=C["panel"]).pack(anchor="w", pady=(6, 0))

    # 5. How to Use ────────────────────────────────────────────────────────────
    def _build_how_to_use(self, parent):
        _label(parent, "How to Use  —  Step-by-Step Guide", size=18, weight="bold"
               ).pack(anchor="w", padx=36, pady=(28, 4))
        _label(parent, "Complete guide for developers and end-users.",
               size=11, color=C["muted"]).pack(anchor="w", padx=36)
        _divider(parent).pack(fill="x", padx=36, pady=(10, 0))

        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        sb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=C["bg"])
        sf.bind("<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        def section(title, steps):
            sec = _card(sf)
            sec.pack(fill="x", padx=36, pady=(16, 0))
            si = tk.Frame(sec, bg=C["panel"], padx=22, pady=18)
            si.pack(fill="x")
            _label(si, title, size=13, weight="bold", bg=C["panel"],
                   color=C["accent"]).pack(anchor="w", pady=(0, 10))
            for num, step in enumerate(steps, 1):
                row = tk.Frame(si, bg=C["panel"])
                row.pack(fill="x", pady=4)
                _label(row, f"{num}.", size=11, weight="bold",
                       color=C["accent"], bg=C["panel"], width=3).pack(
                    side="left", anchor="n")
                _label(row, step, size=10, color=C["text"], bg=C["panel"],
                       justify="left", wraplength=680).pack(
                    side="left", anchor="w", padx=(6, 0))

        section("🚀 Getting Started", [
            "Download and run Software Protector: python main.py",
            "On first launch you get a 15-day free trial automatically.",
            "Your Hardware ID is displayed on the Dashboard and Activate License page.",
            "To purchase a license, contact the developer at www.maxtechfix.com.",
        ])
        section("🛡️ Protecting a File  (Developer workflow)", [
            "Click 'Protect File' in the left sidebar.",
            "Click the browse area and select your file (.py, .exe, or any other type).",
            "Set the Application Name — this appears in trial dialogs shown to your customers.",
            "Choose an output directory where the protected file will be saved.",
            "Set the Trial Days (default 15). Customers get this many days before a license is required.",
            "Click 'Protect File'. The tool generates a protected version in the output directory.",
            "For .py files: a protected_<name>.py is created — compile it to .exe with PyInstaller.",
            "For .exe files: a launch_<name>.py launcher is created — compile it too if needed.",
            "For other files: an encrypted .spdata file + launch_<name>.py launcher are created.",
            "Distribute the protected file(s) to your customers.",
        ])
        section("🔑 Generating a License Key  (Developer workflow)", [
            "Click 'Key Generator' in the sidebar.",
            "Ask your customer for their Hardware ID (visible in the protected app or in this tool).",
            "Enter the customer's email address and Hardware ID in the form.",
            "Click 'Generate Key' to create a unique HMAC-SHA256 license key.",
            "Copy and send the key to your customer via email or your sales channel.",
            "The key is permanently bound to that email + hardware combination.",
        ])
        section("✅ Activating a License  (Customer workflow)", [
            "Run Software Protector (or the protected application).",
            "Navigate to 'Activate License' in the sidebar.",
            "Your Hardware ID is shown at the top — copy it and send it to the developer.",
            "Once you receive your license key, enter your email and the key in the form.",
            "Click 'Activate License'. If correct, the software is permanently unlocked.",
            "The license file is saved securely on your machine in ~/.sp_data/.",
        ])
        section("📦 Converting .py to .exe  (using PyInstaller)", [
            "Install PyInstaller:  pip install pyinstaller",
            "Navigate to your protected file:  cd /path/to/output/",
            "Run:  pyinstaller --onefile protected_yourapp.py",
            "Your .exe will appear in the dist/ folder.",
            "Distribute the .exe to customers — no Python installation required.",
        ])
        section("🔒 Security Tips", [
            "The license key is bound to one Hardware ID; customers cannot share it.",
            "Trial and license data are XOR-encrypted on disk to prevent simple tampering.",
            "For maximum security, use PyArmor or Cython to obfuscate your .py before protecting.",
            "Consider adding server-side license validation for critical applications.",
        ])

        _label(sf, "Need help?  Contact: Zulfiqar Ali  |  www.maxtechfix.com",
               size=10, color=C["muted"]).pack(pady=(20, 30))

    # 6. About ─────────────────────────────────────────────────────────────────
    def _build_about(self, parent):
        canvas = tk.Canvas(parent, bg=C["bg"], highlightthickness=0)
        sb = tk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=C["bg"])
        sf.bind("<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # Hero section
        hero = tk.Frame(sf, bg=C["sidebar"])
        hero.pack(fill="x")
        hi = tk.Frame(hero, bg=C["sidebar"], padx=50, pady=40)
        hi.pack(fill="x")
        _label(hi, "🛡️", size=48, bg=C["sidebar"]).pack()
        _label(hi, "MaxTechFix Software Protector", size=22, weight="bold",
               bg=C["sidebar"]).pack(pady=(10, 4))
        _label(hi, "Version 1.0.0  ·  Professional Edition", size=12,
               color=C["muted"], bg=C["sidebar"]).pack()
        _label(hi, "All-in-One Trial · License · Hardware-Binding · File Protection",
               size=11, color=C["accent"], bg=C["sidebar"]).pack(pady=(8, 0))

        p = tk.Frame(sf, bg=C["bg"])
        p.pack(fill="both", padx=50, pady=(28, 0))

        # Developer card
        dev_card = _card(p)
        dev_card.pack(fill="x", pady=(0, 20))
        di = tk.Frame(dev_card, bg=C["panel"], padx=28, pady=22)
        di.pack(fill="x")
        _label(di, "👨‍💻  Developer", size=13, weight="bold", bg=C["panel"],
               color=C["accent"]).pack(anchor="w", pady=(0, 12))

        rows = [
            ("Name:",    "Zulfiqar Ali"),
            ("Company:", "MaxTechFix"),
            ("Website:", "www.maxtechfix.com"),
            ("Email:",   "contact@maxtechfix.com"),
        ]
        for label, value in rows:
            row = tk.Frame(di, bg=C["panel"])
            row.pack(fill="x", pady=4)
            _label(row, label, size=10, color=C["muted"], bg=C["panel"],
                   width=12, anchor="w").pack(side="left")
            _label(row, value, size=10, weight="bold", bg=C["panel"]).pack(side="left")

        # Features card
        feat_card = _card(p)
        feat_card.pack(fill="x", pady=(0, 20))
        fi = tk.Frame(feat_card, bg=C["panel"], padx=28, pady=22)
        fi.pack(fill="x")
        _label(fi, "⚡  Key Features", size=13, weight="bold", bg=C["panel"],
               color=C["accent"]).pack(anchor="w", pady=(0, 12))

        features = [
            "🛡️  Protect any file — .py, .exe, documents, images, and more",
            "⏱️  15-day trial system with countdown dialog on every launch",
            "🔑  HMAC-SHA256 hardware-bound license keys",
            "🖥️  One license = one PC (hardware fingerprinting via MAC address)",
            "🔒  XOR-encrypted trial and license data stored on disk",
            "👨‍💻  Developer Mode with password-protected Key Generator",
            "📋  One-click copy for Hardware ID and license keys",
            "📦  PyInstaller-compatible — distribute as a standalone .exe",
            "🌍  Works on Windows, macOS, and Linux",
            "🎨  Professional dark-theme GUI — no command line needed",
        ]
        for feat in features:
            _label(fi, f"  {feat}", size=10, bg=C["panel"],
                   justify="left").pack(anchor="w", pady=2)

        # Tech stack
        tech_card = _card(p)
        tech_card.pack(fill="x", pady=(0, 20))
        ti = tk.Frame(tech_card, bg=C["panel"], padx=28, pady=22)
        ti.pack(fill="x")
        _label(ti, "🔧  Technology", size=13, weight="bold", bg=C["panel"],
               color=C["accent"]).pack(anchor="w", pady=(0, 12))
        techs = [
            ("Language",    "Python 3.8+"),
            ("GUI",         "tkinter (built-in, cross-platform)"),
            ("Encryption",  "XOR + SHA-256 + base64 (no extra deps)"),
            ("Licensing",   "HMAC-SHA256 with hardware binding"),
            ("Packaging",   "PyInstaller (optional, for .exe distribution)"),
        ]
        for lbl, val in techs:
            row = tk.Frame(ti, bg=C["panel"])
            row.pack(fill="x", pady=3)
            _label(row, f"{lbl}:", size=10, color=C["muted"], bg=C["panel"],
                   width=16, anchor="w").pack(side="left")
            _label(row, val, size=10, bg=C["panel"]).pack(side="left")

        # Copyright
        copy_frame = tk.Frame(sf, bg=C["bg"])
        copy_frame.pack(fill="x", pady=(8, 36))
        _divider(copy_frame).pack(fill="x", padx=50, pady=(0, 16))
        _label(copy_frame, "© 2024 Zulfiqar Ali · MaxTechFix · www.maxtechfix.com",
               size=10, color=C["dim"]).pack()
        _label(copy_frame, "All rights reserved. Protect your work with confidence.",
               size=9, color=C["dim"]).pack(pady=(4, 0))


# ── Entry point ───────────────────────────────────────────────────────────────

def run_app():
    app = SoftwareProtectorApp()
    app.mainloop()


if __name__ == "__main__":
    run_app()
